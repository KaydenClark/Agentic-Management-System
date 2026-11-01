"""S-004 TK-002: answering a card through the board's HTTP interface writes
the answer into the record the card names, records it on the card and
commits both; a changed target, an unsafe path or a cross-origin request
is refused with nothing written."""

import os
import re
import subprocess
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import pytest

from ams.grill_board.server import make_server

CARD = """# Fixture: should the board keep one card per file?

**Priority:** P1
**Priority reason:** Every later card follows this rule.
**Value:** V1
**Value reason:** One word answers it.
**Topic:** Card format
**Recommendation:** Keep one Markdown file per card.
**Owner record:** records/decision.md
**Write after:** ## Owner answer

Fixture context.
"""

RECORD = """# Fixture decision: one card per file

**Status:** awaiting the owner

## Owner answer

## History

- Drafted by a fixture.
"""


def git(repo, *args):
    return subprocess.run(
        ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", *args],
        cwd=repo, check=True, capture_output=True, text=True,
    ).stdout


def head(repo):
    return git(repo, "rev-parse", "HEAD").strip()


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "room"
    (root / "grill-board" / "cards").mkdir(parents=True)
    (root / "records").mkdir()
    (root / "grill-board" / "cards" / "one-card.md").write_text(CARD)
    (root / "records" / "decision.md").write_text(RECORD)
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.name", "fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "fixture")
    return root


@pytest.fixture
def board(repo):
    servers = []

    def start():
        server = make_server(repo / "grill-board" / "cards", port=0)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        servers.append(server)
        return server

    yield start
    for server in servers:
        server.shutdown()
        server.server_close()


def origin(server):
    host, port = server.server_address[:2]
    return f"http://{host}:{port}"


def read_form(server, card="one-card.md"):
    """GET the open card and return its answer form's hidden fields."""
    query = urllib.parse.urlencode({"topic": "Card format", "card": card})
    with urllib.request.urlopen(f"{origin(server)}/?{query}", timeout=5) as response:
        html = response.read().decode("utf-8")
    form = html.split('<form class="answer"', 1)[1].split("</form>", 1)[0]
    return dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', form)), html


