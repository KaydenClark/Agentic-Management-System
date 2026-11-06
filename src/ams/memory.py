"""Read-only, navigation-first Wiki recall and explicit claim/source freshness.

Markdown remains the knowledge owner. This module never follows reference bodies
unless a claim explicitly marks a supported local source as reviewed public.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import date, datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

MAX_FILE = 1_000_000
MAX_PAGES = 128
MAX_CORPUS = 4_000_000
KINDS = {'intent', 'observation', 'inference', 'proposal', 'question', 'verification'}
STATES = {'current', 'confirmed', 'unresolved', 'experimental'}
STOP = set('a an and are as at be by do does for from how in is it of on or should that the their this to what when where which who why with'.split())
BINDING = re.compile(r'<!-- ams-memory-bindings\s*\n(.*?)\n-->', re.S)
ENTRY = re.compile(r'<!-- jot-entry -->\n### ([\w-]+)\nKind: ([^\n]+)\nState: ([^\n]+)\nRecorded: ([^\n]+)\nAuthor: ([^\n]+)\nSource: ([^\n]+)\nTopic: ([^\n]+)\nSupersedes: ([^\n]+)\n\n(.*?)\n<!-- /jot-entry -->', re.S)
MD = MarkdownIt()


class MemoryError(ValueError):
    """A refusal whose code is safe to expose without echoing source content."""


def encoded(value):
    return json.dumps(value, ensure_ascii=False, indent=2)


def digest(value: bytes):
    return hashlib.sha256(value).hexdigest()


def terms(value):
    return set(re.findall(r'[\w]+', value.lower())) - STOP


def slug(value):
    return re.sub(r'[^\w\- ]', '', value.lower()).replace(' ', '-')


def _git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, timeout=10)
    if result.returncode not in (0, 1):
        raise MemoryError('git-unavailable')
    return result


def safe_path(root: Path, name: str):
    path = PurePosixPath(name)
    if not name or '\\' in name or '\x00' in name or path.is_absolute() or any(p in ('..', '.') or p.startswith('.') for p in name.split('/')):
        raise MemoryError('unsafe-path')
    current = root
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise MemoryError('unsafe-path')
    if _git(root, 'check-ignore', '--quiet', '--no-index', '--', name).returncode == 0:
        raise MemoryError('ignored')
    if current.exists() and (not current.is_file() or current.stat().st_nlink != 1 or current.stat().st_size > MAX_FILE):
        raise MemoryError('unsafe-file')
    return current


def handling(path: Path, *, required=True):
    """Read only the bounded frontmatter, never a denied page's body."""
    with path.open('rb') as stream:
        first = stream.readline(256)
        if first.rstrip(b'\r\n') != b'---':
            if required:
                raise MemoryError('invalid-handling')
            return {}, 0
        lines = []
        size = len(first)
        while size < 16384:
            line = stream.readline(16384 - size)
            size += len(line)
            if line.rstrip(b'\r\n') == b'---':
                break
            if not line:
                raise MemoryError('invalid-handling')
            lines.append(line.decode('utf-8'))
        else:
            raise MemoryError('invalid-handling')
    data = {}
    for line in lines:
        if line.startswith((' ', '\t')) or not line.strip():
            continue
        match = re.fullmatch(r'([a-z_]+):(?: +(.*))?\r?\n?', line)
        if not match or match[1] in data:
            raise MemoryError('invalid-handling')
        value = (match[2] or '').strip()
        if value.startswith(('"', "'")):
            if len(value) < 2 or value[-1] != value[0]:
                raise MemoryError('invalid-handling')
            value = value[1:-1]
        data[match[1]] = value
    if data.get('sensitivity') not in {'normal', 'private', 'restricted'}:
        raise MemoryError('invalid-handling')
    if data['sensitivity'] != 'normal':
        raise MemoryError('excluded-handling')
    if required and (data.get('status') not in {'active', 'partial', 'stale', 'archived'} or data.get('knowledge_role') not in {'canonical', 'curated', 'derived', 'historical'}):
        raise MemoryError('invalid-handling')
    return data, size


def _read_json(path):
    # Explicit CLI input, never a discovered reference. No paths are echoed.
    path = Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_FILE:
        raise MemoryError('invalid-json-input')
    try:
        return json.loads(path.read_text())
    except (UnicodeError, ValueError):
        raise MemoryError('invalid-json-input') from None


