"""Read-only coverage of committed cards against one frozen site inventory."""
import json
import subprocess
from pathlib import Path

import pytest

from ams import pages
from ams.grill_board.cards import load_cards
from test_pages import git, html, inventory, room  # noqa:F401


def prepared(room):
    listed = inventory(room)
    built = {row['path']: html(row['title']) for row in listed['pages']}
    candidate = git(room, 'rev-parse', 'HEAD')
    pages.generate(room, listed, built, candidate=candidate)
    return listed, built, candidate


def test_complete_committed_coverage_is_read_only_and_counts_current_cards(room):
    from ams.page_coverage import check_coverage
    listed, built, candidate = prepared(room)
    before = git(room, 'rev-parse', 'HEAD'), git(room, 'status', '--porcelain')
    result = check_coverage(room, listed, candidate=candidate, built=built)
    assert result['pages'] == result['cards'] == 2
    assert result['candidate'] == candidate and result['recomputed'] is True
    assert (git(room, 'rev-parse', 'HEAD'), git(room, 'status', '--porcelain')) == before


def commit_json(room, relative, value):
    path = room / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')
    git(room, 'add', relative)
    git(room, 'commit', '-qm', 'Synthetic changed coverage input')


@pytest.mark.parametrize('defect', ['missing-page','missing-card','changed-origin','changed-kind',
                                  'duplicate-open','wrong-card-hash','wrong-owner','removed-page'])
def test_coverage_refuses_each_uncovered_or_stale_page_without_writes(room, defect):
    from ams.page_coverage import CoverageRefused, check_coverage
    listed, built, candidate = prepared(room)
    index = json.loads((room / pages.INDEX).read_text())
    name = index['pages']['/']['card']
    target = room / pages.CARDS / name
    expected = '/'
    if defect == 'missing-page':
        listed['pages'].append({**listed['pages'][0], 'path':'/new'})
        expected = '/new'
    elif defect == 'removed-page':
        listed['pages'] = [row for row in listed['pages'] if row['path'] != '/']
    elif defect == 'changed-origin':
        listed['pages'][0]['landed']['commit'] = 'f' * 40
    elif defect == 'changed-kind':
        listed['pages'][0]['provenance_kind'] = 'verified-containment'
    elif defect == 'missing-card':
        git(room, 'rm', pages.CARDS + '/' + name)
        git(room, 'commit', '-qm', 'Synthetic missing card')
    elif defect == 'duplicate-open':
        other = room / pages.CARDS / 'page-duplicate.md'
        other.write_bytes(target.read_bytes())
        git(room, 'add', str(other))
        git(room, 'commit', '-qm', 'Synthetic duplicate open card')
    else:
        text = target.read_text()
        text = text.replace(index['pages']['/']['hash'], 'sha256:' + 'e' * 64) if defect == 'wrong-card-hash' else text.replace('**Spec:** S-003', '**Spec:** S-008')
        target.write_text(text)
        git(room, 'add', str(target))
        git(room, 'commit', '-qm', 'Synthetic stale card identity')
    before = git(room, 'rev-parse', 'HEAD'), git(room, 'status', '--porcelain')
    with pytest.raises(CoverageRefused, match=expected):
        check_coverage(room, listed, candidate=candidate)
    assert (git(room, 'rev-parse', 'HEAD'), git(room, 'status', '--porcelain')) == before


def test_recompute_detects_served_change_but_retains_footer_only_identity(room):
    from ams.page_coverage import CoverageRefused, check_coverage
    listed, built, candidate = prepared(room)
    same = {path: value.replace('<footer>abc', '<footer>new identity') for path,value in built.items()}
    assert check_coverage(room, listed, candidate=candidate, built=same)['cards'] == 2
    built['/'] = html('Synthetic changed served main')
    with pytest.raises(CoverageRefused, match='/.*served content hash'):
        check_coverage(room, listed, candidate=candidate, built=built)


