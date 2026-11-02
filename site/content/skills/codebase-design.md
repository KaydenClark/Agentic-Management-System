---
name: codebase-design
summary: Gives your agent shared vocabulary and a method for designing deep modules: small interfaces, well-placed seams, and tests that use the seam real callers use.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's Codebase Design](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/codebase-design), MIT License. It draws on Michael Feathers' idea of a seam and John Ousterhout's Design It Twice, and it replaces the retired design-an-interface skill.
credit_license: MIT
---

## What it does

Codebase design is a way of talking about, and deciding, how code should be carved into pieces. Its goal is the **deep module**: a lot of behavior behind a small interface, placed at a seam that tests can reach. The skill is mostly shared vocabulary plus a short method, so you, your agent and other skills mean the same thing by the same word.

- **Module**: anything that offers callers an interface and hides an implementation, from one function to a package.
- **Interface**: everything a caller must know to use the module correctly: inputs, results, invariants, call ordering, error modes, required configuration and performance limits. A type signature alone says too little.
- **Seam**: a spot where you can alter behavior without editing that spot; it is where a module's interface lives. Choosing it is separate from choosing what goes behind it.
- **Adapter**: a concrete thing that fills a seam by satisfying its interface. It names a role, not a size: a small database adapter can wrap a large implementation.
- **Port**: the interface defined at a seam for adapters to plug into.
- **Depth**: what a caller or test can do relative to how much interface it must learn. A shallow module costs almost as much to learn as it does to build.
- **Leverage**: the payoff callers get from each piece of interface they learn.
- **Locality**: changes, bugs and checks gather in one place, so one fix helps every caller.

The agent first recovers the requested outcome and the project's accepted vocabulary. It then reads real call paths and tests to see who calls what, who owns the data, what each part depends on and where tests attach. It favors modules with one clear responsibility and explicit adapters at external dependencies, compares the current design with plausible alternatives, and checks its pick against those call paths and behavioral tests. It writes up the chosen interface, tradeoffs, dependency handling and test seam in the project's existing design record, or in chat if none exists. When sources are missing, it states assumptions and marks affected choices provisional. Your language wins: it keeps the project's accepted terms, and only where none exist does it prefer module over unit or component, interface over API, and seam over boundary.

Principles that steer the comparison:

- **Deletion test.** Picture removing the module. If the complexity disappears, it was a pass-through. If it reappears in every caller, the module earned its place.
- **Tests cross the real seam.** Tests should enter where callers do. Needing to reach past that point suggests the wrong module shape, and internal seams stay private.
- **Real variation only.** A seam with one adapter is hypothetical. Add a port only when two adapters are justified, usually a production one and a test one.
- **Natural testing.** Pass dependencies in and return results rather than mutating caller state.

### Two reference files

The agent reads **Deepening** before choosing dependency adapters or replacing tests, and **Design It Twice** before assigning or comparing designs. Deepening, for merging a cluster of shallow modules, sorts each dependency into a kind, which decides how you test:

| Dependency kind | Strategy |
| --- | --- |
| In-process (pure computation, in-memory state) | Merge and test through the new interface; no adapter. |
| Local-substitutable (a local stand-in exists, such as an in-memory database) | Run the stand-in in the suite; keep the seam internal. |
| Remote but owned (your own network services) | Put a port at the seam, keep logic inside, supply transport as an adapter, and test with an in-memory one. |
| True external (third-party services) | Inject through a port and give tests a mock adapter. |

Tests should check observable outcomes and survive internal refactors. A stand-in or mock only proves behavior at its test seam, so real integration checks are named separately. An old test is retired only when new checks clearly keep its coverage and the change is within the authorized refactor.

**Design It Twice** compares distinct interfaces for one chosen candidate. The agent first shows you the constraints, the dependencies and a sketch that proposes nothing. It then builds alternatives around different priorities: a minimal interface, maximum flexibility, a trivial common case and, where relevant, ports and adapters. Each reports its full interface, a caller example and its tradeoffs. The agent compares them in prose, recommends one, and may propose a hybrid. Parallel fresh-context workers run only if available and authorized, and only as many as give useful, different designs; otherwise it explores in sequence and tells you the designs were not independent.

## When to use it

Ask for it by name when an interface needs designing or improving, when you want to find modules worth deepening or decide where a seam goes, or when you want code that is easier to test and for an agent to navigate. Skills such as [Journey](/skills/journey) and [improve-codebase-architecture](/skills/improve-codebase-architecture) also load it for the vocabulary. It needs no setup of its own.

| What you have | Reach for |
| --- | --- |
| A codebase and no idea where the shallow modules are | [improve-codebase-architecture](/skills/improve-codebase-architecture), a request-only survey that produces a report and uses this skill's vocabulary |
| One chosen module whose interface is unsettled | codebase-design |
| An accepted design ready to build | [tdd](/skills/tdd) |
| A bug with an unknown cause | [diagnosing-bugs](/skills/diagnosing-bugs) |
| Disputed or overloaded business terms | [domain-modeling](/skills/domain-modeling) |

## Example request

> The order-processing code is split across five tiny files and every test mocks half of them. Use codebase design to tell me whether these modules are shallow, and show me two or three different interface options before we touch anything.

The agent should read callers and tests first, then present alternatives and stop at a recommendation.

## What it requires

- Access to the code, callers and existing tests, since the method starts from real call paths.
- The project's instructions and accepted vocabulary, when they exist. Without a glossary the agent uses the terms callers already use and flags uncertain meanings.
- A place for the design to land: the project's existing design record, or chat.
- Optionally, authorized subagents for parallel alternatives.

It does not require a Workbench (the structured project setup this catalog is built around).

## What it does not authorize

Design alone grants no code changes, no test deletion and no publication. A recommendation is not an accepted decision, and comparing designs does not authorize building one. To carry out an accepted design, use [tdd](/skills/tdd) or the project's task workflow.

## FAQs

### Is this a refactoring tool?

No. It produces a vocabulary, a method and a written recommendation. It changes no source code; execution goes through another skill or your task workflow, with its own authority.

### My tests pass against a mock. Does the integration work?

Not necessarily. A mock or local stand-in only exercises behavior at the test seam, not the production network, provider or environment. A good run names the integration checks still needed.

### The agent could not see the callers or tests. What then?

It should state its assumptions and leave affected choices provisional rather than guess. Supply the missing call paths or tests and ask again.

### Will it delete my old tests once the new module exists?

Not on its own. A test goes only when new interface checks preserve its coverage and the change is inside the authorized refactor. Independent contracts and regression cases stay.

## It's working when

- The agent reads callers, data ownership and tests before proposing structure.
- Interfaces are described fully, including ordering, errors and configuration, not just method names.
- Recommendations survive the deletion test and rest on actual variation, in your project's own terms.
- Proposed tests cross the same seam callers use, and mocks come with a note on what they cannot prove.
- Alternatives differ in real ways, and the agent says when they were not independent.
- Recommended and accepted are kept apart. The only things written are design notes in the project's design record or chat; no source code or tests change.

## Where it fits in the workflow

Codebase design is a supporting skill in the Journey stage (build each Task), not a step in the main flow. [Journey](/skills/journey) points to it when an interface is unsettled during implementation, within the design authority you have granted. [improve-codebase-architecture](/skills/improve-codebase-architecture), from the Improve stage, relies on it for vocabulary, dependency classification and any interface alternatives you request. Once a design is accepted, it hands off to [tdd](/skills/tdd) or the project's task workflow, carrying unresolved interface choices.
