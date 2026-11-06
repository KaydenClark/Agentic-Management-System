"""Source-bound plans for agent-supplied Wiki synthesis; no semantic generation."""
from __future__ import annotations

from copy import deepcopy
import json
import posixpath
import re
import subprocess
from urllib.parse import unquote, urlsplit

from .memory import (BINDING, ENTRY, MAX_FILE, Corpus, MemoryError, _claims, _entries, _headings,
                     _source_bytes, digest, handling, safe_path, terms)

CLASSIFICATIONS = ('addition', 'evidence', 'correction', 'contradiction')


def _text(value, maximum=12000):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum or '\x00' in value:
        raise MemoryError('invalid-consolidation-text')
    return value


def _revision(raw):
    return 'sha256:' + digest(raw)


def _incoming(corpus, owner):
    rows = []
    for name in corpus.names():
        if name == owner or not (page := corpus.load(name)):
            continue
        # History is retained evidence, not an affected current summary.
        for line in ENTRY.sub('', page['body']).splitlines():
            for link in re.finditer(r'\[[^\]]+\]\(([^ )]+)\)', line):
                url = urlsplit(unquote(link[1]))
                if url.scheme or url.netloc or not url.path:
                    continue
                target = posixpath.normpath(posixpath.join(posixpath.dirname(name), url.path))
                if target == owner:
                    rows.append({'page': name, 'summary': line.strip()[:2000], 'anchor': url.fragment})
    return rows


def _preserved(before, after):
    """Reject edits of handling, native history, legacy evidence or old bindings."""
    prefix = before[:before.index('\n---', 4) + 4]
    if not after.startswith(prefix):
        raise MemoryError('immutable-handling')
    patterns = (ENTRY, re.compile(r'<!-- jot-legacy-source .*?<!-- /jot-legacy-source -->', re.S))
    for pattern in patterns:
        if [m[0] for m in pattern.finditer(before)] != [m[0] for m in pattern.finditer(after)]:
            raise MemoryError('immutable-history')
    _entries(after)
    old, new = _claims(before), _claims(after)
    if any(claim not in new for claim in old):
        raise MemoryError('immutable-bindings')
    return after


