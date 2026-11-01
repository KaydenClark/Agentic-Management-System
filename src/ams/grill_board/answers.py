"""Answering a card: the owner's verdict becomes committed records.

Confirm writes the card's Recommendation straight into the record the card
names (`Owner record`), just after the line it names (`Write after`), with
no second confirmation (ADR-000B). Every verdict is recorded on the card in
an appended `## Answer` section. The board then makes one Git commit of
exactly those files on the current branch, built on the commit it validated
against and moved onto the branch only if HEAD is still that commit.

A write refuses, writing nothing, when the card or its target changed since
the page showed it (their SHA-256 at render differs from HEAD now), when
either file has uncommitted changes, or when the target path leaves the
repository, crosses a symlink or names `.git` (ADR-002U). Nothing is deleted
or renumbered: answers are inserted, never replaced.
"""

import contextlib
import fcntl
import hashlib
import os
import stat
import subprocess
import tempfile
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


class AnswerWrittenIndexStale(Exception):
    """The answer is committed, but the index still shows the old bytes."""


def _git(root, *args, binary=False, data=None, env=None):
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=not binary and data is None,
        input=data, env={**os.environ, **env} if env else None,
    )
    if data is not None and result.returncode == 0:
        return result.stdout.decode("utf-8")
    if result.returncode != 0:
        error = result.stderr if isinstance(result.stderr, str) else result.stderr.decode("utf-8", "replace")
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


def committed_entry(root, relative, rev="HEAD"):
    """(mode, bytes) of a regular file committed at rev, or None."""
    listed = _git(root, "ls-tree", "-z", rev, "--", relative)
    entry = listed.split("\0", 1)[0]
    if not entry or "\t" not in entry:
        return None
    mode, kind, _ = entry.split("\t", 1)[0].split(" ")
    if kind != "blob" or mode not in REGULAR_MODES:
        return None
    return mode, _git(root, "cat-file", "blob", f"{rev}:{relative}", binary=True)


def committed_blob(root, relative, rev="HEAD"):
    """Bytes of a regular file committed at rev, or None if it is not one."""
    entry = committed_entry(root, relative, rev)
    return entry and entry[1]


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
    """SHA-256 of the card the page shows and of its owning record at the
    same commit; a later write is checked against them."""
    root = repo_root(cards_dir)
    target = card.fields.get("Owner record", "")
    record_blob = None
    if target:
        try:
            owned_path(root, target)
            record_blob = committed_blob(root, target, card.commit or "HEAD")
        except AnswerRefused:
            record_blob = None
    return card.sha, sha256(record_blob) if record_blob is not None else ""


def _unchanged(root, base, relative, path, expected_sha, what):
    """Return (mode, committed bytes at base) after checking nothing moved."""
    entry = committed_entry(root, relative, base)
    if entry is None:
        raise AnswerRefused(f"the {what} {relative} is not a committed regular file")
    mode, blob = entry
    if sha256(blob) != expected_sha:
        raise AnswerRefused(f"the {what} {relative} changed since the page showed it; reload and read it again")
    if _git(root, "status", "--porcelain", "--", relative).strip() or path.read_bytes() != blob:
        raise AnswerRefused(f"the {what} {relative} has uncommitted changes; commit or set them aside first")
    return mode, blob


def _text(blob, relative):
    try:
        return blob.decode("utf-8")
    except UnicodeDecodeError:
        raise AnswerRefused(f"{relative} is not UTF-8 text") from None


def _commit_on(root, base, writes, subject, body):
    """Build a commit of `writes` on top of base in a throwaway index and move
    the branch to it only if HEAD is still base (compare-and-swap)."""
    handle, index = tempfile.mkstemp(prefix="ams-answer-index-")
    os.close(handle)
    try:
        env = {"GIT_INDEX_FILE": index}
        _git(root, "read-tree", base, env=env)
        for relative, _, mode, _, new in writes:
            blob = _git(root, "hash-object", "-w", "--stdin", data=new).strip()
            _git(root, "update-index", "--cacheinfo", f"{mode},{blob},{relative}", env=env)
        tree = _git(root, "write-tree", env=env).strip()
    finally:
        os.unlink(index)
    commit = _git(root, "commit-tree", tree, "-p", base, "-m", subject, "-m", body).strip()
    try:
        _git(root, "update-ref", "-m", f"commit: {subject}", "HEAD", commit, base)
    except AnswerRefused:
        raise AnswerRefused("HEAD moved while the answer was being written; reload and answer again") from None
    return commit


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


