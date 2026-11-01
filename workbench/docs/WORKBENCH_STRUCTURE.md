# Shared Workbench structure

This is the generic layout selected by the Shared Workbench Organization Map.
The room's manifest declares its actual lanes and collections. Optional folders
appear only when used; this diagram does not certify installation or migration.

```text
<project-root>/
├── AGENTS.md, CLAUDE.md                 # Instructions and host entry
├── README.md, TASKBOARD.md              # Human orientation and work continuation
├── BLUEPRINT.md                         # Product destination
├── GLOSSARY.md, ARCHITECTURE.md          # Language and information owners
├── RUNBOOK.md, TASKBOARD.md              # Operations and generated work view
├── [project application files]          # Existing source, assets, tests and data
├── .agents/skills/                     # Managed and room-owned skills, one copy per name
├── .claude/skills -> ../.agents/skills  # The one discovery link to it
├── workbench/
│   ├── manifest.json                    # Room identity and declared paths
│   ├── .workbench-seed.json              # Seeded document hashes and generations
│   ├── docs/
│   │   ├── adr/, ddr/                   # Accepted, proposed and historical decisions
│   │   ├── research/<topic>/            # Optional maintained investigations
│   │   └── releases/<version>/          # Optional release accounts and evidence links
│   ├── wiki/                            # MEMORY router and maintained knowledge
│   │   ├── design-concepts/, features/
│   │   └── guidebooks/, archive/
│   ├── specs                           # workbench/specs/<spec>: SPEC, Tasks and proof
│   ├── landmarks/                       # Existing landmark records
│   ├── landmark-tracker/                # When the manifest declares it
│   ├── feedback/                        # Reports and dispositions
│   ├── sessions/
│   │   ├── grilling/, handoffs/, notepads/ # Local working context
│   │   ├── recovery/                    # Ignored private recovery receipts
│   │   └── checkpoints/                 # Frozen historical records
│   └── tools/                           # Receipt-managed runtime
├── .local/                              # Optional ignored, regenerable app output
└── .worktrees/<assignment>/              # Optional registered project worktrees
```

Host-managed worktrees may remain outside the project at their registered
locations. Use the host's lifecycle operation for those worktrees. Never copy
or rename their common Git directory as part of a layout change.

The Feature catalog and `spec-workbench.mjs list` provide capability and Spec
navigation. There is no separate Specs catalog. Application paths, room-owned
skills, decisions, unfinished work and historical evidence keep their owners.
`.local/` never becomes the sole home of useful work or recovery; add its ignore
rule before using it for output.

The [organization procedure](ORGANIZATION.md) covers selected file movement and
rollback. Seeded copies remain project-owned: `seed-documents` preserves local
changes and reports them for reconciliation. For an installed package's exact
source identity read `workbench/tools/.workbench-tools.json` and the skills
receipt; the seed record names each installed diagram's hash and generation.
A source receipt and a successful fixture establish their stated boundaries,
not native host reliability or release acceptance.

Producer rationale and original proposed diagram remain in the producer's
`workbench/docs/research/shared-workbench-organization/` history. This consumer
reference omits the producer's private checkout tree and retired catalog.
