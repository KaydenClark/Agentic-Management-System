"""Private predecessor proof and one neutral owned execution directory."""
from pathlib import Path
from ams.assessment import require,same_artifact
from ams.trial_inputs import SCOPE,_hash,_no_links,load,digest,encoded
from ams import trial_runtime as runtime

MARKER='.ams-neutral-execution.json'
OWNED={'schema':1,'kind':'ams-owned-neutral-execution','scope':SCOPE}


def execution_context(path,worker,reference,*,create=False):
    path=Path(path).absolute();worker=Path(worker).absolute();oracle=Path(reference).absolute().parent
    _no_links(path)
    require(not any((parent/'.git').exists()for parent in (path,*path.parents)),
            'neutral execution must not inherit moving Git context')
    require(not any(label in part.lower()for part in path.parts for label in (
        'baseline','candidate','no-ams','no_ams','plain-instruction','plain_instruction')),
        'execution cwd must not disclose an arm')
    for protected in (worker,oracle):
        require(not path.is_relative_to(protected) and not protected.is_relative_to(path),
                'neutral execution overlaps protected source/oracle')
    if not path.exists():
        require(create,'owned neutral execution cwd unavailable')
        path.mkdir(parents=True,mode=0o700)
        with (path/MARKER).open('xb')as stream:stream.write(encoded(OWNED)+b'\n')
        (path/MARKER).chmod(0o600)
    require(path.is_dir() and set(p.name for p in path.iterdir())=={MARKER},
            'neutral cwd changed; preserve unexpected data')
    require(same_artifact(load(path/MARKER),OWNED),'unowned neutral cwd')
    return {'path':str(path),'markerDigest':digest(OWNED),'inventory':[MARKER],'gitContext':False}


def _envelope(path):
    row=load(path)
    require(isinstance(row,dict) and type(row.get('schema'))is int and row['schema']==1
            and isinstance(row.get('value'),dict) and row.get('digest')==digest(row['value']),
            'predecessor evidence envelope changed')
    return row['value'],row['digest']


def predecessor_binding(paths,controls,worker,execution,*,semantics):
    require(isinstance(paths,dict) and set(paths)=={'record','qualification'},'predecessor paths required')
    private={}
    for key,file in paths.items():
        path=Path(file).absolute();_no_links(path)
        require(not path.is_relative_to(Path(worker).absolute()) and
                not path.is_relative_to(Path(execution).absolute()),'predecessor exposed to execution')
        private[key]=str(path)
    record,record_digest=_envelope(private['record'])
    qualification,qualification_digest=_envelope(private['qualification'])
    old=record.get('protocol');proof=qualification.get('evidence')
    require(isinstance(old,dict) and isinstance(proof,dict),'predecessor record body missing')
    require(qualification['campaignDigest']==record_digest and proof['protocolDigest']==digest(old),
            'predecessor campaign/protocol mismatch')
    require(same_artifact({key:old.get(key)for key in semantics},semantics),
            'semantic prompt/context or baseline identity changed')
    current_digest=digest(controls)
    require(record['controlsDigest']==digest(record['controls'])==current_digest
            and proof['controlsDigest']==current_digest,'semantic controls changed')
    require(proof.get('qualified') is True and isinstance(proof.get('results'),list)
            and len(proof['results'])==5 and all(isinstance(row,dict)for row in proof['results'])
            and len(controls)==5,
            'actual five-control predecessor qualification missing')
    rows={row['id']:row for row in proof['results']}
    require(len(rows)==5,'duplicate predecessor outcome')
    labels=[]
    for control in controls:
        row=rows.get(control['id']);require(isinstance(row,dict),'predecessor case missing')
        actual=row.get('actual')
        require(isinstance(actual,dict) and isinstance(actual.get('execution'),dict),
                'predecessor execution proof missing')
        execution_result=actual['execution']
        require(row['matches'] is True and row['expected']==control['expected']==actual['verdict'],
                'predecessor outcome does not match frozen label')
        require(isinstance(actual.get('evidence'),str) and bool(actual['evidence'].strip())
                and actual['evidence'] in control['response'],'predecessor literal evidence missing')
        require(execution_result.get('provider')=='firstParty' and execution_result.get('model')==runtime.MODEL
                and execution_result.get('effort')==runtime.EFFORT and execution_result.get('tools')==[]
                and execution_result.get('mcpServers')==[],'predecessor execution conditions changed')
        labels.append({'id':control['id'],'expected':control['expected'],'actual':actual['verdict']})
    _hash(old['sourceRevision'],40);_hash(old['suiteDigest'])
    require(isinstance(old.get('sourceFiles'),dict) and bool(old['sourceFiles']),
            'predecessor source inventory missing')
    for name,identity in old['sourceFiles'].items():
        require(isinstance(name,str) and '/' not in name and name.endswith('.py'),
                'predecessor source path changed')
        _hash(identity)
    return {'paths':private,'recordDigest':record_digest,'qualificationDigest':qualification_digest,
            'controlsDigest':current_digest,'sourceRevision':old['sourceRevision'],
            'sourceFiles':old['sourceFiles'],'suiteDigest':old['suiteDigest'],'labels':labels}
