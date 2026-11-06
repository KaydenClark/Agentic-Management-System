# Grill Board

The local Python Board presents DQC readback questions, their exact history
and connected execution identities. Start
from the repository root with `uv run ams-board`; it serves on 127.0.0.1 only.
S-004: the [native tracker](../workbench/docs/SKILLS.md#concept-lifecycle) owns DQCs;
[TRACKER.md](../TRACKER.md) projects them. Legacy cards remain supported below.

## Current DQCs

The Board calls `landmark-tracker.mjs show --committed --json`, reading the same
native records used in terminal interviews. It renders their full readback,
why, source, scope, revision, separate Priority/Value reasons, dependencies,
confirmed versions, exact owner feedback and revision history. Readback headings receive safe formatting; source and prose stay escaped. DQCs bypass the legacy short-note
restriction; the Board provides no routine page drafting editor.

Topics use the native concept titles. A `/?card=DQC-ID` link follows the stable
identity across topic changes. Pending/reopened actionable proposals enter the
owner frontier once every declared prerequisite DQC is currently confirmed.
Unknown or non-DQC dependencies stay unresolved. Held-for-rewrite, deferred,
superseded and confirmed concepts remain under Context and history. A proposal
with `actionable: false` is source-linked branch context, not a new owner request
or a newly confirmed synthesis. Existing settled questions are not re-asked.

The page checks HEAD every five seconds and refreshes automatically, preserving
unsaved typing. Native views are cached by exact HEAD; dirty DQC text never
appears. Source errors remain visible.

## Owner actions and recovery

Confirm records the exact displayed native readback/digest and scope, with the
actual local Board click as source. Rework wording, Change the why and Change
record the owner's exact note for agent rewriting. They confirm no replacement
wording. Confirmed versions remain recoverable after corrections. Ratings 1–5
and Too taxing use those same native owning operations; a flagged question is
held until the agent changes its readback. A confirmed concept can still be
corrected or rated. These actions grant no implementation authority or Human QA.

Python submits native actions, never editing DQC JSON. Native transactions
serialize writers, check HEAD/revision/digest and preserve unrelated work.
Legacy cards retain their separate compare-and-swap writer.

A stale or refused submission preserves copyable owner words. Words from an old
proposal are not silently attached to its replacement. If a save receipt is lost
or malformed, the Board reports **Save outcome unknown** and preserves an explicit
**Check or retry this exact action** form. This retains the original payload and
event ID even when it contains no note. Native replay returns the original
commit instead of duplicating an action, including after later concept changes.
Do not create a new action to hide an uncertain outcome. A reported successful
commit remains successful if rendering the subsequent view fails.

Legacy files, answers, ratings and flags are preserved. To make an existing card
history-only after an explicitly authorized DQC mapping, add `**DQC:** DQC-ID`
through the normal record editing procedure. The DQC becomes the sole actionable
question; the old file remains navigable and its bytes/history are not migrated
or rewritten by reading the Board. Unmapped legacy cards continue to work.

## Agent capture and round continuation

Capture each main interview branch before asking it, recover prior settled intent
and retain its actual source. Use native tools from the project root:

```sh
node workbench/tools/landmark-tracker.mjs capture --title "Concept title" --question "Owner choice" --source SAFE_SOURCE --reason "Why this branch exists" --json
node workbench/tools/landmark-tracker.mjs show --committed --json
node workbench/tools/landmark-tracker.mjs action DQC-ID --stdin --json < action.json
```

Commit capture records/projections before actions. `propose` supplies a stable
`eventId`, actual `expectHead`/`expectRevision`, and full `proposal` with
`readback`, `why`, `source`, `scope`, `round`, separate Priority/Value objects
`{value: 1..4, reason}`, and `dependencies: ["DQC-ID"]`. Later actions bind its
`digest`. Use only actual sourced owner confirmations. Read the installed
[native reference](../workbench/docs/SKILLS.md#concept-lifecycle) and current CLI;
reusable procedure: `setup-workbench/references/dqc.md`.

**Finish this round** records that the owner is done and lists every unreviewed
DQC change, including corrections, ratings and flags. It preserves unanswered
questions/dependencies and opens the next round. The UI explicitly says agent
review is pending. Tell the agent the round is finished; no background AI service
or implementation dispatch runs from this button.

The agent then reads `show --committed --json` and reviews every entry under
`tracker.rounds[].changed`, including its exact events/history. Reconcile only
confirmed and approved understanding into the actual Wiki/docs, retaining
unsettled choices and quality feedback. Commit those real document changes. Then
submit a native global action (no DQC ID):

```json
{
  "type": "reconcile-round",
  "eventId": "a-unique-stable-reconciliation-id",
  "expectHead": "ACTUAL_FULL_PROJECT_COMMIT",
  "round": "THE_FINISHED_ROUND",
  "receipt": {
    "sources": ["workbench/wiki/actual.md@ACTUAL_FULL_PROJECT_COMMIT"],
    "outcome": "What was actually reconciled and what remains unsettled",
    "nextFrontier": "Authorized preparation or the next ready interview questions"
  }
}
```

Receipt sources must identify real committed Workbench Markdown. Native
source checks do not establish semantic correctness; the agent owns that judgment. Prepare changed proposals in the
reported `currentRound`; the Board refreshes the resulting frontier and receipt.
Round bookkeeping alone supplies no reconciliation, preparation approval,
implementation, independent Review or Human QA.

## Legacy cards

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

Current differences from the artifact: other Dashboard sections, search, filters and batch remain omitted. The later [owner redesign correction](../workbench/wiki/context-grilling-board.md#jot-c9dcebb6-4d50-4d6d-95d7-30d723d66d53) requires those supplied controls to function; these omissions are an implementation gap, superseding the earlier “by choice” characterization. Native DQC rounds/context/history use their actual records; queue rows retain each grade's reason under DDR-000K, and the brand reads "AMS · Grill Board". Delivered DQC lifecycle checks establish neither the later redesign nor owner Human QA.


## DQC verification

`tests/test_grill_board_dqcs.py` exercises the real installed native operations
through disposable Git/HTTP records: exact confirmation, corrections, feedback,
dependencies, migration/history, concurrent writers, commit failure, uncertain
receipt retries, source refusal and a real Wiki reconciliation/next frontier.
`uv run --with playwright pytest tests/test_grill_board_dqc_browser.py tests/test_grill_board_phone.py`
checks dark/light at 375px/desktop, reachable controls, exact readback text,
automatic refresh/unsaved words and the concrete web-to-agent round walkthrough.
Optional `AMS_BOARD_CAPTURE_DIR` saves disposable screenshots to a chosen local
output directory. The existing CI Playwright step includes both test files.
Agent browser checks do not establish owner Human QA.

## Content-bound website review cards

S-005/TK-001 is natively closed. Immutable262d28e produced48 cards through the actual isolated Next build/serve path, including39 skill articles and visitor404; a second generation made no changes. This older local slice is not current expanded coverage or protected-deployment/data-state proof. The local Board/CLI owns review state; public pages receive none.

`ams-pages generate` freezes one already-fetched trusted source SHA, exports only tracked Git bytes, runs one isolated build and server, consumes the postbuild page-list projection from explicit committed owner declarations, compares all actual built/served routes, then creates cards/index/approval anchor through the existing Board lock/CAS. Missing or ambiguous owners refuse; no Spec/Task or landing is invented. Include every skill article and the visitor404 (`/_not-found`, fetched through a nonexistent URL expecting404). Only `_global-error.html` is an internal framework fallback.

```sh
uv run ams-pages generate --project . --source-repo SOURCE_CHECKOUT \
  --ref origin/dev --candidate FULL_CANDIDATE_SHA \
  --image sha256:95a34da32a840bd9b3b09a5b773591c16923e350174b1c50e1200c75bf15eaa9
```

The image must already exist on the supported local Docker engine. Only the owned Git export is mounted; candidate processes receive isolated container HOME, no host credentials/configuration, and only explicitly validated public anonymous site configuration when requested with `--public-config JSON`. Public package acquisition precedes network-disconnected build/serving. Runtime refusal has no host-build fallback. Exact owned process groups/containers are cleaned and read back, including interruption; genuine permission/cleanup failures refuse before Board writes.

Provenance remains explicit: existing historical landings retain their meaning; `verified-containment` identifies actual presence, not creation; `pending-candidate` uses null landing and the collector's frozen candidate with integration pending. Nonempty repository-relative sources and current owners are required before writes. Changed owners, sources or provenance create a replacement card even when content is identical; old answered bytes stay intact with appended supersession. Otherwise an unchanged card preserves its original candidate occurrence, while the index binds the latest build pin. Changed/removed content appends stale history. Returning content gets a new card occurrence. Identical reruns do nothing.

The hash is `sha256:` plus UTF-8 SHA-256 over canonical `<main id="main">`: drop script/style/comments and review-mark/exclude subtrees; retain decoded text and href/src/alt in source order, join with spaces, collapse ASCII whitespace and trim. Footer identity is outside it. Retained independent vectors are under `tests/fixtures/grill_board/pages/`.

For RSI, only freshness/last-successful-read text may be excluded: changed results and availability must change the review hash. A network-isolated unavailable-state build cannot represent different protected-deployment HTML. Actual RSI review needs the existing PR165 freshness correction and a trusted immutable deployed-artifact seam; credentials never enter the candidate build. Explicit `--inventory FILE --built-html FILE --candidate SHA` remains an injected-artifact seam, not live proof by itself.

Approvals stay in the committed owner record; no Supabase approval mirror/public query is added. Actual private criticism must not enter public committed raw evidence. Original failed checks/receipts, scoped corrections and unperformed live outcomes remain in the Task; green fixture tests supply no owner Human QA.

### Committed page approvals

Page Confirm rechecks the committed card, page path, hash and current index
entry while holding the Board lock. Stale cards, changed identities, dirty or
unsafe index files refuse before any write. A valid Confirm retains the normal
single card/approval commit, with no second confirmation. A Confirm note stays
private and adds no voice entry.

`uv run ams-pages status` reads the committed index and approval record at HEAD;
`--ref FULL_COMMIT` inspects an earlier committed snapshot. It reports each
page's current hash and local `approved` or `draft` state. Approval references
retain path, hash, date, card and the original line's committing SHA across
later insertions. Working-tree edits are ignored by readback; malformed
committed approval records refuse. Quoted, fenced or other-section examples
are not approvals. A changed main-content hash reports draft; footer-only
changes retain the matching approval. This state is never a public-site query.

### Private page feedback

The committed manifest declares `pageReview.voice` and
`pageReview.privateFeedback`; one Python reader resolves both. The configured
voice location supplies card references and the private location supplies
capture/replay. New feedback writes reject unsafe or uncommitted
configuration; known receipts are reconciled before current-card checks.

Page returns, ratings and Too taxing capture the exact original privately
before public writes. The ignored local store requires owned, nonlinked
directories and private file permissions. Raw words never enter a Git object,
approval, card or public log. Non-page cards retain their existing behavior.

`grill-board/voice-and-taste.md` contains only safe page/hash/date/card/kind,
event and version references. Interpretation and disposition start as pending;
they are distinct from the private original. Each return, rating or flag adds
one entry and increments its version in the same commit as the card section.
New page cards name the current voice version; legacy open cards receive an
appended reference, while answered history stays unchanged. Storage alone
does not prove a later draft consumed feedback; TK-001E verifies that use.

The Board checks the card, current page index and render-time voice SHA under
its repository lock. A stale or conflicting input refuses before public writes
and keeps copyable words on screen. Without a valid private-feedback context,
page notes still refuse. Keep these words private when copying them.

If a save outcome is uncertain, keep the displayed original and use **Check or
retry this exact action**. Its durable event identity reconciles the original
commit before current-card checks, without repeating the version increment.
Recovery repairs only recognized bytes from its own pending write; unrelated
working or staged changes remain for agent reconciliation. Do not replace the
original action with a newly submitted event while its outcome is unknown.

Metadata cannot contain any line separator recognized by the card parser; generated Page/hash/candidate/owner fields are checked before writes. Note refusal also recognizes the fixed approval record when a Page marker is damaged. Historical/containment provenance requires an explicit branch; an absent PR remains labeled unknown, with no branch inferred.

### Read-only page coverage

`uv run ams-pages check` freezes the fetched `origin/dev` source once, then
reads its declared page inventory and the review repository's committed HEAD.
`pageReview.inventory` in the manifest names the inventory path. Use
`--source-repo PATH` when the canonical AMS source and review checkout differ;
`--candidate FULL_SHA` also verifies the expected source ref identity.

The command names missing/removed pages, absent or malformed current cards,
changed origin/pending provenance, mismatched card identity/hash, extra open
questions and unavailable voice references. Uncommitted drafts are ignored.
Success reports pages/current cards and both immutable revisions; it writes no
cards, approvals, voice entries or commits. If the committed review HEAD or
source ref moves during a check, that run refuses and must be repeated.

`check --recompute --image SHA256` uses the same owned build, cleanup and
protected-capture validation as generation, then compares actual served hashes.
Use the existing `--protected-artifact` and all independent observer pins for
populated protected content. A different local unavailable-data build cannot
stand for that content. Every build/capture must finish verified cleanup. Automatic generation also
rechecks its starting manifest SHA under the write lock; a changed layout
refuses before card writes.
Explicit `--inventory`/`--built-html` inputs remain labeled fixture artifacts,
never live deployment proof. Final owner QA still needs one assembled READY
source and its fresh complete capture/readback.

### Protected capture boundary

For protected page identity, an authenticated outer observer fetches every route from one immutable Vercel deployment. Keep its raw HTML and capture files private and outside the Git export/build. Recover repository, project, deployment, source SHA and immutable origin from the authenticated Vercel observation; supply the exact capture digest independently. A manifest's own claim of trust is insufficient, and the CLI never derives the expected digest from an incoming manifest.

`ams.protected_pages.collect_protected(artifact_directory, built_snapshot, expected_pins=...)` performs no requests and receives no credentials. `manifest.json` schema1 names the independent pins, `observer: authenticated-vercel-web-fetch`, UTC `observed_at`, and `pages`: route → `{file, sha256, url, status, content_type}`. HTML files are unique regular files under `pages/`; symlinks, hardlinks, traversal, oversize/tampered files and missing/extra routes refuse. Expect200 for pages and404 for the visitor surface fetched at a nonexistent URL.

Every response must carry exactly the pinned footer `data-commit-sha` and a Next deployment marker: the root document's `data-dpl-id` or a Next resource's `dpl` query. All present markers must agree with the independent deployment pin; conflicting document/resource markers or absence of both refuse. Static page hashes must equal the same pinned local build. Only `/rsi` may differ in data-dependent content; the original protected HTML supplies its hash, including real results and availability. The shared contract excludes freshness only. Login responses, mixed deployments, old source, redirect/status/type mismatches and missing observer pins refuse before Board writes. No local unavailable-state fallback is permitted.

Automatic CLI collection accepts `--protected-artifact DIR --protected-project PROJECT --protected-deployment DEPLOYMENT --protected-origin IMMUTABLE_ORIGIN --protected-capture-sha256 OBSERVER_DIGEST` alongside the pinned build arguments above. The ordinary build and verified cleanup finish before protected files are consumed. Injected `--built-html` input cannot claim this mode.

Successful collection returns a validated capture bound to the exact raw HTML, inventory and candidate. Generation accepts that in-process result, not a serialized evidence dictionary; replay revalidates the artifact. Safe protection identity/digest goes into the committed index. New verified cards are labeled `protected-capture`; an existing occurrence gets an appended verification receipt, preserving its answer and original context. Ordinary builds remain explicitly pending. A fresh capture with identical content/ownership updates snapshot evidence without re-asking unchanged cards, including older card templates. Hash or owner changes still append staleness. This verifies the observed snapshot; it supplies no owner decision or later-data freshness guarantee.