def test_coverage_uses_one_committed_snapshot_and_ignores_working_tree_drafts(room):
    from ams.page_coverage import check_coverage
    listed, built, candidate = prepared(room)
    card = load_cards(room / pages.CARDS)[0][0]
    (room / pages.CARDS / card.file).write_text('Synthetic uncommitted draft.\n')
    (room / pages.INDEX).write_text('Synthetic uncommitted draft.\n')
    (room / pages.CARDS / 'page-untracked.md').write_text('Synthetic uncommitted draft.\n')
    before = git(room, 'status', '--porcelain')
    assert check_coverage(room, listed, candidate=candidate)['cards'] == 2
    assert git(room, 'status', '--porcelain') == before


def test_current_frozen_candidate_is_required_even_when_historical_landing_is_equal(room):
    from ams.page_coverage import CoverageRefused, check_coverage
    listed, _, _ = prepared(room)
    with pytest.raises(CoverageRefused, match='candidate'):
        check_coverage(room, listed, candidate='a' * 40)


def test_pending_candidate_and_stale_answered_history_keep_truthful_coverage(room):
    from ams.page_coverage import check_coverage
    listed = inventory(room, ('/',))
    listed['pages'][0].update(provenance_kind='pending-candidate', landed=None)
    candidate = git(room, 'rev-parse', 'HEAD')
    pages.generate(room, listed, {'/':html()}, candidate=candidate)
    assert check_coverage(room, listed, candidate=candidate)['cards'] == 1
    from ams.grill_board.answers import answer, render_hashes
    card = load_cards(room / pages.CARDS)[0][0]
    card_sha, owner_sha = render_hashes(room / pages.CARDS, card)
    answer(room / pages.CARDS, card, 'confirm', '', card_sha, owner_sha)
    pages.generate(room, listed, {'/':html('Changed synthetic page')}, candidate=candidate)
    assert check_coverage(room, listed, candidate=candidate, built={'/':html('Changed synthetic page')})['cards'] == 1


def test_cli_check_has_explicit_injected_fixture_mode_and_reports_counts(room, tmp_path, capsys):
    listed, built, candidate = prepared(room)
    data = tmp_path / 'inventory.json'
    bodies = tmp_path / 'bodies.json'
    data.write_text(json.dumps(listed))
    bodies.write_text(json.dumps(built))
    before = git(room, 'rev-parse', 'HEAD'), git(room, 'status', '--porcelain')
    pages.main(['check','--project',str(room),'--inventory',str(data),'--candidate',candidate])
    result = json.loads(capsys.readouterr().out)
    assert result['pages'] == result['cards'] == 2
    assert result['input_mode'] == 'injected-artifact' and not result['recomputed']
    pages.main(['check','--project',str(room),'--inventory',str(data),'--candidate',candidate,
                '--recompute','--built-html',str(bodies)])
    assert json.loads(capsys.readouterr().out)['recomputed']
    assert (git(room, 'rev-parse', 'HEAD'), git(room, 'status', '--porcelain')) == before


def source_fixture(room, *, inventory_path='site/page-list.json'):
    from ams.page_build import AMS_ORIGIN
    listed = inventory(room)
    built = {row['path']:html(row['title']) for row in listed['pages']}
    manifest = json.loads((room / 'workbench/manifest.json').read_text())
    manifest['pageReview']['inventory'] = inventory_path
    (room / 'workbench/manifest.json').write_text(json.dumps(manifest) + '\n')
    path = room / inventory_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(listed) + '\n')
    git(room,'add','workbench/manifest.json',inventory_path)
    git(room,'commit','-qm','Synthetic committed source inventory')
    candidate = git(room,'rev-parse','HEAD')
    git(room,'remote','add','origin',AMS_ORIGIN)
    git(room,'update-ref','refs/remotes/origin/dev',candidate)
    pages.generate(room,listed,built,candidate=candidate)
    return listed,built,candidate