def _claims(body):
    matches = list(BINDING.finditer(body))
    if body.count('<!-- ams-memory-bindings') != len(matches) or len(matches) > 1:
        raise MemoryError('invalid-bindings')
    if not matches:
        return []
    try:
        block = json.loads(matches[0][1])
        if block['version'] != 1 or not isinstance(block['claims'], list):
            raise ValueError()
        seen = set()
        for claim in block['claims']:
            if not re.fullmatch(r'[\w-]{1,100}', claim['id']) or claim['id'] in seen or not re.fullmatch(r'[\w-]{1,200}', claim['anchor']):
                raise ValueError()
            seen.add(claim['id'])
            if claim.get('supersedes') is not None and not isinstance(claim['supersedes'], str):
                raise ValueError()
            if not isinstance(claim['sources'], list):
                raise ValueError()
            for source in claim['sources']:
                if not isinstance(source['identity'], str) or len(source['identity']) > 500 or not isinstance(source.get('reviewed_public', False), bool):
                    raise ValueError()
                observations = source['observations']
                if not isinstance(observations, list) or not observations:
                    raise ValueError()
                for observed in observations:
                    if not re.fullmatch(r'[a-f0-9]{64}', observed['sha256']):
                        raise ValueError()
                    date.fromisoformat(observed['observed_at'])
                    if observed.get('revision') is not None and not re.fullmatch(r'[a-f0-9]{40,64}', observed['revision']):
                        raise ValueError()
        return block['claims']
    except (KeyError, TypeError, ValueError):
        raise MemoryError('invalid-bindings') from None


def _entries(body):
    # Legacy snapshots remain cold evidence, not recursively parsed native entries.
    body = re.sub(r'<!-- jot-legacy-source .*?<!-- /jot-legacy-source -->', '', body, flags=re.S)
    matches = list(ENTRY.finditer(body))
    if body.count('<!-- jot-entry -->') != len(matches) or body.count('<!-- /jot-entry -->') != len(matches):
        raise MemoryError('invalid-jot')
    entries = {}
    for match in matches:
        id, kind, state, recorded, author, source, topic, previous, content = match.groups()
        try:
            datetime.fromisoformat(recorded.replace('Z', '+00:00'))
        except ValueError:
            raise MemoryError('invalid-jot') from None
        if id in entries or kind not in KINDS or state not in STATES:
            raise MemoryError('invalid-jot')
        entries[id] = {'id': id, 'kind': kind, 'state': state, 'recorded': recorded, 'author': author, 'source': source, 'topic': topic, 'supersedes': None if previous == 'none' else previous, 'content': content, 'subject': re.sub(r'^#+\s*', '', content.splitlines()[0])[:200]}
    newer = {}
    for entry in entries.values():
        previous = entry['supersedes']
        if previous:
            if previous not in entries or previous in newer:
                raise MemoryError('invalid-jot')
            newer[previous] = entry['id']
        seen = {entry['id']}
        while previous:
            if previous in seen or previous not in entries:
                raise MemoryError('invalid-jot')
            seen.add(previous)
            previous = entries[previous]['supersedes']
    result = []
    for entry in entries.values():
        if entry['id'] in newer:
            continue
        entry = deepcopy(entry)
        entry['correction_context'] = []
        previous = entry['supersedes']
        while previous:
            original = {**entries[previous], 'state': 'superseded', 'recorded_state': entries[previous]['state'], 'superseded_by': newer[previous]}
            entry['correction_context'].append(original)
            previous = original['supersedes']
        result.append(entry)
    return result


def sections(body):
    lines = body.splitlines(keepends=True)
    heads = []
    counts = {}
    for index, token in enumerate(tokens := MD.parse(body)):
        if token.type != 'heading_open':
            continue
        heading = tokens[index + 1].content
        anchor = slug(heading)
        count = counts.get(anchor, 0)
        counts[anchor] = count + 1
        heads.append((token.map[0], token.map[1], heading, anchor + (f'-{count}' if count else ''), int(token.tag[1:])))
    title = next((h[2] for h in heads if h[4] == 1), '')
    result = []
    context = []
    for i, (start, end, heading, anchor, level) in enumerate(heads):
        while context and context[-1][0] >= level:
            context.pop()
        context.append((level, heading))
        stop = heads[i + 1][0] if i + 1 < len(heads) else len(lines)
        content = ''.join(lines[end:stop]).strip()
        if content:
            result.append({'heading': heading, 'anchor': anchor, 'heading_path': [h[1] for h in context], 'content': content})
    return title, result, {h[3] for h in heads}


