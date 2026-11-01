---
date: 2026-11-01
supersedes:
canonicalized_in:
  - grill-board
---

# The Grill Board theme follows the Grilling Board Redesign artifact

The Grill Board reproduces the owner's "Grilling Board Redesign" design artifact (version 1793538932-43c3): its "topics first" layout, typography, spacing and colors, in dark and light. The artifact is the design guide, not a pixel specification; implementors make small calls and record them. Token values live once in `grill-board/theme/tokens.json`; every surface that uses them is tested against that file.

Neutrals are the page. Five hues are signals, each with one meaning (DDR-000M). Priority and Value grades are ink, graded by weight (1 solid, 2 outline, 3 muted outline, 4 dashed), so no hue ever ranks a card.

| Token | Dark | Light | One meaning |
|---|---|---|---|
| `--ground` | `#0A0A0A` | `#F7F7F7` | Page background |
| `--surface` | `#191919` | `#FFFFFF` | Panels, cards and inputs |
| `--raised` | `#232323` | `#EFEFEF` | Hover, the selected item and progress tracks |
| `--line` | `#333333` | `#E0E0E0` | Hairline dividers |
| `--line-strong` | `#757575` | `#808080` | Control borders; grey, "nothing for you here" |
| `--muted` | `#A8A8A8` | `#474747` | Secondary text |
| `--ink` | `#F7F7F7` | `#0A0A0A` | Primary text, grade badges and progress |
| `--pole` | `#FFFFFF` | `#000000` | Mixing anchor for tone text, outlines and dots |
| `--heat` | `#FF5A1F` | `#F04E12` | Trouble: a failed write, a blocker or a conflict |
| `--worth` | `#FFD60A` | `#F5C400` | Why an answer is worth the owner's time |
| `--owner` | `#4C9BE8` | `#2F86DC` | It waits on the owner |
| `--agent` | `#3DBE5A` | `#27A046` | Agents carry it, or it is the agents' voice |
| `--returned` | `#A66BE0` | `#A66BE0` | It came back for rework |
| `--soft-pct` | `22%` | `22%` | Tint strength of a hue at rest |
| `--line-pct` | `62%` | `68%` | Hue strength of a tone outline |
| `--dot-pct` | `80%` | `72%` | Hue strength of a tone dot |

Mixes, from one hue: `.tone` sets `--on: #0A0A0A`, `--tone-soft: color-mix(in oklab, var(--hue) var(--soft-pct), var(--surface))`, `--tone-ink: color-mix(in oklab, var(--hue) 40%, var(--pole))`, `--tone-line: color-mix(in oklab, var(--hue) var(--line-pct), var(--pole))` and `--tone-dot: color-mix(in oklab, var(--hue) var(--dot-pct), var(--pole))`. `.h-heat`, `.h-worth`, `.h-owner`, `.h-agent` and `.h-returned` set `--hue` to their token; `.h-none` sets it to `--line-strong`. Strong (the hue itself) means now; soft means the same meaning at rest; a filled dot is live and a hollow dot rests.

Fonts: IBM Plex Sans (body), IBM Plex Mono (IDs, grades and counts) and Zilla Slab (headings), self-hosted from @fontsource under the SIL Open Font License. The artifact also loads Pirata One but never uses it, so the board does not ship it.

Dark `--soft-pct` is 22%, as in the artifact's color system page (v2.2), not the 24% its board page carries.

Considered and rejected: a new palette or the site's earlier Workbench tokens, which the owner set aside for the artifact; loading fonts from Google Fonts as the artifact does, because the board is local and loads nothing from other hosts.

Consequences: The board's stylesheet and the site's tested copy follow `grill-board/theme/tokens.json`; a token changes there first. Board-specific detail is in `grill-board/README.md`.

Provenance: Owner, relayed by the coordinating session on 2026-11-01: the board should "basically look exactly like the artifact. The colors, the formatting, the layout. Just make the artifact, but for real." Owner, relayed by orchestrator A on 2026-11-01: "I am not going to micro manage your color choices. Make the grilling board using the artifact as the design guide post."
