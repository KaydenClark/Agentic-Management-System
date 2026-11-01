"""S-004 TK-001: the Grill Board serves every committed card with Priority and
Value and a one-line reason for each, through its HTTP interface."""

import shutil
import subprocess
import sys
import threading
import tomllib
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

import pytest

from ams.grill_board.cards import CardSourceError
from ams.grill_board.server import make_server

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "grill_board"


class CardPage(HTMLParser):
    """Collects each rendered card's fields and each refusal's text."""

    def __init__(self):
        super().__init__()
        self.cards, self.refusals, self._field, self._in_refusal = [], [], None, False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = (attrs.get("class") or "").split()
        if "card" in classes:
            self.cards.append({})
        if "refusal" in classes:
            self.refusals.append("")
            self._in_refusal = True
        if attrs.get("data-field"):
            self._field = attrs["data-field"]

    def handle_endtag(self, tag):
        self._field = None
        if tag == "li":
            self._in_refusal = False

    def handle_data(self, data):
        if self._field and self.cards:
            self.cards[-1][self._field] = self.cards[-1].get(self._field, "") + data
        if self._in_refusal:
            self.refusals[-1] += data


def git(repo, *args):
    subprocess.run(
        ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", *args],
        cwd=repo, check=True, capture_output=True,
    )


def commit(repo, message="cards"):
    """Commit everything under repo; the board shows only committed cards."""
    if not (repo / ".git").exists():
        git(repo, "init", "-q")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "--allow-empty", "-m", message)


