"""S-004 TK-004 and TK-000A: the board's colors are the documented tokens,
each with one meaning, served exactly as grill-board/theme/tokens.json says,
in the artifact's layout, with nothing loaded from another host."""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

import urllib.error
import urllib.request

import pytest

from test_grill_board import FIXTURES, ROOT, board, get  # noqa: F401  (fixture reuse)

TOKENS = json.loads((ROOT / "grill-board" / "theme" / "tokens.json").read_text())
NAMES = [
    "--ground", "--surface", "--raised", "--line", "--line-strong", "--muted", "--ink", "--pole",
    "--heat", "--worth", "--owner", "--agent", "--returned", "--soft-pct", "--line-pct", "--dot-pct",
]
HUES = ["--heat", "--worth", "--owner", "--agent", "--returned"]
COLOR_TOKENS = [name for name in NAMES if not name.endswith("-pct")]
THEME_SELECTORS = {
    ':root,:root[data-theme="dark"]': "dark",
    ':root[data-theme="light"]': "light",
    ":root:not([data-theme])": "light",
}
LITERAL_COLOR = re.compile(
    r"#[0-9A-Fa-f]{3,8}\b|\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch)\(|"
    r"\b(?:white|black|red|green|blue|yellow|orange|purple|gray|grey)\b(?![-\w])",
)


def squash(value):
    return re.sub(r"\s+", "", value)


