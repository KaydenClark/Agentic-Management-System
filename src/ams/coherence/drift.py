"""S-013 TK-001 (ADR-002T): how far `dev` runs ahead of and behind `main`.

Read-only and secret-free: needs only `git` (plus `git fetch` from the remote).
Non-blocking (ADR-000H, S-013 contract): a measurement always exits 0, breach or
not; exit 2 means the check could not measure.

Days = whole days from the oldest commit one side lacks (committer date) to the
measurement time, i.e. how long unmerged work has waited.

Run: uv run python -m ams.coherence.drift [--write PATH] [--json]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULTS = {"remote": "origin", "base": "main", "head": "dev",
            "threshold_commits": 20, "threshold_days": 7}


def _git(repo: str, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True,
                          capture_output=True, text=True).stdout.strip()


def _parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _side(repo: str, frm: str, to: str, now: datetime) -> dict:
    rng = f"{frm}..{to}"
    commits = int(_git(repo, "rev-list", "--count", rng))
    if not commits:
        return {"commits": 0, "days": 0, "oldest": None}
    oldest = min(_parse(t) for t in _git(repo, "log", "--format=%cI", rng).splitlines() if t)
    return {"commits": commits, "days": (now - oldest).days, "oldest": _iso(oldest)}


def measure_drift(repo: str = ".", remote: str = DEFAULTS["remote"], base: str = DEFAULTS["base"],
                  head: str = DEFAULTS["head"], fetch: bool = True, now: str | None = None,
                  threshold_commits: int = DEFAULTS["threshold_commits"],
                  threshold_days: int = DEFAULTS["threshold_days"]) -> dict:
    if fetch:
        _git(repo, "fetch", "--quiet", remote, base, head)
    base_ref, head_ref = (f"{remote}/{base}", f"{remote}/{head}") if fetch else (base, head)
    measured_at = now or _iso(datetime.now(timezone.utc))
    now_dt = _parse(measured_at)
    ahead = _side(repo, base_ref, head_ref, now_dt)
    behind = _side(repo, head_ref, base_ref, now_dt)
    reasons = [name for name, over in (("commits", ahead["commits"] > threshold_commits),
                                       ("days", ahead["days"] > threshold_days)) if over]
    return {
        "measured_at": measured_at, "base": base, "head": head,
        "base_ref": base_ref, "head_ref": head_ref,
        "base_sha": _git(repo, "rev-parse", base_ref),
        "head_sha": _git(repo, "rev-parse", head_ref),
        "ahead": ahead, "behind": behind,
        "threshold": {"commits": threshold_commits, "days": threshold_days,
                      "breached": bool(reasons), "reasons": reasons},
    }


def render_report(r: dict) -> str:
    t = r["threshold"]
    verdict = f"BREACH ({', '.join(t['reasons'])})" if t["breached"] else "within threshold"
    h, b = r["head"], r["base"]
    row = lambda label, s: f"| `{h}` {label} `{b}` | {s['commits']} | {s['days']} | {s['oldest'] or 'none'} |"
    return "\n".join([
        f"# Drift report: `{h}` vs `{b}`",
        "",
        f"- **Measured at (UTC):** {r['measured_at']}",
        f"- **`{b}`:** `{r['base_sha']}` ({r['base_ref']})",
        f"- **`{h}`:** `{r['head_sha']}` ({r['head_ref']})",
        f"- **Threshold:** more than {t['commits']} commits or {t['days']} days ahead. **Result:** {verdict}",
        "- **Check:** `uv run python -m ams.coherence.drift` (S-013 TK-001, non-blocking)",
        "",
        "| Direction | Commits | Days | Oldest unmerged commit |",
        "|---|---|---|---|",
        row("ahead of", r["ahead"]),
        row("behind", r["behind"]),
        "",
        "Days count from the oldest commit one side lacks to the measurement time. "
        "A breach raises a Grill Board item once S-013 TK-005 lands; until then it is reported here only.",
        "",
    ])


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--repo", default=".")
    p.add_argument("--remote", default=DEFAULTS["remote"])
    p.add_argument("--base", default=DEFAULTS["base"])
    p.add_argument("--head", default=DEFAULTS["head"])
    p.add_argument("--now", help="measurement time, ISO-8601 UTC (default: now)")
    p.add_argument("--no-fetch", dest="fetch", action="store_false")
    p.add_argument("--threshold-commits", type=int, default=DEFAULTS["threshold_commits"])
    p.add_argument("--threshold-days", type=int, default=DEFAULTS["threshold_days"])
    p.add_argument("--json", action="store_true")
    p.add_argument("--write", help="also write the output to this path")
    a = p.parse_args(argv)
    try:
        r = measure_drift(a.repo, a.remote, a.base, a.head, a.fetch, a.now,
                          a.threshold_commits, a.threshold_days)
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"drift: cannot measure: {getattr(e, 'stderr', '') or e}", file=sys.stderr)
        return 2
    out = json.dumps(r, indent=2) + "\n" if a.json else render_report(r)
    if a.write:
        Path(a.write).parent.mkdir(parents=True, exist_ok=True)
        Path(a.write).write_text(out)
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