@pytest.mark.parametrize('inventory_path',['site/page-list.json','site/renamed-inventory.json'])
def test_cli_reads_declared_inventory_from_one_frozen_dev_commit(room,capsys,inventory_path):
    listed,built,candidate = source_fixture(room,inventory_path=inventory_path)
    (room / inventory_path).write_text('Synthetic uncommitted inventory must be ignored.\n')
    before = git(room,'rev-parse','HEAD'),git(room,'status','--porcelain')
    pages.main(['check','--project',str(room)])
    result = json.loads(capsys.readouterr().out)
    assert result['pages'] == result['cards'] == 2 and result['candidate'] == candidate
    assert result['input_mode'] == 'committed-inventory' and not result['recomputed']
    assert (git(room,'rev-parse','HEAD'),git(room,'status','--porcelain')) == before


def test_cli_nonzero_names_every_new_listed_page_without_writes(room,capsys):
    listed,built,candidate = source_fixture(room)
    for path in ['/new-one','/new-two']:
        listed['pages'].append({**listed['pages'][0],'path':path})
    commit_json(room,'site/page-list.json',listed)
    next_candidate = git(room,'rev-parse','HEAD')
    git(room,'update-ref','refs/remotes/origin/dev',next_candidate)
    before = git(room,'rev-parse','HEAD'),git(room,'status','--porcelain')
    with pytest.raises(SystemExit) as error:pages.main(['check','--project',str(room)])
    assert error.value.code == 1
    message = capsys.readouterr().err
    assert '/new-one' in message and '/new-two' in message and 'candidate' in message
    assert (git(room,'rev-parse','HEAD'),git(room,'status','--porcelain')) == before


@pytest.mark.parametrize('changed,cleanup',[(False,True),(True,True),(False,False)])
def test_cli_recompute_uses_owned_build_seam_and_refuses_change_or_unverified_cleanup(room,monkeypatch,capsys,changed,cleanup):
    from ams import page_build
    listed,built,candidate = source_fixture(room)
    if changed:built['/'] = html('Synthetic changed served content')
    observed = []
    class Runtime:
        cleanup_verified = cleanup
        def __init__(self,image,**kwargs):assert image == 'sha256:'+'1'*64
    def collect(source,ref,pinned,*,build_start,public_config,inventory_relative):
        assert source == room and ref == 'origin/dev' and pinned == candidate
        assert isinstance(build_start,Runtime) and public_config is None
        assert inventory_relative == 'site/page-list.json'
        observed.append(True)
        return {'candidate':candidate,'inventory':listed,'html':built,'kinds':{},'excluded':{}}
    monkeypatch.setattr(page_build,'DockerBuild',Runtime)
    monkeypatch.setattr(page_build,'collect_current',collect)
    before = git(room,'rev-parse','HEAD'),git(room,'status','--porcelain')
    command = ['check','--project',str(room),'--recompute','--image','sha256:'+'1'*64]
    if changed or not cleanup:
        with pytest.raises(SystemExit) as error:pages.main(command)
        assert error.value.code == 1
        assert ('served content hash' if changed else 'cleanup') in capsys.readouterr().err
    else:
        pages.main(command)
        result = json.loads(capsys.readouterr().out)
        assert result['recomputed'] and result['cleanup_verified'] and result['input_mode'] == 'pinned-container-build'
    assert observed == [True]
    assert (git(room,'rev-parse','HEAD'),git(room,'status','--porcelain')) == before


