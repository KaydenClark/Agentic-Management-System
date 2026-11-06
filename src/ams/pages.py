"""Generate local review cards from one identified, complete website build.

Review state belongs to the local Board. This module has no Supabase writer
and supplies no public-site approval endpoint.
"""

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .grill_board.answers import (
    AnswerRefused, _git, _write_and_commit, committed_blob, repository_lock,
)
from .grill_board.cards import Card, load_cards, parse_card
from .page_approvals import APPROVALS, INDEX, approval_recommendation, page_status

CARDS = "grill-board/cards"
LINE_BREAKS = "\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029"
VOID = set("area base br col embed hr img input link meta param source track wbr".split())
NAMED = {"amp": "&", "lt": "<", "gt": ">", "quot": '"', "apos": "'", "nbsp": "\u00a0"}
ATTR = re.compile(r'''([^\s"'>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?''')
TOKEN = re.compile(r'''<!--[\s\S]*?-->|<!\[CDATA\[[\s\S]*?\]\]>|<![^>]*>|</\s*([a-zA-Z][^\s/>]*)[^>]*>|<([a-zA-Z][^\s/>]*)((?:[^>"']|"[^"]*"|'[^']*')*?)(/?)>''')


class PageRefused(ValueError):
    """The page snapshot cannot safely create or validate review records."""


def _decode(text):
    def replace(match):
        ref = match[1]
        if not ref.startswith("#"):
            return NAMED.get(ref.lower(), match[0])
        code = int(ref[2:], 16) if ref[1:2].lower() == "x" else int(ref[1:])
        return chr(code) if code <= 0x10ffff else match[0]
    return re.sub(r"&(#x[0-9a-f]+|#[0-9]+|[a-z]+);", replace, text, flags=re.I)


def canonical_content(html):
    """Match the existing site/scripts/page-hash.mjs content contract.

    Attribute and text order, the six supported named entities and ASCII
    whitespace are deliberately identical to the existing site implementation.
    Browser DOM serialization would change that contract.
    """
    pieces, stack = [], []
    skip = None
    found = False
    last = 0
    while match := TOKEN.search(html, last):
        if found and stack and skip is None and match.start() > last:
            pieces.append(_decode(html[last:match.start()]))
        last = match.end()
        if match[2]:
            name = match[2].lower()
            if name in {"script", "style"}:
                closing = re.search(rf"</{name}\s*>", html[last:], re.I)
                last = last + closing.end() if closing else len(html)
                continue
            attrs = [(m[1].lower(), _decode(next((v for v in m.groups()[1:] if v is not None), "")))
                     for m in ATTR.finditer(match[3])]
            if not found:
                if name == "main" and ("id", "main") in attrs:
                    found = True
                    stack.append(name)
                continue
            names = {key for key, _ in attrs}
            excluded = bool(names & {"data-review-exclude", "data-review-mark"})
            if skip is None and not excluded:
                pieces.extend(value for key, value in attrs if key in {"href", "src", "alt"})
            if match[4] or name in VOID:
                continue
            stack.append(name)
            if skip is None and excluded:
                skip = len(stack)
        elif match[1] and found:
            name = match[1].lower()
            if name not in stack:
                continue
            at = len(stack) - 1 - stack[::-1].index(name)
            stack = stack[:at]
            if skip is not None and skip > len(stack):
                skip = None
            if not stack:
                break
    if not found:
        raise PageRefused('page has no <main id="main">')
    if stack and skip is None and last < len(html):
        pieces.append(_decode(html[last:]))
    return re.sub(r"[\t\n\f\r ]+", " ", " ".join(pieces)).strip(" ")


