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

# Harness

Use this section for harness; [ai-coding-reference](ai-coding-reference.md) provides the surrounding context.

## Harness

Everything around a model that makes it an agent: its tools, its system prompt, the way the context window is managed, permissions and hooks. It builds each request, executes the tool calls that the model requests, returns the results, keeps the session history, asks the user before risky actions and chooses when to compact. Claude Code, Codex CLI, Cursor and Claude.ai are harnesses.

**In the Workbench.** The Workbench is not a harness: it is the agentic management system that a harness such as Claude Code or Codex loads, so its agents can align the owner's ideas and implement the owner's design concepts. `AGENTS.md`, permission settings and hooks are instructions to the harness. One model behaves differently under different harnesses (Claude.ai answers, Claude Code edits files), so when behavior changes the harness is often the variable. In the Workbench's words "host" means the harness where it names software (a Chat's host, a host adapter such as `CLAUDE.md`) and the machine where it names a machine (Host portability). Public names that carry the word, such as the `update-harness` skill, stay until they are renamed on their own.

Attribution: [AI Coding Dictionary, Harness](https://www.aihero.dev/ai-coding-dictionary/harness).
