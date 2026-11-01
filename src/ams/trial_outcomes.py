"""Same-version descriptive outcomes and public-safe execution summaries."""
import itertools

from ams.assessment import require
from ams import trial_runtime as runtime
from ams.trial_inputs import SCOPE, _hash


def metrics(result):
    worker=result.get('worker')
    source='evals/interview-noise-r1: private execution evidence digest'
    row={'cost_usd':None,'input_tokens':None,'output_tokens':None,'turns':None,
         'wall_seconds':result.get('wallSeconds'), 'metric_unknowns':{}}
    if worker:
        usage=worker['usage']
        row.update(input_tokens=sum(usage[k]for k in ('inputTokens','cacheReadInputTokens','cacheCreationInputTokens')),
                   output_tokens=usage['outputTokens'],turns=1)
    for key in ('cost_usd','input_tokens','output_tokens','turns','wall_seconds'):
        if row[key] is None:
            row['metric_unknowns'][key]={'reason':'Subscription spend unavailable'if key=='cost_usd'
                                      else 'Worker measurement unavailable','source':source}
    return row


def noise_floor(rows):
    require(len(rows)==3, 'three required trial rows per case')
    required=('task_id','split','arm','provider','model','effort','runtime_commit',
              'controls_commit','skills_commit','grader_version','is_test')
    require(all(all(key in row for key in required)for row in rows), 'floor provenance missing')
    require(all(all(row[key]==rows[0][key]for key in required)for row in rows),
            'floor mixes tasks, versions or conditions')
    require({row['trial']for row in rows}=={1,2,3}, 'floor needs trials one through three')
    ids=[row['id']for row in rows]
    require(len(set(ids))==3, 'duplicate trial row')
    grades=[row.get('passed')for row in rows if row.get('execution_state')=='completed'
            and type(row.get('passed')) is bool]
    complete=len(grades)==3
    return {'rowIds':ids,'required':3,'graded':len(grades),'passes':sum(grades),
            'flipRate':sum(a!=b for a,b in itertools.combinations(grades,2))/3 if complete else None,
            'spread':int(max(grades))-int(min(grades))if complete else None,
            'successRate':sum(grades)/3 if complete else None,'passCubed':all(grades)if complete else None,
            'status':'complete'if complete else 'Unknown'}


def safe_detail(result,evidence_digest):
    _hash(evidence_digest)
    worker=result.get('worker')
    usage={k:runtime._count(worker['usage'][k]) for k in (
        'inputTokens','cacheReadInputTokens','cacheCreationInputTokens','outputTokens')} if worker else None
    reason=None if result.get('passed') is not None else (
        'worker-runtime-unavailable' if not result['workerCompleted'] else
        (result.get('grade') or {}).get('reason','semantic-verdict-unknown'))
    require(reason in (None,'worker-runtime-unavailable','judge-parse-failure','missing-final-text',
                       'judge-runtime-failure','semantic-verdict-unknown','cancelled'), 'unsafe grade reason')
    require(type(result['workerCompleted']) is bool and result['failureStage'] in
            (None,'worker','grader'), 'invalid completion summary')
    cost=worker['equivalentApiCostUsd'] if worker else None
    require(cost is None or type(cost) in (int,float) and runtime.math.isfinite(cost) and cost>=0,
            'invalid equivalent API cost')
    return {'scope':SCOPE,'workerCompleted':result['workerCompleted'],
            'failureStage':result['failureStage'],'gradeReason':reason,
            'gradeSource':'protected private evidence digest',
            'gradeState':'graded'if result.get('passed') is not None else 'unknown',
            'evidenceDigest':evidence_digest,'usage':usage,'equivalentApiCostUsd':cost,
            'actualSubscriptionCostUsd':None,
            'inputTokensDefinition':'uncached plus cache-read plus cache-creation',
            'nativeInstallation':False,'tools':[],'mcpServers':[]}

