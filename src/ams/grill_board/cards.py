"""Card files: one Markdown file per question waiting on the owner.

Cards are read from the committed Git snapshot (HEAD), never the working
tree, so drafts and uncommitted edits stay off the board (DDR-000L).

A card is a title line, then `**Field:** value` header lines, then optional
context. Priority and Value each need a grade and a one-line reason
(DDR-000K). Unknown header fields are kept, so later fields extend the
format without breaking older cards. The board appends `## Answer`,
`## Rating` and `## Flag` sections at the end (see answers.py); they are the
committed records the RSI loop reads (DDR-000J).

A card flagged too taxing is held for rewrite. A card that asks a flagged
question again unchanged (same question line, ignoring case and spacing) is
refused, whether it is a new file, a copy, or the same card with its flag
undone: the flagged questions come from every card and every flag the
board ever committed in this branch's history.
"""

import functools

import hashlib
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

PRIORITIES = {"P1": "Interrupt", "P2": "Committed", "P3": "Secondary", "P4": "Backlog"}
VALUES = {"V1": "Quick Win", "V2": "Strategic Value", "V3": "Fill-In", "V4": "Defer / Eliminate"}
FIELD = re.compile(r"^\*\*([^*]+):\*\*[ \t]*(.*)$")
SECTIONS = ("## Answer", "## Rating", "## Flag")
RATINGS = ("1", "2", "3", "4", "5")
FLAG_LINE = "**Too taxing:** yes"


@dataclass
class Card:
    file: str
    question: str
    priority: str
    priority_reason: str
    value: str
    value_reason: str
    fields: dict = field(default_factory=dict)
    context: str = ""
    answer: dict | None = None
    ratings: list = field(default_factory=list)  # every `## Rating`, oldest first; the last one stands
    flag: dict | None = None  # the `## Flag` section, when the owner flagged it too taxing
    sha: str = ""  # SHA-256 of the exact committed bytes this Card was parsed from
    commit: str = ""  # the commit those bytes were read at

    @property
    def rating(self):
        return self.ratings[-1]["Rating"].split()[0] if self.ratings else ""

    @property
    def waiting(self):
        """Still waiting on the owner: neither answered nor held for rewrite."""
        return self.answer is None and self.flag is None

    @property
    def sort_key(self):
        # Priority leads, Value orders within it; the grades are never summed.
        return (self.priority, self.value, self.file)


@dataclass
class Refusal:
    file: str
    problems: list


def parse_card(name, text):
    """Return a Card, or a Refusal naming every problem found."""
    lines = text.splitlines()
    question = lines[0][2:].strip() if lines and lines[0].startswith("# ") else ""
    fields, index = {}, 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    while index < len(lines) and (match := FIELD.match(lines[index])):
        fields[match.group(1).strip()] = match.group(2).strip()
        index += 1
    problems = [] if question else ["first line must be '# <question>'"]
    for label, grades in (("Priority", PRIORITIES), ("Value", VALUES)):
        grade = fields.get(label, "")
        if not grade:
            problems.append(f"{label} grade is missing")
        elif grade not in grades:
            problems.append(f"{label} grade {grade!r} is not one of {', '.join(grades)}")
        if not fields.get(f"{label} reason"):
            problems.append(f"{label} reason is missing or blank")
    if problems:
        return Refusal(name, problems)
    rest = lines[index:]
    starts = [at for at, line in enumerate(rest) if line in SECTIONS]
    sections = [
        (rest[at], dict(m.groups() for line in rest[at + 1:end] if (m := FIELD.match(line))))
        for at, end in zip(starts, starts[1:] + [len(rest)])
    ]
    answers = [f for h, f in sections if h == "## Answer"]
    ratings = [f for h, f in sections if h == "## Rating" and f.get("Rating", "").split(" ")[0] in RATINGS]
    flags = [f for h, f in sections if h == "## Flag" and f.get("Too taxing") == "yes"]
    if starts:
        rest = rest[:starts[0]]
    return Card(
        file=name,
        question=question,
        priority=fields["Priority"],
        priority_reason=fields["Priority reason"],
        value=fields["Value"],
        value_reason=fields["Value reason"],
        fields=fields,
        context="\n".join(rest).strip(),
        answer=answers[0] if answers else None,
        ratings=ratings,
        flag=flags[0] if flags else None,
    )


def question_key(question):
    """The form of a question that a rewrite must change: case and spacing aside."""
    return " ".join(question.split()).casefold()


class CardSourceError(Exception):
    """The card directory cannot be read as committed records."""


def _git(cwd, *args, binary=False):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=not binary)
    if result.returncode != 0:
        error = result.stderr.decode("utf-8", "replace") if binary else result.stderr
        raise CardSourceError(error.strip() or f"git {args[0]} failed")
    return result.stdout


