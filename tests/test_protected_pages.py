"""Synthetic authenticated-observer artifacts, never live deployment proof."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

from ams.pages import PageRefused, content_hash


CANDIDATE = 'a' * 40
DEPLOYMENT = 'dpl_SyntheticPinned'
ORIGIN = 'https://synthetic-immutable.vercel.app'
REPOSITORY = 'https://github.com/KaydenClark/Agentic-Management-System.git'


def document(content, *, candidate=CANDIDATE, deployment=DEPLOYMENT):
    return (f'<main id="main">{content}</main><footer><span data-commit-sha="{candidate}">{candidate[:7]}</span></footer>'
            f'<script src="/_next/static/synthetic.js?dpl={deployment}"></script>')


@pytest.fixture
def capture(tmp_path):
    artifact = tmp_path / 'capture'
    (artifact / 'pages').mkdir(parents=True)
    baseline = {'/': document('Synthetic home'), '/rsi': document('Synthetic results unavailable'),
                '/_not-found': document('Synthetic visitor404')}
    current = {**baseline, '/rsi': document('<p data-result="">Synthetic results3/3</p><p data-review-exclude>read10:00</p>')}
    kinds = {route: 'visitor-404' if route == '/_not-found' else 'page' for route in baseline}
    manifest = {'schema': 1, 'observer': 'authenticated-vercel-web-fetch', 'repository': REPOSITORY,
                'project': 'prj_Synthetic', 'deployment': DEPLOYMENT, 'candidate': CANDIDATE,
                'origin': ORIGIN, 'observed_at': '2026-11-06T09:00:00+00:00', 'pages': {}}
    for i, (route, html) in enumerate(current.items()):
        relative = f'pages/{i}.html'
        (artifact / relative).write_bytes(html.encode())
        request = '/__ams_review_missing__' if route == '/_not-found' else route
        manifest['pages'][route] = {'file': relative, 'sha256': hashlib.sha256(html.encode()).hexdigest(),
                                    'url': ORIGIN + request, 'status': 404 if route == '/_not-found' else 200,
                                    'content_type': 'text/html; charset=utf-8'}
    listed = {'pages': [{'path': route, 'title': 'Synthetic ' + route, 'spec': 'S-003', 'task': 'TK-001',
                        'sources': ['site/app/page.tsx'], 'landed': {'branch': 'dev', 'commit': CANDIDATE, 'pr': 1}}
                       for route in baseline]}
    built = {'candidate': CANDIDATE, 'inventory': listed, 'html': baseline, 'kinds': kinds,
             'excluded': {'_global-error.html': 'internal framework fallback'}}
    pins = {key: manifest[key] for key in ('repository', 'project', 'deployment', 'candidate', 'origin')}
    return artifact, manifest, built, pins


def seal(artifact, manifest, pins):
    """The synthetic trusted observer emits an independent expected digest."""
    raw = (json.dumps(manifest, sort_keys=True) + '\n').encode()
    (artifact / 'manifest.json').write_bytes(raw)
    return {**pins, 'capture_sha256': hashlib.sha256(raw).hexdigest()}


def rewrite(artifact, manifest, route, html):
    row = manifest['pages'][route]
    (artifact / row['file']).write_bytes(html.encode())
    row['sha256'] = hashlib.sha256(html.encode()).hexdigest()


def test_protected_capture_uses_exact_authenticated_results_and_full_routes(capture):
    from ams.protected_pages import collect_protected
    artifact, manifest, built, pins = capture
    expected = seal(artifact, manifest, pins)
    before = copy.deepcopy(built)
    result = collect_protected(artifact, built, expected_pins=expected)
    assert set(result['html']) == set(built['html'])
    assert result['html']['/rsi'] != built['html']['/rsi']
    assert 'results3/3' in result['html']['/rsi']
    assert result['protection']['capture_sha256'] == expected['capture_sha256']
    assert result['protection']['deployment'] == DEPLOYMENT
    assert result['kinds']['/_not-found'] == 'visitor-404'
    assert built == before


def test_adapter_document_deployment_marker_verifies_without_asset_queries(capture):
    from ams.protected_pages import collect_protected
    artifact, manifest, built, pins = capture
    for route, row in manifest['pages'].items():
        page = (artifact / row['file']).read_text().replace('?dpl=' + DEPLOYMENT, '')
        rewrite(artifact, manifest, route, f'<html data-dpl-id="{DEPLOYMENT}">{page}</html>')
    result = collect_protected(artifact, built, expected_pins=seal(artifact, manifest, pins))
    assert all(f'data-dpl-id="{DEPLOYMENT}"' in page for page in result['html'].values())


@pytest.mark.parametrize('defect', ['wrong-document', 'conflicting-asset', 'missing-both'])
def test_document_identity_cannot_hide_missing_or_conflicting_deployment(capture, defect):
    from ams.protected_pages import collect_protected
    artifact, manifest, built, pins = capture
    page = (artifact / manifest['pages']['/rsi']['file']).read_text()
    if defect == 'wrong-document':
        page = f'<html data-dpl-id="dpl_Other">{page}</html>'
    elif defect == 'conflicting-asset':
        page = f'<html data-dpl-id="{DEPLOYMENT}">{page.replace(DEPLOYMENT, "dpl_Other")}</html>'
    else:
        page = '<html>' + page.replace('?dpl=' + DEPLOYMENT, '') + '</html>'
    rewrite(artifact, manifest, '/rsi', page)
    with pytest.raises(PageRefused, match='identity'):
        collect_protected(artifact, built, expected_pins=seal(artifact, manifest, pins))


@pytest.mark.parametrize('field,value', [('candidate', 'b' * 40), ('project', 'prj_Other'),
                                        ('deployment', 'dpl_Other'), ('origin', 'https://different.vercel.app')])
def test_independent_identity_pins_refuse_mixed_or_old_captures(capture, field, value):
    from ams.protected_pages import collect_protected
    artifact, manifest, built, pins = capture
    expected = seal(artifact, manifest, pins)
    with pytest.raises(PageRefused, match='pin|candidate'):
        collect_protected(artifact, built, expected_pins={**expected, field: value})


def test_manifest_and_body_tampering_refuse(capture):
    from ams.protected_pages import collect_protected
    artifact, manifest, built, pins = capture
    expected = seal(artifact, manifest, pins)
    (artifact / manifest['pages']['/rsi']['file']).write_text(document('Synthetic altered result'))
    with pytest.raises(PageRefused, match='digest'):
        collect_protected(artifact, built, expected_pins=expected)
    rewrite(artifact, manifest, '/rsi', document('Synthetic altered result'))
    seal(artifact, manifest, pins)
    with pytest.raises(PageRefused, match='capture.*digest'):
        collect_protected(artifact, built, expected_pins=expected)


@pytest.mark.parametrize('defect', ['missing', 'extra', 'redirect', 'status', 'type', 'duplicate-file'])
def test_route_status_origin_and_media_type_must_match_the_complete_build(capture, defect):
    from ams.protected_pages import collect_protected
    artifact, manifest, built, pins = capture
    if defect == 'missing': manifest['pages'].pop('/rsi')
    elif defect == 'extra': manifest['pages']['/extra'] = dict(manifest['pages']['/'])
    elif defect == 'redirect': manifest['pages']['/rsi']['url'] = 'https://login.example.invalid/rsi'
    elif defect == 'status': manifest['pages']['/_not-found']['status'] = 200
    elif defect == 'type': manifest['pages']['/rsi']['content_type'] = 'text/plain'
    else: manifest['pages']['/rsi']['file'] = manifest['pages']['/']['file']
    with pytest.raises(PageRefused):
        collect_protected(artifact, built, expected_pins=seal(artifact, manifest, pins))


@pytest.mark.parametrize('html', ['<main id="main">Synthetic login</main>',
                                 document('Synthetic stale source', candidate='b' * 40),
                                 document('Synthetic mixed deployment', deployment='dpl_Other')])
def test_login_wrong_source_and_mixed_deployment_markers_refuse(capture, html):
    from ams.protected_pages import collect_protected
    artifact, manifest, built, pins = capture
    rewrite(artifact, manifest, '/rsi', html)
    with pytest.raises(PageRefused, match='identity'):
        collect_protected(artifact, built, expected_pins=seal(artifact, manifest, pins))


def test_only_the_explicit_rsi_data_surface_may_differ_from_the_pinned_build(capture):
    from ams.protected_pages import collect_protected
    artifact, manifest, built, pins = capture
    rewrite(artifact, manifest, '/', document('Synthetic unexpected different static home'))
    with pytest.raises(PageRefused, match='static.*differs'):
        collect_protected(artifact, built, expected_pins=seal(artifact, manifest, pins))


@pytest.mark.parametrize('defect', ['symlink', 'traversal', 'hardlink'])
def test_artifacts_cannot_read_linked_or_outside_files(capture, tmp_path, defect):
    from ams.protected_pages import collect_protected
    artifact, manifest, built, pins = capture
    target = artifact / manifest['pages']['/rsi']['file']
    outside = tmp_path / 'outside.html'
    outside.write_bytes(target.read_bytes())
    if defect == 'traversal': manifest['pages']['/rsi']['file'] = '../outside.html'
    else:
        target.unlink()
        if defect == 'symlink': target.symlink_to(outside)
        else: target.hardlink_to(outside)
    with pytest.raises(PageRefused, match='regular|relative|symlink'):
        collect_protected(artifact, built, expected_pins=seal(artifact, manifest, pins))


def test_result_and_availability_changes_remain_hash_bound_but_freshness_does_not(capture):
    from ams.protected_pages import collect_protected
    artifact, manifest, built, pins = capture
    first = collect_protected(artifact, built, expected_pins=seal(artifact, manifest, pins))
    digest = content_hash(first['html']['/rsi'])
    rewrite(artifact, manifest, '/rsi', first['html']['/rsi'].replace('read10:00', 'read11:00'))
    later = collect_protected(artifact, built, expected_pins=seal(artifact, manifest, pins))
    assert content_hash(later['html']['/rsi']) == digest
    for text in ['Synthetic results1/3', 'Synthetic results empty', 'Synthetic results unavailable']:
        rewrite(artifact, manifest, '/rsi', document(text))
        changed = collect_protected(artifact, built, expected_pins=seal(artifact, manifest, pins))
        assert content_hash(changed['html']['/rsi']) != digest
