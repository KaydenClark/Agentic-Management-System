"""The Grill Board's local HTTP server: one page, read from committed card
files on every request, served on 127.0.0.1 only (DDR-000L, DDR-000P).

The page follows the "Grilling Board Redesign" artifact (DDR-000Y): topics
on the left, the queue in the middle, the open card on the right. Styles,
fonts and the theme script are served from `static/`; nothing loads from
another host. The verdict buttons POST to /answer, which writes the answer
into the card's owning record and commits it (answers.py, TK-002). The
stars POST to /rate and "Too taxing" to /flag; each appends its record to
the card and commits it the same way (DDR-000J, TK-003). A flagged card
leaves the queue, held for rewrite; answered and flagged cards can still be
opened by link, and rated or flagged.

POSTs are accepted only from this page: the Host must be this server and
the Origin (or, without one, the Referer) must be its own origin.
"""

import argparse
import json
import re
import uuid
import threading
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit

from .answers import VERDICTS, AnswerRefused, AnswerWrittenIndexStale, is_record_path, render_hashes
from .answers import answer as write_answer
from .answers import flag as write_flag
from .answers import rate as write_rate
from .cards import PRIORITIES, VALUES, CardSourceError, committed_cards, committed_snapshot, load_cards
from .dqcs import DqcCard, OutcomeUnknown, load_board, submit as submit_dqc

HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_CARDS = Path("grill-board") / "cards"
STATIC = Path(__file__).resolve().parent / "static"
DEFAULT_TOPIC = "Other topics"
MAX_POST = 64 * 1024
CONTENT_TYPES = {".css": "text/css", ".js": "text/javascript", ".woff2": "font/woff2", ".txt": "text/plain"}

OCTAGON = (
    '<svg class="gl" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 2h8l6 6v8l-6 6H8l-6-6V8z"></path>'
    '<path d="M12 8v4"></path><path d="M12 16h.01"></path></svg>'
)
HALF_MOON = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle>'
    '<path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor"></path></svg>'
)


def topic_of(card):
    return card.fields.get("Topic") or DEFAULT_TOPIC


def group_by_topic(cards):
    """[(topic, [cards])], topics ordered by their most urgent card."""
    topics = {}
    for card in cards:  # cards arrive sorted, so each topic's first card leads
        topics.setdefault(topic_of(card), []).append(card)
    return list(topics.items())


def link(topic, card=None):
    query = {"topic": topic}
    if card is not None:
        query["card"] = card.file
    return escape("/?" + urlencode(query), quote=True)


def grade(code, field=None):
    attr = f' data-field="{field}"' if field else ""
    return f'<span class="grade n{escape(code[1:])}"{attr}>{escape(code)}</span>'


def answered(cards):
    return sum(card.answer is not None for card in cards)


def width(cards):
    return f' style="width:{round(100 * answered(cards) / len(cards)) if cards else 0}%"'


def render_rail(groups, topic):
    total = sum(len(cards) for _, cards in groups)
    items = []
    for name, cards in groups:
        current = ' aria-current="page"' if name == topic else ""
        waiting = any(card.waiting for card in cards)
        dot = '<span class="dot tone h-owner" title="Has cards waiting on you"></span>' if waiting else ""
        count = f"{sum(card.waiting for card in cards)} ready" if any(isinstance(card, DqcCard) for card in cards) else f"{answered(cards)}/{len(cards)}"
        items.append(f"""<a class="topic" href="{link(name)}"{current}>
<span class="topic-line"><span class="topic-label">{escape(name)}</span><span class="count">{count}</span></span>
<span class="topic-meter"><span class="track"><span{width(cards)}></span></span>{dot}</span>
</a>""")
    if any(isinstance(card, DqcCard) for _, cards in groups for card in cards):
        source_note = '<div class="eyebrow">Concepts</div><div>Your questions and confirmed understanding stay linked to their history.</div><div class="small">Only ready questions ask for an answer.</div>'
    else:
        source_note = '<div class="eyebrow">Cards</div><div>Read from committed files in <span class="mono">grill-board/cards/</span>.</div><div class="small">Commit a card to post it; drafts never show.</div>'
    return f"""<aside class="rail">
<nav class="nav" aria-label="Board sections"><a class="navlink is-current" href="/" aria-current="page">Grill Board</a></nav>
<div class="topics">
<div class="topics-head"><span class="eyebrow">Topics</span><span class="count">{len(groups)} / {total}</span></div>
{"".join(items)}
</div>
<section class="rail-note" aria-label="Where cards come from">
{source_note}
</section>
</aside>"""


