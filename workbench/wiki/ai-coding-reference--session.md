---
type: meta
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - LLM Workbench template wiki: general AI coding terms adopted from the AI Coding Dictionary
source_paths:
  - GLOSSARY.md
last_verified: 2026-11-01
---

# Session

Use this section for session; [ai-coding-reference](ai-coding-reference.md) provides the surrounding context.

## Session

A single bounded run of working with an agent. It starts empty, accumulates the messages, tool outputs and files opened along the way, and ends when it is cleared, closed, or summarized into a new one. What fills the context window is the session, and its history is the agent's working memory, lost when it ends; only files survive.

**In the Workbench.** A Chat is the owner-visible working context in a host; a session is one run of the context window inside it. A Chat normally holds one session and may hold more when the harness compacts or clears within it, and a Task still maps to one Chat. Inference: this joins the two agreed definitions and is not a separate owner answer. "Session" in `AGENTS.md`'s Session Records And Checkpoints and Long Session Control sections, and the `sessions` support lane, use the word in this sense: the lane's records outlive any one session. Keeping to one task a session keeps what is loaded on topic.

Attribution: [AI Coding Dictionary, Session](https://www.aihero.dev/ai-coding-dictionary/session).
