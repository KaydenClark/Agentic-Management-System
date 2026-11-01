"""Card files: one Markdown file per question waiting on the owner.

Cards are read from the committed Git snapshot (HEAD), never the working
tree, so drafts and uncommitted edits stay off the board (DDR-000L).

A card is a title line, then `**Field:** value` header lines, then optional
context. Priority and Value each need a grade and a one-line reason
(DDR-000K). Unknown header fields are kept, so later fields (rating, flag,
color) extend the format without breaking older cards.
"""

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

PRIORITIES = {"P1": "Interrupt", "P2": "Committed", "P3": "Secondary", "P4": "Backlog"}
VALUES = {"V1": "Quick Win", "V2": "Strategic Value", "V3": "Fill-In", "V4": "Defer / Eliminate"}
FIELD = re.compile(r"^\*\*([^*]+):\*\*[ \t]*(.*)$")


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
    return Card(
        file=name,
        question=question,
        priority=fields["Priority"],
        priority_reason=fields["Priority reason"],
        value=fields["Value"],
        value_reason=fields["Value reason"],
        fields=fields,
        context="\n".join(lines[index:]).strip(),
    )


class CardSourceError(Exception):
    """The card directory cannot be read as committed records."""


def _git(cwd, *args):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise CardSourceError(result.stderr.strip() or f"git {args[0]} failed")
    return result.stdout


def committed_cards(cards_dir):
    """Return [(name, text)] for each `*.md` card committed at HEAD directly
    in cards_dir. Uncommitted edits and untracked or staged files are ignored."""
    cards_dir = Path(cards_dir)
    if not cards_dir.is_dir():
        raise CardSourceError(f"card directory not found: {cards_dir}")
    try:
        root = Path(_git(cards_dir, "rev-parse", "--show-toplevel").strip())
    except CardSourceError:
        raise CardSourceError(f"{cards_dir} is not in a Git repository; the board reads committed cards only") from None
    try:
        _git(root, "rev-parse", "--verify", "--quiet", "HEAD^{commit}")
    except CardSourceError:
        return []
    prefix = cards_dir.resolve().relative_to(root.resolve()).as_posix()
    prefix = "" if prefix == "." else prefix + "/"
    listed = _git(root, "ls-tree", "--name-only", "-z", "HEAD", "--", prefix or ".")
    cards = []
    for path in sorted(name for name in listed.split("\0") if name.endswith(".md")):
        if "/" in path[len(prefix):]:
            continue
        cards.append((path[len(prefix):], _git(root, "show", f"HEAD:{path}")))
    return cards


def load_cards(cards_dir):
    """Read every committed `*.md` card in cards_dir: sorted Cards and Refusals."""
    cards, refusals = [], []
    for name, text in committed_cards(cards_dir):
        result = parse_card(name, text)
        (cards if isinstance(result, Card) else refusals).append(result)
    return sorted(cards, key=lambda card: card.sort_key), refusals
