"""S-004 TK-000J: at 375px the board does not scroll sideways and every control
on the open card can be reached and used.

Needs Playwright and a Chromium or installed Chrome, which the default suite
does not carry, so it skips without them. Run it with:

    uv run --with playwright pytest tests/test_grill_board_phone.py
"""

import pytest

from test_grill_board_answers import CARD, RECORD, board, git, origin, repo  # noqa: F401

sync_api = pytest.importorskip("playwright.sync_api")

PHONE = {"width": 375, "height": 812}
URL_QUERY = "?topic=Card+format&card=one-card.md"

# Every visible control, with where it sits and whether a tap at its center
# lands on it (nothing covers it) once it is scrolled into view.
CONTROLS = r"""
() => [...document.querySelectorAll('a[href], button, textarea, input:not([type=hidden]), summary, select')]
  .filter((el) => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden')
  .map((el) => {
    el.scrollIntoView({block: 'center', inline: 'nearest'});
    const box = el.getBoundingClientRect();
    const hit = document.elementFromPoint(box.left + box.width / 2, box.top + box.height / 2);
    return {
      label: el.getAttribute('aria-label') || el.getAttribute('name') || el.textContent.trim().slice(0, 40) || el.tagName,
      value: el.getAttribute('value') || '', left: box.left, right: box.right, width: box.width, height: box.height,
      tappable: !!hit && (hit === el || el.contains(hit) || (el.labels && [...el.labels].includes(hit))),
    };
  })
"""


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as p:
        try:
            launched = p.chromium.launch()
        except Exception:
            try:
                launched = p.chromium.launch(channel="chrome")
            except Exception as error:  # no browser on this machine
                pytest.skip(f"no Chromium or Chrome for Playwright: {error}")
        yield launched
        launched.close()


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_the_board_at_375px_has_no_sideways_scroll_and_every_control_is_reachable(board, repo, browser, theme):
    server = board()
    page = browser.new_page(viewport=PHONE, color_scheme=theme)
    try:
        page.goto(f"{origin(server)}/{URL_QUERY}")
        page.wait_for_load_state("networkidle")
        width = page.evaluate("document.documentElement.scrollWidth")
        assert width <= PHONE["width"], f"the page is {width}px wide at 375px"
        controls = page.evaluate(CONTROLS)
        assert page.evaluate("window.scrollX") == 0, "reaching a control scrolled the page sideways"
        labels = {c["label"] for c in controls}
        for needed in ("note", "comment", "Too taxing", *(f"Rate {n} of 5" for n in range(1, 6))):
            assert needed in labels, f"{needed} is not on the page at 375px"
        assert {c["value"] for c in controls if c["label"] == "verdict"} == {"confirm", "rework-wording", "change-the-why", "change"}
        for control in controls:
            assert control["width"] > 0 and control["height"] > 0, control
            assert control["left"] >= 0 and control["right"] <= PHONE["width"], f"off-screen at 375px: {control}"
            assert control["tappable"], f"covered at 375px: {control}"
    finally:
        page.close()


def test_a_rating_tap_at_375px_commits(board, repo, browser):
    """Reachable means usable: a tap on a star at 375px saves the rating."""
    server = board()
    page = browser.new_page(viewport=PHONE, color_scheme="dark")
    try:
        page.goto(f"{origin(server)}/{URL_QUERY}")
        page.get_by_role("button", name="Rate 4 of 5").click()
        page.wait_for_load_state("networkidle")
    finally:
        page.close()
    assert git(repo, "log", "-1", "--format=%s").strip() == "Grill Board: rate one-card.md 4 of 5"
    assert (repo / "workbench" / "wiki" / "decision.md").read_text() == RECORD