def content_hash(html):
    canonical = canonical_content(html)
    # Node's UTF-8 encoder replaces lone surrogate code points.
    canonical = "".join("\ufffd" if 0xd800 <= ord(c) <= 0xdfff else c for c in canonical)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _metadata(listed, built):
    result = {}
    for row in listed.get("pages", []):
        path = row.get("path", "")
        if not re.fullmatch(r"/(?:[a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_-]+)*)?", path):
            raise PageRefused(f"invalid page path: {path!r}")
        if path in result:
            raise PageRefused(f"duplicate page path: {path}")
        for key in ("title", "spec", "task"):
            if not isinstance(row.get(key), str) or not row[key].strip() or any(char in LINE_BREAKS for char in row[key]):
                raise PageRefused(f"{path}: invalid {key}")
        sources = row.get("sources")
        if not isinstance(sources, list) or not sources or any(
            not isinstance(source, str)
            or not source.strip()
            or any(char in LINE_BREAKS for char in source)
            or not re.fullmatch(r"(?![A-Za-z]:)[^/\\\x00-\x1f]+(?:/[^/\\\x00-\x1f]+)*/?", source)
            or any(part in {".", "..", ".git"} for part in source.rstrip("/").split("/"))
            for source in sources
        ):
            raise PageRefused(f"{path}: sources must name nonempty repository-relative paths")
        kind = row.get("provenance_kind", "historical-landing")
        if kind not in {"historical-landing", "verified-containment", "pending-candidate"}:
            raise PageRefused(f"{path}: unsupported provenance kind; current ownership and actual containment are required")
        landed = row.get("landed")
        if kind == "pending-candidate":
            if landed is not None:
                raise PageRefused(f"{path}: pending candidate cannot assert a landing")
        elif not isinstance(landed, dict) or not re.fullmatch(r"[0-9a-f]{40,64}", landed.get("commit", "")):
            raise PageRefused(f"{path}: no immutable landed commit")
        if landed is not None:
            branch = landed.get("branch")
            if not isinstance(branch, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9/._-]*", branch):
                raise PageRefused(f"{path}: provenance requires an explicit branch")
            pr = landed.get("pr")
            if pr is not None and (type(pr) is not int or pr < 1):
                raise PageRefused(f"{path}: provenance PR must be a positive number or unknown")
        result[path] = row
    missing = sorted(set(result) - set(built))
    uncovered = sorted(set(built) - set(result))
    if missing or uncovered:
        raise PageRefused("built/page-list coverage mismatch: " + "; ".join(
            [*(f"{p} has no built page" for p in missing), *(f"{p} has no page-list owner" for p in uncovered)]))
    if not result:
        raise PageRefused("the built page inventory is empty")
    return result


def _safe_file(root, relative):
    path = Path(root)
    for part in relative.split("/"):
        path /= part
        if path.is_symlink():
            raise PageRefused(f"generated path crosses a symlink: {relative}")
    return path