def consolidation_plan(root, request):
    if not isinstance(request, dict) or set(request) - {'topic', 'owner', 'changes', 'edits', 'jots'}:
        raise MemoryError('invalid-consolidation-request')
    corpus = Corpus(root)
    topic = _text(request['topic'], 500)
    router = corpus.load(corpus.wiki + '/MEMORY.md')
    if not router:
        raise MemoryError('unavailable-router')
    # Inspect bounded Wiki pages only; no source bodies are followed here.
    owner = request.get('owner')
    if owner:
        corpus.load(owner)
    incoming = _incoming(corpus, owner)
    candidates = []
    for name, page in corpus.pages.items():
        if page and name != router['path'] and page['metadata']['status'] != 'archived':
            overlap = len(terms(topic) & terms(page['title'] + ' ' + ' '.join(p['content'] for p in page['parts'])))
            if overlap >= min(2, len(terms(topic))):
                candidates.append((overlap, name))
    candidates.sort(key=lambda c: (-c[0], c[1]))
    if owner is None:
        owner = candidates[0][1] if candidates else None
        incoming = _incoming(corpus, owner)
    if owner not in {name for _, name in candidates} or not incoming:
        raise MemoryError('no-sufficient-existing-owner')
    allowed = {owner, *(row['page'] for row in incoming)}
    changes = request['changes']
    edits = request.get('edits', [])
    jots = request.get('jots', [])
    if not isinstance(changes, list) or not 1 <= len(changes) <= 16 or not isinstance(edits, list) or len(edits) > 32 or not isinstance(jots, list) or len(jots) > 16:
        raise MemoryError('invalid-consolidation-bounds')
    classified = {key: [] for key in CLASSIFICATIONS}
    by_id, sources, unresolved = {}, {}, []
    for change in changes:
        identifier = _text(change['id'], 100)
        classification = change['classification']
        if identifier in by_id or classification not in classified or change['kind'] not in {'intent', 'observation', 'inference', 'proposal', 'question', 'verification'} or change['state'] not in {'current', 'confirmed', 'unresolved', 'experimental'}:
            raise MemoryError('invalid-consolidation-change')
        _text(change['summary'], 2000)
        if not isinstance(change['sources'], list) or not 1 <= len(change['sources']) <= 16:
            raise MemoryError('missing-consolidation-sources')
        confirmed_intent = False
        for source in change['sources']:
            identity = _text(source['identity'], 500)
            if source.get('reviewed_public') is not True:
                raise MemoryError('source-not-reviewed-public')
            raw = _source_bytes(corpus, identity)
            if len(sources) >= 32 and identity not in sources:
                raise MemoryError('invalid-consolidation-bounds')
            sources[identity] = {'identity': identity, 'sha256': digest(raw), 'reviewed_public': True}
            if '#jot-' in identity.lower():
                entries = _entries(raw.decode('utf-8'))
                confirmed_intent |= any(e['kind'] == 'intent' and e['state'] == 'confirmed' for e in entries)
        if change['state'] == 'confirmed' and (change['kind'] != 'intent' or not confirmed_intent):
            raise MemoryError('unsupported-confirmation')
        if change['kind'] == 'inference':
            _text(change.get('attribution'), 500)
            _text(change.get('limits'), 2000)
            if change['state'] != 'experimental':
                raise MemoryError('inference-remains-experimental')
        if classification == 'contradiction' or change['state'] == 'unresolved':
            unresolved.append(identifier)
        by_id[identifier] = change
        classified[classification].append(identifier)
    targets, proposed = {}, {}
    for operation in [*edits, *jots]:
        target = operation['target']
        # Check path/handling before any target body read, even for denied targets.
        path = safe_path(corpus.root, target)
        handling(path)
        if target not in allowed or target.startswith(corpus.wiki + '/history/') or target.endswith(('/SCHEMA.md', '/AGENTS.md')):
            raise MemoryError('unsupported-consolidation-target')
        change = by_id[operation['change']]
        if change['kind'] == 'intent' and change['state'] != 'confirmed':
            raise MemoryError('unresolved-governing-replacement')
        if not (page := corpus.load(target)):
            raise MemoryError('unavailable-consolidation-target')
        if page['metadata']['status'] == 'archived':
            raise MemoryError('unsupported-consolidation-target')
        raw = path.read_bytes()
        targets[target] = _revision(raw)
        proposed.setdefault(target, raw.decode('utf-8'))
    for edit in edits:
        before, after = _text(edit['before']), _text(edit['after'])
        content = proposed[edit['target']]
        if edit['change'] in unresolved and not after.startswith(before):
            raise MemoryError('unresolved-replacement')
        if content.count(before) != 1:
            raise MemoryError('ambiguous-or-missing-edit')
        proposed[edit['target']] = _preserved(content, content.replace(before, after, 1))
    for operation in jots:
        if set(operation) - {'target', 'change', 'kind', 'state', 'source', 'author', 'content', 'supersedes'}:
            raise MemoryError('invalid-native-operation')
        if operation['kind'] not in {'observation', 'inference', 'proposal', 'question', 'verification'} or operation['state'] not in {'current', 'unresolved', 'experimental'}:
            raise MemoryError('unsupported-native-confirmation')
        if operation['source'] not in {s['identity'] for s in by_id[operation['change']]['sources']}:
            raise MemoryError('unbound-native-source')
        _text(operation['author'], 120)
        content = _text(operation['content'])
        if '<!-- jot-' in content or '<!-- /jot-' in content:
            raise MemoryError('reserved-native-boundary')
        change = by_id[operation['change']]
        if operation['kind'] != change['kind'] or operation['state'] != change['state']:
            raise MemoryError('native-classification-mismatch')
        previous = operation.get('supersedes')
        if previous and operation['change'] in unresolved:
            raise MemoryError('unresolved-native-supersession')
        entries = corpus.pages[operation['target']]['entries']
        if any(e['id'] == previous and e['kind'] == 'intent' and e['state'] == 'confirmed' for e in entries):
            raise MemoryError('unsupported-native-confirmation')
        if previous and not any(e['id'] == previous for e in entries):
            raise MemoryError('invalid-native-supersession')
        if any(j['target'] == operation['target'] for j in jots if j is not operation):
            raise MemoryError('one-native-operation-per-target')
    # A whole-file source cannot also be edited. Anchored sources may share an owner.
    for identity, source in sources.items():
        name, _, anchor = identity.partition('#')
        if name in proposed:
            if not anchor:
                raise MemoryError('whole-source-is-target')
            original = _source_bytes(corpus, identity)
            if original.decode('utf-8') not in proposed[name]:
                raise MemoryError('immutable-source')
    for name, content in proposed.items():
        anchors = {head[3] for head in _headings(content)}
        old = corpus.pages[name]['claims']
        for claim in _claims(content):
            if claim['anchor'] not in anchors:
                raise MemoryError('invalid-bindings')
            if claim in old:
                continue
            if not claim['sources']:
                raise MemoryError('unbound-new-claim')
            for source in claim['sources']:
                if source.get('reviewed_public') is not True or source['identity'] not in sources or source['observations'][-1]['sha256'] != sources[source['identity']]['sha256']:
                    raise MemoryError('unsupported-new-claim')
    plan = {'status': 'planned', 'operation': 'consolidate-plan', 'owner': owner,
            'candidates': [name for _, name in candidates], 'request': deepcopy(request),
            'classifications': classified, 'unresolved': unresolved, 'incoming': incoming,
            'sources': list(sources.values()),
            'revisions': {'targets': targets, 'sources': {key: 'sha256:' + s['sha256'] for key, s in sources.items()}},
            'proposed': proposed, 'excluded': corpus.excluded,
            'limits': 'Agent supplies synthesis and authorization. Labels and repeated observations do not establish truth or confirmation. No write performed.'}
    plan['plan_id'] = digest(json.dumps(plan, sort_keys=True, ensure_ascii=False).encode())
    if len(json.dumps(plan, ensure_ascii=False).encode()) > MAX_FILE:
        raise MemoryError('consolidation-plan-bound')
    return plan


