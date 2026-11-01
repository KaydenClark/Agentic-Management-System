"""S-004 TK-003: a 1-5 rating and a "too taxing" flag are one click each and
saved as committed records on the card, through the same one-commit,
refuse-on-change write path as answers (DDR-000J, ADR-002U). A flagged card
is held for rewrite: re-posting its question unchanged is shown as refused
and cannot be answered, while a rewritten question is accepted."""

import re
import threading
import urllib.parse
import urllib.request

import pytest

from test_grill_board_answers import CARD, RECORD, board, git, head, origin, post, read_form, repo, snapshot  # noqa: F401

CARD_PATH = "grill-board/cards/one-card.md"


def get(server, query=None):
    query = urllib.parse.urlencode(query or {"topic": "Card format", "card": "one-card.md"})
    with urllib.request.urlopen(f"{origin(server)}/?{query}", timeout=5) as response:
        return response.read().decode("utf-8")


def rating_form(html):
    """The open card's rating form: its hidden fields and the form's HTML."""
    form = html.split('<form class="rating"', 1)[1].split("</form>", 1)[0]
    return dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', form)), form


def send(server, path, fields, headers=None):
    data = urllib.parse.urlencode(fields).encode()
    request = urllib.request.Request(f"{origin(server)}{path}", data=data, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    for key, value in ({"Origin": origin(server)} if headers is None else headers).items():
        request.add_header(key, value)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8")


def card_text(repo, name="one-card.md"):
    return (repo / "grill-board" / "cards" / name).read_text()


def queue(html):
    return html.split('<ol class="rows">', 1)[1].split("</ol>", 1)[0]


def post_card(repo, name, text, message):
    (repo / "grill-board" / "cards" / name).write_text(text)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", message)


def flag(server, comment=""):
    fields, _ = rating_form(get(server))
    return send(server, "/flag", {**fields, "comment": comment})


def test_the_open_card_offers_five_live_stars_and_a_live_flag(board, repo):
    fields, form = rating_form(get(board()))
    assert 'method="post" action="/rate"' in form
    assert fields["card"] == "one-card.md" and re.fullmatch(r"[0-9a-f]{64}", fields["card_sha"])
    stars = re.findall(r'<button type="submit" name="rating" value="(\d)"[^>]*>', form)
    assert stars == ["1", "2", "3", "4", "5"]
    flag_button = re.search(r'<button type="submit" formaction="/flag"[^>]*class="taxing[^"]*"[^>]*>', form)
    assert flag_button, form
    assert "disabled" not in form
    assert 'name="comment"' in form
    assert "Not wired yet" not in get(board())


def test_one_click_saves_a_rating_as_a_committed_record_on_the_card(board, repo):
    server = board()
    before = head(repo)
    fields, _ = rating_form(get(server))
    status, body = send(server, "/rate", {**fields, "rating": "4", "comment": "Clear, but long."})
    assert status == 200, body
    card = card_text(repo)
    assert card.startswith(CARD), "nothing on the card is rewritten"
    assert re.search(r"\n## Rating\n\n\*\*Rating:\*\* 4 of 5\n\*\*Rated:\*\* \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ\n\n> Clear, but long\.\n$", card), card
    # One commit, on the branch, of exactly the card; tracked and never ignored.
    assert git(repo, "rev-parse", "HEAD~1").strip() == before
    assert git(repo, "show", "--name-only", "--format=", "HEAD").split() == [CARD_PATH]
    assert git(repo, "log", "-1", "--format=%s").strip() == "Grill Board: rate one-card.md 4 of 5"
    assert CARD_PATH in git(repo, "ls-files", "--", CARD_PATH)
    assert git(repo, "status", "--porcelain") == ""
    assert (repo / "records" / "decision.md").read_text() == RECORD, "a rating never writes the owning record"
    # The page shows the saved rating and the card stays in the queue to answer.
    assert "Written and committed" in body
    assert re.search(r'value="4"[^>]*aria-pressed="true"', rating_form(body)[1])
    assert "one-card.md" in queue(body)


def test_a_rating_can_be_changed_by_appending_and_nothing_is_deleted(board, repo):
    server = board()
    for stars in ("2", "5"):
        fields, _ = rating_form(get(server))
        assert send(server, "/rate", {**fields, "rating": stars})[0] == 200
    card = card_text(repo)
    assert card.count("## Rating") == 2 and "**Rating:** 2 of 5" in card and "**Rating:** 5 of 5" in card
    assert re.search(r'value="5"[^>]*aria-pressed="true"', rating_form(get(server))[1])


@pytest.mark.parametrize("rating", ["0", "6", "4.5", "", "five", " 3"])
def test_a_rating_outside_one_to_five_is_refused_and_nothing_is_written(board, repo, rating):
    server = board()
    fields, _ = rating_form(get(server))
    before = snapshot(repo)
    status, body = send(server, "/rate", {**fields, "rating": rating})
    assert status == 409 and "Not written" in body
    assert snapshot(repo) == before


def test_one_click_saves_the_flag_and_holds_the_card_for_rewrite(board, repo):
    server = board()
    before = head(repo)
    status, body = flag(server, "Three questions in one.")
    assert status == 200, body
    card = card_text(repo)
    assert card.startswith(CARD)
    assert re.search(r"\n## Flag\n\n\*\*Too taxing:\*\* yes\n\*\*Flagged:\*\* \S+Z\n\n> Three questions in one\.\n$", card), card
    assert git(repo, "rev-parse", "HEAD~1").strip() == before
    assert git(repo, "show", "--name-only", "--format=", "HEAD").split() == [CARD_PATH]
    assert git(repo, "log", "-1", "--format=%s").strip() == "Grill Board: flag one-card.md too taxing"
    assert git(repo, "status", "--porcelain") == ""
    # Held: out of the queue, shown as held when opened, and not answerable.
    assert "one-card.md" not in queue(body)
    assert "held for rewrite" in body.split('class="open"', 1)[1]
    assert '<form class="answer"' not in body
    status, again = flag(server)
    assert status == 409 and "already flagged" in again


def test_a_flagged_card_cannot_be_answered(board, repo):
    server = board()
    fields, _ = read_form(server)
    flag(server)
    from ams.grill_board.answers import sha256

    fresh = {**fields, "card_sha": sha256((repo / "grill-board" / "cards" / "one-card.md").read_bytes())}
    before = snapshot(repo)
    status, body = post(server, {**fresh, "verdict": "confirm"})
    assert status == 409 and "too taxing" in body
    assert snapshot(repo) == before


@pytest.mark.parametrize("question", [
    "Fixture: should the board keep one card per file?",
    "  fixture:   SHOULD the board keep one card per file?  ",
])
def test_a_new_card_repeating_a_flagged_question_is_refused(board, repo, question):
    """Must fail: a flagged card re-posted with the same text."""
    server = board()
    flag(server)
    repost = CARD.replace("# Fixture: should the board keep one card per file?", f"# {question}")
    post_card(repo, "repost.md", repost, "an agent re-posts the flagged question unchanged")
    html = get(server, {"topic": "Card format"})
    alert = html.split('aria-label="Refused cards"', 1)[1].split("</section>", 1)[0]
    assert "repost.md" in alert and "flagged too taxing" in alert and "one-card.md" in alert
    assert "repost.md" not in queue(html)
    status, body = post(server, {"card": "repost.md", "card_sha": "0" * 64, "record_sha": "", "verdict": "confirm"})
    assert status == 409 and "no committed card" in body


def test_a_rewritten_question_is_accepted(board, repo):
    server = board()
    flag(server)
    rewrite = CARD.replace("should the board keep one card per file?", "one card per file: yes or no?")
    post_card(repo, "rewrite.md", rewrite, "an agent rewrites the flagged question")
    html = get(server, {"topic": "Card format"})
    assert "rewrite.md" in queue(html)
    assert 'aria-label="Refused cards"' not in html


def test_reverting_the_flag_does_not_re_ask_the_same_card(board, repo):
    """The same card re-posted by undoing the flag commit is still refused."""
    server = board()
    flag(server)
    git(repo, "revert", "--no-edit", "HEAD")
    assert "## Flag" not in card_text(repo)
    html = get(server, {"topic": "Card format"})
    assert "one-card.md" in html.split('aria-label="Refused cards"', 1)[1].split("</section>", 1)[0]
    assert "one-card.md" not in queue(html)


def test_a_copy_of_the_flagged_card_without_its_flag_is_refused(board, repo):
    server = board()
    flag(server)
    copy = card_text(repo).split("\n## Flag\n", 1)[0] + "\n"
    (repo / "grill-board" / "cards" / "copy.md").write_text(copy)
    git(repo, "rm", "-q", CARD_PATH)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "an agent deletes the flagged card and posts a copy")
    html = get(server, {"topic": "Card format"})
    assert "copy.md" in html.split('aria-label="Refused cards"', 1)[1].split("</section>", 1)[0]


