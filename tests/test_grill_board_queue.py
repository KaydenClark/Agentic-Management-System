"""The owner's queue is a live projection of explicit requests in records."""

import json
import subprocess
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import pytest

from ams.grill_board.cards import load_cards
from ams.grill_board.server import make_server


RECORD = "workbench/specs/S-001-example/SPEC.md"
REQUEST = {
    "schema": "grill-board/request@1",
    "key": "event-location",
    "question": "Should we hold the event in the library?",
    "recommendation": "Hold the event in the library, within the existing budget.",
    "priority": "P2",
    "priority_reason": "The venue must be settled before invitations go out.",
    "value": "V1",
    "value_reason": "The available venue meets the event requirements at low cost.",
    "topic": "The event",
    "context": "The library has confirmed availability and accessibility.",
}


def git(root, *args):
    return subprocess.check_output(
        ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", *args],
        cwd=root, text=True, stderr=subprocess.PIPE,
    ).strip()


def commit(root):
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture")


def source(request=REQUEST, status="active", blockers="none"):
    return (
        "# S-001 - The event\n\n**Spec ID:** S-001\n"
        f"**Status:** {status}\n**Blockers:** {blockers}\n\n"
        "## Owner requests\n\n```grill-board\n"
        + json.dumps(request, indent=2) + "\n```\n"
    )


