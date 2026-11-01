"""Capture the Grill Board QA screenshots: the design artifact beside the built
board, dark and light, plus the board at 375px.

    uv run --with playwright python grill-board/qa/capture.py --artifact DIR

DIR holds a local copy of the "Grilling Board Redesign" artifact (Board.dc.html).
The artifact is rendered with its own template and styles but with the same
generic fixture cards the board shows, so no artifact sample text is published.
Fonts the artifact requests from Google are answered from the board's own
self-hosted files, so neither page reaches another host.
"""

import argparse
import base64
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from ams.grill_board.cards import load_cards  # noqa: E402
from ams.grill_board.server import STATIC, make_server, topic_of  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "grill_board" / "showcase"
OUT = Path(__file__).resolve().parent
DESKTOP = {"width": 1440, "height": 1000}
PHONE = {"width": 375, "height": 812}

# A tiny stand-in for the artifact's component runtime (support.js is not part
# of the local copy): it evaluates the Component class, swaps in fixture data
# and expands {{...}}, <sc-for> and <sc-if> in the template.
RENDER = r"""
([props, items, topics]) => {
  class DCLogic { constructor(p) { this.props = p || {}; this.state = {}; } setState(s) { Object.assign(this.state, s); } }
  const source = document.querySelector('script[type="text/x-dc"]').textContent;
  const Component = new Function('DCLogic', source + '; return Component;')(DCLogic);
  Component.prototype.items = () => items;
  Component.prototype.topicsData = () => topics;
  const c = new Component(props);
  Object.assign(c.state, { sel: items[0].id, topic: topics[0].key, lane: 'open' });
  const vals = c.renderVals();
  const root = document.querySelector('x-dc');
  const helmet = root.querySelector('helmet');
  for (const node of [...helmet.childNodes]) document.head.appendChild(node);
  helmet.remove();
  const look = (scope, path) => path.trim().split('.').reduce((v, k) => (v == null ? v : v[k]), scope);
  const fill = (text, scope) => text.replace(/\{\{([^}]+)\}\}/g, (_, p) => { const v = look(scope, p); return v == null ? '' : String(v); });
  const expand = (node, scope) => {
    if (node.nodeType === 3) return [document.createTextNode(fill(node.textContent, scope))];
    if (node.nodeType !== 1) return [];
    const tag = node.tagName.toLowerCase();
    const kids = (n, s) => [...n.childNodes].flatMap((k) => expand(k, s));
    if (tag === 'sc-for') {
      const list = look(scope, node.getAttribute('list').replace(/[{}]/g, '')) || [];
      const as = node.getAttribute('as');
      return list.flatMap((item) => kids(node, { ...scope, [as]: item }));
    }
    if (tag === 'sc-if') return look(scope, node.getAttribute('value').replace(/[{}]/g, '')) ? kids(node, scope) : [];
    const out = node.cloneNode(false);
    for (const attr of [...out.attributes]) {
      if (/^on/i.test(attr.name) || attr.name.startsWith('hint-')) { out.removeAttribute(attr.name); continue; }
      if (attr.value.includes('{{')) {
        const value = fill(attr.value, scope);
        if (['checked', 'selected', 'disabled'].includes(attr.name) && value !== 'true') out.removeAttribute(attr.name);
        else out.setAttribute(attr.name, value);
      }
    }
    for (const k of kids(node, scope)) out.appendChild(k);
    return [out];
  };
  const rendered = [...root.childNodes].flatMap((n) => expand(n, vals));
  root.replaceWith(...rendered);
}
"""


def fixture_repo(workdir):
    cards = workdir / "cards"
    shutil.copytree(FIXTURE, cards)
    run = lambda *a: subprocess.run(["git", "-c", "user.name=qa", "-c", "user.email=qa@example.invalid", *a], cwd=workdir, check=True, capture_output=True)
    run("init", "-q")
    run("add", "-A")
    run("commit", "-q", "-m", "fixture cards")
    return cards


