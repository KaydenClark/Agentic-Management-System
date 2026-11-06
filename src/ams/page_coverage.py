"""Read-only coverage of committed review cards for one pinned site inventory."""
from collections import Counter
import json
from pathlib import Path

from .grill_board.answers import AnswerRefused, _git, committed_blob
from .grill_board.cards import Card, parse_card
from .page_approvals import APPROVALS, CARDS, HASH, committed_ref, read_page_index
from .page_feedback import card_voice_version, read_voice
from .pages import PageRefused, _metadata, _same_owners, content_hash
from .project_paths import feedback_paths


class CoverageRefused(Exception):
    """The pinned inventory is not completely covered by current committed cards."""


def check_coverage(root, listed, *, candidate, built=None, review_commit=None):
    root = Path(root).resolve()
    try:
        # Reuse the generator's metadata contract, including pending/null origin.
        declared = {row.get('path'): None for row in listed.get('pages', [])}
        rows = _metadata(listed, built if built is not None else declared)
        review = committed_ref(root, review_commit or 'HEAD')
        index = read_page_index(root, review)
        voice = read_voice(root, review)
        voice_path = voice.path
        failures = []
        if index['candidate'] != candidate:
            failures.append('review index candidate differs from the frozen source; regenerate current coverage')
        named = {entry['card'] for entry in index['pages'].values()}
        cards = {}
        files = _git(root, 'ls-tree', '-r', '--name-only', '-z', review, '--', CARDS + '/').split('\0')
        for relative in files:
            name = relative.removeprefix(CARDS + '/')
            if not name.endswith('.md') or '/' in name:
                continue
            blob = committed_blob(root, relative, review)
            try:
                card = parse_card(name, blob.decode('utf-8')) if blob is not None else None
            except UnicodeDecodeError:
                card = None
            if not isinstance(card, Card):
                if name in named or name.startswith('page-'):
                    failures.append(f'{name}: committed page card is missing, unsafe or malformed')
                continue
            if card.fields.get('Page') or card.fields.get('Owner record') == APPROVALS or name in named:
                cards[name] = card
        for path in sorted(set(index['pages']) - set(rows)):
            failures.append(f'{path}: index entry has no page in the frozen source inventory')
        matched = 0
        for path, row in rows.items():
            entry = index['pages'].get(path)
            if entry is None:
                failures.append(f'{path}: listed page has no index entry')
                continue
            expected_origin = row['landed']['commit'] if row.get('landed') else None
            kind = row.get('provenance_kind', 'historical-landing')
            if entry.get('landed') != expected_origin or entry.get('provenance_kind') != kind:
                failures.append(f'{path}: provenance changed; its hash must be recomputed')
            if kind == 'pending-candidate' and (entry.get('candidate') != candidate or entry.get('integration') != 'pending'):
                failures.append(f'{path}: pending provenance differs from the frozen candidate')
            card = cards.get(entry['card'])
            if (card is None or card.stale is not None or card.fields.get('Page') != path
                    or card.fields.get('Content hash') != entry['hash']
                    or not _same_owners(card, row, entry['hash'], candidate, voice_path)):
                failures.append(f'{path}: no current committed card matches its index hash')
            else:
                matched += 1
                if card.waiting:
                    try:
                        version = card_voice_version(card, voice_path)
                        if version is None or version > voice.version:
                            failures.append(f'{path}: open page card has no available voice version')
                    except AnswerRefused:
                        failures.append(f'{path}: open page card has an invalid voice reference')
            if built is not None and content_hash(built[path]) != entry['hash']:
                failures.append(f'{path}: served content hash differs from the review index')
        open_pages = Counter()
        for card in cards.values():
            path = card.fields.get('Page', '')
            if card.stale is not None:
                continue
            entry = index['pages'].get(path)
            digest = card.fields.get('Content hash', '')
            if entry is None or not HASH.fullmatch(digest) or digest != entry['hash']:
                failures.append(f'{path or card.file}: card hash is not current and has no Stale section')
            if card.answer is None:
                open_pages[path] += 1
        for path, count in sorted(open_pages.items()):
            if count > 1:
                failures.append(f'{path}: {count} page cards are neither stale nor answered')
        if committed_ref(root) != review:
            raise CoverageRefused('review records changed during coverage check; rerun against the new committed state')
        if failures:
            raise CoverageRefused('\n'.join(failures))
        return {'pages': len(rows), 'cards': matched, 'candidate': candidate,
                'review_commit': review, 'recomputed': built is not None}
    except (AnswerRefused, PageRefused, AttributeError, KeyError, TypeError) as error:
        raise CoverageRefused(f'invalid committed coverage input: {error}') from None


def run_check(args, parser):
    """Read the frozen source inventory, or explicitly labeled fixture inputs."""
    from .page_build import AMS_ORIGIN, _pin
    from .pages import _collect_for_review
    review = committed_ref(args.project)
    if args.inventory:
        if (not args.candidate or any((args.source_repo, args.ref, args.image, args.public_config,
                                       args.protected_artifact))):
            parser.error('injected check requires --inventory and --candidate without automatic build options')
        if args.recompute != bool(args.built_html):
            parser.error('injected --recompute requires --built-html; supplied HTML requires --recompute')
        listed = json.loads(args.inventory.read_text())
        built = json.loads(args.built_html.read_text()) if args.recompute else None
        result = check_coverage(args.project, listed, candidate=args.candidate, built=built, review_commit=review)
        result['input_mode'] = 'injected-artifact'
        return result
    if args.built_html:
        parser.error('--built-html requires explicit --inventory fixture inputs')
    if not args.recompute and any((args.image, args.public_config, args.protected_artifact)):
        parser.error('build/capture options require check --recompute')
    if args.recompute and not args.image:
        parser.error('automatic --recompute requires the approved --image')
    source = args.source_repo or args.project
    ref = args.ref or 'origin/dev'
    args.candidate = args.candidate or committed_ref(source, ref)
    candidate = _pin(source, ref, args.candidate, AMS_ORIGIN)
    paths = feedback_paths(args.project, review)
    if paths.inventory is None:
        raise CoverageRefused('the committed manifest must declare pageReview.inventory for check')
    if args.recompute:
        collected = _collect_for_review(args, review_commit=review)
        result = check_coverage(args.project, collected['inventory'], candidate=candidate,
                                built=collected['html'], review_commit=review)
        result.update(input_mode=collected['input_mode'], build_image=collected['build_image'],
                      cleanup_verified=collected['cleanup_verified'])
        if collected.get('protection'):
            result['protection'] = collected['protection']
        _pin(source, ref, candidate, AMS_ORIGIN)
        return result
    blob = committed_blob(source, paths.inventory, candidate)
    if blob is None:
        raise CoverageRefused('the frozen source has no committed regular page inventory')
    result = check_coverage(args.project, json.loads(blob), candidate=candidate, review_commit=review)
    _pin(source, ref, candidate, AMS_ORIGIN)
    result['input_mode'] = 'committed-inventory'
    return result
