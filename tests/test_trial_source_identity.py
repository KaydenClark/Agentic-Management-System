"""Actual inert Git source-identity adversaries; no authentication or model calls."""
import json
import pytest
from ams import trial_series as series
from ams.assessment import Refused


def source_repo(tmp_path,monkeypatch):
    import hashlib,subprocess
    from ams import trial_campaign
    root=tmp_path/'repository';(root/'src/ams').mkdir(parents=True);(root/'evals').mkdir()
    def git(*args):
        return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
    git('init','-q');git('config','user.name','Synthetic');git('config','user.email','synthetic@example.invalid')
    (root/'src/ams/trial_runtime.py').write_text('actual committed bytes')
    suite={'synthetic':'suite'};(root/'evals/interview-dev-cases.json').write_text(json.dumps(suite))
    git('add','.');git('commit','-qm','synthetic accepted source');revision=git('rev-parse','HEAD')
    git('update-ref','refs/remotes/origin/main',revision)
    monkeypatch.setattr(trial_campaign,'__file__',str(root/'src/ams/trial_campaign.py'))
    protocol={'sourceRevision':revision,'sourceFiles':{
        'trial_runtime.py':hashlib.sha256(b'actual committed bytes').hexdigest()},'suiteDigest':series.digest(suite)}
    return root,git,protocol


def test_source_verification_refuses_git_replace_blob_bypass(tmp_path,monkeypatch):
    import hashlib
    from ams import trial_campaign
    root,git,protocol=source_repo(tmp_path,monkeypatch)
    bad=git('rev-parse','HEAD:src/ams/trial_runtime.py')
    (root/'replacement').write_bytes(b'frozen local bytes')
    replacement=git('hash-object','-w','replacement');git('replace',bad,replacement)
    protocol['sourceFiles']['trial_runtime.py']=hashlib.sha256(b'frozen local bytes').hexdigest()
    assert git('show','HEAD:src/ams/trial_runtime.py')=='frozen local bytes'
    with pytest.raises(Refused,match='frozen code'):
        trial_campaign.verify_source_revision(protocol)


def test_source_verification_missing_promisor_blob_cannot_lazy_fetch(tmp_path,monkeypatch):
    from ams import trial_campaign
    root,git,protocol=source_repo(tmp_path,monkeypatch)
    blob=git('rev-parse','HEAD:src/ams/trial_runtime.py')
    marker=root/'FETCH_ATTEMPTED';upload=root/'synthetic-upload-pack'
    upload.write_text('#!/bin/sh\ntouch "'+str(marker)+'"\nexit 1\n');upload.chmod(0o700)
    git('config','extensions.partialClone','origin');git('config','remote.origin.promisor','true')
    git('config','remote.origin.url',str(root/'nonexistent-remote'))
    git('config','remote.origin.uploadpack',str(upload))
    (root/'.git/objects'/blob[:2]/blob[2:]).unlink()
    with pytest.raises(Refused):trial_campaign.verify_source_revision(protocol)
    assert not marker.exists()
    assert not (root/'.git/objects'/blob[:2]/blob[2:]).exists()