def committed_cards(cards_dir):
    """Return [(name, text)] for each `*.md` card committed at HEAD directly
    in cards_dir. Uncommitted edits and untracked or staged files are ignored."""
    _, cards = committed_snapshot(cards_dir)
    return [(name, data.decode("utf-8")) for name, data in cards]


def committed_snapshot(cards_dir):
    """Return (commit, [(name, bytes)]): HEAD resolved once, and each card's
    exact bytes at that commit, so a page and its hashes show one snapshot."""
    cards_dir = Path(cards_dir)
    if not cards_dir.is_dir():
        raise CardSourceError(f"card directory not found: {cards_dir}")
    try:
        root = Path(_git(cards_dir, "rev-parse", "--show-toplevel").strip())
    except CardSourceError:
        raise CardSourceError(f"{cards_dir} is not in a Git repository; the board reads committed cards only") from None
    try:
        commit = _git(root, "rev-parse", "--verify", "--quiet", "HEAD^{commit}").strip()
    except CardSourceError:
        return "", []
    prefix = cards_dir.resolve().relative_to(root.resolve()).as_posix()
    prefix = "" if prefix == "." else prefix + "/"
    listed = _git(root, "ls-tree", "--name-only", "-z", commit, "--", prefix or ".")
    cards = []
    for path in sorted(name for name in listed.split("\0") if name.endswith(".md")):
        if "/" in path[len(prefix):]:
            continue
        cards.append((path[len(prefix):], _git(root, "cat-file", "blob", f"{commit}:{path}", binary=True)))
    return commit, cards


@functools.lru_cache(maxsize=32)
def _flagged_in_history(root, commit, prefix):
    """((question key, card name), ...) for every card version that carried a
    flag line in a commit reachable from `commit`, directly under prefix.
    Commits never change, so the result is cached per commit."""
    if not commit:
        return ()
    pattern = "^" + re.escape(FLAG_LINE)
    listed = _git(Path(root), "log", "-z", "--no-renames", "--format=%x01%H", "--name-only",
                  "-G", pattern, commit, "--", prefix or ".")
    flagged = []
    for block in listed.split("\x01")[1:]:  # each block: SHA NUL, then NUL-ended paths
        sha, *paths = [part.lstrip("\n") for part in block.split("\0")]
        for path in filter(None, paths):
            name = path[len(prefix):]
            if not path.startswith(prefix) or "/" in name or not name.endswith(".md"):
                continue
            try:
                data = _git(Path(root), "cat-file", "blob", f"{sha}:{path}", binary=True)
            except CardSourceError:
                continue  # this commit removed the file; the commit that added the flag lists it too
            card = parse_card(name, data.decode("utf-8", "replace"))
            if isinstance(card, Card) and card.flag is not None:
                flagged.append((question_key(card.question), name))
    return tuple(flagged)


def load_cards(cards_dir):
    """Read every committed `*.md` card in cards_dir: sorted Cards and Refusals.
    A card that would ask a flagged question again is a Refusal: its question
    line is unchanged, or it is a card once flagged whose flag is gone."""
    cards, refusals = [], []
    commit, snapshot = committed_snapshot(cards_dir)
    for name, data in snapshot:
        result = parse_card(name, data.decode("utf-8"))
        if isinstance(result, Card):
            result.sha, result.commit = hashlib.sha256(data).hexdigest(), commit
        (cards if isinstance(result, Card) else refusals).append(result)
    flagged = []
    if commit:
        root = Path(_git(Path(cards_dir), "rev-parse", "--show-toplevel").strip()).resolve()
        prefix = Path(cards_dir).resolve().relative_to(root).as_posix()
        flagged = list(_flagged_in_history(str(root), commit, "" if prefix == "." else prefix + "/"))
    flagged += [(question_key(card.question), card.file) for card in cards if card.flag is not None]
    by_question, by_name = {}, set()
    for key, name in flagged:
        by_question.setdefault(key, name)
        by_name.add(name)
    held = []
    for card in cards:
        if not card.waiting:
            continue
        if question_key(card.question) in by_question:
            problem = (f"asks again the question flagged too taxing in {by_question[question_key(card.question)]} "
                       "without a rewrite; rewrite the question line before posting it again (DDR-000J)")
        elif card.file in by_name:
            problem = ("was flagged too taxing and its flag is gone; keep the flag on the card and "
                       "post the rewritten question as a new card (DDR-000J)")
        else:
            continue
        held.append(card)
        refusals.append(Refusal(card.file, [problem]))
    cards = [card for card in cards if not any(card is h for h in held)]
    return sorted(cards, key=lambda card: card.sort_key), sorted(refusals, key=lambda r: r.file)