def render_row(card, topic, selected):
    current = card is selected
    state = ' is-current" aria-current="true' if current else ""
    return f"""<li class="card"><a class="row tone h-owner{state}" href="{link(topic, card)}">
<span class="dot"></span>
<span class="row-body">
<span class="row-title clamp" data-field="question">{escape(card.question)}</span>
<span class="row-meta"><span class="mono">{escape(card.file)}</span><span>To answer</span></span>
<span class="row-why"><b>Priority</b> <span data-field="priority-reason">{escape(card.priority_reason)}</span></span>
<span class="row-why"><b>Value</b> <span data-field="value-reason">{escape(card.value_reason)}</span></span>
</span>
<span class="row-grades">{grade(card.priority, "priority")}{grade(card.value, "value")}</span>
</a></li>"""


def render_queue(topic, all_cards, selected, unavailable=False):
    cards = [card for card in all_cards if card.waiting]
    count = len(cards)
    rows = "\n".join(render_row(card, topic, selected) for card in cards)
    if not rows:
        rows = '<li class="empty">The queue is unavailable; read the source issues above.</li>' if unavailable else '<li class="empty">Nothing here needs you.</li>'
    progress = f"{count} ready to answer · {len(all_cards) - count} context/history" if any(isinstance(c, DqcCard) for c in all_cards) else f"{answered(all_cards)} of {len(all_cards)} answered"
    return f"""<section class="queue" aria-label="Question queue">
<div class="queue-head">
<h1>{escape(topic) if all_cards else "Grill Board"}</h1>
<div class="progress">
<div class="bar8"><div{width(all_cards)}></div></div>
<div class="progress-line">{progress}</div>
</div>
</div>
<div class="lanes" role="group" aria-label="Where it is in the workflow">
<span class="lane"><span class="dot tone h-owner"></span>To answer<span class="count">{count}</span></span>
</div>
<div class="sortbar"><span>{count} card(s)</span><span class="sorted">Sorted by Priority, then Value</span></div>
<ol class="rows">
{rows}
</ol>
</section>"""


def render_verdicts(cards_dir, topic, card):
    card_sha, record_sha = render_hashes(cards_dir, card)
    target, anchor = card.fields.get("Owner record", ""), card.fields.get("Write after", "")
    if not (target and anchor):
        where, ready = "Confirm needs this card to name its Owner record and Write after line.", False
    elif not is_record_path(target):
        where, ready = "Confirm needs an Owner record that is a Markdown record under a record root (see grill-board/README.md).", False
    elif not card.fields.get("Recommendation"):
        where, ready = "Confirm needs a Recommendation on this card.", False
    else:
        where = f'Confirm writes the recommendation into <span class="mono">{escape(target)}</span>, after <span class="mono">{escape(anchor)}</span>, and commits it.'
        ready = True
    hidden = "".join(
        f'<input type="hidden" name="{name}" value="{escape(value, quote=True)}">'
        for name, value in (("card", card.file), ("topic", topic), ("card_sha", card_sha), ("record_sha", record_sha))
    )
    buttons = []
    for value, label in VERDICTS.items():
        kind = "verdict confirm tone h-agent" if value == "confirm" else "verdict tone h-returned"
        off = "" if value != "confirm" or ready else " disabled"
        buttons.append(f'<button type="submit" name="verdict" value="{value}" class="{kind}"{off}>{escape(label)}</button>')
    return f"""<form class="answer" method="post" action="/answer">
{hidden}
<p class="verdict-note">{where} The other verdicts return the card with your note.</p>
<div class="verdicts">
{chr(10).join(buttons)}
</div>
<label class="sr-only" for="note">Note</label>
<textarea id="note" name="note" rows="3" maxlength="4000" placeholder="What should change, in your words"></textarea>
</form>"""


def render_rating(topic, card):
    """One click each: a star POSTs its rating to /rate, "Too taxing" POSTs to
    /flag. The optional comment travels with either click."""
    hidden = "".join(
        f'<input type="hidden" name="{name}" value="{escape(value, quote=True)}">'
        for name, value in (("card", card.file), ("topic", topic), ("card_sha", card.sha))
    )
    stars = "".join(
        f'<button type="submit" name="rating" value="{n}" class="star{" on" if card.rating and n <= int(card.rating) else ""}" '
        f'aria-pressed="{"true" if str(n) == card.rating else "false"}" aria-label="Rate {n} of 5">&#9733;</button>'
        for n in range(1, 6)
    )
    if card.flag is not None:
        taxing = '<span class="taxing is-flagged tone h-returned">Flagged too taxing</span>'
    else:
        taxing = '<button type="submit" formaction="/flag" class="taxing">Too taxing</button>'
    saved = f'<span class="small">Rated {escape(card.rating)} of 5</span>' if card.rating else ""
    return f"""<form class="rating" method="post" action="/rate">
{hidden}
<span class="ask">Was this a good question?</span>
<span class="stars" role="group" aria-label="Rate this question, one to five">{stars}</span>{saved}
{taxing}
<label class="sr-only" for="comment">Comment on the question</label>
<input id="comment" class="comment" type="text" name="comment" maxlength="1000" placeholder="Optional comment on the question">
</form>"""