class Corpus:
    def __init__(self, root):
        self.root = Path(root).absolute()
        if any(p.is_symlink() for p in [self.root, *self.root.parents]):
            raise MemoryError('unsafe-project')
        manifest = json.loads(safe_path(self.root, 'workbench/manifest.json').read_text())
        self.wiki = manifest['lanes']['wiki'].rstrip('/')
        # Validate the declared lane without reading a directory body.
        safe_path(self.root, self.wiki + '/MEMORY.md')
        self.excluded = []
        self.pages = {}
        self.bytes = 0
        self.scanned = 0

    def load(self, name):
        if name in self.pages:
            return self.pages[name]
        self.scanned += 1
        if self.scanned > MAX_PAGES or self.bytes > MAX_CORPUS:
            raise MemoryError('corpus-bound')
        try:
            if not name.startswith(self.wiki + '/') or not name.endswith('.md'):
                raise MemoryError('outside-wiki')
            path = safe_path(self.root, name)
            meta, offset = handling(path)
            if self.bytes + path.stat().st_size > MAX_CORPUS:
                raise MemoryError('corpus-bound')
            raw = path.read_bytes()
            self.bytes += len(raw)
            body = raw[offset:].decode('utf-8').replace('\r\n', '\n')
            claims = _claims(body)
            entries = _entries(body)
            prose = ENTRY.sub('', body)
            prose = re.sub(r'<!-- jot-legacy-source .*?<!-- /jot-legacy-source -->', '', prose, flags=re.S)
            title, parts, anchors = sections(BINDING.sub('', prose))
            if any(c['anchor'] not in anchors for c in claims):
                raise MemoryError('invalid-bindings')
            page = {'path': name, 'title': title or Path(name).stem, 'metadata': meta, 'revision': 'sha256:' + digest(raw), 'body': body, 'parts': parts, 'entries': entries, 'claims': claims}
            self.pages[name] = page
            return page
        except (MemoryError, OSError, UnicodeError) as exc:
            self.excluded.append({'page': name, 'reason': str(exc) if isinstance(exc, MemoryError) else 'unavailable'})
            self.pages[name] = None
            return None

    def names(self):
        """Flat active Wiki collections only; never follow directory symlinks."""
        base = self.root / self.wiki
        for directory in [base, *(base / p for p in ('design-concepts', 'features', 'guidebooks', 'history'))]:
            if directory.is_symlink() or not directory.exists():
                continue
            for path in sorted(directory.iterdir()):
                if path.suffix == '.md' and not path.name.startswith('.'):
                    yield str(path.relative_to(self.root))


def _routes(router):
    routes = []
    for line in router['body'].splitlines():
        for match in re.finditer(r'\[([^\]]+)\]\(([^ )]+)\)', line):
            target = unquote(match[2]).split('#')[0]
            if not target or ':' in target or target.startswith('/'):
                continue
            path = PurePosixPath(router['path']).parent / target
            # Wiki routes must stay in the lane, not traverse to root source bodies.
            if '..' in path.parts or not target.endswith('.md'):
                continue
            routes.append({'target': str(path), 'label': match[1], 'summary': line.strip()[:600], 'page': router['path']})
    return routes


