"""Answering a card: the owner's verdict becomes committed records.

Confirm writes the card's Recommendation straight into the record the card
names (`Owner record`), just after the line it names (`Write after`), with
no second confirmation (ADR-000B). Every verdict is recorded on the card in
an appended `## Answer` section. The board then makes one Git commit of
exactly those files on the current branch.

A write refuses, writing nothing, when the card or its target changed since
the page showed it (their SHA-256 at render differs from HEAD now), when
either file has uncommitted changes, or when the target path leaves the
repository, crosses a symlink or names `.git` (ADR-002U). Nothing is deleted
or renumbered: answers are inserted, never replaced.
"""

import hashlib
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

VERDICTS = {
    "confirm": "Confirm",
    "rework-wording": "Rework wording",
    "change-the-why": "Change the why",
    "change": "Change",
}
REGULAR_MODES = {"100644", "100755"}


class AnswerRefused(Exception):
    """The answer was not written; the message says why."""


def _git(root, *args, binary=False):
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=not binary)
    if result.returncode != 0:
        error = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise AnswerRefused(error.strip() or f"git {args[0]} failed")
    return result.stdout


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def repo_root(cards_dir):
    return Path(_git(Path(cards_dir), "rev-parse", "--show-toplevel").strip())


def card_path(root, cards_dir, name):
    """The card's repository-relative POSIX path."""
    prefix = Path(cards_dir).resolve().relative_to(root.resolve()).as_posix()
    return name if prefix == "." else f"{prefix}/{name}"


def committed_blob(root, relative):
    """Bytes of a regular file committed at HEAD, or None if it is not one."""
    listed = _git(root, "ls-tree", "-z", "HEAD", "--", relative)
    entry = listed.split("\0", 1)[0]
    if not entry or "\t" not in entry:
        return None
    mode, kind, _ = entry.split("\t", 1)[0].split(" ")
    if kind != "blob" or mode not in REGULAR_MODES:
        return None
    return _git(root, "cat-file", "blob", f"HEAD:{relative}", binary=True)


def owned_path(root, relative):
    """Resolve a card's `Owner record` inside the repository, or refuse."""
    if not relative or "\\" in relative or "\0" in relative:
        raise AnswerRefused(f"the owning record path {relative!r} is not a plain repository path")
    parts = relative.split("/")
    if relative.startswith("/") or any(part in ("", ".", "..") for part in parts):
        raise AnswerRefused(f"the owning record {relative!r} escapes the repository")
    if any(part.lower() == ".git" for part in parts):
        raise AnswerRefused(f"the owning record {relative!r} is inside .git")
    path = root
    for part in PurePosixPath(relative).parts:
        path = path / part
        if path.is_symlink():
            raise AnswerRefused(f"the owning record {relative!r} goes through a symlink")
    if not path.resolve().is_relative_to(root.resolve()):
        raise AnswerRefused(f"the owning record {relative!r} escapes the repository")
    if not path.is_file():
        raise AnswerRefused(f"the owning record {relative!r} is not a file in the repository")
    return path


def render_hashes(cards_dir, card):
    """SHA-256 of the committed card and owning record, captured when the
    page shows the card; a later write is checked against them."""
    root = repo_root(cards_dir)
    card_blob = committed_blob(root, card_path(root, cards_dir, card.file)) or b""
    target = card.fields.get("Owner record", "")
    record_blob = None
    if target:
        try:
            owned_path(root, target)
            record_blob = committed_blob(root, target)
        except AnswerRefused:
            record_blob = None
    return sha256(card_blob), sha256(record_blob) if record_blob is not None else ""


def _unchanged(root, relative, path, expected_sha, what):
    """Return the committed bytes after checking nothing moved under them."""
    blob = committed_blob(root, relative)
    if blob is None:
        raise AnswerRefused(f"the {what} {relative} is not a committed regular file")
    if sha256(blob) != expected_sha:
        raise AnswerRefused(f"the {what} {relative} changed since the page showed it; reload and read it again")
    if _git(root, "status", "--porcelain", "--", relative).strip() or path.read_bytes() != blob:
        raise AnswerRefused(f"the {what} {relative} has uncommitted changes; commit or set them aside first")
    return blob


