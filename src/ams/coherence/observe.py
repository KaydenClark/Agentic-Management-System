"""Non-blocking, secret-free coherence observations of pinned Git artifacts.

The frozen contract is read at --source, never from the candidate under test.
Only safe derived facts enter the existing Markdown coherence-report lane.
This does not execute product code, install skills, or qualify improvements.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile


SHA = re.compile(r"[a-f0-9]{40}\Z")
DIGEST = re.compile(r"[a-f0-9]{64}\Z")
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,99}\Z")
SPEC = re.compile(r"S-[A-Z0-9]{3,}\Z")
TASK = re.compile(r"TK-[A-Z0-9]{3,}\Z")
MARKER = "<!-- ams-coherence-observation-v1 -->\n```json\n"
LIMIT = 1024 * 1024
REASONS = {
    "acceptance-miss": ("required-text-present", {"artifact-missing", "required-text-absent"}),
    "missing-map": ("verified-existing-map", {"absent-or-changed"}),
    "missing-plan": ("verified-existing-plan", {"absent-or-changed"}),
    "prepare-stop-bypass": ("changes-within-frozen-scope", {"out-of-scope-change"}),
    "assignment-scope": ("changes-within-frozen-scope", {"out-of-scope-change"}),
    "unknown-loaded-skill": ("native-loaded-use-evidence", {"unavailable"}),
    "stale-loaded-skill": ("frozen-loaded-identity", {"different-loaded-identity"}),
}


class Refused(ValueError):
    """Unsafe, unpinned or conflicting observation. No raw input is echoed."""


def require(condition, reason):
    if not condition:
        raise Refused(reason)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def fields(value, names):
    require(type(value) is dict and value.keys() == set(names.split()), "fields are allowlisted")


def identity(value, pattern=ID):
    require(type(value) is str and pattern.fullmatch(value), "invalid identity")


def safe_path(value):
    require(type(value) is str and 0 < len(value) < 300 and
            re.fullmatch(r"[A-Za-z0-9_.\-/]+", value), "unsafe artifact path")
    parts = PurePosixPath(value).parts
    require(not value.startswith("/") and all(p not in ("..", ".", ".git", ".local", "sessions")
            and not p.startswith(".env") for p in parts), "private or escaping artifact path")
    require(str(PurePosixPath(value)) == value, "artifact path must be canonical")
    return value


def git(repo, *args, optional=False):
    # Local objects only; no credential, database or provider environment reaches Git.
    env = {"PATH": os.defpath, "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0",
           "GIT_NO_LAZY_FETCH": "1", "GIT_ALLOW_PROTOCOL": "", "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_CONFIG_GLOBAL": os.devnull}
    try:
        r = subprocess.run(["git", "--no-replace-objects", "-c", "core.fsmonitor=false", *args],
                           cwd=repo, env=env, capture_output=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        raise Refused("local Git evidence unavailable") from None
    if r.returncode:
        if optional:
            return None
        raise Refused("local Git evidence unavailable")
    require(len(r.stdout) <= LIMIT, "artifact exceeds observation limit")
    return r.stdout


def blob(repo, commit, path, optional=False):
    safe_path(path)
    # A committed symlink is not an ordinary observation artifact.
    entry = git(repo, "ls-tree", commit, "--", path)
    if not entry:
        if optional:
            return None
        raise Refused("observation artifact missing")
    require(entry.startswith((b"100644 blob ", b"100755 blob ")), "artifact is not an ordinary blob")
    return git(repo, "show", f"{commit}:{path}")


def decode(raw):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, "duplicate JSON field")
            out[key] = value
        return out
    try:
        return json.loads(raw, object_pairs_hook=unique,
                          parse_constant=lambda _: (_ for _ in ()).throw(Refused("nonfinite JSON")))
    except (ValueError, UnicodeError):
        raise Refused("invalid observation JSON") from None


def contract_at(repo, source, path):
    raw = blob(repo, source, path)
    c = decode(raw)
    fields(c, "schema_version synthetic family failure_id spec_id task_id phase probes workflow skill")
    require(type(c["schema_version"]) is int and c["schema_version"] == 1, "unsupported schema")
    require(type(c["synthetic"]) is bool, "synthetic label required")
    for key in ("family", "failure_id"):
        identity(c[key])
    identity(c["spec_id"], SPEC)
    identity(c["task_id"], TASK)
    require(c["phase"] in ("acceptance", "expected-red"), "invalid observation phase")
    require(type(c["probes"]) is list and 0 < len(c["probes"]) <= 100, "bounded acceptance probes required")
    seen = set()
    for probe in c["probes"]:
        fields(probe, "id path contains")
        identity(probe["id"])
        require(probe["id"] not in seen, "duplicate probe")
        seen.add(probe["id"])
        safe_path(probe["path"])
        require(type(probe["contains"]) is str and 0 < len(probe["contains"]) <= 4000, "invalid probe")
    w = c["workflow"]
    fields(w, "size limit source_repository map plan allowed_paths")
    require(w["size"] in ("small", "large") and w["limit"] in ("prepare", "implement"), "invalid workflow scope")
    require(w["source_repository"] in ("ams", "KaydenClark/skills"), "unsupported source owner")
    require(type(w["allowed_paths"]) is list and 0 < len(w["allowed_paths"]) <= 100, "bounded scope required")
    for path in w["allowed_paths"]:
        safe_path(path)
    for kind in ("map", "plan"):
        if w[kind] is not None:
            fields(w[kind], "path sha256")
            safe_path(w[kind]["path"])
            identity(w[kind]["sha256"], DIGEST)
    s = c["skill"]
    if s is not None:
        fields(s, "accepted_commit expected_commit expected_digest intentional_baseline receipt_path")
        for key in ("accepted_commit", "expected_commit"):
            identity(s[key], SHA)
        identity(s["expected_digest"], DIGEST)
        require(type(s["intentional_baseline"]) is bool, "baseline label required")
        require(s["intentional_baseline"] or s["accepted_commit"] == s["expected_commit"], "unapproved source mismatch")
        safe_path(s["receipt_path"])
    return c, digest(raw)


def task_path(repo, source, spec_id, task_id):
    files = git(repo, "ls-tree", "-r", "--name-only", source).decode().splitlines()
    suffix = f"/tasks/{task_id}/TASK.md"
    hits = [p for p in files if p.endswith(suffix) and re.search(rf"/{re.escape(spec_id)}-[^/]+/tasks/", "/" + p)]
    require(len(hits) == 1, "responsible Task is missing or ambiguous")
    text = blob(repo, source, hits[0]).decode()
    require(re.search(rf"^\*\*Task ID:\*\* {re.escape(task_id)}$", text, re.M) and
            re.search(rf"^\*\*Spec ID:\*\* {re.escape(spec_id)}$", text, re.M), "responsible Task identity differs")
    return hits[0]


def observe(repo, source, candidate, contract_path, occurrence_id, observed_at, *, previous=None):
    for sha in (source, candidate):
        identity(sha, SHA)
        require(git(repo, "rev-parse", f"{sha}^{{commit}}").decode().strip() == sha, "commit does not resolve")
    require(git(repo, "merge-base", "--is-ancestor", source, candidate, optional=True) is not None,
            "frozen source must precede candidate")
    identity(occurrence_id)
    try:
        require(observed_at.endswith("Z") and datetime.fromisoformat(observed_at[:-1] + "+00:00"), "invalid observation time")
    except (ValueError, AttributeError):
        raise Refused("invalid observation time") from None
    c, contract_digest = contract_at(repo, source, contract_path)
    owner = {"spec_id": c["spec_id"], "task_id": c["task_id"]}
    path = task_path(repo, source, **owner)
    previous_occurrence = None
    if previous is not None:
        validate_report(previous)
        require(previous["family"] == c["family"] and previous["owner"] == owner and
                previous["synthetic"] == c["synthetic"] and previous["failure_id"] == c["failure_id"] and
                previous["occurrence_id"] != occurrence_id and
                previous["observed_at"] <= observed_at, "invalid recurrence predecessor")
        previous_occurrence = previous["occurrence_id"]
    findings, probes, red = [], [], 0

    def finding(code, expected, observed, *, target=None, probe=None):
        prior = next((f["id"] for f in (previous or {}).get("findings", [])
                      if f["code"] == code and f["probe_id"] == probe), None)
        findings.append({"id": "COH-" + digest(f"{occurrence_id}:{code}:{probe}".encode())[:24],
                         "failure_id": c["failure_id"], "code": code, "probe_id": probe,
                         "owner": target or owner, "expected": expected, "observed": observed,
                         "severity": "unknown" if code.startswith("unknown-") else "error",
                         "disposition": "pending", "next_action": "inspect-and-route-to-existing-owner",
                         "previous_finding": prior})

    for p in c["probes"]:
        raw = blob(repo, candidate, p["path"], optional=True)
        passed = raw is not None and p["contains"].encode() in raw
        probes.append({"id": p["id"], "path": p["path"], "artifact_digest": digest(raw) if raw is not None else None,
                       "passed": passed})
        if not passed:
            if c["phase"] == "expected-red":
                red += 1
            else:
                finding("acceptance-miss", "required-text-present", "artifact-missing" if raw is None else "required-text-absent",
                        probe=p["id"])
    w = c["workflow"]
    repair_owner = {"spec_id": "S-000A", "task_id": None}
    if w["size"] == "large":
        for kind in ("map", "plan"):
            ref = w[kind]
            raw = blob(repo, source, ref["path"], optional=True) if ref else None
            if not raw or digest(raw) != ref["sha256"]:
                finding("missing-" + kind, "verified-existing-" + kind, "absent-or-changed", target=repair_owner)
    changed = git(repo, "diff", "--name-only", "-z", source, candidate).decode().split("\0")
    out_of_scope = [p for p in changed if p and not any(p == allowed or p.startswith(allowed + "/")
                                                       for allowed in w["allowed_paths"])]
    if out_of_scope:
        finding("prepare-stop-bypass" if w["limit"] == "prepare" else "assignment-scope",
                "changes-within-frozen-scope", "out-of-scope-change", target=repair_owner)
    skill_use = None
    if c["skill"] is not None:
        s = c["skill"]
        raw = blob(repo, candidate, s["receipt_path"], optional=True)
        if raw is None:
            finding("unknown-loaded-skill", "native-loaded-use-evidence", "unavailable")
        else:
            receipt = decode(raw)
            fields(receipt, "kind host use_id source_commit installed_digest loaded_digest use_observed")
            require(receipt["kind"] == "native-loaded-use" and receipt["host"] in ("codex", "claude"), "invalid native observation")
            identity(receipt["use_id"])
            for key, pattern in (("source_commit", SHA), ("installed_digest", DIGEST), ("loaded_digest", DIGEST)):
                if receipt[key] is not None:
                    identity(receipt[key], pattern)
            require(type(receipt["use_observed"]) is bool, "native use must be observed separately")
            skill_use = {**receipt, "receipt_digest": digest(raw),
                         "condition": "intentional-baseline" if s["intentional_baseline"] else "accepted-version"}
            if any(receipt[k] is None for k in ("source_commit", "installed_digest", "loaded_digest")) or not receipt["use_observed"]:
                skill_use["condition"] = "unknown"
                finding("unknown-loaded-skill", "native-loaded-use-evidence", "unavailable")
            elif receipt["source_commit"] != s["expected_commit"] or any(
                    receipt[k] != s["expected_digest"] for k in ("installed_digest", "loaded_digest")):
                skill_use["condition"] = "stale"
                finding("stale-loaded-skill", "frozen-loaded-identity", "different-loaded-identity")
    report = {"schema_version": 1, "synthetic": c["synthetic"], "occurrence_id": occurrence_id,
            "previous_occurrence": previous_occurrence, "observed_at": observed_at, "family": c["family"],
            "failure_id": c["failure_id"], "owner": owner, "task_path": path,
            "source": source, "candidate": candidate, "contract_path": contract_path, "contract_digest": contract_digest,
            "phase": c["phase"], "source_repository": w["source_repository"], "probes": probes,
            "findings": findings, "skill_use": skill_use, "expected_red_count": red,
            "eligible_uses": int(not findings and not red and c["phase"] == "acceptance" and skill_use is not None),
            "non_blocking": True}
    validate_report(report)
    return report


def validate_report(report):
    # Validate the safe derived projection before publication/recovery. This
    # does not authenticate the upstream native host observation.
    fields(report, "schema_version synthetic occurrence_id previous_occurrence observed_at family failure_id owner task_path source candidate contract_path contract_digest phase source_repository probes findings skill_use expected_red_count eligible_uses non_blocking")
    require(type(report["schema_version"]) is int and report["schema_version"] == 1 and report["non_blocking"] is True,
            "invalid report version")
    for key in ("occurrence_id", "family", "failure_id"):
        identity(report[key])
    if report["previous_occurrence"] is not None:
        identity(report["previous_occurrence"])
    for key in ("source", "candidate"):
        identity(report[key], SHA)
    identity(report["contract_digest"], DIGEST)
    safe_path(report["task_path"])
    safe_path(report["contract_path"])
    # Output never contains arbitrary messages, expected text, raw bodies or locators.
    require(type(report["synthetic"]) is bool and type(report["findings"]) is list, "invalid report labels")
    require(type(report["owner"]) is dict and report["owner"].keys() == {"spec_id", "task_id"}, "invalid report owner")
    identity(report["owner"]["spec_id"], SPEC)
    identity(report["owner"]["task_id"], TASK)
    require(report["phase"] in ("acceptance", "expected-red") and
            report["source_repository"] in ("ams", "KaydenClark/skills"), "invalid report scope")
    require(type(report["observed_at"]) is str and re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", report["observed_at"]),
            "invalid report timestamp")
    try:
        datetime.fromisoformat(report["observed_at"][:-1] + "+00:00")
    except ValueError:
        raise Refused("invalid report timestamp") from None
    require(type(report["probes"]) is list and 0 < len(report["probes"]) <= 100, "invalid report probes")
    probe_ids = set()
    for p in report["probes"]:
        fields(p, "id path artifact_digest passed")
        identity(p["id"])
        require(p["id"] not in probe_ids, "duplicate report probe")
        probe_ids.add(p["id"])
        safe_path(p["path"])
        if p["artifact_digest"] is not None:
            identity(p["artifact_digest"], DIGEST)
        require(type(p["passed"]) is bool, "invalid probe outcome")
    for f in report["findings"]:
        fields(f, "id failure_id code probe_id owner expected observed severity disposition next_action previous_finding")
        require(type(f["code"]) is str and f["code"] in REASONS, "unknown finding code")
        expected, observed = REASONS[f["code"]]
        require(f["expected"] == expected and f["observed"] in observed and
                f["severity"] == ("unknown" if f["code"].startswith("unknown-") else "error") and
                f["disposition"] == "pending" and f["next_action"] == "inspect-and-route-to-existing-owner",
                "invalid finding facts")
        require(f["failure_id"] == report["failure_id"], "failure identity differs")
        require(f["probe_id"] is None or f["probe_id"] in probe_ids, "unknown finding probe")
        require(f["id"] == "COH-" + digest(f"{report['occurrence_id']}:{f['code']}:{f['probe_id']}".encode())[:24],
                "finding identity differs")
        if f["previous_finding"] is not None:
            require(type(f["previous_finding"]) is str and re.fullmatch(r"COH-[a-f0-9]{24}", f["previous_finding"]),
                    "invalid previous finding")
        require(f["owner"] == report["owner"] or f["owner"] == {"spec_id": "S-000A", "task_id": None},
                "invalid routed owner")
        target = {"spec_id": "S-000A", "task_id": None} if f["code"] in (
            "missing-map", "missing-plan", "prepare-stop-bypass", "assignment-scope") else report["owner"]
        require(f["owner"] == target, "finding routed to wrong owner")
    s = report["skill_use"]
    if s is not None:
        fields(s, "kind host use_id source_commit installed_digest loaded_digest use_observed receipt_digest condition")
        require(s["kind"] == "native-loaded-use" and s["host"] in ("codex", "claude"), "invalid host identity")
        identity(s["use_id"])
        for k, pattern in (("source_commit", SHA), ("installed_digest", DIGEST), ("loaded_digest", DIGEST), ("receipt_digest", DIGEST)):
            if s[k] is not None:
                identity(s[k], pattern)
        require(type(s["use_observed"]) is bool and s["condition"] in
                ("accepted-version", "intentional-baseline", "unknown", "stale"), "invalid use observation")
    require(type(report["expected_red_count"]) is int and 0 <= report["expected_red_count"] <= len(probe_ids),
            "invalid expected-red count")
    failed = {p["id"] for p in report["probes"] if not p["passed"]}
    missed = [f["probe_id"] for f in report["findings"] if f["code"] == "acceptance-miss"]
    require(set(missed) == (failed if report["phase"] == "acceptance" else set()) and len(missed) == len(set(missed)) and
            report["expected_red_count"] == (len(failed) if report["phase"] == "expected-red" else 0),
            "failed acceptance probe lost its finding")
    require(type(report["eligible_uses"]) is int and report["eligible_uses"] == int(
        not report["findings"] and not report["expected_red_count"] and report["phase"] == "acceptance" and
        s is not None and s["condition"] in ("accepted-version", "intentional-baseline") and s["use_observed"]),
        "invalid eligible-use count")


def report_text(report):
    validate_report(report)
    return (f"# Coherence occurrence {report['occurrence_id']}\n\n"
            f"{'Synthetic fixture' if report['synthetic'] else 'Observed evidence'}; non-blocking. "
            "No Human QA, skill causation or improvement benefit is established.\n\n" + MARKER +
            json.dumps(report, indent=2, sort_keys=True) + "\n```\n")


def ordinary_directory(directory, *, create=False):
    directory = Path(directory).absolute()
    for path in [*reversed(directory.parents), directory]:
        require(not path.is_symlink(), "report path traverses a symlink")
    if create:
        directory.mkdir(parents=True, exist_ok=True)
    require(directory.is_dir(), "report directory unavailable")
    return directory


def publish(report, directory):
    text = report_text(report)
    directory = ordinary_directory(directory, create=True)
    retained = recover(directory)
    if report["previous_occurrence"] is not None:
        previous = [p for p in retained if p["occurrence_id"] == report["previous_occurrence"]]
        require(len(previous) == 1 and all(previous[0][k] == report[k] for k in ("family", "owner", "failure_id", "synthetic")),
                "recurrence predecessor unavailable or different")
        for f in report["findings"]:
            expected = next((p["id"] for p in previous[0]["findings"] if p["code"] == f["code"] and
                             p["probe_id"] == f["probe_id"]), None)
            require(f["previous_finding"] == expected, "recurrence link differs")
    if report["skill_use"] is not None:
        for prior in retained:
            if prior["synthetic"] == report["synthetic"] and prior["skill_use"] is not None and \
                    prior["skill_use"]["use_id"] == report["skill_use"]["use_id"]:
                require(prior == report, "native use already belongs to an occurrence")
    path = directory / ("OBS-" + digest(report["occurrence_id"].encode())[:32] + ".md")
    require(not path.is_symlink(), "report is not an ordinary file")
    # Write complete bytes first; exclusive linking cannot expose a partial
    # report or replace another writer's same-occurrence file.
    fd, temporary = tempfile.mkstemp(prefix=".observation-", dir=directory)
    try:
        with os.fdopen(fd, "w") as out:
            out.write(text)
            out.flush()
            os.fsync(out.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            require(not path.is_symlink() and path.is_file() and path.read_text() == text,
                    "same occurrence has conflicting evidence")
            return "unchanged"
    finally:
        os.unlink(temporary)
    return "created"


def recover(directory, spec_id=None, task_id=None):
    reports = []
    for path in sorted(ordinary_directory(directory).glob("OBS-*.md")):
        require(not path.is_symlink() and path.is_file() and path.stat().st_size <= LIMIT, "invalid report file")
        text = path.read_text()
        require(text.count(MARKER) == 1 and text.endswith("\n```\n"), "invalid observation report")
        report = decode(text.split(MARKER)[1][:-5])
        validate_report(report)
        require(report_text(report) == text, "observation report has changed")
        owners = [report["owner"], *(f["owner"] for f in report["findings"])]
        if any((spec_id is None or o["spec_id"] == spec_id) and
               (task_id is None or o["task_id"] == task_id) for o in owners):
            reports.append(report)
    return reports


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check")
    check.add_argument("--repo", default=".")
    for option in ("source", "candidate", "contract", "occurrence", "observed-at"):
        check.add_argument("--" + option, required=True)
    check.add_argument("--reports", default="workbench/feedback/coherence")
    check.add_argument("--previous")
    check.add_argument("--write", action="store_true")
    read = commands.add_parser("recover")
    read.add_argument("--reports", default="workbench/feedback/coherence")
    read.add_argument("--spec")
    read.add_argument("--task")
    args = parser.parse_args(argv)
    try:
        if args.command == "recover":
            out = recover(args.reports, args.spec, args.task)
        else:
            previous = None
            if args.previous:
                found = [r for r in recover(args.reports) if r["occurrence_id"] == args.previous]
                require(len(found) == 1, "recurrence predecessor unavailable")
                previous = found[0]
            out = observe(args.repo, args.source, args.candidate, args.contract, args.occurrence, args.observed_at,
                          previous=previous)
            if args.write:
                publish(out, args.reports)
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0
    except (Refused, OSError, UnicodeError):
        print("coherence observation refused: unsafe, unavailable or conflicting evidence", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
