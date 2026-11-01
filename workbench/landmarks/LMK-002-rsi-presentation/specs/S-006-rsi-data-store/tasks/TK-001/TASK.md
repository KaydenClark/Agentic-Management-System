# TK-001 - A key check reports only whether the service key loads and authenticates, for `sb_secret_` and legacy keys

**Task ID:** TK-001
**Spec ID:** S-006
**Slice:** A key check reports only whether the service key loads and authenticates, for `sb_secret_` and legacy keys
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Key loads and authenticates; No secrets in Git
**Planned verification:** pytest with fake keys plus one live run whose output holds no key value

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** claude-s006-tk001
**Current claimant:** claude-s006-tk001

Run only in orchestrator B's local lane, which holds the key in the gitignored local environment file of the owner's main checkout ([ADR-003C](../../../../../../docs/adr/003C-the-supabase-project-and-its-read-only-baseline.md)). Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), ADR-003C and [ADR-003D](../../../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md).

Deliver the writer's first seam: a Python module under `src/` that reads `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` from the process environment, recognizes the format (new `sb_secret_` key or legacy JWT), and one command that calls the Supabase REST endpoint with the key in the `apikey` header and prints only: loaded yes/no, format label, authenticated yes/no and the HTTP status. It never prints, logs, raises with or writes the value or any part of it. Write tests first with fake keys and a stubbed HTTP layer.

Out of scope: tables and inserts (TK-002).

Hand back to S-006 with `close`; the proof is the test output and the live run's output, which must contain no key value.

## Acceptance

- [ ] With the real key loaded, the command reports `loaded: yes`, the right format label and `authenticated: yes`.
- [ ] With the variable unset, it reports `loaded: no` and exits non-zero.
- [ ] With a fake `sb_secret_` key and with a fake JWT, tests show the format is recognized and Supabase's refusal is reported as `authenticated: no`.
- [ ] A test captures stdout, stderr and logs from every path and fails if any contains the fake key or a substring of it longer than its format prefix.
- [ ] `uv run pytest` passes; the hygiene grep finds no key in the diff.
