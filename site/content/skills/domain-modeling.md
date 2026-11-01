---
name: domain-modeling
summary: Sharpens your project's vocabulary and concepts by challenging terms, testing edge cases and checking code, then records confirmed definitions in the glossary.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's domain-modeling skill](https://github.com/mattpocock/skills) (MIT License, upstream revision d81f3a183412e71a5b1e84ca21bc1a35eea03a60), with a local decision-record template added. The glossary format file follows upstream, with a short note added above it.
credit_license: MIT
---

## What it does

Domain modeling is deciding what the nouns in your project mean: what an Order is, where a Customer ends and a User begins. This skill does that work with you while the choices can still change cheaply. It is for changing the model, not for reading it; looking up a word is not domain modeling.

The agent works through five moves:

- **Challenge against the glossary.** If a term you use conflicts with the project glossary, the agent flags it at once, names the definition and its file, and asks which meaning you intend.
- **Sharpen fuzzy language.** For a vague or overloaded word, it proposes one canonical term and asks you to choose between the things the word was covering.
- **Test with scenarios.** It invents edge cases that force you to say where one concept stops.
- **Cross-reference with code.** When you describe how something works, it checks source and tests, then labels the result as one of four outcomes: **agreement**, **documentation drift** (the source is newer, so the document is stale), **implementation gap** (the accepted meaning is ahead of the source, so the gap is tracked as work, not papered over in a doc) or **unresolved contradiction** (the order is unclear, so it states what each side claims and leaves the choice to you).
- **Trace consequences upstream.** Before a name, boundary or relationship settles, it follows the choice to what depends on it: the glossary entry, Specs, decision records, docs, source identifiers and tests. A **Spec** is the Workbench's written record of what a feature must do. You see only the few consequences that could change your mind, each led by a file path.

**Pending meaning** is the core discipline. Until you explicitly confirm a definition, proposed terms, interpretations and corrections are labeled pending, in the chat or a notes file. An agent recommendation, your silence or an unresolved contradiction never counts as confirmation.

When you do explicitly confirm a term's definition, the agent updates `GLOSSARY.md` right then, without waiting for the session to end or asking again. It reads the current file first so other entries and concurrent edits survive, follows the bundled format, then reads the saved entry back. If the write fails, it keeps your claim and tells you the entry is unsaved.

The format is opinionated: a sentence or two per term, an `_Avoid_` list of rejected synonyms, and only project-specific terms. Several contexts get a `GLOSSARY-MAP.md`; if no glossary exists, one is created when the first term is resolved.

## When to use it

Use it when you are reworking terminology or a concept: two words for one thing, one word for two things, a boundary that keeps moving, or a name you are about to commit to. It is optional: you or a calling skill invoke it, often beside [grilling](/skills/grilling), which finishes fine without it.

Inside a grilling or [align-docs](/skills/align-docs) interview, it folds its challenges into that interview's question tree, defers dependent questions, and keeps interviewing instead of implementing. Otherwise it asks one question at a time. align-docs reads this skill before editing domain terms or decision records.

| What you have | Reach for |
|---|---|
| A plan or decision to stress-test, no vocabulary problem | [grilling](/skills/grilling) |
| A concept to interview and save as confirmed intent | [align-concept](/skills/align-concept) |
| A concept where documentation should be edited too | [align-docs](/skills/align-docs) |
| Conflicting, overloaded or unsettled terms | `domain-modeling` (this skill) |
| Pending claims or corrections that are not canon | [jot](/skills/jot) |

## Example request

> We say "account" in the billing code and the support docs, and I think they mean different things. Use domain modeling to pin this down before I rename anything.

The agent would check the glossary, code and tests for the word, ask which meaning you intend, test your answer with an edge case, and show what a rename would touch. It writes the glossary entry only after you confirm.

## What it requires

- A **Workbench**, the folder of records and tools that [setup-workbench](/skills/setup-workbench) creates. The agent first checks for its manifest and the `spec-workbench.mjs` tool under `workbench/`; if either is absent it stops and sends you to setup-workbench.
- The glossary at the Workbench root, `GLOSSARY.md`. Older Workbenches may call it `LEXICON.md`; the agent treats that as the glossary.
- Read access to source and tests.
- For decision records, the docs lane (the docs folder the manifest declares) with an `adr/` or `ddr/` collection, its template and its index.
- [jot](/skills/jot) for preserving pending claims and the exact confirmed **readback**, the agent's written summary of what it understood, which you review and confirm. Relevant glossary entries and decision records link back to it. During align-docs, the agent follows the [align-concept](/skills/align-concept) procedure for readback confirmation.

## What it does not authorize

- **Execution.** Investigating sources and recording understanding is in scope. Maps, plans, implementation designs, building from them and reviewing the result all count as execution, even for documentation. A terminology answer cannot start those later stages (Prepare, where work is mapped and planned; Journey, where it is built; Judge, where it is reviewed). That takes your confirmed readback plus scoped authorization.
- **Assembled intent.** Confirming one definition, or accepting one decision record, settles that recording step only. It does not confirm your overall readback or authorize preparation, implementation, judgment, publishing or merging.
- **Wider edits.** The glossary write covers only the entry you confirmed, not a different term the agent inferred from it, and not changes to requirements or agent instructions.
- **A second glossary.** The agent creates no competing terminology file; a suspected second context becomes a question to you. Specs, scratch notes and implementation choices stay out of `GLOSSARY.md`.

If a change turns out to be material, the agent keeps your confirmed intent, records the correction as pending, and gets a revised readback confirmed before affected execution continues.

## Decision records, offered sparingly

A decision record (called CDR, ADR or DDR; the same thing) holds the rationale behind a choice. The agent offers one only if the choice is hard to reverse, would surprise a future reader, and came from a real trade-off with genuine alternatives. If any test fails, it skips the record and says which one.

Offering is not writing. After you accept, the agent links an existing record if the index already has one; otherwise it writes a numbered record in the Workbench's decision collection, adds it to the index and reads both back. A record stays `proposed` until its cited source supports acceptance. To change a decision, it writes a new record and marks the old one superseded.

## FAQs

### Will it edit my glossary without asking?

Only after you explicitly confirm a specific definition, and only that entry. Proposed terms stay pending until then.

### It refused to start and told me to run setup-workbench. Why?

It requires a Workbench and checks for the manifest and `spec-workbench.mjs` first. If either is missing it stops rather than improvising records. Run [setup-workbench](/skills/setup-workbench), then try again.

### It says my code and docs disagree and will not pick a winner. Is that a bug?

No. It names the kind of mismatch it found. When the order is unclear, it reports what each source claims and leaves the call to you.

### Why did it decline to write a decision record?

One of the three tests failed, and it should say which. The agent skips the record rather than writing one that does not qualify.

### My project already keeps terms in another file. Will it make a new one?

It should not. An existing glossary is updated in place. If the agent proposes a parallel file anyway, point it at the existing one.

## It's working when

- It quotes the glossary definition and file when you use a conflicting term, instead of quietly adapting.
- Vague words get a proposed canonical term and a question, not a guess.
- Code or test contradictions come back with a file and a label: agreement, drift, gap or unresolved.
- Pending interpretations are labeled pending, and the glossary changes only after you confirm.
- A saved entry is read back, and a failed write is reported as unsaved.
- Decision records are rare, and a skipped one comes with the failed test named.
- Nothing is mapped, planned or built from a terminology answer alone.

## Where it fits in the workflow

Domain modeling sits in the Align stage, where you and the agent come to mean the same thing before building. It supports, rather than belongs to, the main flow of [grilling](/skills/grilling) and [readback](/skills/readback). It typically runs beside grilling or [align-docs](/skills/align-docs) when terminology is being reworked, and you can call it directly.

It hands pending claims and the exact confirmed readback to [jot](/skills/jot), and confirmed vocabulary lands in the glossary for later stages to read. Moving on to Prepare ([map](/skills/map), [plan](/skills/plan)) needs a confirmed readback and your scoped go-ahead.
