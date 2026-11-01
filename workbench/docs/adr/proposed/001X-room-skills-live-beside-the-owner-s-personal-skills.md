---
date: 2026-11-01
canonicalized_in:
  - .agents/skills
---

# Room skills live beside the owner's personal skills

Room-owned skills live in `.agents/skills`, with `.claude/skills` as one relative link. The owner's personal skills stay authoritative, so the room ships no skill whose name is in the personal catalog. A clash is reported and never fixed by touching a personal skill.

Considered and rejected: room copies that shadow personal skills.

Consequences: Skill sync reports name clashes.

Provenance: Owner decision review, 2026-11-01.
