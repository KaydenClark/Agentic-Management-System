"""Content-bound page review behavior through disposable Git records."""
import hashlib
import json
import tempfile
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from ams import pages
from ams.grill_board.answers import AnswerRefused, answer, flag, rate, render_hashes
from ams.grill_board.cards import load_cards


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def room(tmp_path):
    root = tmp_path / "room"
    (root / "grill-board/cards").mkdir(parents=True)
    git(root, "init", "-q", "-b", "feature")
    git(root, "config", "user.name", "fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    (root / "README.md").write_text("Synthetic fixture.\n")
    (root / 'workbench').mkdir()
    (root / 'workbench/manifest.json').write_text(json.dumps({'pageReview': {
        'voice': 'grill-board/voice-and-taste.md', 'privateFeedback': '.local/page-feedback'}}) + '\n')
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture")
    return root


def inventory(root, paths=("/", "/skills/grilling")):
    commit = git(root, "rev-parse", "HEAD")
    return {"pages": [{"path": path, "title": "Synthetic " + path, "spec": "S-008" if path.startswith("/skills") else "S-003", "task": "TK-001", "landed": {"branch": "dev", "commit": commit, "pr": 1}, "sources": ["site/app/page.tsx"]} for path in paths]}


def html(text="Hello", footer="abc"):
    return f'<main id="main"><h1>{text}</h1><p data-review-exclude>live 99</p></main><footer>{footer}</footer>'


def test_generate_commits_one_current_card_per_route_and_is_idempotent(room):
    listed = inventory(room)
    built = {p["path"]: html(p["title"]) for p in listed["pages"]}
    before = git(room, "rev-list", "--count", "HEAD")
    result = pages.generate(room, listed, built, candidate=git(room, "rev-parse", "HEAD"))
    assert result["changed"] and result["pages"] == 2
    assert int(git(room, "rev-list", "--count", "HEAD")) == int(before) + 1
    cards, refused = load_cards(room / "grill-board/cards")
    assert not refused and len(cards) == 2
    assert {c.fields["Page"] for c in cards} == {"/", "/skills/grilling"}
    assert all(c.fields["Content hash"] == pages.content_hash(built[c.fields["Page"]]) for c in cards)
    assert not git(room, "status", "--porcelain")
    first = git(room, "rev-parse", "HEAD")
    again = pages.generate(room, listed, built, candidate=result["candidate"])
    assert not again["changed"] and git(room, "rev-parse", "HEAD") == first


def test_changed_content_appends_stale_without_rewriting_answered_history(room):
    listed = inventory(room, ("/",))
    candidate = git(room, "rev-parse", "HEAD")
    pages.generate(room, listed, {"/": html()}, candidate=candidate)
    card = load_cards(room / "grill-board/cards")[0][0]
    card_sha, owner_sha = render_hashes(room / "grill-board/cards", card)
    answer(room / "grill-board/cards", card, "confirm", "", card_sha, owner_sha)
    old_file = room / "grill-board/cards" / card.file
    answered = old_file.read_bytes()
    unchanged = git(room, "rev-parse", "HEAD")
    assert not pages.generate(room, listed, {"/": html(footer="new sha")}, candidate=candidate)["changed"]
    assert git(room, "rev-parse", "HEAD") == unchanged
    pages.generate(room, listed, {"/": html("Correction")}, candidate=candidate)
    assert old_file.read_bytes().startswith(answered)
    assert b"## Stale" in old_file.read_bytes()[len(answered):]
    cards, refused = load_cards(room / "grill-board/cards")
    assert not refused and sum(c.waiting for c in cards) == 1
    stale = next(c for c in cards if c.file == card.file)
    assert stale.stale and not stale.waiting
    sha, owner = render_hashes(room / "grill-board/cards", stale)
    before = git(room, "rev-parse", "HEAD")
    with pytest.raises(AnswerRefused, match="stale"):
        answer(room / "grill-board/cards", stale, "change", "synthetic correction", sha, owner)
    assert git(room, "rev-parse", "HEAD") == before


def test_missing_built_route_or_dirty_owned_file_refuses_without_partial_write(room):
    listed = inventory(room, ("/",))
    before = git(room, "rev-parse", "HEAD")
    with pytest.raises(pages.PageRefused, match="/skills/new"):
        pages.generate(room, listed, {"/": html(), "/skills/new": html()}, candidate=before)
    assert git(room, "rev-parse", "HEAD") == before
    assert list((room / "grill-board/cards").glob("*.md")) == []
    pages.generate(room, listed, {"/": html()}, candidate=before)
    path = room / "grill-board/pages/index.json"
    path.write_text(path.read_text() + " ")
    dirty = path.read_bytes()
    with pytest.raises(pages.PageRefused, match="uncommitted"):
        pages.generate(room, listed, {"/": html("Changed")}, candidate=before)
    assert path.read_bytes() == dirty
    assert len(list((room / "grill-board/cards").glob("*.md"))) == 1


def test_hash_matches_existing_site_contract_vectors():
    vectors = json.loads((Path(__file__).parent / "fixtures/grill_board/pages/vectors.json").read_text())
    for vector in vectors["vectors"]:
        assert pages.canonical_content(vector["html"]) == vector["canonical"]
        assert pages.content_hash(vector["html"]) == vector["hash"]
    with pytest.raises(pages.PageRefused, match="main"):
        pages.content_hash("<p>No main</p>")


def test_removed_page_stales_history_and_readded_content_gets_fresh_occurrence(room):
    listed = inventory(room)
    candidate = git(room, 'rev-parse', 'HEAD')
    built = {row['path']: html(row['title']) for row in listed['pages']}
    pages.generate(room, listed, built, candidate=candidate)
    cards = load_cards(room / 'grill-board/cards')[0]
    removed = next(card for card in cards if card.fields['Page'] == '/skills/grilling')
    before = (room / 'grill-board/cards' / removed.file).read_bytes()
    reduced = {'pages': [listed['pages'][0]]}
    pages.generate(room, reduced, {'/': built['/']}, candidate=candidate)
    history = next(card for card in load_cards(room / 'grill-board/cards')[0] if card.file == removed.file)
    assert history.stale and not history.waiting
    assert history.stale['Removed in'] == candidate
    assert (room / 'grill-board/cards' / removed.file).read_bytes().startswith(before)
    pages.generate(room, listed, built, candidate=candidate)
    current = [card for card in load_cards(room / 'grill-board/cards')[0] if card.fields['Page'] == '/skills/grilling' and card.waiting]
    assert len(current) == 1 and current[0].file != removed.file


def test_verified_containment_is_never_labeled_as_original_landing(room):
    listed = inventory(room, ('/',))
    listed['pages'][0]['provenance_kind'] = 'verified-containment'
    candidate = git(room, 'rev-parse', 'HEAD')
    pages.generate(room, listed, {'/': html()}, candidate=candidate)
    card = load_cards(room / 'grill-board/cards')[0][0]
    assert card.fields['Provenance kind'] == 'verified-containment'
    assert 'Verified containment' in card.fields
    assert 'Landed' not in card.fields
    index = json.loads((room / 'grill-board/pages/index.json').read_text())
    assert index['pages']['/']['provenance_kind'] == 'verified-containment'


def test_automatic_cli_collects_frozen_candidate_before_any_board_write(room, monkeypatch, capsys):
    import ams.page_build as build
    candidate = git(room, 'rev-parse', 'HEAD')
    listed = inventory(room, ('/',))
    image = 'sha256:' + '1' * 64
    observed = []
    class Runtime:
        cleanup_verified = True
        def __init__(self, selected, *, timeout):
            assert selected == image and timeout == 300
    def collect(source, ref, expected, **options):
        assert git(room, 'rev-parse', 'HEAD') == candidate
        assert options['public_config'] is None
        observed.append((source, ref, expected))
        return {'candidate': candidate, 'inventory': listed, 'html': {'/': html()}, 'kinds': {'/': 'page'}, 'excluded': {}}
    monkeypatch.setattr(build, 'DockerBuild', Runtime)
    monkeypatch.setattr(build, 'collect_current', collect)
    pages.main(['generate','--project',str(room),'--ref','dev','--candidate',candidate,'--image',image])
    assert observed == [(room, 'dev', candidate)]
    result = json.loads(capsys.readouterr().out)
    assert result['input_mode'] == 'pinned-container-build' and result['cleanup_verified']
    assert len(load_cards(room / 'grill-board/cards')[0]) == 1


def test_automatic_cli_refusal_and_unverified_cleanup_never_write_cards(room, monkeypatch):
    import ams.page_build as build
    candidate = git(room, 'rev-parse', 'HEAD')
    image = 'sha256:' + '1' * 64
    class Runtime:
        cleanup_verified = False
        def __init__(self, *args, **kwargs): pass
    monkeypatch.setattr(build, 'DockerBuild', Runtime)
    def missing(*args, **kwargs):
        raise pages.PageRefused('/skills/new has no page-list owner')
    monkeypatch.setattr(build, 'collect_current', missing)
    command = ['generate','--project',str(room),'--candidate',candidate,'--image',image]
    with pytest.raises(SystemExit) as refused:
        pages.main(command)
    assert refused.value.code == 1 and git(room, 'rev-parse', 'HEAD') == candidate
    monkeypatch.setattr(build, 'collect_current', lambda *args, **kwargs: {'candidate': candidate, 'inventory': inventory(room, ('/',)), 'html': {'/': html()}, 'kinds': {'/': 'page'}, 'excluded': {}})
    with pytest.raises(SystemExit) as cleanup:
        pages.main(command)
    assert cleanup.value.code == 1 and git(room, 'rev-parse', 'HEAD') == candidate
    assert not list((room / 'grill-board/cards').glob('*.md'))


def test_pending_candidate_keeps_landing_unknown_and_binds_actual_candidate(room):
    listed = inventory(room, ('/new-page',))
    listed['pages'][0].update(provenance_kind='pending-candidate', landed=None)
    candidate = git(room, 'rev-parse', 'HEAD')
    pages.generate(room, listed, {'/new-page': html('New synthetic page')}, candidate=candidate)
    card = load_cards(room / 'grill-board/cards')[0][0]
    assert card.fields['Provenance kind'] == 'pending-candidate'
    assert card.fields['Candidate'] == candidate and card.fields['Integration'] == 'pending'
    assert 'Landed' not in card.fields and 'Verified containment' not in card.fields
    index = json.loads((room / 'grill-board/pages/index.json').read_text())['pages']['/new-page']
    assert index['landed'] is None and index['candidate'] == candidate and index['integration'] == 'pending'
    bad = inventory(room, ('/second-page',))
    bad['pages'][0].update(provenance_kind='pending-candidate', spec='')
    with pytest.raises(pages.PageRefused, match='invalid spec'):
        pages.generate(room, bad, {'/second-page': html()}, candidate=candidate)


@pytest.mark.parametrize('sources', [None, [], 'site/app/page.tsx', [''], [17], ['source\n**Owner record:** unsafe'], ['../outside'], ['/outside']])
def test_missing_or_unsafe_sources_refuse_before_any_write(room, sources):
    listed = inventory(room, ('/',))
    if sources is None:
        listed['pages'][0].pop('sources')
    else:
        listed['pages'][0]['sources'] = sources
    before = git(room, 'rev-parse', 'HEAD')
    with pytest.raises(pages.PageRefused, match='sources'):
        pages.generate(room, listed, {'/': html()}, candidate=before)
    assert git(room, 'rev-parse', 'HEAD') == before
    assert not git(room, 'status', '--porcelain')
    assert not list((room / 'grill-board/cards').glob('*.md'))


def test_equal_content_refreshes_changed_owners_and_provenance_without_rewriting_history(room):
    listed = inventory(room, ('/new',))
    row = listed['pages'][0]
    row.update(provenance_kind='pending-candidate', landed=None)
    candidate = git(room, 'rev-parse', 'HEAD')
    pages.generate(room, listed, {'/new': html()}, candidate=candidate)
    first = load_cards(room / 'grill-board/cards')[0][0]
    card_sha, owner_sha = render_hashes(room / 'grill-board/cards', first)
    answer(room / 'grill-board/cards', first, 'confirm', '', card_sha, owner_sha)
    original = (room / 'grill-board/cards' / first.file).read_bytes()
    current = git(room, 'rev-parse', 'HEAD')
    row.update(title='Current synthetic title', spec='S-008', task='TK-002',
               sources=['site/app/new/page.tsx'], provenance_kind='verified-containment',
               landed={'branch': 'dev', 'commit': current, 'pr': 2})
    result = pages.generate(room, listed, {'/new': html()}, candidate=current)
    assert result['changed']
    cards, refused = load_cards(room / 'grill-board/cards')
    assert not refused
    replacement = next(card for card in cards if card.waiting)
    assert replacement.file != first.file
    assert replacement.fields['Content hash'] == first.fields['Content hash']
    assert replacement.fields['Candidate'] == current
    assert replacement.fields['Title'] == row['title']
    assert replacement.fields['Spec'] == row['spec'] and replacement.fields['Task'] == row['task']
    assert replacement.fields['Provenance kind'] == 'verified-containment'
    assert 'Integration' not in replacement.fields and 'Landed' not in replacement.fields
    assert row['sources'][0] in (room / 'grill-board/cards' / replacement.file).read_text()
    assert (room / 'grill-board/cards' / first.file).read_bytes().startswith(original)
    assert next(card for card in cards if card.file == first.file).stale
    index = json.loads((room / 'grill-board/pages/index.json').read_text())
    assert index['pages']['/new']['card'] == replacement.file
    assert not pages.generate(room, listed, {'/new': html()}, candidate=current)['changed']


def test_unchanged_content_and_owners_keep_the_original_card_when_the_build_pin_moves(room):
    listed = inventory(room, ('/',))
    listed['pages'][0]['sources'] = ['site/app/Synthetic page.tsx']
    candidate = git(room, 'rev-parse', 'HEAD')
    pages.generate(room, listed, {'/': html()}, candidate=candidate)
    card = load_cards(room / 'grill-board/cards')[0][0]
    original = (room / 'grill-board/cards' / card.file).read_bytes()
    current = git(room, 'rev-parse', 'HEAD')
    pages.generate(room, listed, {'/': html(footer='new build pin')}, candidate=current)
    cards, refused = load_cards(room / 'grill-board/cards')
    assert not refused and len(cards) == 1 and cards[0].file == card.file
    assert (room / 'grill-board/cards' / card.file).read_bytes() == original
    index = json.loads((room / 'grill-board/pages/index.json').read_text())
    assert index['candidate'] == current and cards[0].fields['Candidate'] == candidate


@pytest.mark.parametrize('operation', ['confirm', 'change', 'rework-wording', 'change-the-why', 'rate', 'flag'])
def test_page_feedback_notes_never_enter_committed_public_records(room, operation):
    listed = inventory(room, ('/',))
    pages.generate(room, listed, {'/': html()}, candidate=git(room, 'rev-parse', 'HEAD'))
    card = load_cards(room / 'grill-board/cards')[0][0]
    card_sha, owner_sha = render_hashes(room / 'grill-board/cards', card)
    before = git(room, 'rev-parse', 'HEAD')
    original = {p: p.read_bytes() for p in (room / 'grill-board').rglob('*') if p.is_file()}
    note = 'Synthetic private feedback must remain outside public Git.'
    with pytest.raises(AnswerRefused, match='privat'):
        if operation == 'rate':
            rate(room / 'grill-board/cards', card, '4', note, card_sha)
        elif operation == 'flag':
            flag(room / 'grill-board/cards', card, note, card_sha)
        else:
            answer(room / 'grill-board/cards', card, operation, note, card_sha, owner_sha)
    assert git(room, 'rev-parse', 'HEAD') == before
    assert not git(room, 'status', '--porcelain')
    assert all(path.read_bytes() == data for path, data in original.items())


@pytest.mark.parametrize('field', ['title', 'spec', 'task', 'sources', 'branch', 'pr'])
@pytest.mark.parametrize('separator', ['\x85', '\u2028', '\u2029'])
def test_metadata_cannot_inject_card_fields_through_unicode_lines(room, field, separator):
    listed = inventory(room, ('/',))
    row = listed['pages'][0]
    injected = 'Synthetic' + separator + '**Page:**'
    if field == 'sources':
        row[field] = [injected]
    elif field in {'branch', 'pr'}:
        row['landed'][field] = injected
    else:
        row[field] = injected
    before = git(room, 'rev-parse', 'HEAD')
    with pytest.raises(pages.PageRefused):
        pages.generate(room, listed, {'/': html()}, candidate=before)
    assert git(room, 'rev-parse', 'HEAD') == before
    assert not git(room, 'status', '--porcelain')


def test_page_note_guard_does_not_depend_on_a_nonempty_page_field(room):
    listed = inventory(room, ('/',))
    pages.generate(room, listed, {'/': html()}, candidate=git(room, 'rev-parse', 'HEAD'))
    card = load_cards(room / 'grill-board/cards')[0][0]
    path = room / 'grill-board/cards' / card.file
    path.write_text(path.read_text().replace('**Page:** /', '**Page:**'))
    git(room, 'add', str(path)); git(room, 'commit', '-qm', 'synthetic damaged page marker')
    damaged = load_cards(room / 'grill-board/cards')[0][0]
    card_sha, owner_sha = render_hashes(room / 'grill-board/cards', damaged)
    before = git(room, 'rev-parse', 'HEAD')
    with pytest.raises(AnswerRefused, match='privat'):
        answer(room / 'grill-board/cards', damaged, 'change', 'Synthetic private canary.', card_sha, owner_sha)
    assert git(room, 'rev-parse', 'HEAD') == before
    assert not git(room, 'status', '--porcelain')


@pytest.mark.parametrize('kind', ['historical-landing', 'verified-containment'])
def test_provenance_never_invents_a_branch(room, kind):
    listed = inventory(room, ('/',))
    row = listed['pages'][0]
    row['provenance_kind'] = kind
    row['landed'].pop('branch')
    before = git(room, 'rev-parse', 'HEAD')
    with pytest.raises(pages.PageRefused, match='branch'):
        pages.generate(room, listed, {'/': html()}, candidate=before)
    assert git(room, 'rev-parse', 'HEAD') == before
    assert not git(room, 'status', '--porcelain')


def test_built_card_does_not_claim_unverified_protected_deployment(room):
    candidate = git(room, 'rev-parse', 'HEAD')
    pages.generate(room, inventory(room, ('/',)), {'/': html()}, candidate=candidate)
    card = load_cards(room / 'grill-board/cards')[0][0]
    assert f'built candidate {candidate}' in card.context
    assert 'Protected-deployment verification is pending' in card.context
    assert 'protected dev candidate' not in card.context


def protected_evidence(candidate):
    return {'repository': 'https://github.com/KaydenClark/Agentic-Management-System.git',
            'project': 'prj_Synthetic', 'deployment': 'dpl_Synthetic', 'candidate': candidate,
            'origin': 'https://synthetic-immutable.vercel.app', 'capture_sha256': 'b' * 64,
            'observed_at': '2026-11-06T09:00:00+00:00'}


def validated_capture(room, listed, candidate, *, observed_at='2026-11-06T09:00:00+00:00'):
    """Synthetic outer-observer artifact, not live deployment evidence."""
    from ams.protected_pages import collect_protected
    artifact = Path(tempfile.mkdtemp(prefix='synthetic-capture-', dir=room.parent))
    (artifact / 'pages').mkdir()
    proof = protected_evidence(candidate)
    pins = {key: value for key, value in proof.items() if key not in {'capture_sha256', 'observed_at'}}
    manifest = {**pins, 'schema': 1, 'observer': 'authenticated-vercel-web-fetch',
                'observed_at': observed_at, 'pages': {}}
    baseline = {row['path']: html() for row in listed['pages']}
    for i, (route, page) in enumerate(baseline.items()):
        observed = (page + f'<footer><span data-commit-sha="{candidate}"></span></footer>'
                    f'<script src="/_next/static/synthetic.js?dpl={proof["deployment"]}"></script>')
        relative = f'pages/{i}.html'
        (artifact / relative).write_bytes(observed.encode())
        manifest['pages'][route] = {'file': relative, 'sha256': hashlib.sha256(observed.encode()).hexdigest(),
                                    'url': pins['origin'] + route, 'status': 200, 'content_type': 'text/html'}
    raw = (json.dumps(manifest, sort_keys=True) + '\n').encode()
    (artifact / 'manifest.json').write_bytes(raw)
    built = {'candidate': candidate, 'inventory': listed, 'html': baseline,
             'kinds': {route: 'page' for route in baseline}, 'excluded': {}}
    return collect_protected(artifact, built, expected_pins={**pins, 'capture_sha256': hashlib.sha256(raw).hexdigest()})


def test_evidence_dictionary_alone_cannot_assert_protected_verification(room):
    candidate = git(room, 'rev-parse', 'HEAD')
    with pytest.raises(pages.PageRefused, match='validated|capture'):
        pages.generate(room, inventory(room, ('/',)), {'/': html()}, candidate=candidate,
                       protection=protected_evidence(candidate))
    assert git(room, 'rev-parse', 'HEAD') == candidate
    assert not list((room / 'grill-board/cards').glob('*.md'))


@pytest.mark.parametrize('legacy', [False, True])
@pytest.mark.parametrize('source', ['site/app/page.tsx', 'site/Synthetic, page.tsx', 'site/Sources: page.tsx'])
def test_proof_upgrade_does_not_reask_already_approved_identical_content(room, legacy, source):
    candidate = git(room, 'rev-parse', 'HEAD')
    listed = inventory(room, ('/',))
    listed['pages'][0]['sources'] = [source]
    pages.generate(room, listed, {'/': html()}, candidate=candidate)
    card = load_cards(room / 'grill-board/cards')[0][0]
    if legacy:
        path = room / 'grill-board/cards' / card.file
        path.write_text(''.join(line for line in path.read_text().splitlines(keepends=True)
                                if not line.startswith(('**Verification:**', '**Sources:**'))))
        git(room, 'add', '.'); git(room, 'commit', '-qm', 'synthetic legacy template')
        card = load_cards(room / 'grill-board/cards')[0][0]
    card_sha, owner_sha = render_hashes(room / 'grill-board/cards', card)
    answer(room / 'grill-board/cards', card, 'confirm', '', card_sha, owner_sha)
    answered = (room / 'grill-board/cards' / card.file).read_bytes()
    captured = validated_capture(room, listed, candidate)
    pages.generate(room, listed, captured['html'], candidate=candidate, protection=captured['verified_capture'])
    cards, refused = load_cards(room / 'grill-board/cards')
    assert not refused and len(cards) == 1 and cards[0].file == card.file
    assert cards[0].answer and not cards[0].stale and not cards[0].waiting
    assert (room / 'grill-board/cards' / card.file).read_bytes().startswith(answered)

    assert cards[0].verification['State'] == 'protected-capture'
    from ams.grill_board.server import render_open
    assert 'This content was verified on the protected deployment' in render_open(room / 'grill-board/cards', 'Website pages', cards, cards[0])

def test_protected_generation_binds_evidence_without_reasking_unchanged_content(room):
    candidate = git(room, 'rev-parse', 'HEAD')
    listed = inventory(room, ('/',))
    captured = validated_capture(room, listed, candidate)
    first = pages.generate(room, listed, captured['html'], candidate=candidate, protection=captured['verified_capture'])
    card = load_cards(room / 'grill-board/cards')[0][0]
    assert first['protected_verified']
    assert card.fields['Verification'] == 'protected-capture'
    assert 'Protected deployment content verified' in card.context
    assert 'verification is pending' not in card.context
    assert not pages.generate(room, listed, captured['html'], candidate=candidate, protection=captured['verified_capture'])['changed']
    later = validated_capture(room, listed, candidate, observed_at='2026-11-06T10:00:00+00:00')
    original = (room / 'grill-board/cards' / card.file).read_bytes()
    pages.generate(room, listed, later['html'], candidate=candidate, protection=later['verified_capture'])
    assert len(load_cards(room / 'grill-board/cards')[0]) == 1
    assert (room / 'grill-board/cards' / card.file).read_bytes() == original
    index = json.loads((room / 'grill-board/pages/index.json').read_text())
    assert index['protection'] == later['protection']


def test_ordinary_build_retains_historical_proof_without_claiming_current_snapshot_verification(room):
    candidate = git(room, 'rev-parse', 'HEAD')
    listed = inventory(room, ('/',))
    captured = validated_capture(room, listed, candidate)
    pages.generate(room, listed, captured['html'], candidate=candidate, protection=captured['verified_capture'])
    before = load_cards(room / 'grill-board/cards')[0][0]
    original = (room / 'grill-board/cards' / before.file).read_bytes()
    result = pages.generate(room, listed, {'/': html()}, candidate=candidate)
    cards, refused = load_cards(room / 'grill-board/cards')
    assert not refused and len(cards) == 1 and cards[0].file == before.file
    assert not result['protected_verified']
    assert (room / 'grill-board/cards' / before.file).read_bytes() == original
    assert cards[0].verification['Capture SHA256'] == captured['protection']['capture_sha256']
    assert 'current snapshot evidence' not in cards[0].context
    assert json.loads((room / 'grill-board/pages/index.json').read_text())['protection'] is None


@pytest.mark.parametrize('mutation', ['html', 'inventory', 'candidate'])
def test_validated_capture_cannot_be_reused_after_snapshot_mutation(room, mutation):
    candidate = git(room, 'rev-parse', 'HEAD')
    listed = inventory(room, ('/',))
    captured = validated_capture(room, listed, candidate)
    if mutation == 'html': captured['html']['/'] += '<footer>Synthetic alteration outside canonical content</footer>'
    elif mutation == 'inventory': listed['pages'][0]['title'] = 'Synthetic changed owner title'
    else: candidate = 'c' * 40
    with pytest.raises(pages.PageRefused, match='validated capture differs'):
        pages.generate(room, listed, captured['html'], candidate=candidate, protection=captured['verified_capture'])
    assert not list((room / 'grill-board/cards').glob('*.md'))


@pytest.mark.parametrize('refuse', [False, True])
def test_cli_checks_protected_capture_after_clean_build_before_any_board_write(room, monkeypatch, capsys, refuse):
    import ams.page_build as build
    import ams.protected_pages as protected
    candidate = git(room, 'rev-parse', 'HEAD')
    listed = inventory(room, ('/',))
    captured = validated_capture(room, listed, candidate)
    proof = captured['protection']
    class Runtime:
        cleanup_verified = True
        def __init__(self, *args, **kwargs): pass
    monkeypatch.setattr(build, 'DockerBuild', Runtime)
    built = {'candidate': candidate, 'inventory': listed, 'html': {'/': html()},
             'kinds': {'/': 'page'}, 'excluded': {}}
    monkeypatch.setattr(build, 'collect_current', lambda *a, **k: built)
    observed = []
    def capture(directory, snapshot, *, expected_pins):
        assert snapshot is built and git(room, 'rev-parse', 'HEAD') == candidate
        assert directory == room / 'private-capture'
        assert expected_pins == {key: value for key, value in proof.items() if key != 'observed_at'}
        observed.append(True)
        if refuse: raise pages.PageRefused('synthetic protected identity refusal')
        return captured
    monkeypatch.setattr(protected, 'collect_protected', capture)
    command = ['generate', '--project', str(room), '--candidate', candidate, '--image', 'sha256:' + '1' * 64,
               '--protected-artifact', str(room / 'private-capture'), '--protected-project', proof['project'],
               '--protected-deployment', proof['deployment'], '--protected-origin', proof['origin'],
               '--protected-capture-sha256', proof['capture_sha256']]
    if refuse:
        with pytest.raises(SystemExit) as error: pages.main(command)
        assert error.value.code == 1 and git(room, 'rev-parse', 'HEAD') == candidate
        assert not list((room / 'grill-board/cards').glob('*.md'))
    else:
        pages.main(command)
        result = json.loads(capsys.readouterr().out)
        assert result['input_mode'] == 'protected-capture' and result['protected_verified']
        assert result['protection'] == proof
    assert observed == [True]


def test_protected_cli_requires_independent_pins_before_execution(room):
    candidate = git(room, 'rev-parse', 'HEAD')
    with pytest.raises(SystemExit) as error:
        pages.main(['generate', '--project', str(room), '--candidate', candidate,
                    '--image', 'sha256:' + '1' * 64, '--protected-artifact', str(room / 'capture')])
    assert error.value.code == 2 and git(room, 'rev-parse', 'HEAD') == candidate
