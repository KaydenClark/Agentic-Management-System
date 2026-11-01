#!/usr/bin/env bash
# Stop hook (Claude Code and Codex): refuse to end a turn while AMS has
# uncommitted work. Blocks once with instructions; if the agent still
# cannot commit, it may stop but the owner sees a visible warning.
set -u
input="$(cat)"
root="$(cd "$(dirname "$0")/../.." && pwd)"
dirty="$(git -C "$root" status --porcelain 2>/dev/null)"
[ -z "$dirty" ] && exit 0

count="$(printf '%s\n' "$dirty" | wc -l | tr -d ' ')"
branch="$(git -C "$root" branch --show-current 2>/dev/null)"

if printf '%s' "$input" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  msg="AMS still has $count uncommitted change(s) on '$branch'. The agent ended without committing them."
  printf '{"systemMessage": %s}\n' "$(printf '%s' "$msg" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')"
  exit 0
fi

reason="AMS has $count uncommitted change(s) on branch '$branch'. Uncommitted work loses the owner's intent. Before ending this turn: review 'git status', then commit your work on the current branch (never main) with a message that states what changed and why. Do not stash, reset or discard. If you truly cannot commit (sandbox or permission denial), say so plainly to the owner and list the files."
printf '{"decision": "block", "reason": %s}\n' "$(printf '%s' "$reason" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')"
exit 0