def test_cli_recompute_validates_protected_capture_before_comparing_actual_hash(room,monkeypatch,capsys):
    from ams import page_build,protected_pages
    listed,actual,candidate = source_fixture(room)
    class Runtime:
        cleanup_verified = True
        def __init__(self,*args,**kwargs):pass
    local = {'candidate':candidate,'inventory':listed,'html':{p:html('Synthetic unavailable data state') for p in actual},'kinds':{},'excluded':{}}
    monkeypatch.setattr(page_build,'DockerBuild',Runtime)
    monkeypatch.setattr(page_build,'collect_current',lambda *args,**kwargs:local)
    pins = {'repository':page_build.AMS_ORIGIN,'project':'synthetic-project','deployment':'synthetic-deployment',
            'candidate':candidate,'origin':'https://synthetic.example.invalid','capture_sha256':'a'*64}
    observed = []
    def capture(directory,snapshot,*,expected_pins):
        assert directory == room/'capture' and snapshot is local and expected_pins == pins
        observed.append(True)
        return {**local,'html':actual,'protection':pins}
    monkeypatch.setattr(protected_pages,'collect_protected',capture)
    pages.main(['check','--project',str(room),'--recompute','--image','sha256:'+'1'*64,
                '--protected-artifact',str(room/'capture'),'--protected-project',pins['project'],
                '--protected-deployment',pins['deployment'],'--protected-origin',pins['origin'],
                '--protected-capture-sha256',pins['capture_sha256']])
    result = json.loads(capsys.readouterr().out)
    assert result['input_mode'] == 'protected-capture' and result['protection'] == pins
    assert result['pages'] == result['cards'] == 2 and observed == [True]


def test_cli_capture_without_independent_pins_refuses_before_execution(room):
    with pytest.raises(SystemExit) as error:
        pages.main(['check','--project',str(room),'--recompute','--image','sha256:'+'1'*64,
                    '--protected-artifact',str(room/'capture')])
    assert error.value.code == 2


def test_unindexed_damaged_page_marker_refuses_instead_of_hiding_an_extra_question(room):
    from ams.page_coverage import CoverageRefused,check_coverage
    listed,_,candidate = prepared(room)
    card = next(c for c in load_cards(room / pages.CARDS)[0] if c.fields['Page']=='/')
    text = (room / pages.CARDS / card.file).read_text()
    extra = room / pages.CARDS / 'page-orphan.md'
    extra.write_text('\n'.join(line for line in text.splitlines() if not line.startswith('**Page:**'))+'\n')
    git(room,'add',str(extra));git(room,'commit','-qm','Synthetic damaged extra page question')
    with pytest.raises(CoverageRefused,match='page-orphan'):
        check_coverage(room,listed,candidate=candidate)


@pytest.mark.parametrize('reference',['missing','future'])
def test_current_open_page_needs_an_available_voice_reference(room,reference):
    from ams.page_coverage import CoverageRefused,check_coverage
    listed,built,candidate = prepared(room)
    card = next(c for c in load_cards(room / pages.CARDS)[0] if c.fields['Page']=='/')
    path = room / pages.CARDS / card.file
    text = path.read_text()
    if reference=='missing':
        text='\n'.join(line for line in text.splitlines() if not line.startswith('**Voice record:**'))+'\n'
    else:
        text=text.replace('voice-and-taste.md version 0','voice-and-taste.md version 42')
    path.write_text(text);git(room,'add',str(path));git(room,'commit','-qm','Synthetic unavailable voice reference')
    with pytest.raises(CoverageRefused,match='/.*voice'):
        check_coverage(room,listed,candidate=candidate)
    if reference=='missing':
        pages.generate(room,listed,built,candidate=candidate)
        assert check_coverage(room,listed,candidate=candidate)['cards']==2


def test_concurrent_review_commit_refuses_this_check_without_overwriting_it(room,monkeypatch):
    from ams import page_coverage
    listed,_,candidate = prepared(room)
    read = page_coverage.committed_blob
    observed=[]
    def concurrent(root,relative,rev='HEAD'):
        value=read(root,relative,rev)
        if relative.startswith(pages.CARDS+'/') and not observed:
            (room/'README.md').write_text('Synthetic concurrent reviewer work.\n')
            git(room,'add','README.md');git(room,'commit','-qm','Synthetic concurrent review revision')
            observed.append(git(room,'rev-parse','HEAD'))
        return value
    monkeypatch.setattr(page_coverage,'committed_blob',concurrent)
    with pytest.raises(page_coverage.CoverageRefused,match='changed during'):
        page_coverage.check_coverage(room,listed,candidate=candidate)
    assert git(room,'rev-parse','HEAD')==observed[0]
    assert (room/'README.md').read_text()=='Synthetic concurrent reviewer work.\n'


