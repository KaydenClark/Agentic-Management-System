"""The Grill Board's local HTTP server: one page, read from committed card
files on every request, served on 127.0.0.1 only (DDR-000L, DDR-000P).

The page follows the "Grilling Board Redesign" artifact (DDR-000Y): topics
on the left, the queue in the middle, the open card on the right. Styles,
fonts and the theme script are served from `static/`; nothing loads from
another host. The verdict buttons POST to /answer, which writes the answer
into the card's owning record and commits it (answers.py, TK-002); rating
and the too-taxing flag stay disabled until TK-003 wires them.

POSTs are accepted only from this page: the Host must be this server and
the Origin (or, without one, the Referer) must be its own origin.
"""

import argparse
import threading
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit

from .answers import VERDICTS, AnswerRefused, AnswerWrittenIndexStale, render_hashes
from .answers import answer as write_answer
from .cards import PRIORITIES, VALUES, CardSourceError, committed_cards, load_cards

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
        waiting = len(cards) > answered(cards)
        dot = '<span class="dot tone h-owner" title="Has cards waiting on you"></span>' if waiting else ""
        items.append(f"""<a class="topic" href="{link(name)}"{current}>
<span class="topic-line"><span class="topic-label">{escape(name)}</span><span class="count">{answered(cards)}/{len(cards)}</span></span>
<span class="topic-meter"><span class="track"><span{width(cards)}></span></span>{dot}</span>
</a>""")
    return f"""<aside class="rail">
<nav class="nav" aria-label="Board sections"><a class="navlink is-current" href="/" aria-current="page">Grill Board</a></nav>
<div class="topics">
<div class="topics-head"><span class="eyebrow">Topics</span><span class="count">{len(groups)} / {total}</span></div>
{"".join(items)}
</div>
<section class="rail-note" aria-label="Where cards come from">
<div class="eyebrow">Cards</div>
<div>Read from committed files in <span class="mono">grill-board/cards/</span>.</div>
<div class="small">Commit a card to post it; drafts never show.</div>
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


def render_queue(topic, all_cards, selected):
    cards = [card for card in all_cards if card.answer is None]
    count = len(cards)
    rows = "\n".join(render_row(card, topic, selected) for card in cards)
    if not rows:
        rows = '<li class="empty">Nothing here needs you.</li>'
    return f"""<section class="queue" aria-label="Question queue">
<div class="queue-head">
<h1>{escape(topic) if all_cards else "Grill Board"}</h1>
<div class="progress">
<div class="bar8"><div{width(all_cards)}></div></div>
<div class="progress-line">{answered(all_cards)} of {len(all_cards)} answered</div>
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