def render_open(cards_dir, topic, cards, card):
    if card in cards:
        index = cards.index(card)
        before, after = cards[index - 1], cards[(index + 1) % len(cards)]
    extras = ""
    if getattr(card, 'verification', None) and card.verification.get('State') == 'protected-capture':
        extras += ('<div class="block"><div class="eyebrow">Verification</div><p>'
                   'This content was verified on the protected deployment. The earlier context below is preserved history. '
                   f'Observed {escape(card.verification.get("Observed at", ""))}.</p></div>\n')
    if card.context:
        extras += f'<div class="block"><div class="eyebrow">Context</div><p class="context">{escape(card.context)}</p></div>\n'
    if card.fields.get("Why it matters"):
        extras += f"""<div class="box tone h-worth"><div class="box-head">Why this choice matters</div>
<p>{escape(card.fields["Why it matters"])}</p></div>\n"""
    if card.fields.get("Recommendation"):
        extras += f"""<div class="box tone h-agent"><div class="box-head"><span class="dot rest"></span>Agent recommendation</div>
<p>{escape(card.fields["Recommendation"])}</p></div>\n"""
    if getattr(card, 'stale', None) is not None:
        target = card.stale.get('Superseded by', '')
        state = '<span class="pill tone h-none">Stale content · history only</span>'
        if card.stale.get('Removed in'):
            verdict = '<p>This page was removed from the current candidate. Its review remains history.</p>'
        else:
            verdict = f'<p>Read the current <a href="/?{urlencode({"topic": topic, "card": target})}">replacement review card</a>. This content approval is no longer current.</p>'
    elif card.flag and card.flag.get('Migrated'):
        target = card.flag['Migrated']
        state = '<span class="pill tone h-none">Legacy history · DQC owns the question</span>'
        verdict = f'<p>Continue on <a href="/?{urlencode({"card":target})}">{escape(target)}</a>. This legacy card and its history are preserved.</p>'
    elif card.flag is not None:
        state = '<span class="pill tone h-returned"><span class="dot"></span>Too taxing: held for rewrite</span>'
        verdict = '<p class="verdict-note">Flagged too taxing. An agent rewrites the question and posts it as a new card before it is asked again.</p>'
    elif card.answer is not None:
        state = f'<span class="pill tone h-none"><span class="dot rest"></span>Answered: {escape(card.answer.get("Verdict", ""))}</span>'
        verdict = f'<p class="verdict-note">Answered {escape(card.answer.get("Answered", ""))}. You can still rate it or flag it too taxing.</p>'
    else:
        state = '<span class="pill tone h-owner"><span class="dot"></span>To answer</span>'
        verdict = render_verdicts(cards_dir, topic, card)
    if card in cards:
        index = cards.index(card)
        place = f"{index + 1} of {len(cards)} in this topic"
    else:
        before = after = cards[0] if cards else card
        place = f"Not in the queue; {len(cards)} waiting in this topic"
    return f"""<main class="open" aria-label="Open card">
<article>
<div class="open-meta">
{state}
<span class="open-id">{escape(card.file)}</span>
<span class="open-id">{escape(topic)}</span>
</div>
<h2>{escape(card.question)}</h2>
<div class="why-grid">
<details class="grade-why"><summary>{grade(card.priority)}<span class="label">Priority · {escape(PRIORITIES[card.priority])} · why this grade</span></summary><p>{escape(card.priority_reason)}</p></details>
<details class="grade-why"><summary>{grade(card.value)}<span class="label">Value · {escape(VALUES[card.value])} · why this grade</span></summary><p>{escape(card.value_reason)}</p></details>
</div>
{extras}<section class="verdict-area" aria-label="Your verdict">
<div class="eyebrow">Your verdict</div>
{verdict}
{render_rating(topic, card)}
<div class="pager">
<span>{place}</span>
<span class="buttons"><a class="ghost" href="{link(topic, before)}">Previous</a><a class="inkbtn" href="{link(topic, after)}">Next question</a></span>
</div>
</section>
</article>
</main>"""


def render_refusals(refusals):
    if not refusals:
        return ""
    items = "\n".join(
        f'<li class="refusal"><span class="mono">{escape(r.file)}</span>: {escape("; ".join(r.problems))}</li>'
        for r in refusals
    )
    return f"""<section class="alert tone h-heat strong" role="alert" aria-label="Refused cards">
{OCTAGON}
<div><div>Refused cards ({len(refusals)}): these files are not shown until fixed.</div>
<ul>
{items}
</ul></div>
</section>"""


