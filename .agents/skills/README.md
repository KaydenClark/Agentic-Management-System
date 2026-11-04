# Project design skills

Owner authorized project-local installation of UI UX Pro Max, Taste and Impeccable
on 2026-11-03 for trials. Hallmark is excluded. Installation does not establish
measured benefit or authorize a redesign, paid services or personal installation.

## Sources

Pinned upstream packages; retain their supporting files and licenses. Updates
are explicit, not automatic.

| Skill / invocation | Repository | Commit | Source directory | License |
|---|---|---|---|---|
| `$ui-ux-pro-max` | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | `713eef51b04efc98d6fa565323b495f7c9c89fd4` | `.claude/skills/ui-ux-pro-max` | MIT |
| `$design-taste-frontend` | https://github.com/Leonxlnx/taste-skill | `12af471f627f866411b4bd785b19646d3672784c` | `skills/taste-skill` | MIT |
| `$impeccable` | https://github.com/pbakaus/impeccable | `9fadc41729c38fd47d7ae622b501558653f9d2e9` | `plugin/skills/impeccable` | Apache-2.0 |

Codex discovers `.agents/skills`; Claude uses the existing `.claude/skills` link.
Use one design lead per trial. Repository authority, factual claims, existing
visual decisions and checks still govern. Consult `site/README.md` before site
work: preserve the token owner, self-hosted fonts and request restrictions.
Generated PRODUCT.md, DESIGN.md or design-system files must not become competing
owners for established project truth.

## Runtime

- UI UX Pro Max requires Python 3. Resolve its script from the installed skill
  directory; provider placeholders in upstream examples are not portable shell
  variables. Example from the project root:
  `python3 .agents/skills/ui-ux-pro-max/scripts/search.py "keyboard focus modal" --domain ux`.
- Taste requires Node 22+ and Chrome, Edge or Chromium for browser checks.
  Set `TASTE_SKILL_HISTORY` to an ignored session path when drawing directions
  so trial history stays project-local. Asset discovery needs network access;
  remote assets cannot bypass site request restrictions.
- Impeccable 4.8.0 includes a launcher and reference playbooks. Its first invocation
  obtains a checksum-verified engine (version in `scripts/VERSION`). Set
  `IMPECCABLE_HOME` to an ignored session cache to keep downloads project-local.
  The upstream live Apply fallback can launch a CLI with approvals and sandboxing
  disabled: do not use that fallback. Set `IMPECCABLE_LIVE_COPY_AGENT=off` for live
  sessions; make source edits through the current authorized agent.

The Impeccable engine was verified in an ignored project-local session cache.
Only skill packages are tracked. No hooks, global packages, API credentials,
shortcuts or design-context files were installed or generated. No design trial
has been performed. These packages are third-party code; inspect the relevant
script before executing it and use the current host's supported browser tools.

## Local adjustments

Trailing whitespace is normalized in imported Markdown and Python files. Two
UI UX Pro Max negative-example paths (Avalonia and JavaFX) use generic machine
asset locations instead of home-directory paths to satisfy public hygiene.
The Impeccable shell launcher retains its upstream executable bit.
No rule, runtime behavior or repository check was disabled.