def post(server, fields, headers=None):
    data = urllib.parse.urlencode(fields).encode()
    request = urllib.request.Request(f"{origin(server)}/answer", data=data, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    for key, value in ({"Origin": origin(server)} if headers is None else headers).items():
        request.add_header(key, value)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8")


def snapshot(repo):
    return {
        "card": (repo / "grill-board" / "cards" / "one-card.md").read_bytes(),
        "record": (repo / "records" / "decision.md").read_bytes(),
        "head": head(repo),
    }


def test_the_open_card_offers_working_verdicts_with_render_time_hashes(board, repo):
    fields, html = read_form(board())
    assert fields["card"] == "one-card.md"
    assert re.fullmatch(r"[0-9a-f]{64}", fields["card_sha"])
    assert re.fullmatch(r"[0-9a-f]{64}", fields["record_sha"])
    form = html.split('<form class="answer"', 1)[1].split("</form>", 1)[0]
    assert 'method="post" action="/answer"' in html
    for verdict in ("confirm", "rework-wording", "change-the-why", "change"):
        button = re.search(rf'<button type="submit" name="verdict" value="{verdict}"[^>]*>', form)
        assert button and "disabled" not in button.group(0), verdict
    assert 'name="note"' in form and "records/decision.md" in html


def test_confirm_writes_the_owning_record_and_the_card_in_one_commit(board, repo):
    server = board()
    before = head(repo)
    fields, _ = read_form(server)
    status, body = post(server, {**fields, "verdict": "confirm", "note": "Yes, and keep names short."})
    assert status == 200, body
    record = (repo / "records" / "decision.md").read_text()
    card = (repo / "grill-board" / "cards" / "one-card.md").read_text()
    # The answer lands in the owner, right after the named line; nothing is deleted.
    assert record.startswith(RECORD.split("## Owner answer")[0] + "## Owner answer\n\n**Owner answer")
    assert "Confirmed: Keep one Markdown file per card." in record
    assert "> Yes, and keep names short." in record
    assert record.endswith("## History\n\n- Drafted by a fixture.\n")
    for line in RECORD.splitlines():
        assert line in record.splitlines()
    # The card records the answer; its question and header are untouched.
    assert card.startswith(CARD)
    assert "## Answer" in card and "**Verdict:** Confirm" in card and "**Written to:** records/decision.md" in card
    # One commit, on the current branch, with exactly those two files.
    assert git(repo, "rev-parse", "HEAD~1").strip() == before
    assert git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip() == "main"
    changed = git(repo, "show", "--name-only", "--format=%s", "HEAD").split()
    assert sorted(changed[-2:]) == ["grill-board/cards/one-card.md", "records/decision.md"]
    assert "confirm" in git(repo, "log", "-1", "--format=%s").lower()
    assert git(repo, "status", "--porcelain") == ""
    assert "Written and committed" in body
    # An answered card leaves the queue; a second answer is refused.
    status, _ = post(server, {**fields, "verdict": "confirm"})
    assert status == 409 and head(repo) != before and len(git(repo, "log", "--format=%H").split()) == 2


def test_an_answer_that_only_changes_board_state_is_not_a_confirm(board, repo):
    """Must fail: a confirm that leaves the owning record unchanged."""
    server = board()
    fields, _ = read_form(server)
    post(server, {**fields, "verdict": "confirm"})
    assert (repo / "records" / "decision.md").read_bytes() != RECORD.encode()


def test_a_target_changed_since_the_card_was_read_is_refused_and_nothing_is_written(board, repo):
    server = board()
    fields, _ = read_form(server)
    record = repo / "records" / "decision.md"
    record.write_text(RECORD.replace("awaiting the owner", "edited by someone else"))
    git(repo, "commit", "-qam", "someone else edits the record")
    before = snapshot(repo)
    status, body = post(server, {**fields, "verdict": "confirm"})
    assert status == 409
    assert "Not written" in body and "changed since" in body
    assert snapshot(repo) == before


def test_uncommitted_edits_in_the_target_are_refused_and_kept(board, repo):
    server = board()
    fields, _ = read_form(server)
    record = repo / "records" / "decision.md"
    record.write_text(RECORD + "\nan uncommitted edit\n")
    before = snapshot(repo)
    status, body = post(server, {**fields, "verdict": "confirm"})
    assert status == 409 and "uncommitted" in body
    assert snapshot(repo) == before


def test_a_card_changed_since_it_was_read_is_refused(board, repo):
    server = board()
    fields, _ = read_form(server)
    card = repo / "grill-board" / "cards" / "one-card.md"
    card.write_text(CARD.replace("Keep one Markdown file per card.", "Keep two."))
    git(repo, "commit", "-qam", "card reworded")
    before = snapshot(repo)
    status, body = post(server, {**fields, "verdict": "confirm"})
    assert status == 409 and "changed since" in body
    assert snapshot(repo) == before


@pytest.mark.parametrize(
    "target",
    ["../outside.md", "/etc/hosts", ".git/config", "records/../../outside.md", "records/link.md", "linkdir/x.md"],
)
def test_owner_paths_that_escape_the_repository_are_refused(board, repo, target):
    outside = repo.parent / "outside.md"
    outside.write_text("outside\n")
    os.symlink(outside, repo / "records" / "link.md")
    os.symlink(repo.parent, repo / "linkdir")
    card = repo / "grill-board" / "cards" / "one-card.md"
    card.write_text(CARD.replace("records/decision.md", target))
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "card points elsewhere")
    server = board()
    fields, _ = read_form(server)
    before = snapshot(repo)
    status, body = post(server, {**fields, "verdict": "confirm"})
    assert status == 409 and "Not written" in body
    assert snapshot(repo) == before
    assert outside.read_text() == "outside\n"
    assert (repo / ".git" / "config").read_text().count("[core]") == 1


@pytest.mark.parametrize(
    "verdict, label", [("rework-wording", "Rework wording"), ("change-the-why", "Change the why"), ("change", "Change")]
)
def test_non_confirm_verdicts_are_recorded_on_the_card_as_returns_with_the_note(board, repo, verdict, label):
    server = board()
    fields, _ = read_form(server)
    status, body = post(server, {**fields, "verdict": verdict, "note": "Say who reads it.\nThen ask again."})
    assert status == 200, body
    card = (repo / "grill-board" / "cards" / "one-card.md").read_text()
    assert card.startswith(CARD)
    assert f"**Verdict:** {label}" in card and "**Returned:** yes" in card
    assert "> Say who reads it.\n> Then ask again." in card
    assert (repo / "records" / "decision.md").read_text() == RECORD, "a return never writes the owner"
    assert git(repo, "show", "--name-only", "--format=", "HEAD").split() == ["grill-board/cards/one-card.md"]