def _atomic_write(path, raw):
    import os
    import tempfile
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.ams-memory-', delete=False) as stream:
            temporary = stream.name
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def consolidation_apply(root, plan, authorization, revisions):
    """Preflight all targets/sources before the first live write; retain failures."""
    import os
    from pathlib import Path
    import tempfile

    if not isinstance(plan, dict):
        raise MemoryError('invalid-consolidation-plan')
    supplied_id = plan.get('plan_id')
    unsigned = {key: value for key, value in plan.items() if key != 'plan_id'}
    if supplied_id != digest(json.dumps(unsigned, sort_keys=True, ensure_ascii=False).encode()):
        raise MemoryError('invalid-consolidation-plan')
    if authorization != 'apply:' + supplied_id:
        raise MemoryError('operation-authority-required')
    if revisions != plan['revisions']:
        raise MemoryError('revision-acknowledgment-required')
    corpus = Corpus(root)
    # Check every target before rediscovery so stale/missing targets cannot be
    # silently dropped from a newly computed plan.
    for target, revision in plan['revisions']['targets'].items():
        path = safe_path(corpus.root, target)
        handling(path)
        if _revision(path.read_bytes()) != revision:
            raise MemoryError('stale-target')
    for identity, revision in plan['revisions']['sources'].items():
        if _revision(_source_bytes(corpus, identity)) != revision:
            raise MemoryError('changed-source-reinspection-required')
    current = consolidation_plan(root, plan['request'])
    if current['plan_id'] != supplied_id:
        raise MemoryError('changed-plan-reinspection-required')
    native_tool = _native_preflight(corpus, plan) if plan['request'].get('jots') else None
    lock = Path(tempfile.gettempdir()) / ('ams-memory-lock-' + digest(str(corpus.root).encode())[:24])
    try:
        lock.mkdir(mode=0o700)
    except FileExistsError:
        raise MemoryError('concurrent-consolidation') from None
    recovery = None
    written = []
    native = []
    try:
        # Revalidate after acquiring the operation lock. Native Jot/other editors
        # still have their own revision guards; no cross-file atomicity is claimed.
        for target, revision in plan['revisions']['targets'].items():
            path = safe_path(corpus.root, target)
            handling(path)
            if _revision(path.read_bytes()) != revision:
                raise MemoryError('stale-target')
        recovery = Path(tempfile.mkdtemp(prefix='ams-memory-recovery-'))
        originals = {}
        for index, target in enumerate(plan['proposed']):
            raw = safe_path(corpus.root, target).read_bytes()
            backup = f'{index}.original'
            (recovery / backup).write_bytes(raw)
            originals[target] = {'backup': backup, 'revision': _revision(raw)}
        journal = {'plan_id': supplied_id, 'originals': originals, 'written': written, 'status': 'prepared'}
        (recovery / 'journal.json').write_text(json.dumps(journal, indent=2))
        for target, text in plan['proposed'].items():
            path = safe_path(corpus.root, target)
            handling(path)
            if _revision(path.read_bytes()) != originals[target]['revision']:
                raise MemoryError('stale-target-during-write')
            for identity, revision in plan['revisions']['sources'].items():
                if _revision(_source_bytes(Corpus(root), identity)) != revision:
                    raise MemoryError('source-changed-during-write')
            _atomic_write(path, text.encode('utf-8'))
            written.append({'target': target, 'before': originals[target]['revision'], 'after': _revision(path.read_bytes())})
            journal['status'] = 'writing'
            (recovery / 'journal.json').write_text(json.dumps(journal, indent=2))
        for operation in plan['request'].get('jots', []):
            target = operation['target']
            path = safe_path(corpus.root, target)
            expected = next(row['after'] for row in written if row['target'] == target)
            if _revision(path.read_bytes()) != expected:
                raise MemoryError('stale-target-during-native-write')
            output = _native_capture(corpus.root, native_tool, operation, expected[7:], supplied_id)
            native.append(output)
            written.append({'target': target, 'before': expected, 'after': _revision(path.read_bytes()), 'native_id': output['entry']['id']})
            journal['native'] = native
            (recovery / 'journal.json').write_text(json.dumps(journal, indent=2))
        for identity, revision in plan['revisions']['sources'].items():
            if _revision(_source_bytes(Corpus(root), identity)) != revision:
                raise MemoryError('source-changed-during-write')
        journal['status'] = 'applied'
        (recovery / 'journal.json').write_text(json.dumps(journal, indent=2))
        return {'status': 'applied', 'operation': 'consolidate-apply', 'plan_id': supplied_id,
                'written': written, 'native': native, 'unresolved': plan['unresolved'], 'recovery': str(recovery),
                'sources': plan['sources'], 'limits': 'Local supplied synthesis only. Retained originals and journal support inspection/recovery; no confirmation, verification date or acceptance inferred.'}
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        if recovery is None:
            raise
        # Do not mask possible partial writes with a success or automatic rollback.
        return {'status': 'failed', 'operation': 'consolidate-apply', 'plan_id': supplied_id,
                'written': written, 'recovery': str(recovery),
                'reason': str(error) if isinstance(error, MemoryError) else 'write-failure',
                'limits': 'Inspect every target against retained originals and journal before an authorized recovery. No automatic rollback attempted.'}
    finally:
        lock.rmdir()