@pytest.fixture
def board(tmp_path):
    git(tmp_path, "init", "-q", "-b", "feature/queue")
    git(tmp_path, "config", "user.name", "fixture")
    git(tmp_path, "config", "user.email", "fixture@example.invalid")
    cards = tmp_path / "grill-board/cards"
    cards.mkdir(parents=True)
    (cards / ".gitkeep").touch()
    record = tmp_path / RECORD
    record.parent.mkdir(parents=True)
    record.write_text(source())
    (tmp_path / "workbench/manifest.json").write_text(json.dumps({
        "lanes": {"specs": "workbench/specs"},
        "collections": {"landmarks": "workbench/landmarks"},
    }))
    commit(tmp_path)
    server = make_server(cards, port=0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield tmp_path, cards, record, server
    server.shutdown()
    server.server_close()


def get(server, path="/"):
    url = f"http://127.0.0.1:{server.server_address[1]}{path}"
    with urllib.request.urlopen(url, timeout=10) as response:
        return response.read().decode()


def post(board, card, verdict="confirm", note="", **overrides):
    from ams.grill_board.answers import render_hashes
    _, cards_dir, _, server = board
    card_sha, record_sha = render_hashes(cards_dir, card)
    data = {"card": card.file, "verdict": verdict, "note": note,
            "card_sha": card_sha, "record_sha": record_sha, **overrides}
    url = f"http://127.0.0.1:{server.server_address[1]}"
    request = urllib.request.Request(url + "/answer", urllib.parse.urlencode(data).encode(),
                                     headers={"Origin": url})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode()


def test_pending_request_renders_without_preparing_a_card(board):
    root, cards, _, server = board
    before = git(root, "rev-parse", "HEAD")
    page = get(server)
    assert REQUEST["question"] in page
    assert REQUEST["recommendation"] in page
    assert RECORD in page
    assert "Nothing here needs you" not in page
    assert not list(cards.glob("*.md"))
    assert git(root, "rev-parse", "HEAD") == before
    assert git(root, "status", "--porcelain") == ""


def test_changed_and_resolved_requests_update_on_the_next_read(board):
    root, cards, record, server = board
    original, _ = load_cards(cards)
    changed = {**REQUEST, "question": "Should we hold the event in the community hall?"}
    record.write_text(source(changed))
    commit(root)
    assert changed["question"] in get(server)
    current, _ = load_cards(cards)
    assert len(current) == 1
    assert current[0].fields["Request key"] == original[0].fields["Request key"]
    assert current[0].file != original[0].file
    record.write_text(source(changed, status="complete"))
    commit(root)
    assert changed["question"] not in get(server)
    assert not load_cards(cards)[0]


def test_owner_answer_is_preserved_in_its_record_and_not_asked_again(board):
    root, cards, record, server = board
    card = load_cards(cards)[0][0]
    status, body = post(board, card, note="Please retain wheelchair access.")
    assert status == 200, body
    assert REQUEST["recommendation"] in record.read_text()
    assert "> Please retain wheelchair access." in record.read_text()
    current, failures = load_cards(cards)
    assert not failures
    assert len(current) == 1 and not current[0].waiting
    assert current[0].answer["Verdict"] == "Confirm"
    assert len(list(cards.glob("*.md"))) == 1
    assert REQUEST["question"] not in get(server)
    assert git(root, "status", "--porcelain") == ""
    assert post(board, card)[0] == 409


def test_revised_question_keeps_the_previous_owner_answer(board):
    root, cards, record, server = board
    old = load_cards(cards)[0][0]
    assert post(board, old, note="My exact original note.")[0] == 200
    saved = (cards / old.file).read_bytes()
    # A revision updates the source declaration, preserving the recorded answer.
    text = record.read_text().replace(REQUEST["question"], "Should we use the accessible community hall instead?")
    record.write_text(text)
    commit(root)
    current, _ = load_cards(cards)
    waiting = [c for c in current if c.waiting]
    assert len(waiting) == 1 and waiting[0].file != old.file
    assert waiting[0].fields["Request key"] == old.fields["Request key"]
    assert (cards / old.file).read_bytes() == saved
    assert "community hall" in get(server)


def test_changed_or_dirty_source_refuses_without_creating_a_card(board):
    root, cards, record, _ = board
    card = load_cards(cards)[0][0]
    record.write_text(record.read_text() + "\nAn uncommitted edit.\n")
    head = git(root, "rev-parse", "HEAD")
    assert post(board, card)[0] == 409
    assert "uncommitted edit" in record.read_text()
    assert not list(cards.glob("*.md"))
    assert git(root, "rev-parse", "HEAD") == head
    commit(root)
    record.write_text(source({**REQUEST, "question": "Should we postpone the event?"}))
    commit(root)
    assert post(board, card)[0] == 409
    assert not list(cards.glob("*.md"))


def test_unreadable_request_is_visible_and_never_an_empty_success(board):
    root, _, record, server = board
    record.write_text(source().replace('"P2"', '"P9"'))
    commit(root)
    body = get(server)
    assert "owner-request source unavailable" in body and "P9" in body
    assert "Nothing here needs you" not in body


def test_deliberate_owner_hold_is_not_fabricated_as_an_approval_question(board):
    root, cards, record, server = board
    record.write_text("# S-001 - Held work\n\n**Status:** active\n**Blockers:** owner:prepare-only\n")
    commit(root)
    body = get(server)
    assert "Recorded owner hold" in body and "prepare-only" in body
    assert "no new approval is inferred" in body
    assert "Nothing here needs you" not in body
    assert not load_cards(cards)[0]


def test_agent_add_and_revise_publish_only_the_source_without_rebuilding_cards(board):
    from ams.grill_board.queue import publish_request
    root, cards, record, server = board
    second = {**REQUEST, "key": "event-date", "question": "Should the event be on Saturday?"}
    assert publish_request(root, RECORD, second, agent="fixture")["status"] == "added"
    assert second["question"] in get(server)
    assert not list(cards.glob("*.md"))
    before = git(root, "rev-parse", "HEAD")
    assert publish_request(root, RECORD, second, agent="fixture", revise=True, reason="same request")["status"] == "unchanged"
    assert git(root, "rev-parse", "HEAD") == before
    revised = {**second, "question": "Should the event be on Sunday?"}
    publish_request(root, RECORD, revised, agent="fixture", revise=True, reason="Saturday unavailable")
    assert revised["question"] in get(server) and second["question"] not in get(server)
    publish_request(root, RECORD, {**revised, "state": "withdrawn"}, agent="fixture", revise=True, reason="Already settled elsewhere")
    assert revised["question"] not in get(server)
    assert REQUEST["question"] in get(server)
    assert git(root, "status", "--porcelain") == ""


def test_returns_are_readable_by_agents_without_changing_the_owners_words(board, monkeypatch, capsys):
    from ams.grill_board.server import main
    root, cards, record, _ = board
    card = load_cards(cards)[0][0]
    before = record.read_bytes()
    note = "Please use the community hall.\nIt has step-free access."
    assert post(board, card, verdict="change", note=note)[0] == 200
    assert record.read_bytes() == before
    monkeypatch.chdir(root)
    assert main(["pending", "--json"]) == 0
    returned = json.loads(capsys.readouterr().out)["items"][0]
    assert returned["note"] == note
    assert returned["answer"]["Verdict"] == "Change"
    assert not load_cards(cards)[0][0].waiting


def test_rating_and_flag_preserve_the_request_and_prevent_an_unchanged_reask(board):
    from ams.grill_board.answers import flag, rate
    root, cards, record, server = board
    before = record.read_bytes()
    card = load_cards(cards)[0][0]
    rate(cards, card, "4", "A useful question.", card.sha)
    rated = load_cards(cards)[0][0]
    assert rated.rating == "4" and rated.waiting
    flag(cards, rated, "Make it easier to answer.", rated.sha)
    assert record.read_bytes() == before
    assert not load_cards(cards)[0][0].waiting
    record.write_text(source({**REQUEST, "context": "Reworded context with the same question."}))
    commit(root)
    current, failures = load_cards(cards)
    assert not any(c.waiting for c in current)
    assert any("flagged too taxing" in " ".join(r.problems) for r in failures)
    assert "Nothing here needs you" not in get(server)


def test_commit_race_restores_the_record_and_removes_only_the_new_response(board, monkeypatch):
    from ams.grill_board import answers
    root, cards, record, _ = board
    card = load_cards(cards)[0][0]
    before = record.read_bytes()

    def refuse_commit(*args, **kwargs):
        raise answers.AnswerRefused("HEAD moved in the fixture")

    monkeypatch.setattr(answers, "_commit_on", refuse_commit)
    assert post(board, card)[0] == 409
    assert record.read_bytes() == before
    assert not list(cards.glob("*.md"))
    assert git(root, "status", "--porcelain") == ""


def test_untracked_response_collision_is_preserved(board):
    root, cards, record, _ = board
    card = load_cards(cards)[0][0]
    before = record.read_bytes()
    (cards / card.file).write_text("Someone else's uncommitted file.\n")
    assert post(board, card)[0] == 409
    assert (cards / card.file).read_text() == "Someone else's uncommitted file.\n"
    assert record.read_bytes() == before


@pytest.mark.parametrize("change", [
    lambda text: text + "\n```grill-board\n" + json.dumps(REQUEST) + "\n```\n",
    lambda text: text.replace('"P2"', '"P9"'),
    lambda text: text.replace('"context":', '"Owner record": "AGENTS.md", "context":'),
    lambda text: text.replace('"context":', '"answer": "approve", "context":'),
])
def test_malformed_or_ambiguous_source_never_offers_an_answer(board, change):
    root, cards, record, server = board
    record.write_text(change(source()))
    commit(root)
    assert not load_cards(cards)[0]
    assert "source unavailable" in get(server)
    assert "Nothing here needs you" not in get(server)


def test_quoted_examples_and_retired_or_linked_records_are_not_live_requests(board):
    root, cards, record, server = board
    record.write_text("# S-001 - Examples\n\n**Status:** active\n\n" + "\n".join("> " + line for line in source().splitlines()))
    retired = record.parent / "archive/SPEC.md"
    retired.parent.mkdir()
    retired.write_text(source())
    linked = record.parent / "TASK.md"
    linked.symlink_to(record)
    commit(root)
    current, failures = load_cards(cards)
    assert not current
    assert any("linked" in " ".join(r.problems) for r in failures)
    assert REQUEST["question"] not in get(server)


def test_revision_endpoint_and_unsaved_note_survive_a_source_conflict(board):
    root, cards, record, server = board
    card = load_cards(cards)[0][0]
    revision = json.loads(get(server, "/api/revision"))["revision"]
    assert revision == git(root, "rev-parse", "HEAD")
    record.write_text(record.read_text() + "\nA local draft.\n")
    status, body = post(board, card, note="Keep my unsaved words & punctuation.")
    assert status == 409
    assert "Keep my unsaved words &amp; punctuation." in body


def test_regrading_an_answered_question_does_not_ask_the_decision_again(board):
    root, cards, record, server = board
    original = load_cards(cards)[0][0]
    assert post(board, original)[0] == 200
    saved = (cards / original.file).read_bytes()
    text = record.read_text().replace('"priority": "P2"', '"priority": "P1"').replace('"topic": "The event"', '"topic": "Event review"')
    record.write_text(text)
    commit(root)
    current, _ = load_cards(cards)
    assert len(current) == 1 and current[0].file == original.file
    assert current[0].priority == "P1" and current[0].fields["Topic"] == "Event review"
    assert not current[0].waiting and current[0].answer["Verdict"] == "Confirm"
    assert (cards / original.file).read_bytes() == saved
    assert REQUEST["question"] not in get(server)


def test_owner_next_gate_without_a_published_question_is_an_agent_preparation_issue(board):
    root, cards, record, server = board
    record.write_text("# S-001 - Pending review\n\n**Status:** active\n**Next gate:** Owner Human QA, then complete.\n")
    commit(root)
    assert not load_cards(cards)[0]
    body = get(server)
    assert "owner-related next gate has no published question" in body
    assert "Nothing here needs you" not in body