def _replace(path, data):
    """Write data to a fresh, exclusively created temporary file beside path
    (never following a planted name), keep path's mode, then swap it in."""
    mode = stat.S_IMODE(path.stat().st_mode)
    handle, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".answer-tmp")
    try:
        with os.fdopen(handle, "wb") as out:
            out.write(data)
        os.chmod(tmp, mode)
        os.replace(tmp, path)
        if not stat.S_ISREG(os.lstat(path).st_mode):
            raise AnswerRefused(f"{path.name} is not a regular file after the write")
    except BaseException:
        if os.path.lexists(tmp):
            os.unlink(tmp)
        raise


@contextlib.contextmanager
def repository_lock(root):
    """One writer per checkout, across every board instance: an exclusive
    flock on a file in this worktree's Git directory."""
    git_dir = Path(_git(root, "rev-parse", "--absolute-git-dir").strip())
    with open(git_dir / "ams-grill-board.lock", "a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def answer(cards_dir, card, verdict, note, card_sha, record_sha, now=None):
    """Record the owner's verdict on `card` and commit it; return the commit
    SHA. Raises AnswerRefused, with every file left as it was, otherwise.
    Validation through commit runs under the repository lock."""
    with repository_lock(repo_root(cards_dir)):
        return _answer(cards_dir, card, verdict, note, card_sha, record_sha, now)


def _answer(cards_dir, card, verdict, note, card_sha, record_sha, now):
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
    base = _git(root, "rev-parse", "--verify", "HEAD^{commit}").strip()
    card_rel = card_path(root, cards_dir, card.file)
    card_file = Path(cards_dir) / card.file
    if card_file.is_symlink():
        raise AnswerRefused(f"the card {card_rel} is a symlink")
    card_mode, card_blob = _unchanged(root, base, card_rel, card_file, card_sha, "card")
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
        if record_file.resolve() == card_file.resolve():
            raise AnswerRefused("this card names itself as its owning record; an answer must land in another record")
        record_mode, record_blob = _unchanged(root, base, target, record_file, record_sha, "owning record")
        block = f"**Owner answer ({when[:10]}, Grill Board card `{card.file}`):** Confirmed: {recommendation}\n"
        if note:
            block += "\n" + _quote(note)
        written = _insert_after(_text(record_blob, target), anchor, block)
        writes.append((target, record_file, record_mode, record_blob, written.encode("utf-8")))
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
    card_text = _text(card_blob, card_rel)
    card_text += ("" if card_text.endswith("\n") else "\n") + "\n" + section
    writes.append((card_rel, card_file, card_mode, card_blob, card_text.encode("utf-8")))
    if len({path.resolve() for _, path, *_ in writes}) != len(writes):
        raise AnswerRefused("two writes would land in one file, so neither is written")
    try:
        for _, path, _, _, new in writes:
            _replace(path, new)
        commit = _commit_on(root, base, writes, subject, body)
    except (AnswerRefused, OSError) as error:
        for _, path, _, old, _ in writes:  # put back exactly the committed bytes this call replaced
            _replace(path, old)
        raise AnswerRefused(f"nothing was kept: {error}") from None
    # The branch now holds the answer; stage the same bytes so the tree reads clean.
    try:
        _git(root, "update-index", "--", *[relative for relative, *_ in writes])
    except AnswerRefused as error:
        raise AnswerWrittenIndexStale(f"committed {commit[:7]}, but refreshing the index failed ({error}); run git status") from None
    return commit
