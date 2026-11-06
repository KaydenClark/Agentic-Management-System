"""Read a pinned capture made by an independently authenticated observer.

This module performs no requests and receives no credentials. A manifest does
not establish its own trust: the caller supplies deployment pins and the exact
capture digest from the trusted outer observation, outside the candidate build.
"""
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import stat
from urllib.parse import parse_qs, urlsplit

from .page_build import AMS_ORIGIN
from .pages import PageRefused, VOID, _metadata, _safe_file, content_hash


PIN_FIELDS = {'repository', 'project', 'deployment', 'candidate', 'origin', 'capture_sha256'}
_CAPTURE_SEAL = object()


@dataclass(frozen=True)
class _VerifiedCapture:
    record_json: str
    snapshot_sha256: str
    seal: object


def _snapshot_digest(candidate, inventory, html):
    # Bind raw bytes too: a caller may not change even an excluded/footer
    # region after the observer artifact has been validated.
    snapshot = {'candidate': candidate, 'inventory': inventory,
                'html_sha256': {route: hashlib.sha256(page.encode('utf-8')).hexdigest()
                                for route, page in html.items()}}
    return hashlib.sha256(json.dumps(snapshot, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def verified_record(capture, candidate, inventory, html):
    """Accept only the in-process result of validation for these exact inputs.

    This is a data-flow check, not authentication of arbitrary host code.
    Serialized records are evidence summaries; replay revalidates artifacts.
    """
    if not isinstance(capture, _VerifiedCapture) or capture.seal is not _CAPTURE_SEAL:
        raise PageRefused('protected generation requires a validated capture result')
    if capture.snapshot_sha256 != _snapshot_digest(candidate, inventory, html):
        raise PageRefused('validated capture differs from the generated snapshot')
    return json.loads(capture.record_json)


class _Identity(HTMLParser):
    def __init__(self, origin):
        super().__init__(convert_charrefs=True)
        self.origin, self.stack, self.commits, self.deployments = origin, [], set(), set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if 'footer' in self.stack and 'data-commit-sha' in attrs:
            self.commits.add(attrs['data-commit-sha'])
        for name in ('src', 'href'):
            value = attrs.get(name)
            if not isinstance(value, str):
                continue
            url = urlsplit(value)
            if url.path.startswith('/_next/') and (not url.netloc or f'{url.scheme}://{url.netloc}' == self.origin):
                self.deployments.update(parse_qs(url.query).get('dpl', []))

    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]


def _read(root, relative, limit):
    if (not isinstance(relative, str) or '\\' in relative or any(ord(c) < 32 for c in relative)
            or any(part in {'', '.', '..'} for part in relative.split('/'))):
        raise PageRefused('protected artifacts require plain relative file paths')
    path = _safe_file(root, relative)
    try:
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > limit:
            raise PageRefused('protected artifacts must be bounded regular files without hardlinks')
        raw = path.read_bytes()
    except PageRefused:
        raise
    except (OSError, ValueError) as error:
        raise PageRefused('protected artifact is unavailable') from error
    if len(raw) > limit:
        raise PageRefused('protected artifact exceeds its byte bound')
    return raw


def _pins(expected_pins):
    if not isinstance(expected_pins, dict) or set(expected_pins) != PIN_FIELDS:
        raise PageRefused('independent protected deployment and capture pins are required')
    pins = dict(expected_pins)
    for key, pattern in [('project', r'prj_[A-Za-z0-9]+'), ('deployment', r'dpl_[A-Za-z0-9]+'),
                         ('candidate', r'[0-9a-f]{40}'), ('capture_sha256', r'[0-9a-f]{64}')]:
        if not isinstance(pins[key], str) or not re.fullmatch(pattern, pins[key]):
            raise PageRefused(f'invalid protected {key} pin')
    if pins['repository'] != AMS_ORIGIN:
        raise PageRefused('protected repository pin is not the trusted AMS origin')
    if not isinstance(pins['origin'], str):
        raise PageRefused('protected origin pin must identify the immutable deployment')
    try:
        origin = urlsplit(pins['origin'])
    except ValueError as error:
        raise PageRefused('invalid protected origin pin') from error
    if (origin.scheme != 'https' or not origin.hostname or not origin.hostname.endswith('.vercel.app')
            or origin.username or origin.password or origin.query or origin.fragment
            or origin.path or origin.netloc != origin.hostname):
        raise PageRefused('protected origin pin must be an exact HTTPS deployment origin')
    return pins


def protection_record(expected_pins, observed_at):
    """Serialize only safe observer identity fields; this supplies no trust itself."""
    pins = _pins(expected_pins)
    try:
        when = datetime.fromisoformat(observed_at)
        if when.utcoffset() != timezone.utc.utcoffset(when):
            raise ValueError('UTC observation required')
    except (TypeError, ValueError) as error:
        raise PageRefused('protected observation timestamp must identify UTC') from error
    return {**pins, 'observed_at': observed_at}


def collect_protected(artifact_directory, built_snapshot, *, expected_pins):
    """Match an outer observer's complete capture to one frozen build.

    Only `/rsi` may have data-dependent HTML different from the local build.
    Its original protected HTML remains intact and fully content-hashed; no
    results or availability region is excluded or substituted here.
    """
    pins = _pins(expected_pins)
    if built_snapshot.get('candidate') != pins['candidate']:
        raise PageRefused('protected candidate pin differs from the frozen build')
    _metadata(built_snapshot['inventory'], built_snapshot['html'])
    kinds = built_snapshot['kinds']
    if set(kinds) != set(built_snapshot['html']) or any(kind not in {'page', 'visitor-404'} for kind in kinds.values()):
        raise PageRefused('protected build classification is incomplete')
    root = Path(artifact_directory)
    if root.is_symlink() or not root.is_dir():
        raise PageRefused('protected artifact directory must be a regular directory, not a symlink')
    root = root.resolve()
    raw = _read(root, 'manifest.json', 1024 * 1024)
    if hashlib.sha256(raw).hexdigest() != pins['capture_sha256']:
        raise PageRefused('protected capture digest differs from the independent observation')
    try:
        manifest = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as error:
        raise PageRefused('protected capture manifest is not readable JSON') from error
    if not isinstance(manifest, dict) or manifest.get('schema') != 1:
        raise PageRefused('unsupported protected capture schema')
    for key in PIN_FIELDS - {'capture_sha256'}:
        if manifest.get(key) != pins[key]:
            raise PageRefused(f'protected capture {key} differs from the independent pin')
    if manifest.get('observer') != 'authenticated-vercel-web-fetch' or not isinstance(manifest.get('observed_at'), str):
        raise PageRefused('protected capture needs the outer authenticated observation receipt')
    proof = protection_record(pins, manifest['observed_at'])
    pages = manifest.get('pages')
    if not isinstance(pages, dict) or set(pages) != set(kinds):
        raise PageRefused('protected capture route coverage differs from the complete frozen build')
    html, files, total = {}, set(), 0
    for route, kind in kinds.items():
        row = pages[route]
        if not isinstance(row, dict):
            raise PageRefused(f'{route}: invalid protected page receipt')
        file = row.get('file')
        if not isinstance(file, str) or not file.startswith('pages/') or file in files:
            raise PageRefused(f'{route}: protected page needs a unique relative file')
        files.add(file)
        try:
            url = urlsplit(row.get('url', ''))
        except (TypeError, ValueError) as error:
            raise PageRefused(f'{route}: invalid protected response URL') from error
        expected = 404 if kind == 'visitor-404' else 200
        if (f'{url.scheme}://{url.netloc}' != pins['origin'] or url.query or url.fragment
                or (kind == 'page' and url.path != route)
                or (kind == 'visitor-404' and url.path in kinds)
                or row.get('status') != expected
                or str(row.get('content_type', '')).split(';', 1)[0].strip().lower() != 'text/html'):
            raise PageRefused(f'{route}: protected status/type/origin/path differs from its build classification')
        body = _read(root, file, 10 * 1024 * 1024)
        total += len(body)
        if total > 64 * 1024 * 1024:
            raise PageRefused('complete protected capture exceeds its byte bound')
        if hashlib.sha256(body).hexdigest() != row.get('sha256'):
            raise PageRefused(f'{route}: protected body digest differs from the authenticated capture')
        try:
            page = body.decode('utf-8')
        except UnicodeDecodeError as error:
            raise PageRefused(f'{route}: protected HTML is not UTF-8') from error
        identity = _Identity(pins['origin'])
        try:
            identity.feed(page)
        except ValueError as error:
            raise PageRefused(f'{route}: protected HTML identity is malformed') from error
        if identity.commits != {pins['candidate']} or identity.deployments != {pins['deployment']}:
            raise PageRefused(f'{route}: protected HTML source/deployment identity differs or is absent')
        if route != '/rsi' and content_hash(page) != content_hash(built_snapshot['html'][route]):
            raise PageRefused(f'{route}: protected static content differs from the frozen build')
        content_hash(page)  # RSI must still provide the complete canonical main surface.
        html[route] = page
    verified = _VerifiedCapture(json.dumps(proof, sort_keys=True),
                                _snapshot_digest(pins['candidate'], built_snapshot['inventory'], html), _CAPTURE_SEAL)
    return {**built_snapshot, 'html': html, 'protection': proof, 'verified_capture': verified}