def _native_capture(root, tool, operation, revision, plan_id):
    import subprocess
    options = {key: value for key, value in operation.items() if key not in {'target', 'change'}}
    options.update(page=operation['target'], visibility='shared', revision=revision,
                   operation='ams-memory consolidation ' + plan_id)
    # Import the installed native operation; no copied parser or direct Jot write.
    script = "const m=await import(process.argv[1]);let s='';for await(const c of process.stdin)s+=c;const o=JSON.parse(s);const r=(o.supersedes?m.correctJot:m.addJot)(process.argv[2],o);process.stdout.write(JSON.stringify(r));"
    result = subprocess.run(['node', '--input-type=module', '-e', script, tool.as_uri(), str(root)],
                            input=json.dumps(options), text=True, capture_output=True, timeout=30)
    try:
        output = json.loads(result.stdout)
    except ValueError:
        raise MemoryError('native-operation-unavailable') from None
    if result.returncode or output.get('status') != 'added':
        raise MemoryError('native-refused-' + output.get('error', {}).get('code', 'unavailable'))
    return output


def _native_preflight(corpus, plan):
    import subprocess
    import tempfile
    from pathlib import Path
    tool = safe_path(corpus.root, 'workbench/tools/jot.mjs')
    if not tool.is_file():
        raise MemoryError('native-operation-unavailable')
    # Native capture has no dry-run. Exercise the exact operations in a private
    # disposable Git room, copying only already eligible explicit public inputs.
    with tempfile.TemporaryDirectory(prefix='ams-memory-preflight-') as directory:
        staged = Path(directory)
        run = subprocess.run(['git', 'init', '-q', str(staged)], capture_output=True)
        if run.returncode:
            raise MemoryError('native-preflight-unavailable')
        manifest = staged / 'workbench/manifest.json'
        manifest.parent.mkdir(parents=True)
        manifest.write_bytes(safe_path(corpus.root, 'workbench/manifest.json').read_bytes())
        names = {identity.split('#')[0] for identity in plan['revisions']['sources']} | set(plan['proposed'])
        for name in names:
            target = staged / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(plan['proposed'][name].encode('utf-8') if name in plan['proposed'] else safe_path(corpus.root, name).read_bytes())
        for operation in plan['request']['jots']:
            revision = digest((staged / operation['target']).read_bytes())
            _native_capture(staged, tool, operation, revision, plan['plan_id'])
    return tool