def _source_bytes(corpus, identity):
    parsed = urlsplit(identity)
    if parsed.scheme or parsed.netloc or parsed.query:
        raise MemoryError('unsupported-source')
    name, _, anchor = identity.partition('#')
    path = safe_path(corpus.root, name)
    if not path.exists():
        raise FileNotFoundError()
    if _git(corpus.root, 'ls-files', '--error-unmatch', '--', name).returncode != 0:
        raise MemoryError('source-not-tracked')
    root_docs = {'AGENTS.md', 'BLUEPRINT.md', 'GLOSSARY.md', 'ARCHITECTURE.md', 'RUNBOOK.md', 'README.md'}
    if path.suffix != '.md' or '/' not in name and name not in root_docs:
        raise MemoryError('unsupported-source')
    if not name.startswith(corpus.wiki + '/') and not (name in root_docs or name.startswith(('workbench/docs/', 'workbench/landmarks/', 'workbench/specs/', 'grill-board/'))):
        raise MemoryError('unsupported-source')
    handling(path, required=name.startswith(corpus.wiki + '/'))
    raw = path.read_bytes()
    if not anchor:
        return raw
    text = raw.decode('utf-8')
    if anchor.lower().startswith('jot-'):
        # Hash exact retained native block, including its original labels and bytes.
        for match in ENTRY.finditer(text):
            if match[1].lower() == anchor.lower():
                return match[0].encode('utf-8')
        raise MemoryError('missing-source-anchor')
    # Only heading sections are supported; links never trigger recursive ingestion.
    lines = text.splitlines(keepends=True)
    tokens = MD.parse(text)
    for i, token in enumerate(tokens):
        if token.type == 'heading_open' and slug(tokens[i + 1].content) == anchor:
            end = len(lines)
            for following in tokens[i + 2:]:
                if following.type == 'heading_open' and int(following.tag[1:]) <= int(token.tag[1:]):
                    end = following.map[0]
                    break
            return ''.join(lines[token.map[0]:end]).encode('utf-8')
    raise MemoryError('missing-source-anchor')


def _claim_status(corpus, page, claim, previous):
    output = {'id': claim['id'], 'explanation': page['path'] + '#' + claim['anchor'], 'supersedes': claim.get('supersedes'), 'sources': [], 'possibly_stale': False}
    for source in claim['sources']:
        row = {**deepcopy(source), 'status': 'unavailable'}
        try:
            if source.get('reviewed_public') is not True:
                raise MemoryError('source-not-reviewed-public')
            observed = digest(_source_bytes(corpus, source['identity']))
            expected = source['observations'][-1]['sha256']
            row['current_sha256'] = observed
            row['status'] = 'unchanged' if observed == expected else 'possibly-stale'
            prior = previous.get((output['explanation'], claim['id'], source['identity']))
            if row['status'] == 'unchanged' and prior and prior != observed:
                row['status'] = 'restored'
            elif observed != expected and any(o['sha256'] == observed for o in source['observations'][:-1]):
                row['status'] = 'restored-historical'
        except FileNotFoundError:
            row['status'] = 'missing'
        except (MemoryError, OSError, UnicodeError, ValueError) as exc:
            row['reason'] = str(exc) if isinstance(exc, MemoryError) else 'unavailable'
        if row['status'] not in {'unchanged', 'restored'}:
            output['possibly_stale'] = True
        output['sources'].append(row)
    if not claim['sources']:
        output['possibly_stale'] = True
        output['status'] = 'unbound'
    return output


def check(root, previous=None):
    corpus = Corpus(root)
    prior = {}
    if previous is not None:
        if not isinstance(previous, dict) or previous.get('operation') != 'check':
            raise MemoryError('invalid-previous-check')
        try:
            prior = {(c['explanation'], c['id'], s['identity']): s.get('current_sha256') for c in previous['claims'] for s in c['sources']}
        except (KeyError, TypeError):
            raise MemoryError('invalid-previous-check') from None
    claims, unbound = [], []
    for name in corpus.names():
        if not (page := corpus.load(name)):
            continue
        if not page['claims']:
            unbound.append(name)
        claims.extend(_claim_status(corpus, page, claim, prior) for claim in page['claims'])
    return {'status': 'ok', 'operation': 'check', 'claims': claims, 'unbound': unbound, 'excluded': corpus.excluded, 'limits': 'Changed/restored bytes are review signals, not truth or renewed verification. No source, claim, date or confirmation was written.'}


def _hit(page, part, route):
    return {'page': page['path'], 'page_title': page['title'], 'heading': part['heading'], 'heading_path': part.get('heading_path', []), 'kind': part.get('kind', 'section'), 'state': part.get('state', page['metadata']['status']), 'revision': page['revision'], 'navigation': route, **part}


