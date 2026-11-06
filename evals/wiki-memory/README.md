# Wiki memory development comparison

`development.json` freezes four inspected development questions, source revision
`280725648ed4a2a7d0e97236fd51def5c02aaa65`, limit6 and max6400 characters.
`baseline.json` retains actual pre-candidate navigation and native-Jot outputs,
case digests and60 active public Wiki file digests. These questions were seen
by the implementor; none is held out. Original failed results remain linked
through FAIL-118–125 and the stopped-candidate report.

Use a separately exported, reviewed public snapshot at that revision, retaining
the exact source bytes, native tools and Git ignore rules. The snapshot's
`corpus-manifest.json` must have `revision` and a nonempty `files` mapping from
repository-relative public paths to SHA-256 digests. Only active eligible Wiki
paths enter this comparison; archive templates are excluded. Validate metadata,
case/manifest identity and actual bytes before baseline reading or evaluation.
`PUBLIC_SNAPSHOT` and `LOCAL_RESULT` below stand for actual local paths:

```sh
uv run python evals/wiki-memory/capture_baseline.py PUBLIC_SNAPSHOT evals/wiki-memory/development.json LOCAL_RESULT
uv run ams-memory --project PUBLIC_SNAPSHOT evaluate --cases evals/wiki-memory/development.json --baseline evals/wiki-memory/baseline.json --json
```

Capture validates requested routes and public handling before body reads; it
bounds navigation before extraction and retains actual blocked native-search
results separately from valid routed reads. The frozen corpus-wide native
search refuses pre-existing malformed `context-owner-answers-coherence.md`.
Neither the absent historical memory CLI nor a blocked reader is an accuracy
failure. Same-source evaluation refuses a changed/missing/added Wiki file,
changed case/budget identity or empty comparison; do not silently resnapshot
and call different sources comparable.

Measured fields are deterministic source/Jot presence, unknown abstention and
returned context characters. The baseline uses a human-selected MEMORY route
plus native Jot; the candidate ranks keyword context. Baseline bookkeeping and
candidate JSON have different shapes, both under the same context ceiling.
These are retrieval checks, not answer-quality or efficiency proof.
Independent answer correctness, stale-answer repetition and human correction
effort remain explicitly unmeasured. TK-002W owns broader functional cases,
untouched held-out inputs and fresh-agent correction recovery.
