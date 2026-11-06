"""Baseline is an executable reader and must enforce the same public boundary."""
import json
from pathlib import Path
import runpy
import sys

import pytest

from test_memory import HEADER, page, room

SCRIPT = Path(__file__).parents[1] / 'evals/wiki-memory/capture_baseline.py'


def test_baseline_private_route_refused_before_body_read(room, monkeypatch, capsys):
    protected = page(room, 'restricted.md', '# Protected\nNEVER-READ-BODY\n', HEADER.replace('normal', 'restricted'))
    case_file = room / 'cases.json'
    case_file.write_text(json.dumps({'version': 1, 'split': 'development', 'source_revision': 'a'*40, 'budget': {'limit': 6, 'max_chars': 6400}, 'cases': [{'id': 'private', 'query': 'protected', 'route': 'workbench/wiki/restricted.md', 'native_query': 'protected', 'expected_sources': []}]}))
    original = Path.read_text
    def guard(self, *args, **kwargs):
        if self == protected:
            pytest.fail('baseline read denied body before handling check')
        return original(self, *args, **kwargs)
    monkeypatch.setattr(Path, 'read_text', guard)
    monkeypatch.setattr(sys, 'argv', [str(SCRIPT), str(room), str(case_file), str(room / 'baseline.json')])
    with pytest.raises(SystemExit) as exited:
        runpy.run_path(str(SCRIPT), run_name='__main__')
    assert exited.value.code == 1
    assert json.loads(capsys.readouterr().out)['status'] == 'blocked'
    assert not (room / 'baseline.json').exists()


def test_baseline_source_identity_checked_before_native_call(room, monkeypatch, capsys):
    import subprocess
    case_file = room / 'cases.json'
    case_file.write_text(json.dumps({'version': 1, 'split': 'development', 'source_revision': 'a'*40, 'budget': {'limit': 6, 'max_chars': 6400}, 'cases': [{'id': 'valid', 'query': 'violet', 'route': 'workbench/wiki/context-violet.md', 'native_query': 'violet', 'expected_sources': ['workbench/wiki/context-violet.md']}]}))
    (room / 'corpus-manifest.json').write_text(json.dumps({'revision': 'a'*40, 'files': {'workbench/wiki/MEMORY.md': '0'*64, 'workbench/wiki/context-violet.md': '0'*64}}))
    def refused(*args, **kwargs):
        pytest.fail('native reader called before source identity validation')
    monkeypatch.setattr(subprocess, 'run', refused)
    # Keep the native-order assertion separate from established fixture Git facts.
    from types import SimpleNamespace
    monkeypatch.setattr('ams.memory._git', lambda root, *args: SimpleNamespace(returncode=1))
    monkeypatch.setattr(sys, 'argv', [str(SCRIPT), str(room), str(case_file), str(room / 'baseline.json')])
    with pytest.raises(SystemExit) as exited:
        runpy.run_path(str(SCRIPT), run_name='__main__')
    assert exited.value.code == 1
    assert json.loads(capsys.readouterr().out)['reason'] == 'baseline-source-mismatch'
    assert not (room / 'baseline.json').exists()


@pytest.mark.parametrize('kind', ['ignored', 'symlink', 'escape', 'malformed'])
def test_baseline_unsafe_routes_refuse_before_native(room, monkeypatch, capsys, kind):
    import subprocess
    protected = page(room, 'denied.md', '# Protected\nNEVER-READ-BODY\n')
    route = 'workbench/wiki/denied.md'
    if kind == 'ignored':
        (room / '.gitignore').write_text(route + '\n')
    elif kind == 'symlink':
        protected.unlink()
        protected.symlink_to(room / 'workbench/wiki/context-violet.md')
    elif kind == 'escape':
        route = 'workbench/wiki/../../outside.md'
    else:
        protected.write_text(HEADER.replace('sensitivity: normal', 'sensitivity: normal\nsensitivity: private') + 'NEVER-READ-BODY')
    cases = room / 'cases.json'
    cases.write_text(json.dumps({'version': 1, 'split': 'development', 'source_revision': 'a'*40, 'budget': {'limit': 6, 'max_chars': 6400}, 'cases': [{'id': 'unsafe', 'query': 'protected', 'route': route, 'native_query': 'protected', 'expected_sources': []}]}))
    original = subprocess.run
    def guard(args, *a, **kw):
        assert args[0] != 'node', 'native body reader ran before unsafe route refusal'
        return original(args, *a, **kw)
    monkeypatch.setattr(subprocess, 'run', guard)
    monkeypatch.setattr(sys, 'argv', [str(SCRIPT), str(room), str(cases), str(room / 'baseline.json')])
    with pytest.raises(SystemExit) as exited:
        runpy.run_path(str(SCRIPT), run_name='__main__')
    assert exited.value.code == 1
    assert json.loads(capsys.readouterr().out)['status'] == 'blocked'
    assert not (room / 'baseline.json').exists()