def _quote(note):
    return "".join(f"> {line}".rstrip() + "\n" for line in note.splitlines())


def _insert_after(text, anchor, block):
    lines = text.splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == anchor]
    if len(hits) != 1:
        found = "is not in" if not hits else "appears more than once in"
        raise AnswerRefused(f"the line {anchor!r} {found} the owning record")
    at = hits[0] + 1
    if not lines[hits[0]].endswith("\n"):
        lines[hits[0]] += "\n"
    rest = lines[at:]
    tail = "" if rest and not rest[0].strip() else "\n" if rest else ""
    return "".join(lines[:at]) + "\n" + block + tail + "".join(rest)


def answer(cards_dir, card, verdict, note, card_sha, record_sha, now=None):
    """Record the owner's verdict on `card` and commit it; return the commit
    SHA. Raises AnswerRefused, with every file left as it was, otherwise."""
    if verdict not in VERDICTS:
        raise AnswerRefused(f"unknown verdict {verdict!r}")
    label, note = VERDICTS[verdict], (note or "").strip()
    if card.answer is not None:
        raise AnswerRefused(f"{card.file} is already answered")
    if verdict != "confirm" and not note:
        raise AnswerRefused("a return needs a note saying what should change")
    root = repo_root(cards_dir)
    if not _git(root, "symbolic-ref", "-q", "--short", "HEAD").strip():
        raise AnswerRefused("HEAD is detached; answers commit on a branch")
    card_rel = card_path(root, cards_dir, card.file)
    card_file = Path(cards_dir) / card.file
    if card_file.is_symlink():
        raise AnswerRefused(f"the card {card_rel} is a symlink")
    card_blob = _unchanged(root, card_rel, card_file, card_sha, "card")
    when = (now or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
    writes = []
    if verdict == "confirm":
        target, anchor = card.fields.get("Owner record", ""), card.fields.get("Write after", "")
        recommendation = card.fields.get("Recommendation", "")
        if not target or not anchor:
            raise AnswerRefused("this card names no owning record and place (Owner record, Write after)")
        if not recommendation:
            raise AnswerRefused("this card has no Recommendation to confirm")
        record_file = owned_path(root, target)
        record_blob = _unchanged(root, target, record_file, record_sha, "owning record")
        block = f"**Owner answer ({when[:10]}, Grill Board card `{card.file}`):** Confirmed: {recommendation}\n"
        if note:
            block += "\n" + _quote(note)
        written = _insert_after(record_blob.decode("utf-8"), anchor, block)
        writes.append((target, record_file, record_blob, written.encode("utf-8")))
        recorded = f"**Written to:** {target}, after `{anchor}`\n"
        subject = f"Grill Board: confirm {card.file} into {target}"
        body = "The owner confirmed this card; its answer is written into the owning record and recorded on the card (ADR-000B)."
    else:
        recorded = "**Returned:** yes\n"
        subject = f"Grill Board: return {card.file} ({label})"
        body = "The owner returned this card with a note; an agent reworks it and posts it again before it is re-asked."
    section = f"## Answer\n\n**Verdict:** {label}\n**Answered:** {when}\n{recorded}"
    if note:
        section += "\n" + _quote(note)
    card_text = card_blob.decode("utf-8")
    card_text += ("" if card_text.endswith("\n") else "\n") + "\n" + section
    writes.append((card_rel, card_file, card_blob, card_text.encode("utf-8")))
    try:
        for _, path, _, new in writes:
            tmp = path.with_name(f".{path.name}.answer-tmp")
            tmp.write_bytes(new)
            os.replace(tmp, path)
        _git(root, "commit", "-q", "--only", "-m", subject, "-m", body, "--", *[rel for rel, *_ in writes])
    except (AnswerRefused, OSError) as error:
        for _, path, old, _ in writes:  # put back exactly the committed bytes this call replaced
            path.write_bytes(old)
        raise AnswerRefused(f"the commit failed, so nothing was kept: {error}") from None
    return _git(root, "rev-parse", "HEAD").strip()