def render_notice(notice):
    if not notice:
        return ""
    kind, text = notice
    if kind in ("refused", "uncertain"):
        return f"""<section class="alert tone h-heat strong" role="alert" aria-label="Answer not written">
{OCTAGON}<div>{"Save outcome unknown" if kind == "uncertain" else "Not written"}: {escape(text)}</div>
</section>"""
    return f'<section class="alert notice" role="status" aria-label="Answer written"><div>{escape(text)}</div></section>'


def hidden_fields(fields):
    inputs = []
    for name, value in fields.items():
        # Character references preserve exact multiline scope/notes in HTML attributes.
        attribute = escape(str(value), quote=True).replace('\r', '&#13;').replace('\n', '&#10;').replace('\t', '&#9;')
        inputs.append(f'<input type="hidden" name="{escape(name, quote=True)}" value="{attribute}">')
    return ''.join(inputs)


def dqc_fields(card, drafts=None):
    life = card.dqc['lifecycle']
    same_view = bool(drafts and drafts.get('card') == card.file and drafts.get('expectHead') == card.commit
                     and drafts.get('expectRevision') == str(card.dqc['revision']) and drafts.get('digest') == life.get('digest'))
    return {'dqc':'yes', 'card':card.file, 'topic':topic_of(card), 'expectHead':card.commit,
            'expectRevision':card.dqc['revision'], 'digest':life.get('digest') or '',
            'eventId':drafts['eventId'] if same_view else uuid.uuid4().hex, 'scope':(life.get('proposal') or {}).get('scope', '')}


def exact_text(value, label=''):
    attribute = f' aria-label="{escape(label, quote=True)}"' if label else ''
    return f'<pre class="readback"{attribute}><span>{escape(str(value))}</span></pre>'


def render_drafts(drafts):
    if not drafts:
        return ''
    fields = []
    for name, label in (('note', 'Your note'), ('comment', 'Your comment')):
        if drafts.get(name):
            fields.append(f'<label>{label}<textarea readonly rows="3">{escape(drafts[name])}</textarea></label>')
    retry = ''
    if drafts.get('_uncertain'):
        endpoint = drafts['_endpoint']
        original = {name:value for name,value in drafts.items() if not name.startswith('_')}
        retry = f'<form class="retry" method="post" action="{escape(endpoint, quote=True)}" data-unsaved-action>{hidden_fields(original)}<button class="verdict" type="submit">Check or retry this exact action</button></form>'
        message = 'The save outcome is unknown. Keep these words and use the original action below to check or retry without creating another event.'
    else:
        message = 'Your submission was not saved. Copy your words before leaving this page.'
    if not fields and not retry:
        return ''
    return f'<section class="alert" aria-label="Unsaved submission"><div><p>{message}</p>{"".join(fields)}{retry}</div></section>'


def render_context(cards, topic):
    other = [card for card in cards if not card.waiting]
    if not other:
        return ''
    links = ''.join(f'<li><a href="{link(topic, card)}">{escape(card.file)} · {escape(card.question)}</a></li>' for card in other)
    return f'<section class="context-list" aria-label="Context and history"><h2>Context and history</h2><p>Confirmed concepts, branch context and questions held for agent work.</p><ul>{links}</ul></section>'


READBACK_HEADING = re.compile(
    r'^\s*(?:\*\*|#{1,6}\s*)?(Summary|The why|The intended result|My next step|What I will do)\s*:?(?:\*\*)?\s*$',
    re.IGNORECASE,
)


def render_readback(value):
    """Recognize only readback section headings; all other source is escaped prose."""
    sections, lines = [], []
    for line in value.splitlines(keepends=True):
        match = READBACK_HEADING.fullmatch(line.rstrip('\r\n'))
        if match:
            if lines:
                sections.append('<div class="readback">' + escape(''.join(lines).strip('\r\n')) + '</div>')
                lines = []
            sections.append('<h3>' + escape(match[1]) + '</h3>')
        else:
            lines.append(line)
    if lines:
        sections.append('<div class="readback">' + escape(''.join(lines).strip('\r\n')) + '</div>')
    displayed = '<div class="readback-proposal" aria-label="Exact displayed readback">' + ''.join(sections) + '</div>'
    source = '<details class="readback-source"><summary>Exact source wording</summary>' + exact_text(value, 'Exact source readback') + '</details>'
    return displayed + source


