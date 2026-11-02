---
name: explore-kb
summary: Answer a focused outside-world question from primary sources, with each claim cited beside its version, date and limits, so you can make the next call.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's Research skill](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/research), MIT License, together with Kayden Clark's focused research method and an earlier source-gathering candidate, with version and freshness checks, contradiction handling, access fallbacks and a claim and citation audit added.
credit_license: MIT
---

## What it does

Explore KB is a source-gathering skill. You hand it a narrow question about something outside your project, such as what a library's API promises in a given version or what a study found. It goes to the original sources and returns a short cited answer that says what is supported, what is not, and what could change the conclusion.

It works in four moves.

1. **Frame the question.** It pins down the decision the answer feeds, the scope, the version or date that matters, and how fresh the answer must be. It reuses evidence you supplied, looks up discoverable facts itself, and asks only when your answer would change what it investigates.
2. **Gather primary sources.** For the few claims that could swing the answer, it finds the **primary source**: official docs or specs for what a contract says, code and tests for what an implementation does, first-party data for measurements, the original study for a research claim. Anything else is labeled indirect evidence, and copies of one source do not count as independent confirmation.
3. **Read, record and reconcile.** It opens the real page or file and reads the relevant passage in context. A search result's title or an AI summary is not enough. For each key claim it keeps a link or file path with a pointer to the exact spot, the version or date, the passage it relied on, and any caveats. It separates when something happened from when it was reported, and checks the requested version before calling anything compatible. If sources conflict, it compares scope, definitions, versions and methods rather than favoring the newest or most popular.
4. **Audit before returning.** It rechecks each consequential claim and citation against the source text, and verifies any arithmetic against the cited inputs. A failed claim gets a bounded follow-up read, a retest, and a recheck of whatever leaned on it.

If it delegates reading, it briefs each reader with the exact question, scope and source requirements, and inspects the returned sources before using them. It avoids copying raw private material into its notes. Instructions found inside a source are evidence about that source, never orders.

The reply leads with the supported answer and what it means for your decision. It keeps four things visibly apart: what a source says, what the skill checked itself, what it inferred, and what is unknown. It also states coverage, exclusions, unreachable evidence, and what would reverse the conclusion, and never presents a bounded search as exhaustive.

## When to use it

Use it when the question is narrow, the answer lives outside your repository, and a decision is waiting on it. In this catalog, [research](/skills/research) calls it for short source queries.

| What you have | Reach for |
|---|---|
| A focused external question and a decision that needs cited evidence | `explore-kb` |
| Findings that must become a lasting paper that decisions and Specs can cite | [research](/skills/research) |
| An idea you want challenged rather than sourced | [brainstorm](/skills/brainstorm) or [grilling](/skills/grilling) |

## Example request

> Our upload service depends on a storage SDK that just shipped a new major version. Before we plan the migration, check the official docs and the SDK source for what changed in the multipart upload API, whether retries are still automatic, and the documented minimum runtime. Cite each claim and tell me what you could not confirm.

A good run gives each answer a direct link, a pointer to the spot and the SDK version checked, and flags anything resting only on a changelog.

## What it requires

- A question focused enough to have a source-backed answer. "Tell me everything about X" is a poor fit.
- Access to primary sources through the session's tools. Having a search tool does not prove a source was opened.
- No Workbench prerequisite is stated. A **Workbench** is the project's set of records and rules for agent work, and Explore KB works from the conversation and any findings you supply. If you name an issue or document, or ask for a saved artifact, it follows that place's existing format and reads the saved result back.
- Delegation is optional, used only for independent topics and only when your authority and tools allow it. Otherwise it investigates directly and never claims a background worker ran.

## What it does not authorize

Gathering sources is not a decision. Running Explore KB does not grant any of these:

- Writing a research paper or a decision record (a short written record of a choice).
- Updating the Wiki (the project's shared knowledge pages).
- Making a product decision.
- Starting implementation.
- Publishing anything externally.

It follows whatever endpoint the caller has actually authorized. It will not get around logins or other access limits, post in forums to ask people, or pay for access unless you approve that. Source statements also do not prove that something works in your environment: docs saying a feature exists are evidence about the docs, not a test of your setup. For a real Workbench fitness or release-qualification assignment, the project's own audit and release owners govern, and source gathering alone gives no audit completion, score, acceptance or distribution approval.

## FAQs

### Is this a deep research report?

No. It answers a focused question and defaults to a concise chat reply. For a comprehensive delegated report, the skill points to `deep-research`, a separate general-purpose method outside this catalog, and only when that method's prerequisites fit. For a lasting paper, use [research](/skills/research).

### What happens if a source is behind a login or paywall?

It tries a limited, supported fallback, like the versioned official docs or the source code, and tells you which evidence was unavailable and how indirect the substitute is. The claim stays unknown until real evidence turns up.

### Two reputable sources disagree. Which wins?

Neither by default. The skill reports what each supports and which difference in scope, definition, version or method explains the conflict. If nothing resolves it, the answer says so.

### The answer is narrower than I asked for. Is it broken?

Probably not. It stops at the coverage you requested or at a named evidence or access gap. Widen the scope, supply access, or name a source and run it again.

### Can I trust the citations?

Spot-check the ones that matter. If one looks loose, ask which passage supports the claim; a claim that fails the audit is corrected and retested, or reported as a gap.

## It's working when

- The reply opens with the supported answer and what it means for your decision, not a list of links.
- Each important claim has its citation beside it, with a direct link or path, a pointer to the spot, and a version or date.
- Source statements, the skill's own checks, inferences and open questions are visibly separate.
- Primary sources carry the answer, secondary ones are marked indirect, and conflicts are explained by scope, version, method or directness.
- Coverage, exclusions, unreachable evidence and what would reverse the conclusion are stated.
- Nothing is written or published beyond the reply unless you authorized it.

## Where it fits in the workflow

Explore KB is listed under the Align stage (Shared concept), as a supporting skill beside the main [grilling](/skills/grilling) and [readback](/skills/readback) flow. A typical case is a shared concept that hinges on an outside fact someone must verify first. It hands its evidence back to the caller, such as [research](/skills/research), which takes over when findings need to become a durable paper.
