"""Disposable native DQC records exercised through the Python HTTP boundary."""
import html
import json
import re
import shutil
import subprocess
import threading
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

import pytest

from ams.grill_board.server import make_server
from test_grill_board_answers import git, head, origin

ROOT = Path(__file__).resolve().parents[1]
READBACK = '  **Summary**\n\nKeep the library accessible.\n\n**The why**\n\n' + ('A complete proposed concept needs its exact context. ' * 28) + '\n\n**The intended result**\n\nBook the accessible room.\n\n**My next step**\n\nPrepare invitations after approval.\n  '
PROPOSAL = dict(readback=READBACK, why='The venue controls access.', source='Disposable interview fixture', scope='Venue choice only; no booking authority.', round='fixture-round-1', priority=dict(value=1, reason='Before invitations.'), value=dict(value=2, reason='Preserve access.'), dependencies=[])


def native(root, command, *args, payload=None):
    result = subprocess.run(['node', 'workbench/tools/landmark-tracker.mjs', command, *args, '--json'], cwd=root, input=json.dumps(payload) if payload is not None else None, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def view(root):
    return native(root, 'show', '--committed')


def action(root, kind, ident='DQC-000A', **fields):
    current = view(root)
    request = dict(type=kind, eventId=uuid.uuid4().hex, expectHead=current['head'], source='Disposable CLI fixture', **fields)
    if ident:
        card = next(c for c in current['tracker']['questions'] if c['id'] == ident)
        request.update(expectRevision=card['revision'], digest=card['lifecycle']['digest'])
    return native(root, 'action', *([ident] if ident else []), '--stdin', payload=request)


def create_room(root):
    root.mkdir()
    shutil.copytree(ROOT / 'workbench/tools', root / 'workbench/tools')
    manifest = json.loads((ROOT / 'workbench/manifest.json').read_text())
    (root / 'workbench/manifest.json').write_text(json.dumps(manifest))
    for relative in ['grill-board/cards', 'workbench/wiki', 'workbench/specs', 'workbench/landmarks', 'workbench/docs/adr', 'workbench/sessions/grilling', *manifest['landmarkTracker']['collections'].values()]:
        (root / relative).mkdir(parents=True, exist_ok=True)
        (root / relative / '.gitkeep').touch()
    git(root, 'init', '-q', '-b', 'main')
    git(root, 'config', 'user.name', 'fixture')
    git(root, 'config', 'user.email', 'fixture@example.invalid')
    native(root, 'capture', '--id', 'DQC-000A', '--title', 'Accessible venue', '--question', 'Should we use the library?', '--source', 'fixture-interview', '--reason', 'Choose a venue')
    git(root, 'add', '-A'); git(root, 'commit', '-qm', 'Capture fixture branch')
    action(root, 'propose', proposal=PROPOSAL)
    return root


@pytest.fixture
def dqc_room(tmp_path):
    return create_room(tmp_path / 'room')


@pytest.fixture
def dqc_board(dqc_room):
    server = make_server(dqc_room / 'grill-board/cards', port=0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield server
    server.shutdown(); server.server_close()


def get(server, path='/?card=DQC-000A'):
    with urllib.request.urlopen(origin(server) + path, timeout=30) as response:
        return response.read().decode()


def form(server, css='answer', path='/?card=DQC-000A'):
    page = get(server, path)
    body = page.split(f'<form class="{css}"', 1)[1].split('</form>', 1)[0]
    return {key: html.unescape(value) for key, value in re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', body)}


def post(server, fields, endpoint='/answer', headers=None):
    req = urllib.request.Request(origin(server) + endpoint, data=urllib.parse.urlencode(fields).encode(), headers={'Content-Type':'application/x-www-form-urlencoded', **({'Origin':origin(server)} if headers is None else headers)})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode()


def test_complete_native_readback_is_current_and_not_limited_as_legacy_context(dqc_room, dqc_board):
    before = head(dqc_room)
    page = get(dqc_board)
    assert 'DQC-000A' in page and 'Should we use the library?' in page
    assert html.escape(READBACK) in page
    assert PROPOSAL['why'] in page and PROPOSAL['scope'] in page
    assert 'Before invitations.' in page and 'Preserve access.' in page
    assert 'Revision 2' in page and 'Suggested readback' in page
    assert head(dqc_room) == before
    assert git(dqc_room, 'status', '--porcelain') == ''


def test_web_confirmation_preserves_exact_words_and_retry_uses_original_commit(dqc_room, dqc_board):
    fields = {**form(dqc_board), 'verdict':'confirm', 'note':'  My exact note.\nKeep its spacing.  '}
    status, page = post(dqc_board, fields)
    assert status == 200, page
    saved = view(dqc_room)['tracker']['questions'][0]
    assert saved['answer'] == READBACK
    assert saved['lifecycle']['confirmations'][0]['readback'] == READBACK
    assert saved['lifecycle']['events'][-1]['note'] == fields['note']
    assert saved['lifecycle']['confirmations'][0]['source'] == 'Owner action on the local Grill Board'
    original = head(dqc_room)
    status, page = post(dqc_board, fields)
    assert status == 200 and 'Replayed' in page
    assert head(dqc_room) == original
    assert 'Preserved confirmations' in page
    assert 'name="verdict" value="confirm"' not in page
    assert git(dqc_room, 'status', '--porcelain') == ''


def test_correction_and_quality_feedback_share_native_history(dqc_room, dqc_board):
    fields = {**form(dqc_board, 'rating'), 'rating':'2', 'comment':'  Too much context.  '}
    assert post(dqc_board, fields, '/rate')[0] == 200
    correction = {**form(dqc_board), 'verdict':'change-the-why', 'note':'  The reason is access,\nnot cost.  '}
    status, page = post(dqc_board, correction)
    assert status == 200, page
    saved = view(dqc_room)['tracker']['questions'][0]['lifecycle']
    assert saved['state'] == 'needs-rewrite'
    assert saved['digest'] == fields['digest']
    assert saved['events'][-2]['note'] == fields['comment']
    assert saved['events'][-1]['note'] == correction['note']
    assert saved['events'][-1]['kind'] == 'change-the-why'
    assert html.escape(correction['note']) in page
    assert 'Held for agent rewrite' in page
    assert 'name="verdict" value="confirm"' not in page
    # The terminal prepares changed wording; the Board reads that same current DQC.
    action(dqc_room, 'propose', proposal={**PROPOSAL, 'readback':'Revised accessible venue readback.'})
    assert 'Revised accessible venue readback.' in get(dqc_board)


def test_stale_submission_keeps_exact_words_even_after_context_withdrawal(dqc_room, dqc_board):
    fields = {**form(dqc_board), 'verdict':'change', 'note':'  <script>My unsaved words</script>  '}
    action(dqc_room, 'defer', note='Await venue availability.')
    before = head(dqc_room)
    status, page = post(dqc_board, fields)
    assert status == 409
    assert 'Unsaved submission' in page and html.escape(fields['note']) in page
    assert '<script>My unsaved words</script>' not in page
    assert head(dqc_room) == before
    assert 'Deferred concept' in page


def test_context_only_branches_are_navigable_without_asking_settled_questions(dqc_room, dqc_board):
    action(dqc_room, 'propose', proposal={**PROPOSAL, 'actionable':False})
    page = get(dqc_board)
    assert 'Branch context · no owner answer requested' in page
    assert 'Context and history' in page and READBACK.strip()[:10] in html.unescape(page)
    assert '<form class="answer"' not in page
    assert '<form class="rating"' not in page


def add_branch(root, ident='DQC-000B', dependencies=None):
    native(root, 'capture', '--id', ident, '--title', 'Invitations', '--question', 'May invitations be prepared?', '--source', 'fixture-interview', '--reason', 'Distinct follow-up')
    git(root, 'add', '-A'); git(root, 'commit', '-qm', 'Capture next fixture branch')
    action(root, 'propose', ident, proposal={**PROPOSAL, 'readback':'Prepare accessible invitations.', 'dependencies':dependencies or []})


def test_unconfirmed_and_unknown_dependencies_hold_frontier_until_native_confirmation(dqc_room, dqc_board):
    add_branch(dqc_room, dependencies=['DQC-000A'])
    page = get(dqc_board, '/?card=DQC-000B')
    assert 'Waiting on dependencies' in page
    assert 'name="verdict" value="confirm"' not in page
    action(dqc_room, 'confirm', scope=PROPOSAL['scope'])
    page = get(dqc_board, '/?card=DQC-000B')
    assert 'name="verdict" value="confirm"' in page
    action(dqc_room, 'propose', 'DQC-000B', proposal={**PROPOSAL, 'readback':'Prepare accessible invitations.', 'dependencies':['legacy-unknown']})
    page = get(dqc_board, '/?card=DQC-000B')
    assert 'legacy-unknown · unconfirmed or unresolved' in page
    assert 'name="verdict" value="confirm"' not in page


def test_round_handoff_reconciles_actual_wiki_commit_and_carries_next_frontier(dqc_room, dqc_board):
    # An actual disposable web confirmation and quality event, not synthetic live owner data.
    assert post(dqc_board, {**form(dqc_board), 'verdict':'confirm'})[0] == 200
    assert post(dqc_board, {**form(dqc_board,'rating'), 'rating':'3', 'comment':'Please shorten the next question.'}, '/rate')[0] == 200
    add_branch(dqc_room, dependencies=['DQC-000A'])
    assert post(dqc_board, {**form(dqc_board, path='/?card=DQC-000B'), 'verdict':'change', 'note':'Ask about timing first.'})[0] == 200
    status, page = post(dqc_board, form(dqc_board, 'round'), '/round')
    assert status == 200 and 'Agent review pending' in page
    changed = view(dqc_room)['tracker']['rounds'][0]['changed']
    assert {item['id'] for item in changed} == {'DQC-000A','DQC-000B'}
    assert {event['type'] for item in changed for event in item['events']} >= {'confirm','rate','correct'}
    assert next(c for c in changed if c['id']=='DQC-000B')['unanswered']
    wiki = dqc_room/'workbench/wiki/venue.md'
    wiki.write_text('# Venue understanding\n\nDQC-000A confirms the accessible library concept. DQC-000B timing is unsettled.\n')
    git(dqc_room,'add','workbench/wiki/venue.md');git(dqc_room,'commit','-qm','Reconcile fixture venue understanding')
    source = f'workbench/wiki/venue.md@{head(dqc_room)}'
    action(dqc_room,'reconcile-round',None,round='fixture-round-1',receipt=dict(sources=[source],outcome='Recorded confirmed venue; kept timing unresolved.',nextFrontier='Ask about invitation timing.'))
    current = view(dqc_room)['tracker']['currentRound']
    action(dqc_room,'propose','DQC-000B',proposal={**PROPOSAL,'round':current,'readback':'Prepare invitations after the accessible venue is confirmed.','dependencies':['DQC-000A']})
    page = get(dqc_board,'/?card=DQC-000B')
    assert 'Reconciled:' in page and source in page and 'Ask about invitation timing.' in page
    assert 'Prepare invitations after the accessible venue is confirmed.' in page
    assert 'name="verdict" value="confirm"' in page
    assert git(dqc_room,'status','--porcelain') == ''


@pytest.mark.parametrize('endpoint,fields', [('/answer',{'verdict':'confirm'}),('/rate',{'rating':'4'}),('/flag',{}),('/round',{})])
def test_dqc_posts_keep_origin_guard(dqc_room,dqc_board,endpoint,fields):
    posted = form(dqc_board,'round' if endpoint=='/round' else 'rating' if endpoint in ('/rate','/flag') else 'answer')
    before = head(dqc_room)
    assert post(dqc_board,{**posted,**fields},endpoint,headers={'Origin':'https://example.invalid'})[0] == 403
    assert head(dqc_room) == before


def test_changed_proposal_does_not_attach_refused_words_to_new_readback(dqc_room,dqc_board):
    old = {**form(dqc_board),'verdict':'change','note':'Words about the OLD proposal.'}
    action(dqc_room,'propose',proposal={**PROPOSAL,'readback':'New proposal, different question context.'})
    status,page = post(dqc_board,old)
    assert status == 409 and 'Unsaved submission' in page
    active_form = page.split('<form class="answer"',1)[1].split('</form>',1)[0]
    assert old['note'] not in active_form
    assert old['note'] in page


def test_failed_native_commit_restores_owned_files_and_unrelated_staged_work(dqc_room,dqc_board):
    hook = dqc_room/'.git/hooks/pre-commit'
    hook.write_text('#!/bin/sh\nexit 1\n');hook.chmod(0o755)
    unrelated = dqc_room/'unrelated.txt';unrelated.write_text('Preserve this staged work.\n')
    git(dqc_room,'add','unrelated.txt')
    before = head(dqc_room)
    originals = {p:p.read_bytes() for p in (dqc_room/'workbench/landmark-tracker').rglob('*') if p.is_file()}
    status,page = post(dqc_board,{**form(dqc_board),'verdict':'confirm','note':'Keep this note after refusal.'})
    assert status == 409 and 'Keep this note after refusal.' in page
    assert head(dqc_room) == before
    assert all(p.read_bytes()==data for p,data in originals.items())
    assert git(dqc_room,'diff','--cached','--name-only').strip() == 'unrelated.txt'


def test_competing_board_instances_record_one_confirmation(dqc_room,dqc_board):
    from concurrent.futures import ThreadPoolExecutor
    other = make_server(dqc_room/'grill-board/cards',port=0)
    threading.Thread(target=other.serve_forever,daemon=True).start()
    try:
        first = {**form(dqc_board),'verdict':'confirm'}
        second = {**form(other),'verdict':'confirm'}
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda item:post(*item),[(dqc_board,first),(other,second)]))
        assert sorted(status for status,_ in results)==[200,409]
        assert len(view(dqc_room)['tracker']['questions'][0]['lifecycle']['confirmations'])==1
    finally:
        other.shutdown();other.server_close()


def test_legacy_cards_and_explicit_dqc_links_preserve_original_bytes(dqc_room,dqc_board):
    from test_grill_board_answers import CARD, RECORD
    cards = dqc_room/'grill-board/cards'
    legacy = cards/'legacy.md';legacy.write_text(CARD)
    owner = dqc_room/'workbench/wiki/decision.md';owner.write_text(RECORD)
    linked = cards/'linked.md';linked.write_text(CARD.replace('**Topic:** Card format','**Topic:** Card format\n**DQC:** DQC-000A'))
    git(dqc_room,'add','-A');git(dqc_room,'commit','-qm','Preserve legacy fixture cards')
    original = linked.read_bytes()
    page = get(dqc_board,'/?topic=Card+format')
    queue = page.split('<ol class="rows">',1)[1].split('</ol>',1)[0]
    assert 'legacy.md' in queue and 'linked.md' not in queue
    fields = form(dqc_board,path='/?topic=Card+format&card=legacy.md')
    assert post(dqc_board,{**fields,'verdict':'confirm'})[0] == 200
    assert 'Confirmed: Keep one Markdown file per card.' in owner.read_text()
    assert linked.read_bytes() == original
    assert 'Legacy history · DQC owns the question' in get(dqc_board,'/?topic=Card+format&card=linked.md')


def test_committed_source_failure_is_visible_and_dirty_dqc_never_displays(dqc_room,dqc_board):
    record = dqc_room/'workbench/landmark-tracker/destination-questions/DQC-000A.json'
    original = record.read_text();record.write_text('not valid uncommitted JSON')
    assert html.escape(READBACK) in get(dqc_board)
    status,page = post(dqc_board,{**form(dqc_board),'verdict':'confirm','note':'Retain my exact words.'})
    assert status == 409 and 'Retain my exact words.' in page
    record.write_text(original)
    record.write_text('not valid committed JSON')
    git(dqc_room,'add',str(record.relative_to(dqc_room)));git(dqc_room,'commit','-qm','Malformed disposable source')
    page = get(dqc_board,'/')
    assert 'DQC tracker' in page and 'queue is unavailable' in page
    assert 'Nothing here needs you.' not in page


def test_uncertain_saved_action_has_exact_ui_retry_and_no_duplicate(dqc_room,dqc_board,monkeypatch):
    from ams.grill_board import dqcs
    original = dqcs.subprocess.run
    once = {'done':False}
    def lose_receipt(args,*a,**kwargs):
        result = original(args,*a,**kwargs)
        if 'action' in args and not once['done']:
            once['done']=True
            return subprocess.CompletedProcess(args,0,'["invalid receipt shape"]','')
        return result
    fields = {**form(dqc_board),'verdict':'confirm','note':'  Exact\nretry words.  '}
    monkeypatch.setattr(dqcs.subprocess,'run',lose_receipt)
    status,page = post(dqc_board,fields)
    assert status == 503 and 'Save outcome unknown' in page
    assert 'Check or retry this exact action' in page and 'data-unsaved-action' in page
    body = page.split('<form class="retry"',1)[1].split('</form>',1)[0]
    retry = {k:html.unescape(v) for k,v in re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"',body)}
    assert retry == fields
    saved = head(dqc_room)
    status,page = post(dqc_board,retry)
    assert status == 200 and 'Replayed' in page
    assert head(dqc_room) == saved
    assert len(view(dqc_room)['tracker']['questions'][0]['lifecycle']['confirmations'])==1


def test_cross_topic_stable_links_follow_native_titles(dqc_room,dqc_board):
    add_branch(dqc_room,dependencies=['DQC-000A'])
    page = get(dqc_board,'/?card=DQC-000B')
    assert '<span class="topic-label">Accessible venue</span>' in page
    assert '<span class="topic-label">Invitations</span>' in page
    assert 'May invitations be prepared?' in page.split('<main class="open"',1)[1]
    parent = get(dqc_board,'/?card=DQC-000A')
    assert 'Should we use the library?' in parent.split('<main class="open"',1)[1]


def test_original_saved_retry_survives_later_context_and_dependency_changes(dqc_room,dqc_board,monkeypatch):
    from ams.grill_board import dqcs
    run = dqcs.subprocess.run
    lose = {'pending':True}
    def lost(args,*a,**kwargs):
        result = run(args,*a,**kwargs)
        if 'action' in args and lose['pending']:
            lose['pending']=False
            return subprocess.CompletedProcess(args,0,'null','')
        return result
    original = {**form(dqc_board),'verdict':'confirm','note':'My exact original confirmation.'}
    monkeypatch.setattr(dqcs.subprocess,'run',lost)
    status,page = post(dqc_board,original)
    assert status == 503
    action(dqc_room,'propose',proposal={**PROPOSAL,'actionable':False,'dependencies':['unknown-prerequisite']})
    after_metadata = head(dqc_room)
    body = page.split('<form class="retry"',1)[1].split('</form>',1)[0]
    retry = {k:html.unescape(v) for k,v in re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"',body)}
    status,page = post(dqc_board,retry)
    assert status == 200 and 'Replayed' in page
    assert head(dqc_room)==after_metadata
    assert len(view(dqc_room)['tracker']['questions'][0]['lifecycle']['confirmations'])==1


@pytest.mark.parametrize('broken',['tracker','confirmation','event','history','round'])
def test_malformed_native_view_shapes_are_visible_source_refusals(dqc_room,dqc_board,monkeypatch,broken):
    from ams.grill_board import dqcs
    value = view(dqc_room)
    if broken=='tracker':value['tracker']=None
    elif broken=='confirmation':value['tracker']['questions'][0]['lifecycle']['confirmations']=[None]
    elif broken=='event':value['tracker']['questions'][0]['lifecycle']['events']=[None]
    elif broken=='history':value['tracker']['questions'][0]['history']=[{'revision':2,'reason':'x','changes':[{'field':'lifecycle','to':None}]}]
    else:value['tracker']['rounds']=[None]
    run = dqcs.subprocess.run
    def malformed(args,*a,**kwargs):
        if args[0]=='node' and 'show' in args:return subprocess.CompletedProcess(args,0,json.dumps(value),'')
        return run(args,*a,**kwargs)
    monkeypatch.setattr(dqcs.subprocess,'run',malformed)
    dqcs._committed.cache_clear()
    page=get(dqc_board,'/')
    assert 'DQC tracker' in page and 'unavailable' in page
    assert 'Nothing here needs you.' not in page


def test_too_taxing_goes_to_same_native_record_and_new_instance_keeps_history(dqc_room,dqc_board):
    fields={**form(dqc_board,'rating'),'comment':'  Ask one smaller question.  '}
    status,page=post(dqc_board,fields,'/flag')
    assert status==200 and 'Held for agent rewrite' in page
    life=view(dqc_room)['tracker']['questions'][0]['lifecycle']
    assert life['events'][-1]['type']=='flag' and life['events'][-1]['note']==fields['comment']
    from ams.grill_board import dqcs
    dqcs._committed.cache_clear()
    restarted=make_server(dqc_room/'grill-board/cards',port=0)
    threading.Thread(target=restarted.serve_forever,daemon=True).start()
    try:
        page=get(restarted)
        assert html.escape(fields['comment']) in page and 'Held for agent rewrite' in page
        assert 'name="verdict" value="confirm"' not in page
    finally:
        restarted.shutdown();restarted.server_close()
