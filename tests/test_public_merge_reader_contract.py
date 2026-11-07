"""Offline source-backed fixture for the existing Python -> public-reader seam."""
import hashlib
import json
from pathlib import Path

from ams import writer


def test_public_merge_fixture_is_exact_existing_python_producer_output():
    root = Path(__file__).resolve().parents[1]
    fixture = json.loads((root / 'site/app/rsi/fixtures/merge-from-writer.json').read_text())
    assert fixture['producerMain'] == 'c787b2958fa7a23f55c6406f3ce367a91e9162dc'
    assert hashlib.sha256(Path(writer.__file__).read_bytes()).hexdigest() == fixture['writerSha256']
    calls = []

    def git_only(args):
        calls.append(args)
        return fixture['gitShow']

    row = writer.merge_event(fixture['row']['source_ref'], git=git_only)
    assert row == fixture['row']
    assert calls == [['show', '-s', '--format=%H%n%P%n%cI%n%s%n%b', row['source_ref']]]
    assert row['subject'] == 'PR #186'
