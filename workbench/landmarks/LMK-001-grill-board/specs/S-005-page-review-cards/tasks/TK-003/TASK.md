# TK-003 - Returns, ratings and too-taxing flags on page cards are appended to the committed voice and taste record, and every page card names its version

**Task ID:** TK-003
**Spec ID:** S-005
**Slice:** Returns, ratings and too-taxing flags on page cards are appended to the committed voice and taste record, and every page card names its version
**Status:** blocked
**Blockers:** TK-001
**Destination:** spec-acceptance: Criticism becomes the voice record; Agents cite it
**Planned verification:** pytest that criticism lands in the voice record in the same commit

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Nothing in `site/` changes.

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), `grill-board/README.md` (answers, rating and flag), DDR-000J, DDR-000X, ADR-002U, the TK-001 generator and `src/ams/grill_board/answers.py`.

Owner intent, relayed 2026-11-01: criticism becomes the voice and taste record that feeds the loop. The owner's voice is not prose the owner writes; it is the owner's recorded feedback.

Deliver:

1. **Record.** `grill-board/voice-and-taste.md`, with a `**Version:**` counter and an append-only `## Entries` section. Each entry names the date (UTC), page path, content hash, card, kind (`Rework wording`, `Change the why`, `Change`, rating N of 5, too taxing) and the owner's note verbatim as a quote, sourced to the card.
2. **Same commit.** On a page card, a return, a rating or a flag writes the card section and the voice entry, and increments the version, in one commit through the board's lock and compare-and-swap. The voice record's SHA-256 is checked like the owning record's: a change since render refuses and writes nothing. Confirm adds no voice entry, and cards that are not page cards are unchanged.
3. **Version stamp.** The generator writes `**Voice record:** grill-board/voice-and-taste.md version N` on each new page card; an open page card made before this Task gets an appended `## Voice record` section. Existing sections are never edited.

Tell orchestrator A the record's path, so A adds the pointer from the site's contributing notes on `dev` and cites the version when drafting. Do not edit `site/`.

Out of scope: comparing ratings across pages (S-002 loop); applying criticism to a page (orchestrator A, in a new candidate); approval rows (TK-002).

Hand back to S-005 with `close`.

## Acceptance

- [ ] In a temporary Git repository, a return with a note, a rating with a comment and a flag on a fixture page card each append one voice entry with page, hash, date and verbatim note in the same commit as the card section, and increment the version.
- [ ] Must fail: criticism on a page card whose commit leaves the voice record unchanged fails the test.
- [ ] Editing the voice record after render makes the write refuse; card and record stay byte-identical.
- [ ] Must fail: an open page card that names no voice record version fails the test.
- [ ] `uv run pytest` passes; render and doctor show no blocking finding.
