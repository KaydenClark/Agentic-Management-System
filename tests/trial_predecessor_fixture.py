"""Synthetic predecessor fixtures, never actual qualification evidence."""
from ams import trial_series as series


def predecessor(tmp_path,controls,base,execution_factory):
    previous={'protocol':{'sourceRevision':'a'*40,'sourceFiles':{'trial_runtime.py':'b'*64},
                          **{key:base[key]for key in ('scope','model','effort','workerSystem','judgeSystem',
                              'suiteDigest','skillsCommit','manifestDigest','reference')}},'controls':controls,'controlsDigest':series.digest(controls)}
    prior_folder=tmp_path/'predecessor'
    series.save_private(prior_folder,'record',previous)
    results=[]
    for control in controls:
        actual={'verdict':control['expected'],'evidence':control['response'][:16],'obligation':'synthetic',
                'execution':execution_factory('synthetic prior execution')}
        results.append({'id':control['id'],'expected':control['expected'],'actual':actual,'matches':True})
    q={'campaignDigest':series.digest(previous),'evidence':{
        'protocolDigest':series.digest(previous['protocol']),'controlsDigest':series.digest(controls),
        'qualified':True,'results':results}}
    series.save_private(prior_folder,'qualification',q)
    return {'record':prior_folder/'record.json','qualification':prior_folder/'qualification.json'}