def render_dqc_proposal(card):
    proposal = card.dqc['lifecycle'].get('proposal')
    if not proposal:
        return '<p>No complete proposed readback is recorded. An agent prepares the question before asking it.</p>'
    heading = 'Confirmed readback' if card.dqc['lifecycle']['state'] == 'confirmed' else 'Suggested readback'
    dependencies = []
    for ident in proposal['dependencies']:
        href = escape('/?' + urlencode({'card':ident}), quote=True)
        dependencies.append(f'<li><a href="{href}">{escape(ident)}</a></li>')
    dependency_section = ''
    if dependencies:
        dependency_section = '<section><h3>Dependencies carried forward</h3><ul>' + ''.join(dependencies) + '</ul></section>'
    held = ''
    if card.blocked:
        blockers = ''.join(f'<li>{escape(ident)} · unconfirmed or unresolved</li>' for ident in card.blocked)
        held = f'<section class="box tone h-returned"><h3>Waiting on dependencies</h3><p>These prerequisites remain unresolved:</p><ul>{blockers}</ul></section>'
    return f"""<section class="box tone h-worth"><div class="box-head">Why this choice matters</div>
{exact_text(proposal['why'])}</section>
<section class="box tone h-agent"><div class="box-head">{heading}</div>
{render_readback(proposal['readback'])}</section>
<section class="block"><div class="eyebrow">Source and scope</div>{exact_text(proposal['source'])}
<div class="eyebrow">Scope</div>{exact_text(proposal['scope'])}<p class="small">Round {escape(proposal['round'])}</p></section>
{dependency_section}{held}"""


def render_confirmations(life):
    versions = []
    for saved in reversed(life['confirmations']):
        readback = saved.get('readback')
        if readback is None:
            readback = 'Legacy confirmation has no retained readback.'
        scope = saved.get('scope') or 'Scope not recorded in legacy confirmation.'
        versions.append(f"""<details class="history-entry"><summary>Confirmed version · revision {saved.get('revision', 'legacy')}</summary>
{exact_text(readback)}<p>Source: {escape(saved['source'])}</p>{exact_text(scope)}</details>""")
    if not versions:
        return ''
    current = ''
    if life['state'] != 'confirmed':
        saved = life['confirmations'][-1]
        current = '<section class="block"><h3>Earlier confirmed readback</h3>' + exact_text(saved.get('readback') or 'Legacy readback not retained.') + '<p>Source: ' + escape(saved['source']) + '</p></section>'
    return current + '<section aria-label="Prior confirmed versions"><h3>Preserved confirmations</h3>' + ''.join(versions) + '</section>'


def render_dqc_history(data):
    events = []
    life = data['lifecycle']
    for event in reversed(life['events']):
        rating = f" · {event['rating']} of 5" if event.get('rating') else ''
        note = exact_text(event['note']) if event.get('note') is not None else ''
        source = escape(event.get('source') or 'Source not supplied')
        events.append(f"""<li><b>{escape(event['type'])} · revision {event['revision']}</b>
{escape(event.get('kind', ''))}{rating}<p class="small">{source} · {escape(event.get('at', ''))}</p>{note}</li>""")
    revisions = []
    for entry in reversed(data.get('history', [])):
        changes = []
        for change in entry['changes']:
            if change['field'] == 'lifecycle':
                previous = change.get('to', {}).get('proposal')
                if previous:
                    changes.extend([exact_text(previous['readback']), exact_text(previous['why'])])
            else:
                changes.append(exact_text(json.dumps(change, ensure_ascii=False, indent=2)))
        revisions.append(f"""<details class="history-entry"><summary>Record revision {entry['revision']} · {escape(entry['reason'])}</summary>
{''.join(changes)}</details>""")
    return f"""<details class="history-entry" aria-label="DQC history"><summary>History and exact owner words ({len(life['events'])})</summary>
<ul>{''.join(events)}</ul>{''.join(revisions)}</details>"""


def render_dqc_connections(data):
    related = []
    for item in data.get('related', []):
        state = item.get('state', item.get('resolution', 'unknown'))
        related.append(f'<li>{escape(item["key"])} · {escape(state)} — {escape(item["reason"])}</li>')
    content = ''
    if related:
        content = '<section><h3>Connected execution records</h3><p class="small">Execution status and proof remain in their owning records.</p><ul>' + ''.join(related) + '</ul></section>'
    if data.get('result'):
        content += '<section><h3>Recorded outcome</h3>' + exact_text(data['result']['summary']) + '</section>'
    if data.get('uncertainty'):
        content += '<section><h3>Unresolved understanding</h3>' + ''.join(exact_text(item) for item in data['uncertainty']) + '</section>'
    return content


