# Grill Board

The owner's local attention queue: one page of committed cards that wait on the owner (DDR-000L, DDR-000P). Start it from the repository root with `uv run ams-board`; it serves on 127.0.0.1 only. Spec: S-004.

## Current owner queue

The Python board reads explicit owner requests from committed Spec, Task and
Landmark records on each visit. An open page checks for changes every five
seconds and updates automatically, preserving any unsaved note. No generator or
owner-requested refresh is needed. Existing card files remain supported.

Agents publish a self-contained question in its owning record before reporting
that work needs an owner answer. Use the native queue commands from the repo root:

```sh
uv run ams-board add --record workbench/specs/S-001-example/SPEC.md --file request.json --by AGENT
uv run ams-board revise --record workbench/specs/S-001-example/SPEC.md --file request.json --by AGENT --reason "What changed and why"
uv run ams-board pending --json
uv run ams-board status --json
```

The input is a single JSON object, for example:

```json
{
  "schema": "grill-board/request@1",
  "key": "event-location",
  "question": "Should we hold the event in the library?",
  "recommendation": "Hold the event in the library within the existing budget.",
  "priority": "P2",
  "priority_reason": "The venue must be settled before invitations go out.",
  "value": "V1",
  "value_reason": "The venue meets the requirements at low cost.",
  "topic": "The event",
  "context": "Availability and accessibility are confirmed."
}
```

`add` appends a `grill-board` JSON fence under `## Owner requests` in that
record and commits only the record. `revise` keeps its key, requires a reason and
preserves prior answers. Repeating an identical revision writes nothing. Inputs
are one-line text; context obeys the existing short-note contract. Optional
`why`, full `candidate` SHA and `blocker` name provide relevant context. A request
withdrawn with `state: "withdrawn"` leaves the queue with its history preserved;
use `revise` with the actual reason. Completed/retired records are not pending.
Requests in quoted examples or archived records are not live questions.

The board projects the question directly: no card file is prepared on a read.
Its stable identity is the record path plus request key; its wording has a
content-bound revision. An owner action materializes its response card in the
same locked, compare-and-swap transaction used by existing cards. Confirm writes
the exact recommendation and note into the source record; returns keep their
exact note on the response card for agents to read with `pending`. Earlier
answers remain history after a decision revision; they never confirm changed wording.
Changing only Priority, Value or topic preserves the settled decision and displays
the current grades without rewriting its answer.

A declared owner hold without a published question is shown as an agent
preparation issue, not invented as an approval request. Deliberate Prepare stops
stay stopped. Invalid/unreadable sources show an error rather than a reassuring
empty queue. Agents consume actual answers through the existing owning lifecycle;
a board answer never fabricates independent Review, Human QA, formal Spec
approval or publication. Do not submit answers on the owner's behalf.

