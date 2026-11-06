"""Synthetic page-feedback recovery through actual rendered browser forms."""
import threading
from urllib.parse import parse_qs, urlsplit

import pytest

pytest.importorskip('playwright.sync_api')
from test_grill_board_phone import browser  # noqa: E402,F401
from test_page_feedback import prepare_feedback, current_card, assert_original_private  # noqa: E402
from test_pages import room, pages, git  # noqa: E402,F401
from ams.grill_board.server import make_server  # noqa: E402
from ams.page_feedback import PageRequest, read_voice  # noqa: E402


def test_unknown_private_capture_retains_exact_browser_retry_and_one_event(room, browser, monkeypatch):
    from ams import page_feedback
    card = prepare_feedback(room)
    original = page_feedback._Store.write
    fail = {'once': True}
    def lose_ack(store, packet, **kwargs):
        original(store, packet, **kwargs)
        if packet['state'] == 'captured' and fail['once']:
            fail['once'] = False
            raise OSError('synthetic lost private-capture acknowledgment')
    monkeypatch.setattr(page_feedback._Store, 'write', lose_ack)
    server = make_server(room / pages.CARDS, port=0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    page = browser.new_page(viewport={'width':375,'height':812})
    submissions = []
    page.on('request', lambda request: submissions.append(parse_qs(request.post_data or '', keep_blank_values=True))
            if request.method == 'POST' and urlsplit(request.url).path == '/answer' else None)
    try:
        page.goto(f'http://127.0.0.1:{server.server_address[1]}/?card={card.file}')
        typed = '\n  Synthetic exact browser original.\nKeep café and trailing whitespace.  '
        page.locator('#note').fill(typed)
        event_id = page.locator('form.answer [name=event_id]').input_value()
        fields = page.locator('form.answer').evaluate('(form) => Object.fromEntries(new FormData(form))')
        before = git(room, 'rev-list', '--count', 'HEAD')
        page.get_by_role('button', name='Change', exact=True).click()
        retry = page.get_by_role('button', name='Check or retry this exact action')
        retry.wait_for()
        assert 'Save outcome unknown:' in page.content()
        assert page.locator('[aria-label="Unsaved submission"] textarea').input_value() == typed
        assert page.locator('form.retry [name=note]').input_value() == submissions[0]['note'][0]
        assert page.locator('form.retry [name=event_id]').input_value() == event_id
        assert git(room, 'rev-list', '--count', 'HEAD') == before
        retry.click()
        page.get_by_label('Answer written', exact=True).wait_for()
        assert read_voice(room).version == 1
        assert int(git(room, 'rev-list', '--count', 'HEAD')) == int(before) + 1
        assert submissions[1] == submissions[0]
        request = PageRequest('answer', card.file, 'change', submissions[0]['note'][0], fields['card_sha'],
                              fields['record_sha'], fields['voice_sha'], event_id)
        assert_original_private(room, request)
        assert current_card(room).answer['Feedback event'] == event_id
    finally:
        page.close()
        server.shutdown()
        server.server_close()
