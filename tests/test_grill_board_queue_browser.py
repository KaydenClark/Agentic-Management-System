"""Rendered automatic queue: live updates, draft preservation and phone reachability."""

from pathlib import Path
from urllib.parse import urlsplit

import pytest

from test_grill_board_phone import CONTROLS, browser  # noqa: F401; optional native Playwright fixture
from test_grill_board_queue import REQUEST, board, commit, source  # noqa: F401


@pytest.mark.parametrize("theme", ["dark", "light"])
@pytest.mark.parametrize("width", [375, 1280])
def test_automatic_requests_are_readable_and_controls_reachable(board, browser, theme, width):
    _, _, _, server = board
    origin = f"http://127.0.0.1:{server.server_address[1]}"
    page = browser.new_page(viewport={"width": width, "height": 900}, color_scheme=theme)
    remote, errors = [], []
    page.on("request", lambda request: remote.append(request.url) if urlsplit(request.url).hostname != "127.0.0.1" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    try:
        page.goto(origin)
        page.get_by_role("heading", name=REQUEST["question"], exact=True).wait_for()
        assert page.get_by_text(REQUEST["recommendation"], exact=True).is_visible()
        assert page.evaluate("document.documentElement.scrollWidth") <= width
        controls = page.evaluate(CONTROLS)
        assert all(c["tappable"] and c["left"] >= 0 and c["right"] <= width for c in controls), controls
        assert page.evaluate("window.scrollX") == 0
        page.evaluate("window.scrollTo(0, 0)")
        evidence = Path("/private/tmp/ams-s004-qa")
        evidence.mkdir(exist_ok=True)
        page.screenshot(path=str(evidence / f"queue-{theme}-{width}.png"), full_page=True)
        assert not remote and not errors
    finally:
        page.close()


def test_open_queue_updates_automatically_and_keeps_unsaved_owner_words(board, browser):
    root, _, record, server = board
    page = browser.new_page()
    try:
        page.goto(f"http://127.0.0.1:{server.server_address[1]}")
        page.fill("#note", "Keep my exact unsaved note.")
        revised = {**REQUEST, "question": "Should we move the event to the community hall?"}
        record.write_text(source(revised))
        commit(root)
        notice = page.locator("[data-queue-update]")
        notice.wait_for(state="visible", timeout=12000)
        assert "unsaved words are kept" in notice.inner_text()
        assert page.locator("#note").input_value() == "Keep my exact unsaved note."
        assert page.get_by_role("heading", name=REQUEST["question"], exact=True).is_visible()
        page.fill("#note", "")
        page.get_by_role("heading", name=revised["question"], exact=True).wait_for(timeout=12000)
        assert page.locator("#note").input_value() == ""
        page.route("**/api/revision", lambda route: route.fulfill(status=503, body='{"error":"unavailable"}'))
        page.wait_for_function("document.querySelector('[data-queue-update]').textContent.includes('unavailable')", timeout=12000)
        assert page.get_by_role("heading", name=revised["question"], exact=True).is_visible()
    finally:
        page.close()