This adapts the established queue/revision/answer workflow in
[LLM_Workbench at 9d5e1f25](https://github.com/KaydenClark/LLM_Workbench/blob/9d5e1f25b0d5870589ae1c5752f27f42acb796ef/workbench/grill-board/README.md)
to AMS's Python backend and existing committed-card writer.

## Cards

One Markdown file per question in `cards/`, read from the committed snapshot (HEAD) only. Format: [card-example.md](card-example.md). Required header fields are `Priority`, `Priority reason`, `Value` and `Value reason` (DDR-000K); a card missing one is refused and listed in the heat-colored alert, never shown.

Optional header fields the page shows:

| Field | Shown as |
|---|---|
| `Topic` | The topic in the left rail; cards without one go under "Other topics" |
| `Why it matters` | The yellow "Why this choice matters" box |
| `Recommendation` | The green "Agent recommendation" box; the text Confirm writes |
| `Owner record` | The repository-relative record the confirmed answer is written into; it must be a record (below) |
| `Write after` | One exact, unique line in that record; the answer is inserted below it |

**Owner records.** Confirm writes only into a `.md` file under `workbench/specs/`, `workbench/landmarks/`, `workbench/docs/adr/`, `workbench/docs/ddr/` or `workbench/wiki/`, or into `grill-board/page-approvals.md`, matched exactly, case included (S-004 TK-000G). Everything else is refused before any write: workflows (`.github/`), code (`src/`, `site/`, `supabase/`), config (`pyproject.toml`, `uv.lock`, `*.json`) and root controls such as `AGENTS.md`. The page disables Confirm for such a card.

Text below the header is shown as Context. **Not a drafting surface** (TK-000I): Context is a short note of at most 1,000 characters, with no Markdown heading (`#` to `######`, or a `===` underline) and no `---` line (front matter, a rule or a heading underline). A card whose Context breaks that rule is page content and is refused, listed in the alert, never shown; post the page elsewhere and ask only the question about it. A card without `Owner record`, `Write after` and `Recommendation` can be returned but not confirmed; the page says which is missing.

## Answers

The verdict buttons and note POST to `/answer` (ADR-000B, ADR-002U, S-004 TK-002).

- **Confirm** inserts ``**Owner answer (DATE, Grill Board card `NAME`):** Confirmed: RECOMMENDATION``, and the note as a quote, below the `Write after` line of the `Owner record`. No second confirmation.
- **Rework wording**, **Change the why** and **Change** are returns: they need a note and write only the card. To re-ask, an agent posts the reworked card as a new file.
- Every verdict appends a `## Answer` section to the card (`Verdict`, `Answered` in UTC, then `Written to` or `Returned: yes`, then the note). An answered card leaves the queue and counts as answered. Nothing is deleted or renumbered.

**Commits.** The server makes one Git commit per answer, rating or flag on the current branch, containing only the card and, for Confirm, the owning record. It builds the commit in a throwaway index on the commit it checked, then moves the branch with `git update-ref HEAD NEW CHECKED`, so a commit that landed meanwhile makes it refuse and restore both files. It runs no commit hooks. The subject reads like `Grill Board: confirm NAME into PATH`. Other staged or unstaged work is left alone and not committed. Every board instance on a checkout shares one writer lock (`flock` on `ams-grill-board.lock` in the Git directory), held from the hash check through the commit, so a second writer sees the first one's change and refuses. It refuses on a detached HEAD; if the commit fails, both files are put back to their committed bytes.

**Refusals** (nothing written; the page shows "Not written: ..." in the heat alert):

- The card or owning record changed since the page showed it: the page carries each file's SHA-256 at HEAD, captured at render, and the write compares them.
- Either file has uncommitted changes.
- The owning path is absolute, uses `..` or `.`, names `.git`, is not an owner record (above), goes through a symlink, resolves outside the repository, or is not a committed regular file.
- The card names itself as its owning record.
- The `Write after` line is missing or appears more than once; the card is already answered; a return has no note.
- A rating is not a whole number from 1 to 5; the card is already flagged; an answer targets a flagged card.
- The POST does not come from the board's own page: the `Host` must be `127.0.0.1:PORT` and the `Origin` (or, without one, the `Referer`) that same origin; otherwise 403.

## Rating and flag

Each is one click on the open card, with an optional comment, and is saved on the card through the same write path as answers (DDR-000J, S-004 TK-003). Answered cards stay reachable by link after the answer, so they can still be rated or flagged.

- A star POSTs to `/rate` and appends `## Rating`, `**Rating:** N of 5`, `**Rated:**` in UTC, then the comment as a quote. A new rating is appended; the last one stands.
- **Too taxing** POSTs to `/flag` and appends `## Flag`, `**Too taxing:** yes`, `**Flagged:**` in UTC, then the comment. A flagged card leaves the queue, held for rewrite, and cannot be answered or flagged again.
- Each is one commit of the card alone, subject `Grill Board: rate NAME N of 5` or `Grill Board: flag NAME too taxing`. These committed sections are what the RSI loop reads (S-002).

**Re-asking.** An agent posts the rewrite as a new card file. The page lists as refused, never asks, a card that repeats a flagged question line, compared after Unicode NFKC, removing format characters (Unicode category Cf, such as zero-width spaces and joiners), reading punctuation as spacing, folding case and collapsing spacing (TK-000H), or a card that was flagged and whose flag is gone. Flags are read from every flag commit in the branch history, so a copy, a deletion or a reverted flag does not bring the question back.

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

Both pages render the generic fixture cards in `tests/fixtures/grill_board/showcase/`, so no artifact sample text is published. The script fails if the board requests any host but its own or scrolls sideways. The shots were regenerated at S-004 TK-000J, with the live rating and flag controls, from the artifact at version 1793538932-43c3.

**375px check** (TK-000J): `uv run --with playwright pytest tests/test_grill_board_phone.py` fails if the page is wider than 375px, if reaching a control scrolls sideways, or if any visible control (verdicts, note, stars, Too taxing, comment, links, theme toggle) is off-screen or covered, in dark and light; a star tapped at 375px must commit its rating. The default `uv run pytest` skips it, because Playwright and a browser are not project dependencies.

Differences from the artifact, by choice: the artifact's other Dashboard sections, search, filters, batch, rounds, lanes other than "To answer", a flags view and history are left out until real records back them; queue rows also show each grade's reason, because DDR-000K keeps reasons on every card; the brand reads "AMS · Grill Board".