def artifact_data(cards):
    """The board's fixture cards in the artifact's own data shape."""
    keys, topics, items = {}, [], []
    for card in cards:
        name = topic_of(card)
        if name not in keys:
            keys[name] = f"t{len(keys)}"
            topics.append({"key": keys[name], "label": name, "frame": "", "goal": "", "done": 0, "total": 0})
        next(t for t in topics if t["label"] == name)["total"] += 1
        items.append({
            "id": card.file, "topic": keys[name], "lane": "pending", "p": card.priority, "v": card.value,
            "scale": "Spec", "kind": "Explore / settle decisions", "rev": 1,
            "short": card.question, "title": card.question, "pWhy": card.priority_reason, "vWhy": card.value_reason,
            "q": card.context or card.question, "why": card.fields.get("Why it matters", ""),
            "rec": card.fields.get("Recommendation", ""), "concerns": [], "wiki": [], "changes": "", "impact": "",
            "history": "", "historyCount": "0 earlier revisions", "options": [],
        })
    return items, topics


def font_css():
    css = (STATIC / "board.css").read_text()
    faces = "\n".join(re.findall(r"@font-face\{[^}]+\}", css))
    inline = lambda m: "url(data:font/woff2;base64," + base64.b64encode((STATIC / m.group(1)).read_bytes()).decode() + ")"
    return re.sub(r"url\(/static/([^)]+)\)", inline, faces)


def capture(artifact_dir):
    with tempfile.TemporaryDirectory() as tmp:
        cards_dir = fixture_repo(Path(tmp))
        cards, _ = load_cards(cards_dir)
        items, topics = artifact_data(cards)
        server = make_server(cards_dir, port=0)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        board_url = f"http://127.0.0.1:{server.server_address[1]}/"
        hosts = set()
        try:
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch()
                except Exception:  # no bundled browser: use the installed Chrome
                    browser = p.chromium.launch(channel="chrome")
                for theme in ("dark", "light"):
                    shots = {}
                    page = browser.new_page(viewport=DESKTOP, color_scheme=theme)
                    page.route("**/*", lambda route: route.fulfill(status=200, content_type="text/css", body=font_css())
                               if "fonts.googleapis" in route.request.url
                               else route.abort() if route.request.url.endswith("support.js") or "gstatic" in route.request.url
                               else route.continue_())
                    page.goto((Path(artifact_dir) / "Board.dc.html").as_uri())
                    page.evaluate(RENDER, [{"theme": theme, "banner": False, "error": False, "answerState": "none"}, items, topics])
                    page.wait_for_timeout(400)
                    shots["artifact"] = page.screenshot()
                    page.close()
                    for size, name in ((DESKTOP, "board"), (PHONE, "phone")):
                        page = browser.new_page(viewport=size, color_scheme=theme)
                        page.on("request", lambda request: hosts.add(request.url.split("/")[2]))
                        page.goto(board_url)
                        page.wait_for_load_state("networkidle")
                        width = page.evaluate("document.documentElement.scrollWidth")
                        assert width <= size["width"], f"{name} {theme}: page is {width}px wide"
                        shots[name] = page.screenshot(full_page=name == "phone")
                        page.close()
                    (OUT / f"board-375-{theme}.png").write_bytes(shots["phone"])
                    pair = browser.new_page(viewport={"width": DESKTOP["width"] * 2 + 24, "height": DESKTOP["height"] + 56})
                    img = lambda b: "data:image/png;base64," + base64.b64encode(b).decode()
                    pair.set_content(f"""<body style="margin:0;background:#808080;font:600 15px sans-serif;color:#000000">
<div style="display:flex;gap:24px;padding:0">
<figure style="margin:0"><figcaption style="padding:8px">Artifact ({theme}), fixture data</figcaption><img src="{img(shots['artifact'])}"></figure>
<figure style="margin:0"><figcaption style="padding:8px">Built board ({theme}), same fixture</figcaption><img src="{img(shots['board'])}"></figure>
</div></body>""")
                    (OUT / f"side-by-side-{theme}.png").write_bytes(pair.screenshot(full_page=True))
                    pair.close()
                browser.close()
        finally:
            server.shutdown()
            server.server_close()
        assert hosts == {f"127.0.0.1:{server.server_address[1]}"}, f"the board reached other hosts: {hosts}"
        print("hosts the board requested:", sorted(hosts))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--artifact", required=True, help="folder holding Board.dc.html")
    capture(parser.parse_args().artifact)
    for path in sorted(OUT.glob("*.png")):
        print(path.relative_to(ROOT))
