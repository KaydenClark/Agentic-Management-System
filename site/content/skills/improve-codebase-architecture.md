---
name: improve-codebase-architecture
summary: Surveys your codebase for places where a deeper module would help, shows ranked candidates in a visual HTML report, then explores the one you pick.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's improve-codebase-architecture method and HTML report](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/improve-codebase-architecture), MIT License. This version adds source evidence, migration risk, a smallest falsifying check, an offline report with no CDN dependencies, and an explicit rule that choosing a candidate authorizes no implementation.
credit_license: MIT
---

## What it does

This skill looks for **deepening opportunities**: spots where a lot of behavior could sit behind a smaller interface, so the code is easier to test and easier for an agent (or a person) to navigate. It works in three phases and stops for you between the second and third.

1. **Scope and explore.** The agent recovers what you asked for, then reads the project's glossary and any accepted decision records (ADRs, the written architecture decisions a project keeps). If you name a module or pain point, it follows that. Otherwise it reads a stretch of `git log` and the changed paths for hot spots, meaning areas that change again and again, and tells you the range it read. It then reads real callers and tests instead of judging by file length.
2. **Present candidates.** It writes one self-contained HTML report with a small ranked set of candidates, tries to open it for you (it is static HTML with no scripts or network use), and asks which one you want to explore.
3. **Explore the one you choose.** The agent runs a **grilling** interview on that candidate (a structured question-and-answer session where each question comes with a recommended answer), sharpens domain vocabulary where needed, and returns a recommended direction.

Vocabulary comes from [codebase design](/skills/codebase-design):

- **Deep module**: lots of behavior behind a small interface. A **shallow module** has an interface nearly as complex as its insides.
- **Seam**: a place where behavior can vary without editing that spot, and where a module's interface lives.
- **Deletion test**: imagine removing the module. If the complexity vanishes, it was a pass-through. If it spreads back across callers, the module earned its place. The agent has to say where the complexity goes.

Each candidate carries its evidence: file paths and line pointers, the revision inspected, and a concrete change or test scenario that shows the friction. It also gets a plain-English fix, before and after diagrams labelled as hypotheses, cost, migration risk, the strongest counterargument, the smallest check that could prove the benefit wrong, and a strength label (`Strong`, `Worth exploring` or `Speculative`). New signatures and full interfaces wait until you choose. Doing nothing can be a candidate, and if nothing survives review, the report says so instead of padding the list. It closes with a top recommendation that links to its candidate and argues why it beats the rest.

Before you see it, the agent audits its own work. File references, cause-and-effect claims, diagram edges and risks are rechecked against the code, history, tests, glossary and ADRs, and weak candidates are fixed, downgraded or dropped. If a candidate would contradict an accepted ADR, the report names the record, the contrary evidence and the cost of reopening it, and never quietly overrides it.

## When to use it

You have to ask for it. The skill is set so an agent never picks it up on its own. For example: `find deepening opportunities in the billing module`.

| What you have | Reach for |
|---|---|
| A codebase or subsystem that feels hard to test or navigate | This skill |
| One module whose interface you already want to design or compare | [codebase design](/skills/codebase-design) |
| A failing behavior and no known cause | [diagnosing bugs](/skills/diagnosing-bugs) |
| Conflicting or overloaded names for one concept | [domain modeling](/skills/domain-modeling) |
| A direction you have already settled and want cut into work | [plan](/skills/plan) |

## Example request

> Our checkout code feels scattered: every change touches six tiny files. Survey the last few months of history around it, show me the best deepening candidates in a report, and I'll pick one to dig into.

The agent states the history range it read, builds the report, and waits for your choice.

## What it requires

- Code, callers and tests it can read, plus the project's `GLOSSARY.md` and accepted ADRs where they exist. Version history sharpens the survey, but thin or missing history is disclosed and handled. Missing records never license invented decisions.
- The [codebase design](/skills/codebase-design) skill for vocabulary, [grilling](/skills/grilling) for the phase-three interview, and [domain modeling](/skills/domain-modeling) when terms need sharpening.
- A writable temporary directory outside the repository for the report. A way to open the file helps but is not required.
- Optionally, a fresh-context explorer, only if your setup authorizes one. Otherwise the agent explores directly and says so.

## What it does not authorize

Surveying, ranking and drawing diagrams grant no refactoring, test deletion, publication or merge. Choosing a candidate does not grant them either, and neither does the agent's top recommendation, which is never treated as your answer. The agent waits for your explicit selection.

After exploration it may record the accepted direction or suggest small slices of work, but only inside documentation or planning authority you have given. Implementation needs a separate, explicit request. Glossary terms and decision records are written only once you confirm or accept them.

## FAQs

### Does choosing a candidate mean the agent starts refactoring?

No. Selection starts a design conversation, not a code change. Before handing back, the agent checks the settled shape against your confirmed answers, the evidence and the surviving tests, and fixes authorized mismatches. If you want the change made, ask separately.

### The agent could not save or open the report. What now?

If the temp directory cannot be written, the agent reports the failure and keeps the report text for you, without pretending a file was saved. If opening fails, it hands you the absolute path and says preview was unavailable. Open the path yourself or ask for the content in chat.

### My history is thin or one big squash. Will it still work?

With less certainty. The agent says so and inspects representative change paths within your scope. Naming a module up front helps.

### Why not just flag the longest files?

Length is not friction. The agent looks for concepts that make you hop between many small modules, interfaces nearly as complex as their insides, and knowledge leaking across a seam, and it runs the deletion test on each suspect module. Line and file counts never count as evidence of depth.

## It's working when

- The agent states the scope, the history range it read and any evidence limits before ranking anything.
- Every candidate cites real paths and a concrete scenario, shows cost, risk, a counterargument and a smallest falsifiable check, and labels its diagrams as proposals.
- You get an absolute path to the report, an honest note on whether a preview opened, and the question of which candidate to explore.
- No repository files change before you choose, and afterward only design or planning work follows until you ask for implementation.
- The exploration ends with a recommended direction, what it trades off, the cheapest reversible way to prove it, and what the next approved step is.

## Where it fits in the workflow

It lives in the **Improve** stage (learn and fix), an on-request skill for when the code itself needs improving. Nothing earlier in the main flow calls it, and it leans on [codebase design](/skills/codebase-design), [grilling](/skills/grilling) and [domain modeling](/skills/domain-modeling).

What comes out is a settled direction and, if you permit it, slices or a written design. To turn that into work, [plan](/skills/plan) cuts it into Tasks (each a small assignment in a Workbench, the project's record-keeping setup), and a [Journey](/skills/journey) builds one Task. Both need a Workbench.
