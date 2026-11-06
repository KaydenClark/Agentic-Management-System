"""Bounded unsafe-receipt refusal and repository-lock release, synthetic only."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from ams import page_feedback
from test_page_feedback import prepare_feedback, feedback_request, submit_feedback
from test_pages import git, pages, room  # noqa:F401

PROBE = r'''
from pathlib import Path
import json, os, subprocess, sys
from ams.page_feedback import FeedbackOutcomeUnknown, replay_page_submission
from ams.project_paths import feedback_paths
root, event, mode = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
private = root / feedback_paths(root).private
packet = json.loads((private / (event + '.retained.json')).read_text())
form = packet['request'].copy()
form['verdict'] = form.pop('value')
original_open = os.open
swapped = False
if mode == 'replace-after-stat':
    def replace_receipt(name, flags, *args, **kwargs):
        global swapped
        if name == event + '.json' and kwargs.get('dir_fd') is not None and not swapped:
            swapped = True
            os.unlink(name, dir_fd=kwargs['dir_fd'])
            os.mkfifo(name, mode=0o600, dir_fd=kwargs['dir_fd'])
        return original_open(name, flags, *args, **kwargs)
    os.open = replace_receipt
try:
    replay_page_submission(root / 'grill-board/cards', form, '/answer')
except FeedbackOutcomeUnknown:
    print('refused-recoverably', flush=True)
else:
    raise SystemExit('unsafe receipt was accepted')
# This process stays alive while a separate process proves the lock is free.
lock_probe = 'from pathlib import Path; import sys; from ams.grill_board.answers import repository_lock; ' + '\nwith repository_lock(Path(sys.argv[1])): print("lock-released")'
result = subprocess.run([sys.executable, '-c', lock_probe, str(root)], timeout=2,
                        capture_output=True, text=True, check=True)
print(result.stdout.strip(), flush=True)
'''


@pytest.mark.parametrize('mode', ['fifo', 'replace-after-stat'])
def test_nonregular_receipt_refuses_promptly_and_releases_lock_without_writes(room, mode):
    card = prepare_feedback(room)
    request = feedback_request(room, card)
    commit = submit_feedback(room, card, request)
    private = room / '.local/page-feedback'
    packet = private / (request.event_id + '.json')
    original = packet.read_bytes()
    retained = private / (request.event_id + '.retained.json')
    retained.write_bytes(original)
    retained.chmod(0o600)
    if mode == 'fifo':
        packet.unlink()
        os.mkfifo(packet, mode=0o600)
    voice = (room / 'grill-board/voice-and-taste.md').read_bytes()
    environment = {**os.environ, 'PYTHONPATH': str(Path(page_feedback.__file__).resolve().parents[1])}
    try:
        result = subprocess.run([sys.executable, '-c', PROBE, str(room), request.event_id, mode],
                                env=environment, timeout=5, capture_output=True, text=True, check=True)
        assert result.stdout.splitlines() == ['refused-recoverably', 'lock-released']
        assert request.note not in result.stdout + result.stderr
    finally:
        assert git(room, 'rev-parse', 'HEAD') == commit
        assert (room / 'grill-board/voice-and-taste.md').read_bytes() == voice
        assert retained.read_bytes() == original
        assert json.loads(retained.read_text())['request']['note'] == request.note
    assert packet.is_fifo()
