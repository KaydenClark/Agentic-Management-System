# TK-001 - A key check reports only whether the service key loads and authenticates, for `sb_secret_` and legacy keys

**Task ID:** TK-001
**Spec ID:** S-006
**Slice:** A key check reports only whether the service key loads and authenticates, for `sb_secret_` and legacy keys
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Key loads and authenticates; No secrets in Git
**Planned verification:** pytest with fake keys plus one live run whose output holds no key value

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** claude-s006-tk001
**Current claimant:** claude-s006-tk001
**Proof:** PR #15 merged as 884d021: uv run pytest 37 passed (red run 36 failed first); env -u SUPABASE_SERVICE_ROLE_KEY uv run ams-keycheck printed loaded: no, exit 1; live uv run --directory <main checkout> ams-keycheck printed loaded: yes / format: sb_secret / authenticated: yes / http status: 200, exit 0, no key value; hygiene grep found no key in tracked files or diff; render no diff, doctor no blocking finding

Run only in orchestrator B's local lane, which holds the key in the gitignored local environment file of the owner's main checkout ([ADR-003C](../../../../../../docs/adr/003C-the-supabase-project-and-its-read-only-baseline.md)). Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), ADR-003C and [ADR-003D](../../../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md).

Deliver the writer's first seam: a Python module under `src/` that reads `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` from the process environment, recognizes the format (new `sb_secret_` key or legacy JWT), and one command that calls the Supabase REST endpoint with the key in the `apikey` header and prints only: loaded yes/no, format label, authenticated yes/no and the HTTP status. It never prints, logs, raises with or writes the value or any part of it. Write tests first with fake keys and a stubbed HTTP layer.

Out of scope: tables and inserts (TK-002).

Hand back to S-006 with `close`; the proof is the test output and the live run's output, which must contain no key value.

## Acceptance

- [x] With the real key loaded, the command reports `loaded: yes`, the right format label and `authenticated: yes`.
- [x] With the variable unset, it reports `loaded: no` and exits non-zero.
- [x] With a fake `sb_secret_` key and with a fake JWT, tests show the format is recognized and Supabase's refusal is reported as `authenticated: no`.
- [x] A test captures stdout, stderr and logs from every path and fails if any contains the fake key or a substring of it longer than its format prefix.
- [x] `uv run pytest` passes; the hygiene grep finds no key in the diff.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/s006-tk001-key-check | c1f4182d1aa308584646d9752464d8e87f877334 | ahead 0 behind 0 | 0 | PR #15 merged as 884d021: uv run pytest 37 passed (red run 36 failed first); env -u SUPABASE_SERVICE_ROLE_KEY uv run ams-keycheck printed loaded: no, exit 1; live uv run --directory <main checkout> ams-keycheck printed loaded: yes / format: sb_secret / authenticated: yes / http status: 200, exit 0, no key value; hygiene grep found no key in tracked files or diff; render no diff, doctor no blocking finding | RUNBOOK names uv run pytest and ams-keycheck; ARCHITECTURE names src/ams/keycheck.py | Legacy-JWT path proven only with fakes; the live key is sb_secret. Tables, inserts and the publishable-key read path remain for TK-002 onward; close attribution: {"agent":"claude-s006-tk001","claimant":"claude-s006-tk001","onBehalfOf":null} | 3270d255cea951a5440c1aed32c29ce6971e729bd966e66ca17659ea576cb566 |
