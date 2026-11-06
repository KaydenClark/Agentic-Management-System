"""Scoring for the session-orientation trial (LMK-000B).

Event streams are small synthetic copies of the shapes each CLI emits.
"""

import json

from ams import orientation_trial as trial


def lines(*events):
    return "\n".join(json.dumps(event) for event in events) + "\n"


def claude_stream(reads, answer):
    blocks = [{"type": "tool_use", "name": "Read", "input": {"file_path": path}} for path in reads]
    return lines(
        {"type": "system", "subtype": "init", "model": "claude-opus-5-5"},
        {"type": "assistant", "message": {"content": blocks}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": answer}]}},
        {"type": "result", "subtype": "success", "result": answer},
    )


def codex_stream(commands, messages):
    events = [{"type": "thread.started", "thread_id": "t"}]
    for command in commands:
        events.append({"type": "item.completed",
                       "item": {"type": "command_execution", "command": command, "exit_code": 0}})
    for text in messages:
        events.append({"type": "item.completed", "item": {"type": "agent_message", "text": text}})
    return lines(*events)


NOTE = "**Orientation**\n- Read: AGENTS.md, RUNBOOK.md, TASKBOARD.md\n- Exists: LMK-001\n\nAnswer follows."


def test_claude_run_that_reads_runbook_and_opens_with_note_passes():
    result = trial.score("claude", claude_stream(["/w/AGENTS.md", "/w/RUNBOOK.md"], NOTE))
    assert result["readRunbook"] is True
    assert result["orientationNote"] is True
    assert result["passed"] is True
    assert result["model"] == "claude-opus-5-5"


def test_claude_run_that_answers_without_runbook_fails():
    result = trial.score("claude", claude_stream(["/w/README.md"], "Here is what I recommend."))
    assert result["readRunbook"] is False
    assert result["orientationNote"] is False
    assert result["passed"] is False


def test_note_buried_after_the_answer_does_not_count():
    answer = "I recommend redesigning the board. " * 30 + "\n\nOrientation: read RUNBOOK.md"
    result = trial.score("claude", claude_stream(["/w/RUNBOOK.md"], answer))
    assert result["readRunbook"] is True
    assert result["orientationNote"] is False


def test_codex_shell_read_of_runbook_counts_and_final_message_is_scored():
    stream = codex_stream(["/bin/zsh -lc 'sed -n 1,80p RUNBOOK.md'"], ["I'll orient first.", NOTE])
    result = trial.score("codex", stream)
    assert result["readRunbook"] is True
    assert result["orientationNote"] is True
    assert result["finalAnswer"] == NOTE


def test_codex_mention_in_text_without_reading_does_not_count():
    stream = codex_stream(["/bin/zsh -lc 'ls'"], ["Orientation: the RUNBOOK.md says to orient."])
    result = trial.score("codex", stream)
    assert result["readRunbook"] is False
    assert result["passed"] is False


def test_noise_lines_between_events_are_ignored():
    stream = "WARN something\n" + claude_stream(["/w/RUNBOOK.md"], NOTE)
    assert trial.score("claude", stream)["passed"] is True


def test_cases_file_has_unique_ids_and_prompts():
    cases = trial.load_cases()
    ids = [case["id"] for case in cases]
    assert len(ids) == len(set(ids)) >= 3
    assert all(case["prompt"].strip() for case in cases)