def render_dqc_controls(card, drafts):
    life = card.dqc['lifecycle']
    proposal = life.get('proposal')
    if not proposal or not proposal.get('actionable', True):
        return ''
    controls = ''
    if card.waiting or life['state'] == 'confirmed':
        buttons = []
        for value, label in VERDICTS.items():
            if value == 'confirm' and not card.waiting:
                continue
            style = 'confirm tone h-agent' if value == 'confirm' else 'tone h-returned'
            buttons.append(f'<button type="submit" name="verdict" value="{value}" class="verdict {style}">{label}</button>')
        same_view = drafts and drafts.get('card') == card.file and drafts.get('expectHead') == card.commit and drafts.get('expectRevision') == str(card.dqc['revision'])
        note = drafts.get('note', '') if same_view else ''
        controls += f"""<form class="answer" method="post" action="/answer">{hidden_fields(dqc_fields(card, drafts))}
<p class="verdict-note">Confirm saves exactly the displayed readback and scope. Corrections preserve your words for an agent rewrite; they do not confirm replacement wording.</p>
<div class="verdicts">{''.join(buttons)}</div><label for="note">Your correction or note</label>
<textarea id="note" name="note" rows="3" maxlength="4000">\n{escape(note)}</textarea></form>"""
    else:
        controls += '<p class="verdict-note">This concept is not waiting for confirmation. An agent must prepare a changed proposal before it is asked again.</p>'
    stars = []
    for n in range(1, 6):
        pressed = str(card.rating == str(n)).lower()
        on = ' on' if card.rating and n <= int(card.rating) else ''
        stars.append(f'<button type="submit" name="rating" value="{n}" class="star{on}" aria-label="Rate {n} of 5" aria-pressed="{pressed}">&#9733;</button>')
    flag = '<span class="taxing is-flagged tone h-returned">Held for rewrite</span>' if life['state'] == 'needs-rewrite' else '<button type="submit" formaction="/flag" class="taxing">Too taxing</button>'
    controls += f"""<form class="rating" method="post" action="/rate">{hidden_fields(dqc_fields(card, drafts))}
<span class="ask">Was this a good question?</span><span class="stars" role="group" aria-label="Rate this question, one to five">{''.join(stars)}</span>{flag}
<label class="sr-only" for="comment">Comment on the question</label>
<input id="comment" class="comment" name="comment" maxlength="1000" placeholder="Optional comment on the question"></form>"""
    return controls


def render_dqc(topic, card, drafts=None):
    data, life = card.dqc, card.dqc['lifecycle']
    proposal = life.get('proposal')
    state = life['state']
    if not proposal or not proposal.get('actionable', True):
        label = 'Branch context · no owner answer requested'
    elif card.blocked and state in ('pending', 'reopened'):
        label = 'Waiting on dependencies'
    else:
        label = {'pending':'To answer', 'reopened':'Reopened · to answer', 'confirmed':'Confirmed concept',
                 'needs-rewrite':'Held for agent rewrite', 'deferred':'Deferred concept', 'superseded':'Superseded concept'}[state]
    tone = 'h-owner' if card.waiting else 'h-returned' if state == 'needs-rewrite' else 'h-none'
    return f"""<main class="open" aria-label="Open card"><article>
<div class="open-meta"><span class="pill tone {tone}">{label}</span><span class="open-id">{escape(card.file)} · Revision {data['revision']}</span></div>
<h2>{escape(card.question)}</h2><div class="why-grid">
<details class="grade-why"><summary>{grade(card.priority)}<span>Priority · {escape(PRIORITIES[card.priority])}</span></summary><p>{escape(card.priority_reason)}</p></details>
<details class="grade-why"><summary>{grade(card.value)}<span>Value · {escape(VALUES[card.value])}</span></summary><p>{escape(card.value_reason)}</p></details></div>
{render_dqc_proposal(card)}{render_confirmations(life)}{render_dqc_connections(data)}{render_dqc_history(data)}
<section class="verdict-area" aria-label="Your verdict">{render_dqc_controls(card, drafts)}</section></article></main>"""


def render_rounds(tracker, head):
    if not tracker or tracker.get('error'):
        return ''
    current = tracker.get('currentRound')
    finished = tracker.get('rounds', [])
    if not current:
        current = next((card['lifecycle']['proposal']['round'] for card in tracker['questions'] if card['lifecycle'].get('proposal')), None)
    control = ''
    if current:
        fields = hidden_fields({'eventId':uuid.uuid4().hex, 'expectHead':head, 'round':current, 'topic':'Concepts'})
        control = f'<form class="round" method="post" action="/round">{fields}<span>Current round: {escape(current)}</span><button class="verdict" type="submit">Finish this round</button></form>'
    history = ''
    for item in reversed(finished):
        changed = []
        by_id = {card['id']:card for card in tracker['questions']}
        for card in item['changed']:
            proposal = by_id.get(card['id'], {}).get('lifecycle', {}).get('proposal') or {}
            status = ' · branch context; no answer requested' if proposal.get('actionable') is False else ' · unanswered' if card.get('unanswered') else ''
            dependencies = f" · dependencies: {escape(', '.join(card['dependencies']))}" if card.get('dependencies') else ''
            href = escape('/?' + urlencode({'card':card['id']}), quote=True)
            changed.append(f'<li><a href="{href}">{escape(card["id"])} · revision {card["revision"]}</a> · {len(card.get("events", []))} answer/quality event(s){status}{dependencies}</li>')
        changed = ''.join(changed)
        receipt = item.get('receipt')
        continuation = (f'<p>Reconciled: {escape(receipt["outcome"])}</p><p>Next frontier: {escape(receipt["nextFrontier"])}</p><ul>' + ''.join(f'<li>{escape(source)}</li>' for source in receipt['sources']) + '</ul>') if receipt else '<p>Agent review pending. Tell your agent this round is finished. The agent reviews every changed DQC, including corrections and quality feedback, updates approved Wiki/docs, and records the next frontier. Finishing this round does not start implementation.</p>'
        history += f'<details class="history-entry" open><summary>Finished round {escape(item["id"])} · {"Reconciled" if receipt else "Agent review pending"}</summary><ul>{changed}</ul>{continuation}</details>'
    return f'<section class="rounds" aria-label="Grilling rounds">{control}{history}</section>'