def css_blocks(css):
    """[(selector, {custom property: value})] for every rule declaring one."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    blocks = []
    for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        props = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+)", body))
        if props:
            blocks.append((squash(selector.replace("@media (prefers-color-scheme: light){", "")), props))
    return blocks


class Resources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls, self.styles, self.disabled = [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("src", "href", "action", "poster", "srcset"):
            if attrs.get(key):
                self.urls.append(attrs[key])
        if attrs.get("style"):
            self.styles.append(attrs["style"])
        if "disabled" in attrs:
            self.disabled.append(attrs.get("class") or tag)


@pytest.fixture
def served(board):
    server = board(FIXTURES / "showcase")
    _, html = get(server)
    _, css = get(server, "/static/board.css")
    _, js = get(server, "/static/theme.js")
    return server, html, css, js


def test_tokens_json_has_the_contract_shape():
    assert TOKENS["source"] == {"artifact": "Grilling Board Redesign", "version": "1793538932-43c3"}
    assert set(TOKENS) == {"source", "themes", "meanings", "mixes"}
    for theme in ("dark", "light"):
        assert list(TOKENS["themes"][theme]) == NAMES
    assert TOKENS["themes"]["dark"]["--soft-pct"] == "22%"  # Main.dc.html v2.2, not Board.dc.html's 24%
    assert set(TOKENS["mixes"]) == {".tone", ".h-heat", ".h-worth", ".h-owner", ".h-agent", ".h-returned", ".h-none"}


MIX_NAMES = ["--on", "--tone-soft", "--tone-ink", "--tone-line", "--tone-dot"]


def test_every_token_has_exactly_one_meaning_and_no_meaning_two_tokens():
    meanings = TOKENS["meanings"]
    assert list(meanings) == NAMES + MIX_NAMES
    assert list(TOKENS["mixes"][".tone"]) == MIX_NAMES
    assert all(isinstance(text, str) and text.strip() for text in meanings.values())
    assert len(set(meanings.values())) == len(meanings), "two tokens share a meaning"


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_no_color_carries_two_meanings_within_a_theme(theme):
    values = [TOKENS["themes"][theme][name].upper() for name in COLOR_TOKENS]
    assert len(set(values)) == len(values), f"{theme}: one color value serves two tokens"
    for hue in HUES:
        assert re.fullmatch(r"#[0-9A-F]{6}", TOKENS["themes"][theme][hue].upper())


def test_every_served_custom_property_equals_tokens_json(served):
    _, _, css, _ = served
    seen = set()
    for selector, props in css_blocks(css):
        if selector in THEME_SELECTORS:
            theme = THEME_SELECTORS[selector]
            assert props == TOKENS["themes"][theme], f"{selector} differs from tokens.json {theme}"
            seen.add(selector)
        elif selector in TOKENS["mixes"]:
            assert {k: squash(v) for k, v in props.items()} == {
                k: squash(v) for k, v in TOKENS["mixes"][selector].items()
            }, f"{selector} differs from tokens.json mixes"
            seen.add(selector)
        else:
            pytest.fail(f"{selector} declares custom properties outside tokens.json: {props}")
    assert seen == set(THEME_SELECTORS) | set(TOKENS["mixes"])


def test_a_drifted_token_fails_the_comparison(served):
    _, _, css, _ = served
    drifted = css.replace("--heat:#FF5A1F", "--heat:#FF0000", 1)
    dark = dict(css_blocks(drifted))[':root,:root[data-theme="dark"]']
    assert dark != TOKENS["themes"]["dark"]


def test_no_color_is_used_outside_the_token_list(served):
    _, html, css, js = served
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    without_tokens = re.sub(r"--[\w-]+\s*:\s*[^;}]+", "", css)
    assert not LITERAL_COLOR.findall(without_tokens), "CSS uses a color that is not a token"
    parsed = Resources()
    parsed.feed(html)
    for style in parsed.styles:
        assert not LITERAL_COLOR.findall(style), f"inline style uses a raw color: {style}"
    assert not re.search(r"#[0-9A-Fa-f]{3,8}\b", js)
    known = set(NAMES) | {"--hue"} | {k for mix in TOKENS["mixes"].values() for k in mix}
    for name in re.findall(r"var\((--[\w-]+)", css + html):
        assert name in known, f"{name} is not a documented token or mix"


def test_the_page_loads_nothing_from_another_host(served):
    server, html, css, js = served
    for text in (html, css, js):
        assert "http://" not in text and "https://" not in text
        assert "googleapis" not in text and "gstatic" not in text
    parsed = Resources()
    parsed.feed(html)
    assert parsed.urls
    for url in parsed.urls:
        assert url.startswith("/") and not url.startswith("//"), url
    for url in re.findall(r"url\(([^)]+)\)", css):
        assert url.strip("'\"").startswith("/static/"), url
        host, port = server.server_address[:2]
        with urllib.request.urlopen(f"http://{host}:{port}{url.strip(chr(39) + chr(34))}", timeout=5) as response:
            assert response.status == 200 and response.read(4) == b"wOF2"


def test_the_three_fonts_are_self_hosted_and_licensed(served):
    server, _, css, _ = served
    for family in ("IBM Plex Sans", "IBM Plex Mono", "Zilla Slab"):
        assert f"font-family:'{family}'" in css
    assert "Pirata" not in css
    fonts = ROOT / "src" / "ams" / "grill_board" / "static" / "fonts"
    for name in ("ibm-plex-sans", "ibm-plex-mono", "zilla-slab"):
        assert "SIL Open Font License" in (fonts / f"LICENSE-{name}.txt").read_text()
    host, port = server.server_address[:2]
    with urllib.request.urlopen(f"http://{host}:{port}/static/fonts/zilla-slab-latin-700-normal.woff2") as response:
        assert response.headers["Content-Type"] == "font/woff2"
        assert response.read(4) == b"wOF2"


def test_static_paths_outside_the_folder_are_not_found(served):
    server, _, _, _ = served
    for path in ("/static/../server.py", "/static/%2e%2e/server.py", "/static/missing.css"):
        with pytest.raises(urllib.error.HTTPError) as error:
            get(server, path)
        assert error.value.code == 404


def test_topics_first_layout_with_the_open_card(served):
    server, html, _, _ = served
    for landmark in ('class="rail"', 'class="queue"', 'class="open"', 'class="theme-toggle"'):
        assert landmark in html
    rail = html.split('class="topics"', 1)[1].split("</div>\n<section", 1)[0]
    assert [t for t in re.findall(r'topic-label">([^<]+)<', rail)] == ["Board layout", "Other topics", "Card format"]
    assert "Why this choice matters" in html and "tone h-worth" in html
    assert "Agent recommendation" in html and "tone h-agent" in html
    _, other = get(server, "/?topic=Card+format")
    assert "may a card name an optional topic" in other.split('class="open"', 1)[1]
    _, picked = get(server, "/?topic=Board+layout&card=c-grade4.md")
    assert "may a backlog card stay" in picked.split('class="open"', 1)[1]
    assert 'class="grade n4"' in picked


def test_verdicts_rating_and_flag_are_live(served):
    _, html, _, _ = served
    parsed = Resources()
    parsed.feed(html)
    joined = " ".join(parsed.disabled)
    # The showcase card names no owning record, so Confirm is off and says why; everything else is live.
    assert joined == "verdict confirm tone h-agent"
    assert "Confirm needs this card to name its Owner record" in html
    assert '<form class="answer" method="post" action="/answer">' in html
    assert '<form class="rating" method="post" action="/rate">' in html and 'formaction="/flag"' in html
    assert "Not wired yet" not in html


def test_theme_follows_the_system_and_has_a_toggle(served):
    _, html, css, js = served
    assert "@media (prefers-color-scheme: light)" in css
    assert 'data-theme-toggle' in html and "localStorage" in js
    assert '<meta name="viewport" content="width=device-width, initial-scale=1">' in html
    assert "@media (max-width: 560px)" in css