def test_a_return_needs_a_note(board, repo):
    server = board()
    fields, _ = read_form(server)
    before = snapshot(repo)
    status, body = post(server, {**fields, "verdict": "change", "note": "  "})
    assert status == 409 and "note" in body.lower()
    assert snapshot(repo) == before


@pytest.mark.parametrize(
    "headers",
    [{}, {"Origin": "http://evil.example"}, {"Origin": "null"}, {"Referer": "http://evil.example/"}],
)
def test_cross_origin_or_unmarked_posts_are_refused(board, repo, headers):
    server = board()
    fields, _ = read_form(server)
    before = snapshot(repo)
    status, _ = post(server, {**fields, "verdict": "confirm"}, headers=headers)
    assert status == 403
    assert snapshot(repo) == before


def test_a_foreign_host_header_is_refused(board, repo):
    server = board()
    fields, _ = read_form(server)
    before = snapshot(repo)
    status, _ = post(server, {**fields, "verdict": "confirm"}, headers={"Origin": origin(server), "Host": "evil.example"})
    assert status == 403
    assert snapshot(repo) == before


def test_other_dirty_files_are_left_alone_and_not_committed(board, repo):
    server = board()
    fields, _ = read_form(server)
    (repo / "unrelated.md").write_text("work in progress\n")
    git(repo, "add", "unrelated.md")
    status, _ = post(server, {**fields, "verdict": "confirm"})
    assert status == 200
    assert "unrelated.md" not in git(repo, "show", "--name-only", "--format=", "HEAD")
    assert git(repo, "status", "--porcelain").strip() == "A  unrelated.md"


@pytest.mark.parametrize(
    "target", ["../outside.md", "/etc/hosts", ".git/config", ".GIT/config", "records/./decision.md", "records/link.md", "linkdir/x.md", "records"],
)
def test_the_path_guard_alone_refuses_every_escape(repo, target):
    from ams.grill_board.answers import AnswerRefused, owned_path

    (repo.parent / "x.md").write_text("outside\n")
    os.symlink(repo / "records" / "decision.md", repo / "records" / "link.md")
    os.symlink(repo.parent, repo / "linkdir")
    with pytest.raises(AnswerRefused):
        owned_path(repo, target)
    assert owned_path(repo, "records/decision.md") == repo / "records" / "decision.md"


def test_a_planted_temporary_symlink_never_redirects_the_write(board, repo):
    """Codex P1 on PR #38: a symlink at a predictable temp name must not be followed."""
    outside = repo.parent / "victim.md"
    outside.write_text("victim\n")
    for folder, name in (("records", "decision.md"), ("grill-board/cards", "one-card.md")):
        os.symlink(outside, repo / folder / f".{name}.answer-tmp")
    server = board()
    fields, _ = read_form(server)
    status, body = post(server, {**fields, "verdict": "confirm"})
    assert status == 200, body
    assert outside.read_text() == "victim\n"
    record = repo / "records" / "decision.md"
    assert not record.is_symlink() and "Confirmed:" in record.read_text()
    tree = git(repo, "ls-tree", "HEAD", "records/decision.md", "grill-board/cards/one-card.md")
    assert [line.split()[0] for line in tree.splitlines()] == ["100644", "100644"]


def test_the_form_hash_is_bound_to_the_card_text_the_page_showed(board, repo, monkeypatch):
    """Codex P2 on PR #38: a card committed between reading and hashing is refused."""
    from ams.grill_board import server as board_server

    original, raced = board_server.load_cards, []

    def load_then_race(cards_dir):
        result = original(cards_dir)
        if not raced:
            raced.append(True)
            card = repo / "grill-board" / "cards" / "one-card.md"
            card.write_text(CARD.replace("Keep one Markdown file per card.", "Keep every card in one file."))
            git(repo, "commit", "-qam", "another agent rewrites the recommendation")
        return result

    monkeypatch.setattr(board_server, "load_cards", load_then_race)
    server = board()
    fields, html = read_form(server)
    assert "Keep one Markdown file per card." in html  # the page shows the old text
    monkeypatch.setattr(board_server, "load_cards", original)
    before = snapshot(repo)
    status, body = post(server, {**fields, "verdict": "confirm"})
    assert status == 409 and "changed since" in body
    assert snapshot(repo) == before