def _stamp(now):
    return (now or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _new_card(row, digest, candidate, *, protected=False):
    landed = row.get("landed")
    kind = row.get("provenance_kind", "historical-landing")
    provenance_label = "Verified containment" if kind == "verified-containment" else "Landed"
    pr = landed.get("pr") if landed else None
    provenance = "**Integration:** pending\n" if kind == "pending-candidate" else (
        f'**{provenance_label}:** {landed["branch"]} {landed["commit"]} PR {pr if pr is not None else "unknown"}\n')
    sources = ", ".join(row["sources"])
    verification = ('Protected deployment content verified for this occurrence; see its appended verification receipt. '
                    if protected else 'Protected-deployment verification is pending; ')
    return (f'# Review {row["path"]}: {row["title"]} at {digest}\n\n'
            '**Topic:** Website pages\n**Priority:** P2\n'
            '**Priority reason:** Review this exact candidate before website acceptance.\n'
            '**Value:** V1\n**Value reason:** A content-bound decision prevents repeated review.\n'
            f'**Page:** {row["path"]}\n**Title:** {row["title"]}\n**Content hash:** {digest}\n'
            f'**Candidate:** {candidate}\n**Provenance kind:** {kind}\n'
            f'**Verification:** {"protected-capture" if protected else "built-candidate"}\n'
            f'**Sources:** {json.dumps(row["sources"], ensure_ascii=True)}\n'
            f'{provenance}'
            f'**Spec:** {row["spec"]}\n**Task:** {row["task"]}\n'
            f'**Recommendation:** {approval_recommendation(row["path"], row["title"], digest)}\n'
            f'**Owner record:** {APPROVALS}\n**Write after:** ## Approvals\n\n'
            f'Inspect this page at built candidate {candidate}. '
            f'{verification}This local card supplies no public review status. '
            f'Sources: {sources}.\n')


def _same_owners(parsed, row, digest, candidate):
    expected = parse_card('expected.md', _new_card(row, digest, candidate))
    if not isinstance(expected, Card):
        return False
    keys = ('Page', 'Title', 'Content hash', 'Spec', 'Task', 'Provenance kind',
            'Integration', 'Landed', 'Verified containment', 'Recommendation', 'Owner record', 'Write after')
    if any(parsed.fields.get(key) != expected.fields.get(key) for key in keys):
        return False
    if 'Sources' in parsed.fields:
        try:
            return json.loads(parsed.fields['Sources']) == row['sources']
        except ValueError:
            return False
    # Older committed cards used a prose source suffix and had no structured
    # header. Preserve their occurrence when only the template/proof changes.
    return parsed.context.endswith('Sources: ' + ', '.join(row['sources']) + '.')


def _verification_suffix(proof):
    return ('\n## Verification\n\n**State:** protected-capture\n'
            f'**Candidate:** {proof["candidate"]}\n**Deployment:** {proof["deployment"]}\n'
            f'**Capture SHA256:** {proof["capture_sha256"]}\n**Observed at:** {proof["observed_at"]}\n').encode()


def generate(root, listed, built, *, candidate, now=None, protection=None):
    """Commit one complete built snapshot; append supersession, never rewrite history.

    ``built`` maps every public built route to its served HTML. Injection is
    the deterministic build seam; production callers must supply one pinned
    candidate build, including its shared shell, rather than historical pages.
    """
    if not re.fullmatch(r"[0-9a-f]{40,64}", candidate):
        raise PageRefused("candidate must be an immutable commit")
    if protection is not None:
        from .protected_pages import verified_record
        protection = verified_record(protection, candidate, listed, built)
    rows = _metadata(listed, built)
    hashes = {path: content_hash(built[path]) for path in rows}
    root = Path(root).resolve()
    with repository_lock(root):
        if not _git(root, "symbolic-ref", "-q", "--short", "HEAD").strip():
            raise PageRefused("HEAD is detached; page cards commit on a branch")
        base = _git(root, "rev-parse", "HEAD").strip()
        previous_blob = committed_blob(root, INDEX, base)
        previous = json.loads(previous_blob) if previous_blob else {"pages": {}}
        writes, entries = {}, {}
        for path, row in rows.items():
            digest, old = hashes[path], previous.get("pages", {}).get(path)
            reuse = False
            if old and old["hash"] == digest:
                name = old["card"]
                existing = committed_blob(root, f"{CARDS}/{name}", base)
                parsed = parse_card(name, existing.decode()) if existing else None
                if not isinstance(parsed, Card) or parsed.stale is not None or parsed.fields.get("Page") != path or parsed.fields.get("Content hash") != digest:
                    raise PageRefused(f"{path}: index does not name its current committed card")
                # Reuse an unchanged content occurrence only while its owners,
                # sources and provenance still match. Keep that occurrence's
                # original candidate; the index binds the latest build pin.
                reuse = _same_owners(parsed, row, digest, candidate)
                if (reuse and protection is not None
                        and not (parsed.verification and parsed.verification.get('State') == 'protected-capture')):
                    writes[f'{CARDS}/{name}'] = existing + (b'' if existing.endswith(b'\n') else b'\n') + _verification_suffix(protection)
            if not reuse:
                slug = path.strip("/").replace("/", "-") or "home"
                stem = f"page-{slug}-{digest[7:19]}"
                name, suffix = stem + ".md", 1
                while f"{CARDS}/{name}" in writes or committed_blob(root, f"{CARDS}/{name}", base) is not None:
                    # Returning to an earlier hash must not erase its stale or
                    # answered history. A fresh occurrence gets a new filename.
                    suffix += 1
                    name = f"{stem}-{suffix}.md"
                new_card = _new_card(row, digest, candidate, protected=protection is not None)
                parsed = parse_card(name, new_card)
                required = {"Page": path, "Content hash": digest, "Candidate": candidate,
                            "Title": row["title"], "Spec": row["spec"], "Task": row["task"],
                            "Owner record": APPROVALS, "Write after": "## Approvals"}
                if not isinstance(parsed, Card) or any(parsed.fields.get(key) != value for key, value in required.items()):
                    raise PageRefused(f"{path}: generated card is not valid Board content")
                writes[f"{CARDS}/{name}"] = new_card.encode()
                if protection is not None:
                    writes[f"{CARDS}/{name}"] += _verification_suffix(protection)
                if old:
                    old_rel = f'{CARDS}/{old["card"]}'
                    old_blob = committed_blob(root, old_rel, base)
                    if old_blob is None:
                        raise PageRefused(f"{path}: previous card is missing")
                    writes[old_rel] = old_blob + (b"" if old_blob.endswith(b"\n") else b"\n") + (
                        f'\n## Stale\n\n**Superseded by:** {name}\n**Stale since:** {_stamp(now)}\n').encode()
            entries[path] = {"title": row["title"], "landed": row["landed"]["commit"] if row.get("landed") else None,
                             "provenance_kind": row.get("provenance_kind", "historical-landing"), "hash": digest, "card": name}
            if row.get("provenance_kind") == "pending-candidate":
                entries[path].update(candidate=candidate, integration="pending")
        for path in previous.get("pages", {}).keys() - rows.keys():
            old = previous["pages"][path]
            relative = f'{CARDS}/{old["card"]}'
            old_blob = committed_blob(root, relative, base)
            parsed = parse_card(old["card"], old_blob.decode()) if old_blob else None
            if not isinstance(parsed, Card) or parsed.stale is not None or parsed.fields.get("Page") != path or parsed.fields.get("Content hash") != old["hash"]:
                raise PageRefused(f"{path}: removed route does not name its current committed card")
            writes[relative] = old_blob + (b"" if old_blob.endswith(b"\n") else b"\n") + (
                f'\n## Stale\n\n**Removed in:** {candidate}\n**Stale since:** {_stamp(now)}\n').encode()
        writes[INDEX] = (json.dumps({"candidate": candidate, "pages": entries, "protection": protection}, indent=2, sort_keys=True) + "\n").encode()
        if committed_blob(root, APPROVALS, base) is None:
            writes[APPROVALS] = b"# Website page approvals\n\nOwner-facing content-bound decisions; no public-site status.\n\n## Approvals\n"
        transaction = []
        for relative, new in writes.items():
            path = _safe_file(root, relative)
            old = committed_blob(root, relative, base)
            if _git(root, "status", "--porcelain", "--", relative).strip() or (path.exists() and path.read_bytes() != old):
                raise PageRefused(f"{relative} has uncommitted changes")
            if old == new:
                continue
            mode = _git(root, "ls-tree", base, "--", relative).split(" ", 1)[0] if old is not None else "100644"
            transaction.append((relative, path, mode, old, new))
        if not transaction:
            return {"changed": False, "pages": len(rows), "commit": base, "candidate": candidate, "protected_verified": protection is not None}
        for _, path, *_ in transaction:
            path.parent.mkdir(parents=True, exist_ok=True)
        try:
            commit = _write_and_commit(root, base, transaction, f"Grill Board: page cards for {len(rows)} pages",
                                       f"Review cards bind the complete website build at {candidate}; historical answers remain unchanged.")
        except AnswerRefused as error:
            raise PageRefused(str(error)) from error
        return {"changed": True, "pages": len(rows), "commit": commit, "candidate": candidate, "protected_verified": protection is not None}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["generate", "status"])
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--built-html", type=Path,
                        help="JSON object mapping every public route to served HTML from the pinned candidate")
    parser.add_argument("--candidate")
    parser.add_argument("--source-repo", type=Path, help="trusted source checkout; defaults to --project")
    parser.add_argument("--ref", help="generate: fetched source ref (origin/dev); status: committed review ref (HEAD)")
    parser.add_argument("--image", help="approved local immutable Node Docker image sha256 identity")
    parser.add_argument("--public-config", type=Path, help="explicit public read-only site configuration JSON; no inherited values")
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument('--protected-artifact', type=Path, help='private capture emitted by a trusted authenticated outer observer')
    parser.add_argument('--protected-project')
    parser.add_argument('--protected-deployment')
    parser.add_argument('--protected-origin')
    parser.add_argument('--protected-capture-sha256', help='independent observer digest, not a self-declared trust flag')
    args = parser.parse_args(argv)
    if args.command == 'status':
        if any((args.candidate, args.inventory, args.built_html, args.source_repo, args.image,
                args.public_config, args.protected_artifact, args.protected_project,
                args.protected_deployment, args.protected_origin, args.protected_capture_sha256)):
            parser.error('status reads committed review records; build and capture options do not apply')
        try:
            print(json.dumps(page_status(args.project, args.ref or 'HEAD'), sort_keys=True))
        except (AnswerRefused, OSError) as error:
            parser.exit(1, f'ams-pages: {error}\n')
        return
    if not args.candidate:
        parser.error('generate requires --candidate')
    protected_pins = [args.protected_project, args.protected_deployment, args.protected_origin, args.protected_capture_sha256]
    if args.protected_artifact and (not all(protected_pins) or args.built_html):
        parser.error('protected capture requires automatic collection and every independent observer pin')
    if not args.protected_artifact and any(protected_pins):
        parser.error('protected observer pins require --protected-artifact')
    if args.built_html and (not args.inventory or args.image or args.source_repo or args.ref or args.public_config):
        parser.error("injected HTML requires --inventory and cannot be combined with automatic build options")
    if not args.built_html and (args.inventory or not args.image):
        parser.error("automatic collection reads the pinned inventory and requires --image")
    try:
        if args.built_html:
            result = generate(args.project, json.loads(args.inventory.read_text()), json.loads(args.built_html.read_text()), candidate=args.candidate)
            result["input_mode"] = "injected-artifact"
        else:
            from .page_build import DockerBuild, collect_current
            runtime = DockerBuild(args.image, timeout=args.timeout)
            config = json.loads(args.public_config.read_text()) if args.public_config else None
            collected = collect_current(args.source_repo or args.project, args.ref or "origin/dev", args.candidate,
                                        build_start=runtime, public_config=config)
            if not runtime.cleanup_verified:
                raise PageRefused("owned runtime cleanup is not verified; no Board write")
            if args.protected_artifact:
                from .protected_pages import collect_protected
                from .page_build import AMS_ORIGIN
                collected = collect_protected(args.protected_artifact, collected, expected_pins={
                    'repository': AMS_ORIGIN, 'project': args.protected_project,
                    'deployment': args.protected_deployment, 'candidate': args.candidate,
                    'origin': args.protected_origin, 'capture_sha256': args.protected_capture_sha256})
            result = generate(args.project, collected["inventory"], collected["html"], candidate=collected["candidate"],
                              protection=collected.get('verified_capture'))
            result.update(input_mode="protected-capture" if args.protected_artifact else "pinned-container-build", build_image=args.image,
                          route_kinds=collected["kinds"], excluded=collected["excluded"], cleanup_verified=True)
            if collected.get('protection'):
                result['protection'] = collected['protection']
    except (PageRefused, AnswerRefused, OSError, json.JSONDecodeError) as error:
        parser.exit(1, f"ams-pages: {error}\n")
    print(json.dumps(result, sort_keys=True))
