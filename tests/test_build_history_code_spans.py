"""Historical authority cannot be created by removing Markdown examples (W)."""
import pytest

from ams import build_history as bh
from test_build_history_wiki_sources import relocated, page, PAGE, commit
from test_build_history import _git, _write, git_runner, StubSupabase, URL, FAKE_PUBLISHABLE
from test_build_history_wiki_sources import lifecycle


def set_example(repo, sha, location, transform):
    if location == "article":
        head, links = page(sha).split("\n\n[previous", 1)
        _write(repo, PAGE, head + "\n\n" + transform("[previous" + links))
    else:
        _write(repo, "workbench/wiki/MEMORY.md", transform("[Website](context-website.md)"))
    if _git(repo, "status", "--porcelain"):
        commit(repo, "Inline examples are not source declarations")


@pytest.mark.parametrize("location", ["article", "router"])
@pytest.mark.parametrize("delimiter", ["`", "``", "````"])
def test_multiline_code_examples_do_not_authorize_old_events(relocated, location, delimiter, capsys):
    repo, sha, original = relocated
    set_example(repo, sha, location, lambda links: "Example " + delimiter + "\n" + links + "\nend " + delimiter)
    expected = bh.record_rows(git_runner(repo), lifecycle)
    assert not any("#evidence-" in r["source_ref"] for r in expected)
    assert bh.readcheck(expected, URL, FAKE_PUBLISHABLE, StubSupabase(original)) == 1
    assert "extra: 8" in capsys.readouterr().out


@pytest.mark.parametrize("location", ["article", "router"])
@pytest.mark.parametrize("transform", [
    lambda links: "Example ``literal ` tick\n" + links + "\nend ``",
    lambda links: "Example `\n" + links + "\nend \\`",  # escapes are literal inside a span
    lambda links: "Example \\``\n" + links + "\nend `",  # escaped first tick, one remaining opener
    lambda links: "> Example `\n> " + links.replace("\n", "\n> ") + "\n> end `",
    lambda links: "> Example `\n" + links + "\nend `",  # lazy blockquote continuation
    lambda links: links.replace("](", "]`example`("),  # masking cannot join a false link
    lambda links: "> Example `\n" + links.replace("\n", "\n> ") + "\n> end `",
    lambda links: "> ```text\n> " + links.replace("\n", "\n> ") + "\n> ````",
    lambda links: "- ```text\n  " + links.replace("\n", "\n  ") + "\n  ````",
    lambda links: "Example `\n| " + links.replace("\n", "\n| ") + "\nend `",
    lambda links: "```text\n> ```\n" + links + "\n```",
    lambda links: r"Example \\`" + "\n" + links + "\nend `",
])
def test_exact_delimiters_and_container_spans_do_not_expose_examples(relocated, location, transform):
    repo, sha, _ = relocated
    set_example(repo, sha, location, transform)
    assert not any("#evidence-" in r["source_ref"]
                   for r in bh.record_rows(git_runner(repo), lifecycle))


@pytest.mark.parametrize("location", ["article", "router"])
@pytest.mark.parametrize("transform", [
    lambda links: "Example `unmatched\n" + links,
    lambda links: "Example ``unmatched\n" + links + "\nend `",
    lambda links: "Example \\`\n" + links + "\nend \\`",
    lambda links: "Example `unmatched\n\n" + links + "\nend `",
    lambda links: "Example `unmatched\n## New paragraph\n" + links + "\nend `",
])
def test_literal_backticks_and_block_boundaries_preserve_plain_declarations(relocated, location, transform):
    repo, sha, original = relocated
    set_example(repo, sha, location, transform)
    current = bh.record_rows(git_runner(repo), lifecycle)
    assert [r for r in current if "#evidence-" in r["source_ref"]] == [
        r for r in original if "#evidence-" in r["source_ref"]]


def test_code_text_cannot_be_removed_to_forge_an_exact_declaration_label(relocated):
    repo, sha, _ = relocated
    set_example(repo, sha, "article", lambda links: links.replace("previous", "prev`example`ious"))
    assert not any("#evidence-" in r["source_ref"]
                   for r in bh.record_rows(git_runner(repo), lifecycle))


@pytest.mark.parametrize("location", ["article", "router"])
@pytest.mark.parametrize("indent", ["    ", "\t"])
def test_indented_continuation_cannot_end_an_open_code_span(relocated, location, indent):
    repo, sha, _ = relocated
    set_example(repo, sha, location,
                lambda links: "Example `\n" + indent + "paragraph continuation\n" + links + "\nend `")
    assert not any("#evidence-" in r["source_ref"]
                   for r in bh.record_rows(git_runner(repo), lifecycle))


@pytest.mark.parametrize("location", ["article", "router"])
@pytest.mark.parametrize("prefix", ["    ", "\t", ">     "])
def test_new_indented_code_blocks_remain_non_declarations(relocated, location, prefix):
    repo, sha, _ = relocated
    set_example(repo, sha, location,
                lambda links: "\n".join(prefix + line for line in links.splitlines()))
    assert not any("#evidence-" in r["source_ref"]
                   for r in bh.record_rows(git_runner(repo), lifecycle))


@pytest.mark.parametrize("location", ["article", "router"])
@pytest.mark.parametrize("slashes", [0, 1, 2, 3, 4])
def test_escaped_brackets_are_literals_but_even_backslashes_keep_live_links(relocated, location, slashes):
    repo, sha, _ = relocated
    prefix = "\\" * slashes
    set_example(repo, sha, location, lambda links: prefix + links.replace("\n", "\n" + prefix))
    count = sum("#evidence-" in r["source_ref"] for r in bh.record_rows(git_runner(repo), lifecycle))
    assert count == (0 if slashes % 2 else 8)


@pytest.mark.parametrize("location", ["article", "router"])
@pytest.mark.parametrize("slashes", [0, 1, 2, 3])
def test_image_operator_and_escaped_literal_bang_are_distinct(relocated, location, slashes):
    repo, sha, _ = relocated
    prefix = "\\" * slashes + "!"
    set_example(repo, sha, location, lambda links: prefix + links.replace("\n", "\n" + prefix))
    count = sum("#evidence-" in r["source_ref"] for r in bh.record_rows(git_runner(repo), lifecycle))
    assert count == (8 if slashes % 2 else 0)


@pytest.mark.parametrize("location", ["article", "router"])
@pytest.mark.parametrize("marker", ["2. continuation", "- ", "1234567890. continuation"])
def test_literal_list_like_continuations_do_not_end_open_code_spans(relocated, location, marker):
    repo, sha, _ = relocated
    set_example(repo, sha, location,
                lambda links: "Example `\n" + marker + "\n" + links + "\nend `")
    assert not any("#evidence-" in r["source_ref"]
                   for r in bh.record_rows(git_runner(repo), lifecycle))


@pytest.mark.parametrize("location", ["article", "router"])
@pytest.mark.parametrize("marker", ["1. new list", "001. new list", "- new list"])
def test_real_list_interruptions_keep_ordinary_declarations_visible(relocated, location, marker):
    repo, sha, _ = relocated
    set_example(repo, sha, location,
                lambda links: "Example `unmatched\n" + marker + "\n" + links + "\nend `")
    assert sum("#evidence-" in r["source_ref"]
               for r in bh.record_rows(git_runner(repo), lifecycle)) == 8
