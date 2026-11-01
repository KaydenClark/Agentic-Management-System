"""The Grill Board's local HTTP server: one page, read from card files on
every request, served on 127.0.0.1 only (DDR-000L, DDR-000P)."""

import argparse
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .cards import PRIORITIES, VALUES, load_cards

HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_CARDS = Path("grill-board") / "cards"

STYLE = """
body { font: 16px/1.5 system-ui, sans-serif; max-width: 48rem; margin: 2rem auto;
  padding: 0 1rem; background: #fff; color: #111; }
ol { list-style: none; padding: 0; }
.card, .refusal { border: 1px solid #999; border-radius: 6px; padding: 0.75rem 1rem;
  margin: 0 0 1rem; }
.card h2 { font-size: 1.1rem; margin: 0 0 0.5rem; }
dl { display: grid; grid-template-columns: max-content 1fr; gap: 0.25rem 1rem; margin: 0; }
dt { font-weight: 600; }
dd { margin: 0; }
.context { white-space: pre-wrap; margin: 0.5rem 0 0; }
.file { font-size: 0.85rem; }
"""


def render_card(card):
    context = f'<p class="context">{escape(card.context)}</p>' if card.context else ""
    return f"""<li class="card">
<h2 data-field="question">{escape(card.question)}</h2>
<dl>
<dt>Priority</dt><dd><strong data-field="priority">{escape(card.priority)}</strong> {escape(PRIORITIES[card.priority])}: <span data-field="priority-reason">{escape(card.priority_reason)}</span></dd>
<dt>Value</dt><dd><strong data-field="value">{escape(card.value)}</strong> {escape(VALUES[card.value])}: <span data-field="value-reason">{escape(card.value_reason)}</span></dd>
</dl>
{context}<p class="file"><code>{escape(card.file)}</code></p>
</li>"""


def render_page(cards_dir):
    cards, refusals = load_cards(cards_dir)
    body = "\n".join(render_card(card) for card in cards) or "<li>No cards wait on you.</li>"
    refused = ""
    if refusals:
        items = "\n".join(
            f'<li class="refusal"><code>{escape(r.file)}</code>: {escape("; ".join(r.problems))}</li>'
            for r in refusals
        )
        refused = f"<section><h2>Refused cards ({len(refusals)})</h2>\n<p>These files are not shown until fixed.</p>\n<ul>\n{items}\n</ul></section>"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grill Board</title><style>{STYLE}</style></head>
<body><h1>Grill Board</h1>
<p>{len(cards)} card(s), sorted by Priority, then Value.</p>
<ol>
{body}
</ol>
{refused}
</body></html>
"""


def make_server(cards_dir, port=DEFAULT_PORT):
    cards_dir = Path(cards_dir)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path not in ("/", "/index.html"):
                self.send_error(404)
                return
            payload = render_page(cards_dir).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
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
    if not args.cards.is_dir():
        parser.error(f"card directory not found: {args.cards} (run from the repository root or pass --cards)")
    server = make_server(args.cards, args.port)
    print(f"Grill Board: http://{HOST}:{server.server_address[1]}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