def render_open(cards_dir, topic, cards, card):
    index = cards.index(card)
    before, after = cards[index - 1], cards[(index + 1) % len(cards)]
    extras = ""
    if card.context:
        extras += f'<div class="block"><div class="eyebrow">Context</div><p class="context">{escape(card.context)}</p></div>\n'
    if card.fields.get("Why it matters"):
        extras += f"""<div class="box tone h-worth"><div class="box-head">Why this choice matters</div>
<p>{escape(card.fields["Why it matters"])}</p></div>\n"""
    if card.fields.get("Recommendation"):
        extras += f"""<div class="box tone h-agent"><div class="box-head"><span class="dot rest"></span>Agent recommendation</div>
<p>{escape(card.fields["Recommendation"])}</p></div>\n"""
    stars = "".join(f'<button type="button" class="star" disabled aria-label="{n} of 5">&#9733;</button>' for n in range(1, 6))
    return f"""<main class="open" aria-label="Open card">
<article>
<div class="open-meta">
<span class="pill tone h-owner"><span class="dot"></span>To answer</span>
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
{render_verdicts(cards_dir, topic, card)}
<p class="inert-note">Not wired yet: rating and the flag arrive with S-004 TK-003 and save nothing.</p>
<div class="rating">
<span class="ask">Was this a good question?</span>
<span class="stars" role="group" aria-label="Rate this question, one to five">{stars}</span>
<button type="button" class="taxing" disabled>Too taxing</button>
</div>
<div class="pager">
<span>{index + 1} of {len(cards)} in this topic</span>
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
    if kind == "refused":
        return f"""<section class="alert tone h-heat strong" role="alert" aria-label="Answer not written">
{OCTAGON}<div>Not written: {escape(text)}</div>
</section>"""
    return f'<section class="alert notice" role="status" aria-label="Answer written"><div>{escape(text)}</div></section>'


def render_page(cards_dir, query="", notice=None):
    cards, refusals = load_cards(cards_dir)
    params = parse_qs(query)
    groups = group_by_topic(cards)
    names = [name for name, _ in groups]
    waiting = [name for name, group in groups if any(card.answer is None for card in group)]
    wanted = params.get("topic", [None])[0]
    topic = wanted if wanted in names else (waiting or names or [DEFAULT_TOPIC])[0]
    shown = [card for card in dict(groups).get(topic, []) if card.answer is None]
    wanted_card = params.get("card", [None])[0]
    selected = next((card for card in shown if card.file == wanted_card), shown[0] if shown else None)
    open_card = render_open(cards_dir, topic, shown, selected) if selected else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grill Board</title>
<link rel="stylesheet" href="/static/board.css">
<script src="/static/theme.js"></script>
</head>
<body>
<header class="top"><div class="top-in">
<div class="brand"><span class="brand-name">AMS</span><span class="brand-sub">Grill Board</span></div>
<button type="button" class="theme-toggle" data-theme-toggle hidden aria-label="Switch light or dark theme">{HALF_MOON}<span data-theme-label>Dark</span></button>
</div></header>
{render_notice(notice)}
{render_refusals(refusals)}
<div class="cols">
{render_rail(groups, topic)}
{render_queue(topic, dict(groups).get(topic, []), selected)}
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
            if urlsplit(self.path).path != "/answer":
                self.send_error(404)
                return
            if not self.same_origin():
                self.reply(403, "text/plain", b"Refused: answers are accepted only from this board's own page.\n")
                return
            try:
                length = int(self.headers.get("Content-Length") or 0)
                if not 0 < length <= MAX_POST or self.headers.get("Content-Type", "").split(";")[0] != "application/x-www-form-urlencoded":
                    raise ValueError
                form = {key: values[0] for key, values in parse_qs(self.rfile.read(length).decode("utf-8")).items()}
            except (ValueError, UnicodeDecodeError):
                self.reply(400, "text/plain", b"Refused: send the board's answer form.\n")
                return
            topic = form.get("topic", "")
            status, notice = 200, None
            try:
                with one_writer:
                    cards, _ = load_cards(cards_dir)
                    card = next((c for c in cards if c.file == form.get("card")), None)
                    if card is None:
                        raise AnswerRefused(f"no committed card named {form.get('card')!r}")
                    sha = write_answer(
                        cards_dir, card, form.get("verdict", ""), form.get("note", ""),
                        form.get("card_sha", ""), form.get("record_sha", ""),
                    )
                verdict = VERDICTS[form["verdict"]]
                where = card.fields["Owner record"] if form["verdict"] == "confirm" else "the card as a return"
                notice = ("written", f"Written and committed {sha[:7]}: {verdict} on {card.file}, recorded in {where}.")
            except (AnswerRefused, CardSourceError) as error:
                status, notice = 409, ("refused", str(error))
            except AnswerWrittenIndexStale as error:
                notice = ("written", f"Written: {error}")
            query = urlencode({"topic": topic, "card": form.get("card", "")})
            try:
                page = render_page(cards_dir, query, notice)
            except CardSourceError as error:
                page = f"Grill Board cannot read committed cards: {error}\n"
            self.reply(status, "text/html", page.encode("utf-8"))

        def reply(self, status, kind, payload):
            self.send_response(status)
            charset = "; charset=utf-8" if kind.startswith("text/") else ""
            self.send_header("Content-Type", kind + charset)
            self.send_header("Content-Length", str(len(payload)))
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