def serve(cards_dir):
    server = make_server(cards_dir, port=0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def get(server, path="/"):
    host, port = server.server_address[:2]
    with urllib.request.urlopen(f"http://{host}:{port}{path}", timeout=5) as response:
        return response.status, response.read().decode("utf-8")


@pytest.fixture
def board(tmp_path):
    servers = []

    def start(*sources, cards=None):
        cards = cards or tmp_path / "cards"
        cards.mkdir(exist_ok=True)
        for source in sources:
            for card in sorted(source.glob("*.md")):
                shutil.copy(card, cards / card.name)
        commit(tmp_path)
        server = serve(cards)
        servers.append(server)
        return server

    yield start
    for server in servers:
        server.shutdown()
        server.server_close()


def page(server):
    status, body = get(server)
    assert status == 200
    parsed = CardPage()
    parsed.feed(body)
    return parsed, body


def test_every_fixture_card_renders_with_both_grades_and_reasons(board):
    parsed, _ = page(board(FIXTURES / "cards"))
    assert len(parsed.cards) == len(list((FIXTURES / "cards").glob("*.md"))) == 4
    for card in parsed.cards:
        for field in ("question", "priority", "priority-reason", "value", "value-reason"):
            assert card.get(field, "").strip(), f"{field} missing from {card}"
    assert parsed.refusals == []


def test_cards_render_their_own_grades_and_reasons(board):
    parsed, _ = page(board(FIXTURES / "cards"))
    quick = next(card for card in parsed.cards if "127.0.0.1" in card["question"])
    assert quick["priority"].strip() == "P1"
    assert quick["priority-reason"].strip() == "The server cannot start until this is settled."
    assert quick["value"].strip() == "V1"
    assert quick["value-reason"].strip() == "One word answers it."


def test_cards_sort_by_priority_then_value_never_summed(board):
    parsed, _ = page(board(FIXTURES / "cards"))
    order = [(card["priority"].strip(), card["value"].strip()) for card in parsed.cards]
    # P2/V1 sums lower than P1/V2 would, but Priority always leads.
    assert order == [("P1", "V1"), ("P1", "V2"), ("P2", "V1"), ("P4", "V3")]


def test_a_graded_card_without_a_reason_is_refused_never_rendered(board):
    parsed, body = page(board(FIXTURES / "cards", FIXTURES / "refused"))
    assert len(parsed.cards) == 4, "only the valid cards render"
    assert "a graded card whose Value has no reason" not in body
    assert "a graded card whose Priority reason is blank" not in body
    refusals = " ".join(parsed.refusals)
    assert "value-without-reason.md" in refusals and "Value reason" in refusals
    assert "blank-priority-reason.md" in refusals and "Priority reason" in refusals


def test_unknown_grades_and_missing_grades_are_refused(board, tmp_path):
    odd = tmp_path / "odd"
    odd.mkdir()
    (odd / "bad-grade.md").write_text(
        "# Bad grade\n\n**Priority:** P9\n**Priority reason:** r\n**Value:** V1\n**Value reason:** r\n"
    )
    (odd / "no-value.md").write_text("# No value\n\n**Priority:** P1\n**Priority reason:** r\n")
    parsed, body = page(board(cards=odd))
    assert parsed.cards == []
    refusals = " ".join(parsed.refusals)
    assert "bad-grade.md" in refusals and "P9" in refusals
    assert "no-value.md" in refusals and "Value" in refusals


def test_the_page_reads_committed_files_on_each_request(board, tmp_path):
    server = board(FIXTURES / "cards")
    shutil.copy(FIXTURES / "refused" / "value-without-reason.md", tmp_path / "cards" / "late.md")
    commit(tmp_path, "late card")
    parsed, _ = page(server)
    assert len(parsed.cards) == 4 and len(parsed.refusals) == 1


def test_card_text_is_escaped(board, tmp_path):
    cards = tmp_path / "esc"
    cards.mkdir()
    (cards / "html.md").write_text(
        "# <script>alert(1)</script>\n\n**Priority:** P1\n**Priority reason:** a < b\n"
        "**Value:** V1\n**Value reason:** b > a\n"
    )
    _, body = page(board(cards=cards))
    assert "<script>" not in body and "&lt;script&gt;" in body


def test_unknown_paths_are_not_found(board):
    server = board(FIXTURES / "cards")
    with pytest.raises(urllib.error.HTTPError) as error:
        get(server, "/missing")
    assert error.value.code == 404


def test_server_listens_on_localhost_only(board):
    assert board(FIXTURES / "cards").server_address[0] == "127.0.0.1"


def test_the_runbook_command_starts_the_board_on_localhost(tmp_path):
    scripts = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["scripts"]
    assert scripts["ams-board"] == "ams.grill_board.server:main"
    assert "uv run ams-board" in (ROOT / "RUNBOOK.md").read_text()
    shutil.copytree(FIXTURES / "cards", tmp_path / "grill-board" / "cards")
    commit(tmp_path)
    command = Path(sys.executable).parent / "ams-board"
    process = subprocess.Popen(
        [str(command), "--port", "0"], cwd=tmp_path, stdout=subprocess.PIPE, text=True
    )
    try:
        line = process.stdout.readline()
        assert line.startswith("Grill Board: http://127.0.0.1:"), line
        url = line.split(": ", 1)[1].strip()
        with urllib.request.urlopen(url, timeout=5) as response:
            assert "approve the card file format" in response.read().decode("utf-8")
    finally:
        process.terminate()
        process.wait(timeout=5)


def test_no_vercel_configuration_references_the_board():
    configs = [p for p in ROOT.rglob("vercel.json") if ".venv" not in p.parts]
    configs += [p for p in ROOT.rglob(".vercel*") if ".venv" not in p.parts and p.is_file()]
    for config in configs:
        text = config.read_text()
        for name in ("grill-board", "grill_board", "ams-board"):
            assert name not in text, f"{config} references {name}"


def test_the_committed_example_card_is_valid_and_labeled(board, tmp_path):
    example = ROOT / "grill-board" / "card-example.md"
    assert "Example" in example.read_text().splitlines()[0]
    cards = tmp_path / "example"
    cards.mkdir()
    shutil.copy(example, cards / example.name)
    parsed, _ = page(board(cards=cards))
    assert len(parsed.cards) == 1 and parsed.refusals == []


def test_uncommitted_edits_show_the_committed_text(board, tmp_path):
    server = board(FIXTURES / "cards")
    card = tmp_path / "cards" / "interrupt-quick.md"
    card.write_text(card.read_text().replace("may the board listen", "DRAFT EDIT"))
    parsed, body = page(server)
    assert "DRAFT EDIT" not in body
    assert any("may the board listen only on 127.0.0.1" in c["question"] for c in parsed.cards)


def test_untracked_and_uncommitted_cards_never_appear(board, tmp_path):
    server = board(FIXTURES / "cards")
    shutil.copy(FIXTURES / "cards" / "interrupt-quick.md", tmp_path / "cards" / "untracked.md")
    staged = tmp_path / "cards" / "staged.md"
    shutil.copy(FIXTURES / "cards" / "committed-quick.md", staged)
    git(tmp_path, "add", str(staged))
    parsed, body = page(server)
    assert len(parsed.cards) == 4
    assert "untracked.md" not in body and "staged.md" not in body


def test_a_card_directory_outside_git_is_refused(tmp_path):
    with pytest.raises(CardSourceError, match="not in a Git repository"):
        make_server(tmp_path, port=0)
