"""Pinned private trial inputs, owned fixture reset and protected oracle identity."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil

from ams.assessment import Refused, require, same_artifact
from ams import trial_runtime as runtime

MARKER = '.ams-trial-fixture.json'
SCOPE = 'tool-free-transcript-interview-preservation'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                      allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def _unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON field')
        result[key] = value
    return result


def load(path):
    path = Path(path)
    _no_links(path)
    require(path.stat().st_size <= 2_000_000, 'JSON input exceeds limit')
    return json.loads(path.read_text(), object_pairs_hook=_unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(Refused('non-finite JSON number')))


def _hash(value, size=64):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{'+str(size)+'}', value) is not None,
            'full artifact hash required')


def _no_links(path):
    require('..' not in Path(path).parts, 'parent path traversal refused')
    for parent in (Path(path), *Path(path).absolute().parents):
        require(not parent.is_symlink(), 'symlink path refused')


def _relative(value):
    require(isinstance(value, str) and bool(value) and '\\' not in value,
            'relative artifact path required')
    path = PurePosixPath(value)
    require(not path.is_absolute() and str(path) == value and '..' not in path.parts
            and value != 'manifest.json', 'unsafe artifact path')
    return path


def validate_manifest(path):
    path = Path(path)
    require(path.name == 'manifest.json', 'manifest filename required')
    manifest = load(path)
    require(isinstance(manifest, dict) and type(manifest.get('schema')) is int and manifest['schema'] == 1,
            'manifest schema must be 1')
    _hash(manifest.get('sourceCommit'), 40)
    require(manifest.get('condition') in ('baseline', 'candidate'), 'artifact condition required')
    require(isinstance(manifest.get('repository'), str) and bool(manifest['repository']), 'repository identity required')
    entries = manifest.get('entries')
    require(isinstance(entries, list) and bool(entries), 'artifact entries required')
    listed = set()
    for entry in entries:
        require(isinstance(entry, dict), 'malformed artifact entry')
        relative = _relative(entry.get('path'))
        require(str(relative) not in listed, 'duplicate artifact path')
        listed.add(str(relative))
        file = path.parent/relative
        _no_links(file)
        require(file.is_file(), 'artifact file missing')
        data = file.read_bytes()
        require(type(entry.get('bytes')) is int and entry['bytes'] == len(data), 'artifact byte count changed')
        _hash(entry.get('sha256')); _hash(entry.get('gitBlob'), 40)
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'artifact content changed')
        require(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == entry['gitBlob'],
                'Git blob identity changed')
    actual = set()
    for file in path.parent.rglob('*'):
        _no_links(file)
        if file.is_file():
            actual.add(file.relative_to(path.parent).as_posix())
    require(actual == listed | {'manifest.json'}, 'unlisted artifact files')
    return manifest


def materialize(source, target, *, reset=False):
    source, target = Path(source), Path(target).absolute()
    manifest = validate_manifest(source)  # Refuse before creating anything.
    _no_links(target)
    require(not target.is_relative_to(source.parent.absolute())
            and not source.parent.absolute().is_relative_to(target), 'source/worker overlap refused')
    marker = {'kind': 'ams-owned-trial-fixture', 'schema': 1, 'manifestDigest': digest(manifest)}
    if target.exists():
        require(reset and target.is_dir() and (target/MARKER).is_file(), 'unowned/existing fixture refused')
        require(same_artifact(load(target/MARKER), marker), 'fixture source identity changed')
        for item in target.rglob('*'):
            _no_links(item)
        allowed_files = {MARKER, 'artifacts/manifest.json'} | {'artifacts/'+e['path'] for e in manifest['entries']}
        allowed_dirs = {str(parent) for file in allowed_files for parent in PurePosixPath(file).parents if str(parent) != '.'}
        require(all(item.relative_to(target).as_posix() in (allowed_files if item.is_file() else allowed_dirs)
                    for item in target.rglob('*')), 'unlisted fixture data preserved; reset refused')
        shutil.rmtree(target)
    target.mkdir(parents=True, mode=0o700)
    artifacts = target/'artifacts'; artifacts.mkdir(mode=0o700)
    for entry in manifest['entries']:
        dest = artifacts/entry['path']; dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((source.parent/entry['path']).read_bytes()); dest.chmod(0o600)
    (artifacts/'manifest.json').write_bytes(encoded(manifest)+b'\n')
    validate_manifest(artifacts/'manifest.json')
    (target/MARKER).write_bytes(encoded(marker)+b'\n')
    return {'sourceCommit': manifest['sourceCommit'], 'condition': manifest['condition'],
            'manifestDigest': marker['manifestDigest'], 'files': len(manifest['entries'])}


def fixture_identity(worker):
    worker = Path(worker)
    marker = load(worker/MARKER)
    manifest = validate_manifest(worker/'artifacts/manifest.json')
    require(same_artifact(marker, {'kind': 'ams-owned-trial-fixture', 'schema': 1,
                                  'manifestDigest': digest(manifest)}), 'fixture identity changed')
    return marker['manifestDigest']


def grader_reference(path, worker):
    path = Path(path).absolute(); worker = Path(worker).absolute()
    require(not path.is_relative_to(worker), 'grader must remain protected outside worker fixture')
    ref = load(path)
    require(isinstance(ref, dict) and type(ref.get('schema')) is int and ref['schema'] == 1
            and ref.get('kind') == 'interview-grader-reference', 'grader reference format changed')
    require(ref.get('model') == runtime.MODEL and ref.get('effort') == runtime.EFFORT,
            'grader model/effort changed')
    require(ref.get('qualification') in ('qualified', 'unqualified'), 'grader qualification required')
    _hash(ref.get('sourceRevision'), 40); _hash(ref.get('promptSha256'))
    prompt = path.parent/_relative(ref.get('promptFile'))
    _no_links(prompt)
    require(not prompt.absolute().is_relative_to(worker)
            and hashlib.sha256(prompt.read_bytes()).hexdigest() == ref['promptSha256'],
            'protected grader prompt changed')
    examples_path = path.parent/_relative(ref.get('examplesFile'))
    _hash(ref.get('examplesSha256')); _no_links(examples_path)
    require(not examples_path.absolute().is_relative_to(worker)
            and hashlib.sha256(examples_path.read_bytes()).hexdigest() == ref['examplesSha256'],
            'protected owner example bytes changed')
    examples = load(examples_path)
    require(isinstance(examples, dict) and examples.get('kind') == 'narrow-oracle-seeds' and isinstance(examples.get('source'), str)
            and isinstance(examples.get('examples'), list) and bool(examples['examples']), 'owner seed format missing')
    for example in examples['examples']:
        require(isinstance(example, dict) and example.get('label') in ('Yes', 'No')
                and isinstance(example.get('response'), str)
                and hashlib.sha256(example['response'].encode()).hexdigest() == example.get('responseSha256'),
                'owner-labelled response identity changed')
    return {'referenceDigest': digest(ref), 'promptDigest': ref['promptSha256'],
            'sourceRevision': ref['sourceRevision'], 'qualification': ref['qualification']}


def worker_prompt(worker, case_id, *, suite=None):
    """Expose declared source bytes as prompt context, never as native installation.

    Grader references are not accepted here. The transport has no file tools;
    all source exposure and its exact inventory happen before the worker starts.
    """
    worker = Path(worker)
    manifest_digest = fixture_identity(worker)
    manifest = validate_manifest(worker/'artifacts/manifest.json')
    suite_path = Path(suite) if suite is not None else Path(__file__).resolve().parents[2]/'evals/interview-dev-cases.json'
    cases = load(suite_path)
    require(cases.get('scope') == SCOPE and cases.get('conditions') == {
        'provider': 'firstParty', 'model': runtime.MODEL, 'effort': runtime.EFFORT, 'tools': [], 'mcpServers': []},
        'frozen suite conditions changed')
    matches = [case for case in cases.get('cases', []) if case.get('id') == case_id]
    require(len(matches) == 1 and matches[0].get('split') == 'dev', 'unique development case required')
    case = matches[0]
    require(isinstance(case.get('prompt'), str), 'case prompt missing')
    chunks = ['This controlled condition supplies skill source as context. It does not install or discover a skill. '
              'There are no tools or document provider. Report genuine missing capabilities; do not invent a write.']
    loaded = []
    for entry in manifest['entries']:
        if entry['path'].endswith('SKILL.md') or '/references/' in entry['path'] or entry['path'].endswith('GLOSSARY-FORMAT.md'):
            content = (worker/'artifacts'/entry['path']).read_text()
            chunks.append(json.dumps({'artifact': entry['path'], 'sha256': entry['sha256'], 'content': content}))
            loaded.append({'path': entry['path'], 'sha256': entry['sha256']})
    chunks.append('Current transcript task:\n'+case['prompt'])
    prompt = '\n\n'.join(chunks)
    identity = {'caseId': case_id, 'caseDigest': digest(case), 'suiteDigest': digest(cases),
                'manifestDigest': manifest_digest, 'loadedArtifacts': loaded,
                'nativeInstallation': False, 'promptDigest': hashlib.sha256(prompt.encode()).hexdigest()}
    return prompt, identity
