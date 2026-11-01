---
name: research
summary: Answer one decision-shaping question in a written paper with stable finding IDs, sources, checks and stated limits that decisions and Specs can cite.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from Kayden Clark's research collection, R-0001 and finding records, retaining primary-source investigation from [Matt Pocock's Research skill](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/research), MIT License.
credit_license: MIT
---

## What it does

Research turns one question into a durable paper stored in your project's docs. The paper says what the evidence supports, what it does not, and how someone else could check. Use it when a choice hinges on facts you lack and they should stay citable after the chat is gone.

It works inside a **Workbench**, a project layout created by the [setup-workbench](/skills/setup-workbench) skill, with a manifest, tooling and collections of docs. A **Spec** is the written description of a destination. A decision record (a CDR, ADR or DDR) captures a choice once its owner accepts it. Research informs both and is neither.

A run has four moves.

1. **Pin down the question.** The agent recovers the decision the paper informs, the audience, scope, version and date bounds, and where the paper should land, and reads what you supplied before searching.
2. **Find the owner and the ID.** It locates the project's **research collection**, the docs folder and index where papers live, and checks the index, the files and in-flight work for ID collisions. It never overwrites another record or starts a competing store.
3. **Investigate with a declared method.** Before concluding anything, it writes down its subquestions, search scope, source rules, stopping point and the checks that would separate plausible answers. Official specifications back contracts, versioned code and tests back implementation claims, and first-party data or original studies back measurements. It reads real content, not snippets, and records locators, access dates and versions. Coverage is never claimed as exhaustive, and secondary writing appears only as labeled corroboration. Disagreements between sources are compared and kept.
4. **Write, audit and deliver.** The paper holds the answer, method, findings, inferences, checks, candidate decisions and reverification conditions. The agent audits it, saves it, updates the index and reads everything back.

Key terms:

- A **finding** is one factual claim with a precise citation, an evidence type, the version or date checked, and a confidence level with its reason and limit. Each has a stable ID.
- A **record-plus-finding reference** such as `R-0001 F-CC5` lets a decision record or Spec cite one claim in one paper.
- An **inference** is the agent's reasoning from findings, labeled apart and linked to them.
- A **candidate decision** is a recommendation to the decision owner, and stays one until that owner accepts it elsewhere.

The skill keeps apart what a source says, what was observed when something ran, and what the agent thinks explains it. A well-worded document does not prove how a real host behaves. A command printed in the paper is not a check that ran, and unavailable, skipped or failed checks are marked as such.

## When to use it

Reach for it when findings need a lasting, reproducible record that other documents will cite, such as verifying how an API behaves before a Spec commits to it.

| What you have | Reach for |
|---|---|
| A short source query where you need cited findings but no paper | [explore-kb](/skills/explore-kb) |
| A question that needs a durable paper with finding IDs that decisions can cite | `research` |
| A destination that is already understood and needs writing down as a Spec | [map](/skills/map) |
| A plan or idea you want challenged by interview rather than by evidence | [grilling](/skills/grilling) |

For a short source query, research hands off to explore-kb when it is installed. If it is not, research uses its own direct evidence method and writes no paper. It does not launch a delegated reading campaign by default.

## Example request

> Our Spec assumes the vendor SDK retries failed uploads on its own. Write a research paper on whether that is true for the current release, with findings I can cite from the decision record.

The agent would find an unused ID, state its subquestions and source rules, read the SDK documentation and tests at that release, run a small isolated check if allowed, and record each result as a finding with its confidence and limits.

## What it requires

- A Workbench. The agent first looks for the manifest and the Workbench tooling at the project root. If either is missing it stops and sends you to the setup skill. It will not hand-build Workbench folders or records, and will not fall back to some other tracker.
- The project's research collection, whose README, formats and index decide file layout, ID scheme and confidence scale.
- Access to sources. If one cannot be reached, the agent tries one bounded primary alternative, then narrows the claim or reports the gap.
- Authority for checks. Checks run within the authority you have, in isolated fixtures, without credentials or private data. Spending money, running model campaigns, delegating reading and sending outside messages each need authorization granted beforehand. If delegation is allowed, the brief is bounded and the agent verifies returned claims against sources itself.

## What it does not authorize

- A research paper never accepts a CDR, ADR or DDR, changes requirements or authorizes implementation. Candidate decisions stay candidates.
- It does not edit decisions or Specs that cite an older record. It lists them and suggests re-evaluation, and changes them only if you separately authorize it.
- It supplies no fitness score, audit sign-off or approval to distribute. A real Workbench fitness or release-qualification investigation follows the project's audit and release owners.
- It does not publish beyond the destination you named, and its report separates local, committed, pushed and accepted states.
- It never rewrites a published finding's meaning in place. New evidence gets a new record or a dated note pointing to it, the original ID, claim and history stay, and the decisions and Specs citing the old finding are listed for their owners.
- It does not update the Wiki, the project's separate knowledge area, by default. Nor does it treat a gain published for someone else's model, task or budget as proof of improvement in your project.

## FAQs

### What if a source cannot be reached?

The agent tries one bounded primary alternative. If that fails, it narrows the claim or records the gap. Gaps and failed outcomes stay in the paper, because dropping a finding does not close it.

### Does a finding stay valid forever?

No. Mutable findings are reverified before reuse under the collection's freshness rule, which says how old is too old. The collection this skill was derived from used a threshold of more than one minor release, but the owning project's rule governs. The paper also lists what would reverse its conclusion.

### An audit found a claim or check failing. What happens?

The failure goes back to the evidence behind it. The agent makes a scoped correction or a bounded follow-up, then tests that exact finding and citation, or the failed check, again on the repaired version. Inferences, candidate decisions and earlier findings that leaned on the same evidence get rechecked too.

## It's working when

- The run begins with a stated question, the decision it informs, scope, version bounds and publication endpoint.
- The ID and file location come from the project's own collection, after a collision search.
- Subquestions, source rules and a stopping point precede any conclusions.
- Every finding has its own ID, a nearby citation with a locator, an evidence type, a checked version or date, and a confidence with its limit.
- Inferences, contrary evidence, unknowns and reversal conditions are labeled separately.
- Checks name their setup and expected and observed results, or say why they did not run.
- Candidate decisions trace to findings without claiming acceptance.
- The run ends with a checkable, indexed paper and a report of its path, IDs, coverage limits and pending owner choices, or with the named gap that blocked it.

## Where it fits in the workflow

Research sits in the Align stage (Shared concept), as a supporting skill for decisions that need evidence rather than conversation. It sits beside [explore-kb](/skills/explore-kb), which handles smaller source gathering, and [grilling](/skills/grilling), which tests thinking by interview. It hands off a published, indexed paper with citable finding IDs, and the owners of the decision records and Specs that cite it take it from there. Those findings can also inform a Spec you write with [map](/skills/map), though that is your call rather than a step the skill performs. Run [setup-workbench](/skills/setup-workbench) first if the project has no Workbench.
