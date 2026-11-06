"""Content-bound page review behavior through disposable Git records."""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from ams import pages
from ams.grill_board.answers import AnswerRefused, answer, render_hashes
from ams.grill_board.cards import load_cards


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def room(tmp_path):
    root = tmp_path / "room"
    (root / "grill-board/cards").mkdir(parents=True)
    git(root, "init", "-q", "-b", "feature")
    git(root, "config", "user.name", "fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    (root / "README.md").write_text("Synthetic fixture.\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture")
    return root


def inventory(root, paths=("/", "/skills/grilling")):
    commit = git(root, "rev-parse", "HEAD")
    return {"pages": [{"path": path, "title": "Synthetic " + path, "spec": "S-008" if path.startswith("/skills") else "S-003", "task": "TK-001", "landed": {"branch": "dev", "commit": commit, "pr": 1}, "sources": ["site/app/page.tsx"]} for path in paths]}


def html(text="Hello", footer="abc"):
    return f'<main id="main"><h1>{text}</h1><p data-review-exclude>live 99</p></main><footer>{footer}</footer>'


def test_generate_commits_one_current_card_per_route_and_is_idempotent(room):
    listed = inventory(room)
    built = {p["path"]: html(p["title"]) for p in listed["pages"]}
    before = git(room, "rev-list", "--count", "HEAD")
    result = pages.generate(room, listed, built, candidate=git(room, "rev-parse", "HEAD"))
    assert result["changed"] and result["pages"] == 2
    assert int(git(room, "rev-list", "--count", "HEAD")) == int(before) + 1
    cards, refused = load_cards(room / "grill-board/cards")
    assert not refused and len(cards) == 2
    assert {c.fields["Page"] for c in cards} == {"/", "/skills/grilling"}
    assert all(c.fields["Content hash"] == pages.content_hash(built[c.fields["Page"]]) for c in cards)
    assert not git(room, "status", "--porcelain")
    first = git(room, "rev-parse", "HEAD")
    again = pages.generate(room, listed, built, candidate=result["candidate"])
    assert not again["changed"] and git(room, "rev-parse", "HEAD") == first


def test_changed_content_appends_stale_without_rewriting_answered_history(room):
    listed = inventory(room, ("/",))
    candidate = git(room, "rev-parse", "HEAD")
    pages.generate(room, listed, {"/": html()}, candidate=candidate)
    card = load_cards(room / "grill-board/cards")[0][0]
    card_sha, owner_sha = render_hashes(room / "grill-board/cards", card)
    answer(room / "grill-board/cards", card, "confirm", "", card_sha, owner_sha)
    old_file = room / "grill-board/cards" / card.file
    answered = old_file.read_bytes()
    unchanged = git(room, "rev-parse", "HEAD")
    assert not pages.generate(room, listed, {"/": html(footer="new sha")}, candidate=candidate)["changed"]
    assert git(room, "rev-parse", "HEAD") == unchanged
    pages.generate(room, listed, {"/": html("Correction")}, candidate=candidate)
    assert old_file.read_bytes().startswith(answered)
    assert b"## Stale" in old_file.read_bytes()[len(answered):]
    cards, refused = load_cards(room / "grill-board/cards")
    assert not refused and sum(c.waiting for c in cards) == 1
    stale = next(c for c in cards if c.file == card.file)
    assert stale.stale and not stale.waiting
    sha, owner = render_hashes(room / "grill-board/cards", stale)
    before = git(room, "rev-parse", "HEAD")
    with pytest.raises(AnswerRefused, match="stale"):
        answer(room / "grill-board/cards", stale, "change", "synthetic correction", sha, owner)
    assert git(room, "rev-parse", "HEAD") == before


def test_missing_built_route_or_dirty_owned_file_refuses_without_partial_write(room):
    listed = inventory(room, ("/",))
    before = git(room, "rev-parse", "HEAD")
    with pytest.raises(pages.PageRefused, match="/skills/new"):
        pages.generate(room, listed, {"/": html(), "/skills/new": html()}, candidate=before)
    assert git(room, "rev-parse", "HEAD") == before
    assert list((room / "grill-board/cards").glob("*.md")) == []
    pages.generate(room, listed, {"/": html()}, candidate=before)
    path = room / "grill-board/pages/index.json"
    path.write_text(path.read_text() + " ")
    dirty = path.read_bytes()
    with pytest.raises(pages.PageRefused, match="uncommitted"):
        pages.generate(room, listed, {"/": html("Changed")}, candidate=before)
    assert path.read_bytes() == dirty
    assert len(list((room / "grill-board/cards").glob("*.md"))) == 1


def test_hash_matches_existing_site_contract_vectors():
    vectors = json.loads((Path(__file__).parent / "fixtures/grill_board/pages/vectors.json").read_text())
    for vector in vectors["vectors"]:
        assert pages.canonical_content(vector["html"]) == vector["canonical"]
        assert pages.content_hash(vector["html"]) == vector["hash"]
    with pytest.raises(pages.PageRefused, match="main"):
        pages.content_hash("<p>No main</p>")
