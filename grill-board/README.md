# Grill Board

The owner's local attention queue: one page of committed cards that wait on the owner (DDR-000L, DDR-000P). Start it from the repository root with `uv run ams-board`; it serves on 127.0.0.1 only. Spec: S-004.

## Cards

One Markdown file per question in `cards/`, read from the committed snapshot (HEAD) only. Format: [card-example.md](card-example.md). Required header fields are `Priority`, `Priority reason`, `Value` and `Value reason` (DDR-000K); a card missing one is refused and listed in the heat-colored alert, never shown.

Optional header fields the page shows:

| Field | Shown as |
|---|---|
| `Topic` | The topic in the left rail; cards without one go under "Other topics" |
| `Why it matters` | The yellow "Why this choice matters" box |
| `Recommendation` | The green "Agent recommendation" box; the text Confirm writes |
| `Owner record` | The repository-relative file the confirmed answer is written into |
| `Write after` | One exact, unique line in that record; the answer is inserted below it |

Text below the header is shown as Context. A card without `Owner record`, `Write after` and `Recommendation` can be returned but not confirmed; the page says which is missing.

## Answers

The verdict buttons and note POST to `/answer` (ADR-000B, ADR-002U, S-004 TK-002).

- **Confirm** inserts ``**Owner answer (DATE, Grill Board card `NAME`):** Confirmed: RECOMMENDATION``, and the note as a quote, below the `Write after` line of the `Owner record`. No second confirmation.
- **Rework wording**, **Change the why** and **Change** are returns: they need a note and write only the card. To re-ask, an agent posts the reworked card as a new file.
- Every verdict appends a `## Answer` section to the card (`Verdict`, `Answered` in UTC, then `Written to` or `Returned: yes`, then the note). An answered card leaves the queue and counts as answered. Nothing is deleted or renumbered.

**Commits.** The server makes one Git commit per answer, rating or flag on the current branch, containing only the card and, for Confirm, the owning record. It builds the commit in a throwaway index on the commit it checked, then moves the branch with `git update-ref HEAD NEW CHECKED`, so a commit that landed meanwhile makes it refuse and restore both files. It runs no commit hooks. The subject reads like `Grill Board: confirm NAME into PATH`. Other staged or unstaged work is left alone and not committed. Every board instance on a checkout shares one writer lock (`flock` on `ams-grill-board.lock` in the Git directory), held from the hash check through the commit, so a second writer sees the first one's change and refuses. It refuses on a detached HEAD; if the commit fails, both files are put back to their committed bytes.

**Refusals** (nothing written; the page shows "Not written: ..." in the heat alert):

- The card or owning record changed since the page showed it: the page carries each file's SHA-256 at HEAD, captured at render, and the write compares them.
- Either file has uncommitted changes.
- The owning path is absolute, uses `..` or `.`, names `.git`, goes through a symlink, resolves outside the repository, or is not a committed regular file.
- The card names itself as its owning record.
- The `Write after` line is missing or appears more than once; the card is already answered; a return has no note.
- A rating is not a whole number from 1 to 5; the card is already flagged; an answer targets a flagged card.
- The POST does not come from the board's own page: the `Host` must be `127.0.0.1:PORT` and the `Origin` (or, without one, the `Referer`) that same origin; otherwise 403.

## Rating and flag

Each is one click on the open card, with an optional comment, and is saved on the card through the same write path as answers (DDR-000J, S-004 TK-003). Answered cards stay reachable by link after the answer, so they can still be rated or flagged.

- A star POSTs to `/rate` and appends `## Rating`, `**Rating:** N of 5`, `**Rated:**` in UTC, then the comment as a quote. A new rating is appended; the last one stands.
- **Too taxing** POSTs to `/flag` and appends `## Flag`, `**Too taxing:** yes`, `**Flagged:**` in UTC, then the comment. A flagged card leaves the queue, held for rewrite, and cannot be answered or flagged again.
- Each is one commit of the card alone, subject `Grill Board: rate NAME N of 5` or `Grill Board: flag NAME too taxing`. These committed sections are what the RSI loop reads (S-002).

**Re-asking.** An agent posts the rewrite as a new card file. The page lists as refused, never asks, a card that repeats a flagged question line (ignoring case and spacing), or a card that was flagged and whose flag is gone. Flags are read from every flag commit in the branch history, so a copy, a deletion or a reverted flag does not bring the question back.

## Layout and theme

The page follows the owner's "Grilling Board Redesign" artifact, version 1793538932-43c3 ([DDR-000Y](../workbench/docs/ddr/000Y-the-grill-board-theme-follows-the-grilling-board-redesign-artifact.md)): topics on the left, ordered by their most urgent card; that topic's queue in the middle, sorted by Priority then Value; the open card on the right. Pick a topic or card by link (`/?topic=...&card=...`). Columns stack below about 1,250px and hold at 375px.

Dark is the default; the system preference picks light, and the header toggle overrides it in this browser.

- Token values: [theme/tokens.json](theme/tokens.json), the single source. `src/ams/grill_board/static/board.css` repeats them and `tests/test_grill_board_theme.py` fails on any difference, on a color outside the list, or on a color with two meanings.
- Fonts: IBM Plex Sans, IBM Plex Mono and Zilla Slab (latin, @fontsource 5.3.0, SIL Open Font License; licenses beside the files in `src/ams/grill_board/static/fonts/`). The page loads nothing from another host.

## QA screenshots

`qa/` holds the artifact beside the built board, dark and light, and the board at 375px. Regenerate with a local copy of the artifact (not in this repository):

```bash
uv run --with playwright python grill-board/qa/capture.py --artifact PATH/TO/ARTIFACT
```

Both pages render the generic fixture cards in `tests/fixtures/grill_board/showcase/`, so no artifact sample text is published. The script fails if the board requests any host but its own or scrolls sideways.

Differences from the artifact, by choice: the artifact's other Dashboard sections, search, filters, batch, rounds, lanes other than "To answer", a flags view and history are left out until real records back them; queue rows also show each grade's reason, because DDR-000K keeps reasons on every card; the brand reads "AMS · Grill Board".
