# Interview trial bootstrap

`ams-trials` prepares private inputs and records local runtime facts. It makes no
model requests. [S-002](../workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md)
owns actual qualification, noise-floor runs, comparisons and retention.

```bash
uv run ams-trials materialize PRIVATE_PACK/manifest.json .local/worker
uv run ams-trials materialize PRIVATE_PACK/manifest.json .local/worker --reset
uv run ams-trials preflight .local/worker --reference PRIVATE_ORACLE/reference.json --id bootstrap-r1
uv run ams-trials readback
```

Keep source packs, oracle prompts/examples and execution text private. The public
[three-case suite](interview-dev-cases.json) contains only safe starting scenarios,
declared outcomes and conditions. Worker prompt construction consumes the case's
starting prompt and verified source artifacts; it never consumes the expected
outcome or oracle files. Studied cases are development evidence, never held out.

## Input identity and reset

A private pack has `manifest.json`: schema 1, repository, condition
(`baseline`/`candidate`), full `sourceCommit`, and `entries` containing relative
`path`, exact integer `bytes`, SHA-256 `sha256` and Git blob SHA-1 `gitBlob`.
`sourceUrl` and safe provenance metadata may also be retained. All files must be
listed; traversal, symlinks, duplicate paths, missing files and changed bytes fail.
Materialization creates an owned private fixture. Reset requires its matching
ownership marker and refuses symlinks or unlisted files/directories before reset.
Changed or missing listed artifacts can be restored; unlisted recovery files stay
untouched and block reset. Source
packs and unrelated files are preserved. Interrupted partial output remains
visible for inspection, never reported as a complete fixture.

`trial_inputs.worker_prompt` returns private prompt text plus hashes and loaded
artifact identities. Source text exposure is explicit context injection, not
native skill discovery or installation. Raw skill text is never a CLI argument
or public result. The pinned references are in [the safe manifest](interview-artifacts.json).
No document provider exists in these pinned packs. The installed external docs
router points to Pages; this transcript-only condition does not claim document
capture, filesystem-tool behavior, host reliability or installed-workflow use.
A refusal caused by a missing capability remains an observed limitation.

The protected oracle reference stays outside the worker fixture. It pins schema
1, kind `interview-grader-reference`, exact model/effort, `sourceRevision`, relative
`promptFile`/SHA-256 `promptSha256`, `examplesFile`/SHA-256 `examplesSha256`, and
declared `qualification`. The examples document has kind `narrow-oracle-seeds`,
a source and examples with identity, Yes/No label, response and response SHA-256.
Changing approved response bytes invalidates the reference. Labels are inputs to
qualification; supplying a qualification string is not an independent assessment.

## Runtime boundaries

The command preflight exercises a macOS Codex sandbox with explicit root and
temporary-directory denials, a narrower writable inert fixture and no network.
It checks actual file opens/writes and a permission-denied network syscall.
An enclosing sandbox may refuse nested Seatbelt. Other platforms are reported
unavailable. This is host-command evidence, separate from the Claude boundary.

`trial_runtime.ClaudeAdapter.execute` is a callable seam for a separately
authorized frozen series; there is deliberately no model-running CLI subcommand.
It requires existing first-party subscription authentication, excludes provider
API credentials/config overrides from the subprocess environment, and fixes
`claude-opus-5-5` at medium effort. It uses restricted/safe mode, no built-in
tools, strict empty MCP configuration, no Chrome, no skills and no saved session.
It checks initialization/MCP status before the prompt and validates advertised
empty tool inventory, actual model, permission mode, final text, one-turn result
and matching provider usage. Unexpected tools, tool calls, fallback/model drift,
errors, missing evidence or inconsistent counts refuse the result. Worker
thinking is not returned as final text or supplied to the future judge.
Startup/transport failures retain at most 16 KiB of redacted private stderr,
stage and exit status under `.local/trial-diagnostics`, without worker prompt,
stdout or authentication payloads. A diagnostic-storage failure stays visible to
the caller; it never converts an execution failure to success.

Transport writes are nonblocking and drain stdout/stderr concurrently. One
absolute deadline covers each send and its reply: 15 seconds per control exchange,
55 seconds for execution. Inert subprocess tests exercise large prompts, partial
writes, output floods, nonreading peers, exact delivery and private diagnostics.
The authorized single adapter smoke at source
`5d3632098d4316a8b34ed85a82466aacf9de5bb1` returned `PREFLIGHT_OK`; it is
historical execution evidence, separate from the earlier external CLI smoke.
The corrected transport at `5467b5e3715fd229d260b064c2250d36c54b4068` also
passed one authorized inert adapter smoke. Both are execution facts, not semantic
qualification or controlled skill trials. A future series must bind the exact bootstrap and protected oracle
revision selected by the orchestrator after review.

## Evidence and next gate

Safe execution summaries retain model/effort, source digest, token/cache counts
and API list-equivalent cost. Actual subscription spend remains unknown. Raw
prompts/responses, host paths and oracle content are excluded. Local evidence
records are immutable by canonical JSON identity; readback verifies filenames, digests, fields and gates. This is a cooperating-writer integrity boundary, not
proof that supplied execution claims or evidence are true.

Preflight always keeps controlled execution unreleased. It reports missing
semantic qualification and unavailable/failed command checks explicitly. It
does not write a fabricated assessment packet or a successful RSI trial row.
No database facts are created by this CLI. The original three failed Codex
app-server starts remain failed evidence; the working tool-free Claude resource
does not erase them. Owner labels and the instruction to retain only working
outcomes are preserved in the existing AMS-purpose Wiki owner.

After bootstrap review: qualify the fixed narrow semantic oracle on owner-labelled
good/do-nothing examples plus applicable adverse controls; then run original
TK-002's repeated same-version cases and TK-003's control arms. A useful-benefit
claim additionally needs paired comparisons, retained failures, affected r1 checks
and fresh deciding evidence. A preparation pass establishes none of these.

[Noise-floor protocol](INTERVIEW-NOISE.md) describes the separately released five-call narrow qualification and nine same-version evaluations. Preparation remains model-free; actual calls need the selected accepted reference.
