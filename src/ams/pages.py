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

INDEX = "grill-board/pages/index.json"
APPROVALS = "grill-board/page-approvals.md"
CARDS = "grill-board/cards"
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
            if not isinstance(row.get(key), str) or not row[key].strip() or "\n" in row[key] or "\r" in row[key]:
                raise PageRefused(f"{path}: invalid {key}")
        landed = row.get("landed", {})
        if not re.fullmatch(r"[0-9a-f]{40,64}", landed.get("commit", "")):
            raise PageRefused(f"{path}: no immutable landed commit")
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


def _new_card(row, digest, candidate):
    landed = row["landed"]
    return (f'# Review {row["path"]}: {row["title"]} at {digest}\n\n'
            '**Topic:** Website pages\n**Priority:** P2\n'
            '**Priority reason:** Review this exact candidate before website acceptance.\n'
            '**Value:** V1\n**Value reason:** A content-bound decision prevents repeated review.\n'
            f'**Page:** {row["path"]}\n**Title:** {row["title"]}\n**Content hash:** {digest}\n'
            f'**Candidate:** {candidate}\n**Landed:** {landed.get("branch", "dev")} {landed["commit"]} PR {landed.get("pr", "unknown")}\n'
            f'**Spec:** {row["spec"]}\n**Task:** {row["task"]}\n'
            f'**Recommendation:** Approve page {row["path"]} ({row["title"]}) at content hash {digest}.\n'
            f'**Owner record:** {APPROVALS}\n**Write after:** ## Approvals\n\n'
            f'Inspect this path on the protected dev candidate {candidate}. '
            'This local card supplies no public review status.\n')


def generate(root, listed, built, *, candidate, now=None):
    """Commit one complete built snapshot; append supersession, never rewrite history.

    ``built`` maps every public built route to its served HTML. Injection is
    the deterministic build seam; production callers must supply one pinned
    candidate build, including its shared shell, rather than historical pages.
    """
    if not re.fullmatch(r"[0-9a-f]{40,64}", candidate):
        raise PageRefused("candidate must be an immutable commit")
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
            if old and old["hash"] == digest:
                name = old["card"]
                existing = committed_blob(root, f"{CARDS}/{name}", base)
                parsed = parse_card(name, existing.decode()) if existing else None
                if not isinstance(parsed, Card) or parsed.stale or parsed.fields.get("Page") != path or parsed.fields.get("Content hash") != digest:
                    raise PageRefused(f"{path}: index does not name its current committed card")
            else:
                slug = path.strip("/").replace("/", "-") or "home"
                stem = f"page-{slug}-{digest[7:19]}"
                name, suffix = stem + ".md", 1
                while f"{CARDS}/{name}" in writes or committed_blob(root, f"{CARDS}/{name}", base) is not None:
                    # Returning to an earlier hash must not erase its stale or
                    # answered history. A fresh occurrence gets a new filename.
                    suffix += 1
                    name = f"{stem}-{suffix}.md"
                writes[f"{CARDS}/{name}"] = _new_card(row, digest, candidate).encode()
                if old:
                    old_rel = f'{CARDS}/{old["card"]}'
                    old_blob = committed_blob(root, old_rel, base)
                    if old_blob is None:
                        raise PageRefused(f"{path}: previous card is missing")
                    writes[old_rel] = old_blob + (b"" if old_blob.endswith(b"\n") else b"\n") + (
                        f'\n## Stale\n\n**Superseded by:** {name}\n**Stale since:** {_stamp(now)}\n').encode()
            entries[path] = {"title": row["title"], "landed": row["landed"]["commit"], "hash": digest, "card": name}
        writes[INDEX] = (json.dumps({"candidate": candidate, "pages": entries}, indent=2, sort_keys=True) + "\n").encode()
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
            return {"changed": False, "pages": len(rows), "commit": base, "candidate": candidate}
        for _, path, *_ in transaction:
            path.parent.mkdir(parents=True, exist_ok=True)
        try:
            commit = _write_and_commit(root, base, transaction, f"Grill Board: page cards for {len(rows)} pages",
                                       f"Review cards bind the complete website build at {candidate}; historical answers remain unchanged.")
        except AnswerRefused as error:
            raise PageRefused(str(error)) from error
        return {"changed": True, "pages": len(rows), "commit": commit, "candidate": candidate}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["generate"])
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--built-html", type=Path, required=True,
                        help="JSON object mapping every public route to served HTML from the pinned candidate")
    parser.add_argument("--candidate", required=True)
    args = parser.parse_args(argv)
    try:
        result = generate(args.project, json.loads(args.inventory.read_text()), json.loads(args.built_html.read_text()), candidate=args.candidate)
    except (PageRefused, AnswerRefused, OSError, json.JSONDecodeError) as error:
        parser.exit(1, f"ams-pages: {error}\n")
    print(json.dumps(result, sort_keys=True))
