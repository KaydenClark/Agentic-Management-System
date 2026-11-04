"""Rendered native DQC interactions, using only disposable records."""
import os
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

import pytest

pytest.importorskip('playwright.sync_api')
from test_grill_board_phone import browser, CONTROLS  # noqa: E402,F401
from test_grill_board_dqcs import dqc_room, dqc_board, PROPOSAL, READBACK, action, view, add_branch, git, head, origin  # noqa: E402,F401


@pytest.mark.parametrize('theme',['dark','light'])
@pytest.mark.parametrize('width',[375,1280])
def test_complete_readback_and_controls_reachable(dqc_room,dqc_board,browser,theme,width):
    page = browser.new_page(viewport={'width':width,'height':900},color_scheme=theme)
    external = []
    page.on('request',lambda request:external.append(request.url) if urlsplit(request.url).hostname != '127.0.0.1' else None)
    try:
        page.goto(origin(dqc_board)+'/?card=DQC-000A')
        page.wait_for_load_state('networkidle')
        assert page.get_by_label('Exact displayed readback').text_content() == READBACK
        assert page.evaluate('document.documentElement.scrollWidth') <= width
        page.get_by_label('DQC history',exact=True).evaluate('(element) => element.open = true')
        controls = page.evaluate(CONTROLS)
        assert page.evaluate('window.scrollX') == 0
        for control in controls:
            assert control['left'] >= 0 and control['right'] <= width,control
            assert control['tappable'],control
        for label in ['note','comment','Too taxing','Rate 4 of 5','Finish this round']:
            assert any(c['label']==label for c in controls),label
        assert not external
        capture = os.environ.get('AMS_BOARD_CAPTURE_DIR')
        if capture:
            target = Path(capture);target.mkdir(parents=True,exist_ok=True)
            page.get_by_label('DQC history',exact=True).evaluate('(element) => element.open = false')
            page.evaluate('window.scrollTo(0,0)')
            page.screenshot(path=str(target/f'dqc-{theme}-{width}.png'),full_page=True)
    finally:
        page.close()


def test_refresh_preserves_typing_and_then_updates_changed_readback(dqc_room,dqc_board,browser):
    page = browser.new_page(viewport={'width':375,'height':812})
    try:
        page.goto(origin(dqc_board)+'/?card=DQC-000A')
        page.locator('#note').fill('  My unsaved exact words.  ')
        action(dqc_room,'propose',proposal={**PROPOSAL,'readback':'A new accessible library proposal.'})
        page.locator('[data-queue-update]').wait_for(state='visible',timeout=12000)
        assert page.locator('#note').input_value() == '  My unsaved exact words.  '
        page.locator('#note').fill('')
        page.wait_for_function("document.querySelector('[aria-label=\"Exact displayed readback\"]')?.textContent === 'A new accessible library proposal.'",timeout=12000)
    finally:
        page.close()


def test_web_round_to_actual_wiki_reconciliation_and_next_frontier(dqc_room,dqc_board,browser):
    add_branch(dqc_room,dependencies=['DQC-000A'])
    page = browser.new_page(viewport={'width':1280,'height':900},color_scheme='light')
    try:
        page.goto(origin(dqc_board)+'/?card=DQC-000A')
        page.get_by_role('button',name='Confirm',exact=True).click()
        page.locator('#comment').fill('Please shorten the next question.')
        page.get_by_role('button',name='Rate 3 of 5').click()
        page.goto(origin(dqc_board)+'/?card=DQC-000B')
        page.locator('#note').fill('Ask about timing first.')
        page.get_by_role('button',name='Change',exact=True).click()
        page.get_by_role('button',name='Finish this round').click()
        page.get_by_text('Agent review pending.',exact=False).first.wait_for()
        changed = view(dqc_room)['tracker']['rounds'][0]['changed']
        assert {e['type'] for c in changed for e in c['events']} >= {'confirm','correct','rate'}
        record = dqc_room/'workbench/wiki/round-result.md'
        record.write_text('# Round understanding\n\nDQC-000A venue is confirmed. DQC-000B timing remains unsettled.\n')
        git(dqc_room,'add',str(record.relative_to(dqc_room)));git(dqc_room,'commit','-qm','Reconcile disposable Board round')
        source = f'workbench/wiki/round-result.md@{head(dqc_room)}'
        action(dqc_room,'reconcile-round',None,round='fixture-round-1',receipt=dict(sources=[source],outcome='Captured confirmed venue and unresolved timing.',nextFrontier='Review the invitation timing proposal.'))
        current = view(dqc_room)['tracker']['currentRound']
        action(dqc_room,'propose','DQC-000B',proposal={**PROPOSAL,'readback':'Invite attendees after access is confirmed.','round':current,'dependencies':['DQC-000A']})
        page.wait_for_function("document.querySelector('[aria-label=\"Exact displayed readback\"]')?.textContent === 'Invite attendees after access is confirmed.'",timeout=12000)
        assert page.get_by_text('Next frontier: Review the invitation timing proposal.').is_visible()
        assert page.get_by_role('button',name='Confirm',exact=True).is_visible()
        assert source in page.content()
        assert git(dqc_room,'status','--porcelain') == ''
    finally:
        page.close()


def test_unknown_save_retains_real_retry_after_later_context_change(dqc_room,dqc_board,browser,monkeypatch):
    import subprocess
    from ams.grill_board import dqcs
    run=dqcs.subprocess.run
    lose={'pending':True}
    def corrupt_receipt(args,*a,**kwargs):
        result=run(args,*a,**kwargs)
        if 'action' in args and lose['pending']:
            lose['pending']=False
            return subprocess.CompletedProcess(args,0,'null','')
        return result
    monkeypatch.setattr(dqcs.subprocess,'run',corrupt_receipt)
    page=browser.new_page(viewport={'width':375,'height':812})
    submissions=[]
    page.on('request', lambda request:submissions.append(parse_qs(request.post_data or '',keep_blank_values=True)) if request.method == 'POST' and urlsplit(request.url).path == '/answer' else None)
    try:
        page.goto(origin(dqc_board)+'/?card=DQC-000A')
        typed='  Exact retry words.\nKeep their spacing.  '
        page.locator('#note').fill(typed)
        assert page.locator('#note').input_value()==typed
        page.get_by_role('button',name='Confirm',exact=True).click()
        retry=page.get_by_role('button',name='Check or retry this exact action')
        retry.wait_for()
        assert page.get_by_text('Save outcome unknown:',exact=False).is_visible()
        action(dqc_room,'propose',proposal={**PROPOSAL,'actionable':False,'dependencies':['later-unresolved']})
        current=head(dqc_room)
        page.locator('[data-queue-update]').wait_for(state='visible',timeout=12000)
        assert retry.is_visible()
        retry.click()
        assert 'Replayed' in page.content()
        assert head(dqc_room)==current
        life=view(dqc_room)['tracker']['questions'][0]['lifecycle']
        assert len(life['confirmations'])==1
        # Compare history and retry to the actual form wire bytes, separately from DOM LF text.
        assert '\r\n' in submissions[0]['note'][0]
        assert submissions[1]==submissions[0]
        assert next(event for event in life['events'] if event['type']=='confirm')['note']==submissions[0]['note'][0]
    finally:
        page.close()
