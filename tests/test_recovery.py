"""Recovery identities and checkpoints carry evidence, never execution authority."""
from copy import deepcopy
import hashlib

import pytest

from ams import recovery


def job(namespace="test-recovery", *, job_id="job-1", payload=b"safe synthetic effect"):
    return dict(namespace=namespace, job_id=job_id, spec_id="S-006", task_id="TK-002O",
                campaign_id="synthetic-recovery", case_id="case-v1", candidate_id="candidate-1",
                case_digest="b"*64, skills_commit="d"*40, release_digest="e"*64,
                source_commit="a"*40, is_test=True, synthetic=True,
                slots=[dict(role="publication", arm="candidate", repetition=1,
                            effect_type="keyed-file", payload_digest=hashlib.sha256(payload).hexdigest())])


def test_effect_slot_key_survives_job_task_campaign_renaming():
    first = dict(job(), chain_id="repair-chain", attempt=1)
    second = deepcopy(first)
    second.update(job_id="new-job", task_id="TK-999", campaign_id="renamed")
    assert recovery.effect_key(first, first["slots"][0]) == recovery.effect_key(second, second["slots"][0])
    second["attempt"] = 2
    assert recovery.effect_key(first, first["slots"][0]) != recovery.effect_key(second, second["slots"][0])


@pytest.mark.parametrize("mutation", [
    lambda j: j.update(raw_packet={"secret": "private"}),
    lambda j: j["slots"][0].update(prompt="private"),
    lambda j: j["slots"][0].update(payload_digest="not-pinned"),
    lambda j: j["slots"].append(deepcopy(j["slots"][0])),
    lambda j: j.update(synthetic=True, is_test=False),
    lambda j: j.update(case_digest="main"),
])
def test_job_rejects_private_or_unfrozen_inputs(mutation):
    value = job(); mutation(value)
    with pytest.raises(recovery.Refused): recovery.validate_job(value)


def test_keyed_file_effect_is_atomic_and_readback_bound(tmp_path):
    adapter = recovery.KeyedFileEffect(tmp_path)
    payload = b"safe synthetic effect"; expected = hashlib.sha256(payload).hexdigest(); key="1"*64
    assert adapter.lookup(key, expected)["outcome"] == "absent"
    result = adapter.apply(key, payload)
    assert result["outcome"] == "matched"
    assert adapter.lookup(key, expected) == result
    assert adapter.apply(key, payload) == result
    assert len(list(tmp_path.iterdir())) == 1
    assert adapter.lookup(key, "2"*64)["outcome"] == "conflict"


def test_missing_effect_store_is_unavailable_not_absent(tmp_path):
    adapter = recovery.KeyedFileEffect(tmp_path)
    tmp_path.rmdir()
    assert adapter.lookup("1"*64, "2"*64)["outcome"] == "unavailable"


def test_outage_keeps_safe_original_request_pending_without_publication(tmp_path):
    def unavailable(*args): raise OSError("private exception text")
    store = recovery.Store("http://127.0.0.1:1", "local-key", http=unavailable, pending_dir=tmp_path)
    with pytest.raises(recovery.Unavailable): store.create_job(job())
    pending=list(tmp_path.glob("*.pending.json"))
    assert len(pending)==1
    assert "local-key" not in pending[0].read_text()
    assert "private exception text" not in pending[0].read_text()
    assert "PrivateRecoveryStore" in repr(store)