def test_automatic_generation_refuses_changed_layout_after_collection(room,monkeypatch,capsys):
    from ams import page_build
    listed=inventory(room,('/',))
    manifest=json.loads((room/'workbench/manifest.json').read_text())
    manifest['pageReview']['inventory']='site/page-list.json'
    commit_json(room,'workbench/manifest.json',manifest)
    candidate=git(room,'rev-parse','HEAD')
    observed=[]
    class Runtime:
        cleanup_verified=True
        def __init__(self,*args,**kwargs):pass
    def collect(*args,**kwargs):
        manifest=json.loads((room/'workbench/manifest.json').read_text())
        manifest['pageReview']['voice']='grill-board/changed-layout.md'
        commit_json(room,'workbench/manifest.json',manifest)
        observed.append(git(room,'rev-parse','HEAD'))
        return {'candidate':candidate,'inventory':listed,'html':{'/':html()},'kinds':{},'excluded':{}}
    monkeypatch.setattr(page_build,'DockerBuild',Runtime)
    monkeypatch.setattr(page_build,'collect_current',collect)
    with pytest.raises(SystemExit) as error:
        pages.main(['generate','--project',str(room),'--candidate',candidate,'--image','sha256:'+'1'*64])
    assert error.value.code==1 and 'manifest changed' in capsys.readouterr().err
    assert git(room,'rev-parse','HEAD')==observed[0]
    assert not list((room/pages.CARDS).iterdir())


def test_held_unanswered_page_is_not_covered_and_answered_history_remains_valid(room):
    from ams.page_coverage import CoverageRefused, check_coverage
    from ams.grill_board.answers import flag, render_hashes
    from ams.page_feedback import read_voice
    import uuid
    (room / '.gitignore').write_text('.local/\n')
    git(room, 'add', '.gitignore'); git(room, 'commit', '-qm', 'Synthetic ignored private store')
    listed, _, candidate = prepared(room)
    card = next(c for c in load_cards(room / pages.CARDS)[0] if c.fields['Page'] == '/')
    card_sha, _ = render_hashes(room / pages.CARDS, card)
    flag(room / pages.CARDS, card, '', card_sha, event_id=uuid.uuid4().hex,
         voice_sha=read_voice(room).sha)
    held = next(c for c in load_cards(room / pages.CARDS)[0] if c.file == card.file)
    assert held.flag is not None and not held.waiting and held.answer is None
    before = git(room, 'rev-parse', 'HEAD'), git(room, 'status', '--porcelain')
    with pytest.raises(CoverageRefused, match='/.*held for rewrite'):
        check_coverage(room, listed, candidate=candidate)
    assert (git(room, 'rev-parse', 'HEAD'), git(room, 'status', '--porcelain')) == before
    # An answer is coverage even if a later quality flag holds that question.
    target = room / pages.CARDS / card.file
    original = git(room, 'show', before[0] + ':' + pages.CARDS + '/' + card.file)
    target.write_text(original + '\n## Answer\n\n**Verdict:** change\n')
    git(room, 'add', str(target)); git(room, 'commit', '-qm', 'Synthetic answered held history')
    assert check_coverage(room, listed, candidate=candidate)['cards'] == 2


@pytest.mark.parametrize('command', ['generate', 'check'])
def test_automatic_collection_requires_the_committed_inventory_declaration(room, monkeypatch, capsys, command):
    from ams import page_build
    _, _, candidate = source_fixture(room)
    manifest = json.loads((room / 'workbench/manifest.json').read_text())
    del manifest['pageReview']['inventory']
    commit_json(room, 'workbench/manifest.json', manifest)
    def unexpected(*args, **kwargs):
        pytest.fail('undeclared inventory reached the build seam')
    monkeypatch.setattr(page_build, 'DockerBuild', unexpected)
    args = [command, '--project', str(room), '--candidate', candidate, '--image', 'sha256:'+'1'*64]
    if command == 'check': args.append('--recompute')
    with pytest.raises(SystemExit) as error:
        pages.main(args)
    assert error.value.code == 1 and 'declare pageReview.inventory' in capsys.readouterr().err
