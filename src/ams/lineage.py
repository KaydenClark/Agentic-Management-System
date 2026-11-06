"""Immutable safe RSI lineage. Operational records are private to the writer.

Existing run/result IDs remain authoritative: non-synthetic lineage references
their rows rather than copying measurements or creating another trial ledger.
Publication is an atomic, expected-head append; a timeout remains unpublished
until a subsequent readback verifies the original identities and exact bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlencode

from ams import keycheck, writer

TABLE = "rsi_lineage"
RPC = "ams_append_lineage"
FORMAT = 1
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}\Z")
NAMESPACE = re.compile(r"[a-z][a-z0-9_-]{2,79}\Z")
COMMIT = re.compile(r"[0-9a-f]{40}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
TIME = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z\Z")
FIELDS = {"namespace", "record_id", "kind", "parents", "attributes", "source_commit",
          "artifact_digest", "occurred_at", "is_test", "synthetic"}
# Required parent role -> immutable record kind. Optional parents are explicit.
PARENTS = {
    "failure": {}, "case": {"failure": "failure"},
    "candidate": {"case": "case"},
    "comparison": {"case": "case", "current_candidate": "candidate", "candidate": "candidate"},
    "run": {"comparison": "comparison", "candidate": "candidate"},
    "result": {"run": "run"},
    "disposition": {"comparison": "comparison", "result": "result"},
    "adoption": {"candidate": "candidate", "disposition": "disposition"},
    "use": {"adoption": "adoption"},
}
ATTRS = {
    "failure": {"failure_id", "family"}, "case": {"version"},
    "candidate": {"attempt", "skills_commit"},
    "comparison": {"campaign_id", "contract_digest"}, "run": {"run_key"},
    "result": {"execution_state", "passed"}, "disposition": {"decision"},
    "adoption": {"receipt_digest", "adopted_commit"},
    "use": {"task_id", "loaded_digest", "outcome"},
}


class Refused(ValueError):
    """Invalid or conflicting evidence; contains no remote body or credentials."""


class Unavailable(Refused):
    """No successful publication/readback; keep the local intake pending."""


def require(value, message):
    if not value:
        raise Refused(message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def validate_record(record):
    require(type(record) is dict and record.keys() == FIELDS, "lineage fields are allowlisted")
    kind = record["kind"]
    require(type(kind) is str and kind in PARENTS, "unknown lineage kind")
    require(type(record["namespace"]) is str and NAMESPACE.fullmatch(record["namespace"]), "invalid namespace")
    require(type(record["record_id"]) is str and ID.fullmatch(record["record_id"]), "invalid record identity")
    for field, pattern in (("source_commit", COMMIT), ("artifact_digest", DIGEST), ("occurred_at", TIME)):
        require(type(record[field]) is str and pattern.fullmatch(record[field]), "invalid " + field)
    # Parsing catches invalid calendar dates that a timestamp-shaped string hides.
    from datetime import datetime
    try:
        datetime.fromisoformat(record["occurred_at"].replace("Z", "+00:00"))
    except ValueError:
        raise Refused("invalid occurred_at") from None
    require(type(record["is_test"]) is bool and type(record["synthetic"]) is bool, "test labels must be booleans")
    require(record["is_test"] == record["namespace"].startswith("test-"), "test data requires test namespace")
    require(not record["synthetic"] or record["is_test"], "synthetic data must stay test data")
    parents, attrs = record["parents"], record["attributes"]
    optional = {"previous_candidate"} if kind == "candidate" else set()
    require(type(parents) is dict and set(PARENTS[kind]) <= parents.keys()
            and parents.keys() <= set(PARENTS[kind]) | optional, "invalid parent roles")
    require(all(type(p) is str and ID.fullmatch(p) for p in parents.values()), "invalid parent identity")
    extra = {"rsi_run_id"} if kind == "run" else {"rsi_result_id"} if kind == "result" else set()
    require(type(attrs) is dict and ATTRS[kind] <= attrs.keys() and attrs.keys() <= ATTRS[kind] | extra,
            "lineage attributes are allowlisted")
    for key, value in attrs.items():
        if key in ("version", "attempt", "rsi_run_id", "rsi_result_id"):
            require(type(value) is int and 0 <= value <= 2**63 - 1, "invalid " + key)
            if key != "attempt": require(value > 0, "invalid " + key)
        elif key == "passed":
            require(value is None or type(value) is bool, "passed must be boolean or unknown")
        else:
            pattern = COMMIT if key.endswith("commit") else DIGEST if key.endswith("digest") else ID
            require(type(value) is str and pattern.fullmatch(value), "unsafe or invalid " + key)
    if kind == "candidate":
        require(attrs["attempt"] in range(4), "candidate attempt exhausted")
        require((attrs["attempt"] > 0) == ("previous_candidate" in parents), "candidate attempt needs predecessor")
    if kind == "result":
        require(attrs["execution_state"] in ("completed", "runner_error", "auth_error", "timeout", "capped", "interrupted"),
                "invalid execution state")
        require((attrs["execution_state"] == "completed") == (attrs["passed"] is not None), "ungraded interrupted result required")
    if kind == "disposition": require(attrs["decision"] in ("retained", "rejected", "inconclusive"), "invalid disposition")
    if kind == "use": require(attrs["outcome"] in ("success", "failure", "unknown"), "invalid later-use outcome")
    if not record["synthetic"] and extra:
        require(extra <= attrs.keys(), "real lineage requires existing RSI identity")
    return record


def validate_graph(records):
    """Verify a topological snapshot, preserving occurrence and family identity."""
    require(type(records) is list, "lineage must be a list")
    by_id, roots, attempts = {}, {}, set()
    namespace = records[0].get("namespace") if records and type(records[0]) is dict else None
    for record in records:
        validate_record(record)
        rid, kind, parents, attrs = (record[k] for k in ("record_id", "kind", "parents", "attributes"))
        require(record["namespace"] == namespace, "mixed lineage namespace")
        require(rid not in by_id, "duplicate record identity")
        for role, pid in parents.items():
            expected = PARENTS[kind].get(role, "candidate")
            require(pid in by_id and by_id[pid]["kind"] == expected, "missing or wrong-kind parent")
            require(all(record[f] == by_id[pid][f] for f in ("is_test", "synthetic")), "parent evidence labels differ")
        family = attrs["failure_id"] if kind == "failure" else roots[next(iter(parents.values()))]
        require(all(roots[p] == family for p in parents.values()), "conflicting failure identities")
        if kind == "candidate":
            attempt = attrs["attempt"]
            require((family, attempt) not in attempts, "candidate attempt identity cannot reset")
            if attempt:
                prior = by_id[parents["previous_candidate"]]
                require(prior["attributes"]["attempt"] == attempt - 1, "candidate attempt skips predecessor")
            attempts.add((family, attempt))
        if kind == "comparison":
            require(all(by_id[parents[p]]["parents"]["case"] == parents["case"]
                        for p in ("current_candidate", "candidate")), "comparison case differs")
        if kind == "run":
            require(by_id[parents["comparison"]]["parents"]["candidate"] == parents["candidate"], "run candidate differs")
        if kind == "disposition":
            run = by_id[by_id[parents["result"]]["parents"]["run"]]
            require(run["parents"]["comparison"] == parents["comparison"], "result comparison differs")
        if kind == "adoption":
            decision = by_id[parents["disposition"]]
            comparison = by_id[decision["parents"]["comparison"]]
            require(decision["attributes"]["decision"] == "retained" and
                    comparison["parents"]["candidate"] == parents["candidate"], "adoption lacks retained candidate")
            require(attrs["adopted_commit"] == by_id[parents["candidate"]]["attributes"]["skills_commit"],
                    "adopted source differs")
        by_id[rid], roots[rid] = record, family
    return records


def trace(records, record_id):
    validate_graph(records)
    by_id = {r["record_id"]: r for r in records}
    require(record_id in by_id, "unknown lineage identity")
    included = set()
    def visit(rid):
        if rid in included: return
        for parent in by_id[rid]["parents"].values(): visit(parent)
        included.add(rid)
    visit(record_id)
    return [record for record in records if record["record_id"] in included]


class Store:
    def __init__(self, url, key, http=writer.urllib_http, *, page_size=250, rest_path="/rest/v1"):
        require(type(page_size) is int and 1 <= page_size <= 1000, "invalid page size")
        require(rest_path in ("", "/rest/v1"), "unsupported REST mount")
        self.url, self._key, self.http, self.page_size = url.rstrip("/"), key, http, page_size
        self.rest_path = rest_path

    def __repr__(self): return "PrivateLineageStore()"

    def _call(self, method, path, payload=None):
        status, body = writer._call(self.http, method, self.url + self.rest_path + "/" + path, self._key, payload)
        if status is None or status >= 500:
            raise Unavailable("lineage unavailable; pending evidence requires readback before retry")
        require(200 <= status < 300, "lineage refused (HTTP " + str(status) + ")")
        return body

    def rows(self, namespace):
        require(type(namespace) is str and NAMESPACE.fullmatch(namespace), "invalid namespace")
        def page(query):
            result = self._call("GET", TABLE + "?" + urlencode([("namespace", "eq." + namespace), *query]))
            require(type(result) is list, "invalid lineage readback")
            return result
        top = page([("order", "ordinal.desc"), ("limit", 1)])
        if not top: return []
        require(type(top[0]) is dict and type(top[0].get("ordinal")) is int, "invalid lineage readback ordinal")
        end, after, rows, previous = top[0]["ordinal"], 0, [], None
        while after < end:
            batch = page([("order", "ordinal.asc"), ("ordinal", "gt." + str(after)),
                          ("ordinal", "lte." + str(end)), ("limit", self.page_size)])
            require(bool(batch), "incomplete lineage readback")
            for row in batch:
                require(type(row) is dict and type(row.get("ordinal")) is int and
                        after < row["ordinal"] <= end, "invalid lineage readback ordinal")
                try:
                    record = json.loads(row["record_text"])
                except (ValueError, KeyError, TypeError):
                    raise Refused("invalid lineage readback artifact") from None
                require(canonical(record) == row["record_text"] and digest(record) == row.get("record_digest")
                        and row.get("previous_digest") == previous and row.get("format_version") == FORMAT
                        and all(row.get(k) == record.get(k) for k in ("namespace", "kind", "record_id", "is_test", "synthetic")),
                        "lineage readback identity/digest mismatch")
                require(record["namespace"] == namespace and row["ordinal"] == after + 1, "lineage readback namespace/gap")
                previous, after = row["record_digest"], row["ordinal"]
                rows.append(row)
        validate_graph([json.loads(row["record_text"]) for row in rows])
        return rows

    def read(self, namespace):
        return [json.loads(row["record_text"]) for row in self.rows(namespace)]

    def append(self, records, *, expected_head):
        require(type(records) is list and bool(records), "empty lineage append")
        for record in records: validate_record(record)
        require(len({r["record_id"] for r in records}) == len(records), "duplicate record identity")
        namespace = records[0]["namespace"]
        existing = self.rows(namespace)
        old = {r["record_id"]: json.loads(r["record_text"]) for r in existing}
        for record in records:
            require(record["record_id"] not in old or old[record["record_id"]] == record, "immutable lineage identity conflict")
        new = [r for r in records if r["record_id"] not in old]
        validate_graph(list(old.values()) + new)
        if not new: return existing
        require(expected_head == (existing[-1]["record_digest"] if existing else None), "stale lineage head")
        submitted = [{"record_text": canonical(r), "record_digest": digest(r)} for r in records]
        self._call("POST", "rpc/" + RPC, {"p_namespace": namespace, "p_expected_head": expected_head, "p_records": submitted})
        saved = self.rows(namespace)
        saved_by_id = {r["record_id"]: r["record_text"] for r in saved}
        require(all(saved_by_id.get(r["record_id"]) == canonical(r) for r in records), "lineage append readback differs")
        return saved


def main(argv=None, *, dotenv_path=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    put = sub.add_parser("append"); put.add_argument("file", type=Path)
    put.add_argument("--expected-head", required=True, help="digest, or empty for a new namespace")
    get = sub.add_parser("read"); get.add_argument("namespace")
    args = parser.parse_args(argv)
    settings = keycheck.load_settings(dotenv_path=dotenv_path)
    if settings.key is None:
        print("loaded: no"); return 1
    store = Store(settings.url, settings.key)
    try:
        if args.command == "append":
            records = json.loads(args.file.read_text())
            rows = store.append(records, expected_head=args.expected_head or None)
        else:
            rows = store.rows(args.namespace)
        print(json.dumps({"published": True, "count": len(rows),
                          "head": rows[-1]["record_digest"] if rows else None,
                          "synthetic_count": sum(r["synthetic"] for r in rows)}))
        return 0
    except (Refused, OSError, ValueError) as error:
        # File and parser errors can contain private input. Never echo them.
        print("published: no; " + (str(error) if isinstance(error, Refused) else "invalid local evidence"))
        return 1