def query(root, text, *, limit=6, max_chars=6400):
    if not isinstance(text, str) or not text.strip() or len(text) > 500 or not 1 <= limit <= 20 or not 1000 <= max_chars <= 48000:
        raise MemoryError('invalid-query-bounds')
    corpus = Corpus(root)
    router = corpus.load(corpus.wiki + '/MEMORY.md')
    if not router:
        raise MemoryError('unavailable-router')
    wanted = terms(text)
    routes = _routes(router)
    routes.sort(key=lambda r: (-len(wanted & terms(r['summary'])), r['target']))
    relevant = [r for r in routes if wanted & terms(r['summary'])][:3]
    candidates = []

    def collect(page, route):
        if page['metadata']['status'] == 'archived':
            return
        for part in page['parts']:
            content_terms = terms(part['content'])
            overlap = wanted & (content_terms | terms(part['heading']))
            if len(overlap) < min(2, len(wanted)):
                continue
            context = wanted & terms(page['title'] + ' ' + part['heading'])
            score = len(overlap) * 3 + len(context) * 2
            item = _hit(page, part, route)
            item['source_references'] = list(dict.fromkeys(re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', part['content'])))[:8]
            item['claims'] = [_claim_status(corpus, page, c, {}) for c in page['claims'] if c['anchor'] == part['anchor']]
            item['freshness'] = 'bound' if item['claims'] else 'unbound'
            candidates.append((score, item))
        for entry in page['entries']:
            search = entry['content'] + ' ' + ' '.join(e['content'] for e in entry['correction_context'])
            overlap = wanted & terms(search)
            if len(overlap) < min(2, len(wanted)):
                continue
            score = len(overlap) * 3 + len(wanted & terms(page['title'] + ' ' + entry['subject'])) * 2
            part = {'heading': entry['subject'], 'anchor': entry['id'].lower(), **deepcopy(entry)}
            candidates.append((score, _hit(page, part, route)))

    seen = set()
    for route in relevant:
        if route['target'] in seen:
            continue
        seen.add(route['target'])
        if page := corpus.load(route['target']):
            collect(page, {k: v for k, v in route.items() if k != 'target'})
    fallback = not candidates
    if fallback:
        for name in corpus.names():
            if name in seen or name == router['path']:
                continue
            seen.add(name)
            if page := corpus.load(name):
                collect(page, None)
    candidates.sort(key=lambda pair: (-pair[0], pair[1]['page'], pair[1]['anchor']))
    result = {'status': 'ok' if candidates else 'unknown', 'query': text, 'hits': [], 'fallback': fallback, 'omitted': len(candidates), 'truncated': False, 'excluded': corpus.excluded[:8], 'continuation': 'Read named page/anchor or increase --max-chars/--limit; references are pointers, not authority.'}
    # The bound applies to the full pretty JSON response (including metadata),
    # not merely excerpt text. Reserve continuation and limit metadata first.
    for _, original in candidates[:limit]:
        hit = deepcopy(original)
        hit['content_truncated'] = False
        for old in hit.get('correction_context', []):
            old['content'] = old['content'][:600]
        result['hits'].append(hit)
        result['omitted'] -= 1
        if len(encoded(result)) + 1 > max_chars:
            overflow = len(encoded(result)) + 1 - max_chars
            hit['content'] = hit['content'][:max(0, len(hit['content']) - overflow - 32)]
            hit['content_truncated'] = True
            result['truncated'] = True
        if len(encoded(result)) + 1 > max_chars or not hit['content']:
            result['hits'].pop()
            result['omitted'] += 1
            break
    # Many exclusion records or a long question must not defeat the output cap.
    while len(encoded(result)) + 1 > max_chars and result['excluded']:
        result['excluded'].pop()
        result['truncated'] = True
    if not result['omitted'] and not result['truncated']:
        result['continuation'] = None
    if candidates and not result['hits']:
        result['status'] = 'bounded'
    return result


def evaluate(root, cases, baseline=None):
    if cases.get('version') != 1 or not isinstance(cases.get('cases'), list):
        raise MemoryError('invalid-evaluation')
    root = Path(root)
    mismatches = []
    if baseline is not None:
        if (baseline.get('version') != 1 or not baseline.get('wiki_sha256')
                or not isinstance(baseline.get('rows'), list)
                or baseline.get('cases_identity_sha256') != digest(json.dumps(cases, sort_keys=True).encode())
                or not re.fullmatch(r'[a-f0-9]{40,64}', baseline.get('source_revision', ''))):
            raise MemoryError('invalid-baseline')
        if baseline.get('source_revision') != cases.get('source_revision') or baseline.get('budget') != cases.get('budget'):
            raise MemoryError('baseline-identity-mismatch')
        corpus = Corpus(root)
        if set(corpus.names()) != set(baseline['wiki_sha256']):
            raise MemoryError('baseline-source-mismatch')
        # Compare exactly the frozen public Wiki bytes, not the installed CLI.
        for name, expected in baseline['wiki_sha256'].items():
            if not name.startswith(corpus.wiki + '/') or '/archive/' in name or not re.fullmatch(r'[a-f0-9]{64}', expected):
                raise MemoryError('invalid-baseline')
            try:
                path = safe_path(root, name)
                handling(path)
                actual = digest(path.read_bytes())
            except (MemoryError, OSError):
                actual = None
            if actual != expected:
                mismatches.append(name)
        if mismatches:
            raise MemoryError('baseline-source-mismatch')
    rows = []
    for case in cases['cases']:
        result = query(root, case['query'], **cases['budget'])
        sources = {h['page'] for h in result['hits']}
        jot_ids = {h.get('id') for h in result['hits']}
        row = {'id': case['id'], 'source_hit': not case['expected_sources'] or bool(sources & set(case['expected_sources'])), 'jot_hit': None if not case.get('expected_jot') else case['expected_jot'] in jot_ids, 'abstention_correct': result['status'] == 'unknown' if case.get('expect_abstention') else None, 'context_chars': len(encoded(result)) + 1, 'result': result}
        row['passed'] = row['source_hit'] and row['jot_hit'] is not False and row['abstention_correct'] is not False
        rows.append(row)
    return {'status': 'ok' if all(r['passed'] for r in rows) else 'failed', 'operation': 'evaluate', 'split': cases.get('split', 'unspecified'), 'source_revision': cases.get('source_revision'), 'same_source_verified': baseline is not None, 'budget': cases['budget'], 'baseline_rows': baseline.get('rows') if baseline else None, 'rows': rows, 'independent_answer_correctness': 'unmeasured', 'stale_answer_repetition': 'unmeasured', 'owner_correction_effort': 'unmeasured', 'limits': 'Deterministic development source/context checks only. No independent answer, held-out transfer or human-effort judgment.'}


def readable(result):
    if result.get('operation') != 'query' and 'hits' not in result:
        return encoded(result)
    lines = [f"{result['status']}: {result['query']}"]
    for hit in result['hits']:
        lines += [f"\n{hit['page_title']} / {hit['heading']} [{hit['kind']}; {hit['state']}]", f"{hit['page']}#{hit['anchor']} ({hit['revision']})", hit['content']]
        for old in hit.get('correction_context', []):
            lines += [f"Correction context: {old['id']} [superseded]", old['content']]
        if hit.get('source'):
            lines.append('Source: ' + hit['source'])
        for claim in hit.get('claims', []):
            lines.append('Claim ' + claim['id'] + ': ' + ', '.join(s['identity'] + ' [' + s['status'] + ']' for s in claim['sources']))
    if result['excluded']:
        lines.append(f"Excluded {len(result['excluded'])} unsafe/unavailable pages; JSON names reasons.")
    if result['continuation']:
        lines.append(result['continuation'])
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', default='.')
    sub = parser.add_subparsers(dest='command', required=True)
    q = sub.add_parser('query')
    q.add_argument('query')
    q.add_argument('--limit', type=int, default=6)
    q.add_argument('--max-chars', type=int, default=6400)
    c = sub.add_parser('check')
    c.add_argument('--previous')
    e = sub.add_parser('evaluate')
    e.add_argument('--cases', required=True)
    e.add_argument('--baseline')
    for command in (q, c, e):
        command.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'query':
            result = query(args.project, args.query, limit=args.limit, max_chars=args.max_chars)
        elif args.command == 'check':
            result = check(args.project, _read_json(args.previous) if args.previous else None)
        else:
            cases = _read_json(args.cases)
            baseline = _read_json(args.baseline) if args.baseline else None
            if baseline and baseline.get('cases_sha256') != digest(Path(args.cases).read_bytes()):
                raise MemoryError('baseline-case-mismatch')
            result = evaluate(args.project, cases, baseline)
        print(encoded(result) if args.json else readable(result))
        return 1 if result['status'] == 'failed' else 0
    except (MemoryError, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(encoded({'status': 'blocked', 'reason': str(exc) if isinstance(exc, MemoryError) else 'invalid-or-unavailable-input'}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
