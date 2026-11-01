"""Explicit foreground campaign phases over a frozen, accepted reference.

No import starts models. A caller releases qualification or a single evaluation
slot separately. Private journals precede subsequent calls and public writes.
"""
from datetime import datetime, timezone
from pathlib import Path
import subprocess

from ams.assessment import require, same_artifact
from ams import trial_series as series
from ams import trial_runtime as runtime
from ams.trial_inputs import load, worker_prompt, encoded
from ams import rsi_rows


def verify_source_revision(protocol, *, accepted_ref='origin/main'):
    root=Path(__file__).resolve().parents[2]
    revision=protocol['sourceRevision']
    git=['git','--no-replace-objects','--no-lazy-fetch','-c','protocol.allow=never']
    require(subprocess.run(git+['merge-base','--is-ancestor',revision,accepted_ref],cwd=root,
                           capture_output=True).returncode==0,'source reference is not main-contained')
    for name,expected in protocol['sourceFiles'].items():
        result=subprocess.run(git+['show',revision+':src/ams/'+name],cwd=root,capture_output=True)
        require(result.returncode==0 and series.hashlib.sha256(result.stdout).hexdigest()==expected,
                'source revision does not contain the frozen code')
    suite=subprocess.run(git+['show',revision+':evals/interview-dev-cases.json'],cwd=root,capture_output=True)
    require(suite.returncode==0 and series.digest(series.json.loads(suite.stdout))==protocol['suiteDigest'],
            'suite is not at accepted source revision')


class Campaign:
    def __init__(self,record,worker,reference,store,*,call=None,binary=None,verify_source=True):
        self.protocol=record['protocol'];self.controls=record['controls']
        self.worker=Path(worker);self.reference=Path(reference);self.store=Path(store)
        self.call=call or runtime.ClaudeAdapter().execute
        series.verify_frozen(self.protocol,self.worker,self.reference,
                             actual_binary=binary or series.binary_identity())
        require(record['controlsDigest']==series.digest(self.controls),'control identity changed')
        require(same_artifact(self.controls,series.qualification_controls(reference,self.protocol['suite'])),
                'qualification controls changed')
        if verify_source:verify_source_revision(self.protocol)
        self.identity=series.digest(record)

    def _validate(self):
        series.verify_frozen(self.protocol,self.worker,self.reference,actual_binary=series.binary_identity())
        verify_source_revision(self.protocol)

    def _retain(self,identity,value):
        return series.save_private(self.store,identity,{'campaignDigest':self.identity,'evidence':value})

    def qualify(self):
        """Separately released five-call phase; rerunning any slot is refused."""
        self._validate()
        require(not list(self.store.glob('qualification-*.json')),'qualification already attempted; preserve it')
        oracle=(self.reference.parent/load(self.reference)['promptFile']).read_text()
        # Claim this phase before any call, so a crash cannot silently reset it.
        self._retain('qualification-start',{'controlsDigest':series.digest(self.controls)})
        result=series.calibrate(self.controls,oracle,self.call,cwd=self.worker,
                               retain=lambda row:self._retain('qualification-'+row['id'],row))
        result.update(protocolDigest=series.digest(self.protocol))
        self._retain('qualification-final',result)
        return result

    def run_one(self,index):
        """One explicitly released slot. Never loops or retries on its own."""
        self._validate()
        qualification=series.read_private(self.store,'qualification-final')
        q=qualification['evidence']
        require(qualification['campaignDigest']==self.identity and q['qualified'] is True
                and q['protocolDigest']==series.digest(self.protocol)
                and q['controlsDigest']==series.digest(self.controls),'matching actual qualification required')
        require(type(index)is int and 0<=index<9,'one of nine frozen slots required')
        slot='trial-'+str(index+1)
        require(not list(self.store.glob(slot+'-*.json')),'trial already attempted; no favorable reruns')
        if index:
            prior=series.read_private(self.store,'trial-'+str(index)+'-result')
            require(prior['campaignDigest']==self.identity,'previous slot incomplete or unrelated')
        case_id,trial=self.protocol['order'][index]
        case=next(c for c in self.protocol['suite']['cases']if c['id']==case_id)
        prompt,identity=worker_prompt(self.worker,case_id)
        require(identity['suiteDigest']==self.protocol['suiteDigest'],'worker suite changed')
        self._retain(slot+'-start',{'caseId':case_id,'trial':trial,'inputIdentity':identity})
        oracle=(self.reference.parent/load(self.reference)['promptFile']).read_text()
        return series.evaluate(case,prompt,oracle,self.call,cwd=self.worker,
                               retain=lambda phase,row:self._retain(slot+'-'+phase,row))


def publish_result(store,run,result,*,case_id,trial,evidence_digest):
    """Existing S-006 contract: completed means a completed graded evaluation.

    Grader error/Unknown leaves pipeline runner_error and passed:null. Independent
    workerCompleted and failureStage describe the process truth without implying
    worker failure. A No verdict is a real completed/false task result.
    """
    source='evals/interview-noise-r1#'+evidence_digest
    row=rsi_rows.result_for(run,task_id=case_id,split='dev',trial=trial,
        execution_state=result['execution_state'],passed=result['passed'],
        source_kind='path',source_ref=source,strength='single_trial',
        detail=series.safe_detail(result,evidence_digest),**series.metrics(result))
    saved=store.insert(rsi_rows.RESULT_TABLE,row)
    read=store.get(rsi_rows.RESULT_TABLE,saved['id'])
    require(read is not None and all(same_artifact(read.get(k),v)for k,v in row.items()),
            'result readback differs; preserve uncertain write before retry')
    return read


def create_run(store,protocol,campaign_digest):
    revision=protocol['sourceRevision']
    git=['git','--no-replace-objects','--no-lazy-fetch','-c','protocol.allow=never']
    row={'run_key':'interview-noise-r1-'+campaign_digest[:20], 'arm':'ams','provider':'firstParty',
         'model':runtime.MODEL,'effort':runtime.EFFORT,'runtime_commit':revision,
         'controls_commit':revision,'skills_commit':protocol['skillsCommit'],'grader_version':revision,
         'state':'running','started_at':datetime.now(timezone.utc).isoformat(),
         'source_kind':'path','source_ref':'evals/interview-noise-r1#'+campaign_digest,
         'strength':'repeated_trials','is_test':False,
         'detail':{'scope':series.SCOPE,'protocolDigest':series.digest(protocol),
                   'campaignDigest':campaign_digest,'baselineAttempt':0,'nativeInstallation':False}}
    return store.insert(rsi_rows.RUN_TABLE,row)
