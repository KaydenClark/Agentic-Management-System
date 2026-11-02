# Drift report: `dev` vs `main`

- **Measured at (UTC):** 2026-11-01T15:42:42Z
- **`main`:** `b0fd71f948924981775f34d39199b40dd340e188` (origin/main)
- **`dev`:** `e0317ae83d6b1c4ec2fb45771dc4b8dceedba713` (origin/dev)
- **Threshold:** more than 20 commits or 7 days ahead. **Result:** BREACH (commits)
- **Check:** `uv run python -m ams.coherence.drift` (S-013 TK-001, non-blocking)

| Direction | Commits | Days | Oldest unmerged commit |
|---|---|---|---|
| `dev` ahead of `main` | 84 | 0 | 2026-11-01T12:40:06Z |
| `dev` behind `main` | 62 | 0 | 2026-11-01T14:41:31Z |

Days count from the oldest commit one side lacks to the measurement time. A breach raises a Grill Board item once S-013 TK-005 lands; until then it is reported here only.