def test_an_answered_card_can_still_be_rated_and_flagged(board, repo):
    server = board()
    fields, _ = read_form(server)
    status, body = post(server, {**fields, "verdict": "confirm"})
    assert status == 200
    # The page after the answer opens the answered card, with rating and flag live.
    opened = body.split('class="open"', 1)[1]
    assert "Answered" in opened and '<form class="answer"' not in opened
    rated, _ = rating_form(body)
    status, body = send(server, "/rate", {**rated, "rating": "2"})
    assert status == 200, body
    status, body = send(server, "/flag", {**rating_form(body)[0], "comment": "Too much context to read."})
    assert status == 200, body
    card = card_text(repo)
    assert card.index("## Answer") < card.index("## Rating") < card.index("## Flag")
    assert git(repo, "status", "--porcelain") == ""


def test_a_rating_against_a_card_changed_since_it_was_read_is_refused(board, repo):
    server = board()
    fields, _ = rating_form(get(server))
    (repo / "grill-board" / "cards" / "one-card.md").write_text(CARD.replace("Fixture context.", "Edited context."))
    git(repo, "commit", "-qam", "an agent edits the card")
    before = snapshot(repo)
    for path, extra in (("/rate", {"rating": "3"}), ("/flag", {})):
        status, body = send(server, path, {**fields, **extra})
        assert status == 409 and "changed since" in body, path
    assert snapshot(repo) == before