def render_page(cards_dir, query="", notice=None, drafts=None):
    cards, refusals, tracker, revision = load_board(cards_dir, legacy_loader=load_cards)
    params = parse_qs(query)
    groups = group_by_topic(cards)
    names = [name for name, _ in groups]
    waiting = [name for name, group in groups if any(card.waiting for card in group)]
    wanted = params.get("topic", [None])[0]
    wanted_card = params.get("card", [None])[0]
    linked = next((card for card in cards if card.file == wanted_card), None)
    topic = topic_of(linked) if linked else wanted if wanted in names else (waiting or names or [DEFAULT_TOPIC])[0]
    in_topic = dict(groups).get(topic, [])
    shown = [card for card in in_topic if card.waiting]
    # A link may open an answered or flagged card, so it can still be rated or flagged.
    selected = next((card for card in in_topic if card.file == wanted_card), shown[0] if shown else next((c for c in in_topic if isinstance(c, DqcCard)), None))
    if isinstance(selected, DqcCard):
        open_card = render_dqc(topic, selected, drafts)
    else:
        open_card = render_open(cards_dir, topic, shown, selected) if selected else ""
    recovery = render_drafts(drafts) if drafts else ""
    history = render_context(in_topic, topic)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grill Board</title>
<link rel="stylesheet" href="/static/board.css">
<script src="/static/theme.js"></script>
<script src="/static/queue.js" defer></script>
</head>
<body data-board-revision="{escape(revision, quote=True)}">
<header class="top"><div class="top-in">
<div class="brand"><span class="brand-name">AMS</span><span class="brand-sub">Grill Board</span></div>
<button type="button" class="theme-toggle" data-theme-toggle hidden aria-label="Switch light or dark theme">{HALF_MOON}<span data-theme-label>Dark</span></button>
</div></header>
{render_notice(notice)}
{render_refusals(refusals)}
{recovery}
<p class="verdict-note" data-queue-update role="status" hidden></p>
{render_rounds(tracker, revision)}
<div class="cols">
{render_rail(groups, topic)}
<div class="queue-column">{render_queue(topic, dict(groups).get(topic, []), selected, unavailable=bool(refusals))}{history}</div>
{open_card}
</div>
</body></html>
"""


def static_file(path):
    """Return the packaged static file a `/static/...` path names, or None.
    Only files that exist under STATIC are served; nothing else is reachable."""
    relative = path.removeprefix("/static/")
    files = {p.relative_to(STATIC).as_posix(): p for p in STATIC.rglob("*") if p.is_file()}
    return files.get(relative)


def make_server(cards_dir, port=DEFAULT_PORT):
    cards_dir = Path(cards_dir)
    committed_cards(cards_dir)  # refuse a directory that is not committed records
    one_writer = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            url = urlsplit(self.path)
            if url.path.startswith("/static/") and (found := static_file(url.path)):
                self.reply(200, CONTENT_TYPES.get(found.suffix, "application/octet-stream"), found.read_bytes())
                return
            if url.path == "/api/revision":
                try:
                    revision, _ = committed_snapshot(cards_dir)
                    self.reply(200, "application/json", json.dumps({"revision":revision}).encode())
                except CardSourceError:
                    self.reply(503, "application/json", b'{"error":"The queue source is unavailable."}')
                return
            if url.path not in ("/", "/index.html"):
                self.send_error(404)
                return
            try:
                self.reply(200, "text/html", render_page(cards_dir, url.query).encode("utf-8"))
            except CardSourceError as error:
                self.reply(500, "text/plain", f"Grill Board cannot read committed cards: {error}\n".encode("utf-8"))

        def same_origin(self):
            own = f"{HOST}:{self.server.server_address[1]}"
            if self.client_address[0] != HOST or self.headers.get("Host") != own:
                return False
            if self.headers.get("Sec-Fetch-Site") not in (None, "same-origin"):
                return False
            origin = self.headers.get("Origin")
            if origin is not None:
                return origin == f"http://{own}"
            return (self.headers.get("Referer") or "").startswith(f"http://{own}/")

        def do_POST(self):
            action = urlsplit(self.path).path
            if action not in ("/answer", "/rate", "/flag", "/round"):
                self.send_error(404)
                return
            if not self.same_origin():
                self.reply(403, "text/plain", b"Refused: answers, ratings and flags are accepted only from this board's own page.\n")
                return
            try:
                length = int(self.headers.get("Content-Length") or 0)
                if not 0 < length <= MAX_POST or self.headers.get("Content-Type", "").split(";")[0] != "application/x-www-form-urlencoded":
                    raise ValueError
                form = {key: values[0] for key, values in parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True).items()}
            except (ValueError, UnicodeDecodeError):
                self.reply(400, "text/plain", b"Refused: send one of the board's own forms.\n")
                return
            topic = form.get("topic", "")
            status, notice, drafts = 200, None, None
            try:
                with one_writer:
                    cards, _, _, _ = load_board(cards_dir, legacy_loader=load_cards)
                    card = next((c for c in cards if c.file == form.get("card")), None)
                    if action == "/round" or form.get("dqc") == "yes":
                        if action == '/answer' and form.get('verdict') == 'confirm' and isinstance(card, DqcCard):
                            proposal = card.dqc['lifecycle'].get('proposal') or {}
                            recorded = any(event['eventId'] == form.get('eventId') for event in card.dqc['lifecycle']['events'])
                            # Native replay verifies the original target and complete request before stale/state checks.
                            if not recorded and (card.blocked or not proposal.get('actionable', True)):
                                raise AnswerRefused('This DQC is context-only or waiting on unresolved dependencies; no confirmation was recorded.')
                        result = submit_dqc(cards_dir, form, action)
                        notice = ("written", f"{result['status'].capitalize()} {result['commit'][:7]}: your DQC action is saved.")
                    else:
                        if card is None:
                            raise AnswerRefused(f"no committed card named {form.get('card')!r}")
                        if action == "/rate":
                            sha = write_rate(cards_dir, card, form.get("rating", ""), form.get("comment", ""), form.get("card_sha", ""))
                            done = f"rated {form['rating']} of 5 on {card.file}"
                        elif action == "/flag":
                            sha = write_flag(cards_dir, card, form.get("comment", ""), form.get("card_sha", ""))
                            done = f"{card.file} flagged too taxing and held for rewrite"
                        else:
                            sha = write_answer(cards_dir, card, form.get("verdict", ""), form.get("note", ""), form.get("card_sha", ""), form.get("record_sha", ""))
                            where = card.fields["Owner record"] if form["verdict"] == "confirm" else "the card as a return"
                            done = f"{VERDICTS[form['verdict']]} on {card.file}, recorded in {where}"
                        notice = ("written", f"Written and committed {sha[:7]}: {done}.")
            except OutcomeUnknown as error:
                status, notice = 503, ("uncertain", str(error))
                drafts = {**form, "_uncertain":"yes", "_endpoint":action}
            except (AnswerRefused, CardSourceError) as error:
                status, notice, drafts = 409, ("refused", str(error)), form
            except AnswerWrittenIndexStale as error:
                notice = ("written", f"Written: {error}")
            query = urlencode({"topic":topic, "card":form.get("card", "")})
            try:
                page = render_page(cards_dir, query, notice, drafts=drafts)
            except CardSourceError as error:
                # A rendering failure after a successful commit never changes its save receipt.
                page = render_notice(notice) + f'<p>Current Board source unavailable: {escape(str(error))}</p>' + render_drafts(drafts)
            self.reply(status, "text/html", page.encode("utf-8"))

        def reply(self, status, kind, payload):
            self.send_response(status)
            charset = "; charset=utf-8" if kind.startswith("text/") else ""
            self.send_header("Content-Type", kind + charset)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, format, *args):
            pass

    return ThreadingHTTPServer((HOST, port), Handler)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="ams-board", description="Serve the local Grill Board.")
    parser.add_argument("--cards", type=Path, default=DEFAULT_CARDS, help="card directory (default: grill-board/cards)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"port on {HOST} (default: {DEFAULT_PORT})")
    args = parser.parse_args(argv)
    try:
        server = make_server(args.cards, args.port)
    except CardSourceError as error:
        parser.error(f"{error} (run from the repository root or pass --cards)")
    print(f"Grill Board: http://{HOST}:{server.server_address[1]}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