def test_uncommitted_edits_to_the_card_are_refused_and_kept(board, repo):
    server = board()
    fields, _ = rating_form(get(server))
    (repo / "grill-board" / "cards" / "one-card.md").write_text(CARD + "\nan uncommitted edit\n")
    before = snapshot(repo)
    status, body = send(server, "/rate", {**fields, "rating": "3"})
    assert status == 409 and "uncommitted" in body
    assert snapshot(repo) == before


@pytest.mark.parametrize("path", ["/rate", "/flag"])
@pytest.mark.parametrize("headers", [{}, {"Origin": "http://evil.example"}, {"Referer": "http://evil.example/"}])
def test_cross_origin_ratings_and_flags_are_refused(board, repo, path, headers):
    server = board()
    fields, _ = rating_form(get(server))
    before = snapshot(repo)
    status, _ = send(server, path, {**fields, "rating": "5"}, headers=headers)
    assert status == 403
    assert snapshot(repo) == before


def test_two_boards_rating_one_card_at_once_commit_one_and_refuse_the_other(board, repo):
    first, second = board(), board()
    forms = [rating_form(get(first))[0], rating_form(get(second))[0]]
    results = []
    workers = [
        threading.Thread(target=lambda s=s, f=f, r=r: results.append(send(s, "/rate", {**f, "rating": r})))
        for s, f, r in zip((first, second), forms, ("1", "5"))
    ]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join(timeout=15)
    assert sorted(status for status, _ in results) == [200, 409]
    assert card_text(repo).count("## Rating") == 1
    assert git(repo, "status", "--porcelain") == ""


def test_the_board_is_not_a_drafting_surface(board, repo):
    """Must fail: a page draft posted as a card. The only writes are an answer,
    a rating and a flag; no route creates or edits card or page text."""
    server = board()
    html = get(server)
    assert re.findall(r'<form class="(\w+)" method="post" action="(/\w+)"', html) == [("answer", "/answer"), ("rating", "/rate")]
    assert re.findall(r"<textarea[^>]*name=\"(\w+)\"", html) == ["note"]
    before = snapshot(repo)
    for path in ("/cards", "/card", "/edit", "/draft", "/page", "/rate/../cards"):
        assert send(server, path, {"card": "x.md", "text": "# a page draft"})[0] == 404, path
    post_card(repo, "page-draft.md", "---\ntitle: A page draft\n---\n\nBody of a page.\n", "a page draft posted as a card")
    html = get(server, {"topic": "Card format"})
    assert "page-draft.md" in html.split('aria-label="Refused cards"', 1)[1]
    assert before["record"] == (repo / "records" / "decision.md").read_bytes()
