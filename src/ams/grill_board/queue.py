"""Project explicit owner requests from their committed owning records.

Like the LLM_Workbench queue, requests have stable keys and versioned wording;
agents publish/revise requests and only the owner answers them. Rendering never
creates card files or commits. A card is materialized only when the owner acts.
"""

import functools
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

from markdown_it import MarkdownIt

from .cards import Card, CardSourceError, Refusal, _git, parse_card


SCHEMA = "grill-board/request@1"
ANCHOR = "## Owner requests"
KEY = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
PARSER = MarkdownIt("commonmark")
REQUIRED = ("key", "question", "recommendation", "priority", "priority_reason",
            "value", "value_reason", "context")
OPTIONAL = ("schema", "topic", "why", "state", "blocker", "candidate")


def validate_request(value):
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        raise ValueError(f"an owner request needs schema {SCHEMA}")
    if set(value) - set(REQUIRED + OPTIONAL):
        raise ValueError("unknown owner request field")
    for key in REQUIRED:
        if not isinstance(value.get(key), str) or not value[key].strip():
            raise ValueError(f"owner request {key} must be nonempty text")
    for key, text in value.items():
        if not isinstance(text, str) or len(text) > 1000 or any(ord(c) < 32 for c in text):
            raise ValueError(f"owner request {key} must be one line of at most 1000 characters")
    if not KEY.fullmatch(value["key"]):
        raise ValueError("request key must be a lowercase hyphenated name")
    if value.get("state", "pending") not in ("pending", "withdrawn"):
        raise ValueError("request state must be pending or withdrawn; agents cannot supply owner answers")
    if value.get("candidate") and not re.fullmatch(r"[a-f0-9]{40}", value["candidate"]):
        raise ValueError("a request candidate must be a full commit SHA")
    return value


def request_blocks(text):
    """Explicit top-level fences only; quoted examples are not live requests."""
    return [token for token in PARSER.parse(text)
            if token.type == "fence" and token.level == 0 and token.info.strip() == "grill-board"]


def metadata(text):
    fields = {}
    for token in PARSER.parse(text):
        if token.type == "heading_open" and token.tag == "h2" and token.level == 0:
            break
        if token.type == "inline" and token.level == 1:
            for line in token.content.splitlines():
                if match := re.fullmatch(r"\*\*([^*]+):\*\*[ \t]*(.*)", line):
                    fields[match[1]] = match[2].strip()
    return fields


def _relative(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("record collection must be a relative path")
    parts = value.split("/")
    if PurePosixPath(value).is_absolute() or any(not p or p in (".", "..") or p.startswith(".") for p in parts):
        raise ValueError("unsafe record collection")
    return value.rstrip("/") + "/"


def _blobs(root, commit, paths):
    """Read regular committed records in one bounded Git batch, no working tree."""
    import subprocess

    if not paths:
        return {}
    result = subprocess.run(["git", "cat-file", "--batch"], cwd=root,
                            input="".join(f"{commit}:{p}\n" for p in paths).encode(), capture_output=True)
    if result.returncode:
        raise CardSourceError("cannot read committed owner-request records")
    data, at, blobs = result.stdout, 0, {}
    for relative in paths:
        end = data.index(b"\n", at)
        header = data[at:end].split()
        if len(header) != 3 or header[1] != b"blob":
            raise CardSourceError(f"owner-request record unavailable: {relative}")
        size = int(header[2])
        blobs[relative] = data[end + 1:end + 1 + size]
        at = end + 2 + size
    return blobs


def _card(relative, request, commit, source_sha):
    validate_request(request)
    identity = relative + "#" + request["key"]
    # Regrading or moving a question between topics does not change the
    # decision the owner answered. Wording, context and candidate do.
    decision = {k: v for k, v in request.items()
                if k not in ("priority", "priority_reason", "value", "value_reason", "topic", "state")}
    revision = hashlib.sha256(json.dumps(decision, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    name = f"request-{hashlib.sha256(identity.encode()).hexdigest()[:16]}-{revision[:16]}.md"
    fields = {
        "Priority": request["priority"], "Priority reason": request["priority_reason"],
        "Value": request["value"], "Value reason": request["value_reason"],
        "Topic": request.get("topic", "Owner decisions"),
        "Recommendation": request["recommendation"], "Owner record": relative,
        "Write after": ANCHOR, "Request key": identity, "Source revision": revision,
        "Source record": relative,
    }
    if request.get("why"):
        fields["Why it matters"] = request["why"]
    if request.get("candidate"):
        fields["Candidate"] = request["candidate"]
    content = (f"# {request['question']}\n\n" + "".join(f"**{k}:** {v}\n" for k, v in fields.items())
               + f"\n{request['context']}\n").encode()
    card = parse_card(name, content.decode())
    if not isinstance(card, Card):
        raise ValueError("; ".join(card.problems))
    card.sha, card.commit = hashlib.sha256(content).hexdigest(), commit
    card.projection, card.source_sha = content, source_sha
    return card


@functools.lru_cache(maxsize=16)
def requests_at(root, commit):
    """Immutable projection at one commit; mutable Card objects are made below."""
    listed = _git(Path(root), "ls-tree", "-r", "-z", commit)
    entries = {}
    for entry in filter(None, listed.split("\0")):
        info, relative = entry.split("\t", 1)
        entries[relative] = info.split()
    manifest_path = "workbench/manifest.json"
    if manifest_path not in entries:
        return (), ()  # legacy standalone card directories remain supported
    if entries[manifest_path][0] not in ("100644", "100755"):
        raise CardSourceError("the request manifest must be a committed regular file")
    try:
        manifest = json.loads(_git(Path(root), "show", f"{commit}:{manifest_path}"))
        prefixes = [_relative(p) for p in (manifest.get("lanes", {}).get("specs"),
                                         manifest.get("collections", {}).get("landmarks")) if p]
    except (ValueError, AttributeError) as error:
        raise CardSourceError(f"owner-request manifest unavailable: {error}") from None
    records, refusals = [], []
    for relative, (mode, kind, _) in entries.items():
        if not any(relative.startswith(p) for p in prefixes):
            continue
        if any(p in ("retired", "archive") or p.startswith(".") for p in relative.split("/")):
            continue
        if relative.rsplit("/", 1)[-1] not in ("SPEC.md", "TASK.md", "LANDMARK.md"):
            continue
        if mode not in ("100644", "100755") or kind != "blob":
            refusals.append((relative, "linked owner-request records are not read"))
        elif any(ord(c) < 32 for c in relative):
            refusals.append((relative, "record paths with control characters are not read"))
        else:
            records.append(relative)
    requests = []
    for relative, blob in _blobs(root, commit, records).items():
        try:
            text = blob.decode("utf-8")
            fields = metadata(text)
            if fields.get("Status") in ("done", "complete", "superseded", "retired", "reached"):
                continue
            seen, live = set(), []
            for block in request_blocks(text):
                request = validate_request(json.loads(block.content))
                if request["key"] in seen:
                    raise ValueError(f"duplicate owner request key {request['key']}")
                seen.add(request["key"])
                if request.get("state", "pending") == "pending":
                    if text.splitlines().count(ANCHOR) != 1:
                        raise ValueError(f"requests need one {ANCHOR} answer destination")
                    # Validate the rendered card too, before exposing an actionable request.
                    _card(relative, request, commit, hashlib.sha256(blob).hexdigest())
                    live.append((relative, request, hashlib.sha256(blob).hexdigest()))
            requests.extend(live)
            declared = {r.get("blocker", r["key"]).removeprefix("owner:") for _, r, _ in live}
            holds = re.findall(r"\bowner:([a-z][a-z0-9-]*)", fields.get("Blockers", ""))
            missing = sorted(set(holds) - declared)
            if missing:
                refusals.append((relative, "Recorded owner hold(s): " + ", ".join(missing)
                                 + ". No actionable question is published for these holds. "
                                 "Agents must distinguish deliberate holds from missing requests; no new approval is inferred."))
            gate = fields.get("Next gate", "")
            if not seen and re.search(r"\bowner\b|\bhuman QA\b", gate, re.IGNORECASE):
                refusals.append((relative, "An owner-related next gate has no published question: " + gate
                                 + " Agents must prepare actionable requests without re-asking settled decisions."))
        except (ValueError, UnicodeDecodeError) as error:
            refusals.append((relative, f"owner-request source unavailable: {error}"))
    return tuple(requests), tuple(refusals)


def projected_cards(root, commit):
    if not commit:
        return {}, []
    requests, failures = requests_at(str(root), commit)
    cards = [_card(relative, request, commit, source_sha) for relative, request, source_sha in requests]
    return {card.file: card for card in cards}, [Refusal(p, [error]) for p, error in failures]


def publish_request(root, relative, request, *, agent, revise=False, reason=""):
    """Agent add/revise counterpart: one source write, no generated-card upkeep.

    Owner answers are never edited. A changed request gets another source
    revision; existing response cards remain immutable history.
    """
    from .answers import (AnswerRefused, _unchanged, _write_and_commit, committed_blob,
                          owned_path, repository_lock, sha256)

    root = Path(root)
    try:
        validate_request(request)
        for value in (agent, reason if revise else agent):
            if not value.strip() or "\n" in value or "\r" in value or len(value) > 1000:
                raise ValueError("agent and revision reason must be nonempty single-line text")
    except ValueError as error:
        raise AnswerRefused(str(error)) from None
    with repository_lock(root):
        if not _git(root, "symbolic-ref", "-q", "--short", "HEAD").strip():
            raise AnswerRefused("HEAD is detached; requests commit on a branch")
        base = _git(root, "rev-parse", "--verify", "HEAD^{commit}").strip()
        path = owned_path(root, relative)
        manifest = json.loads(committed_blob(root, "workbench/manifest.json", base) or b"{}")
        prefixes = [_relative(p) for p in (manifest.get("lanes", {}).get("specs"),
                                         manifest.get("collections", {}).get("landmarks")) if p]
        if not any(relative.startswith(p) for p in prefixes) or path.name not in ("SPEC.md", "TASK.md", "LANDMARK.md"):
            raise AnswerRefused("publish requests in a manifest-declared Spec, Task or Landmark record")
        blob = committed_blob(root, relative, base)
        if blob is None:
            raise AnswerRefused("the request owner must be a committed regular record")
        mode, blob = _unchanged(root, base, relative, path, sha256(blob), "request owner")
        try:
            text = blob.decode("utf-8")
            if metadata(text).get("Status") in ("done", "complete", "superseded", "retired", "reached"):
                raise ValueError("completed or retired records cannot publish pending requests")
            blocks = request_blocks(text)
            values = [validate_request(json.loads(b.content)) for b in blocks]
            keys = [v["key"] for v in values]
            if len(keys) != len(set(keys)):
                raise ValueError("duplicate owner request key")
            hit = next((i for i, value in enumerate(values) if value["key"] == request["key"]), None)
            if revise != (hit is not None):
                raise ValueError("use revise for an existing request; use add for a new key")
            if hit is not None and values[hit] == request:
                return {"status": "unchanged", "commit": base, "key": request["key"]}
            _card(relative, request, base, sha256(blob))
            fence = "```grill-board\n" + json.dumps(request, indent=2, ensure_ascii=False) + "\n```\n"
            if hit is not None:
                lines = text.splitlines(keepends=True)
                start, end = blocks[hit].map
                lines[start:end] = [fence]
                text = "".join(lines)
            else:
                if ANCHOR not in text.splitlines():
                    text = text.rstrip() + "\n\n" + ANCHOR + "\n"
                text = text.rstrip() + "\n\n" + fence
            if text.splitlines().count(ANCHOR) != 1:
                raise ValueError(f"one {ANCHOR} answer destination is required")
            if len(text) > 8000:
                raise ValueError("the owner request would exceed the record's 8000-character limit")
        except (ValueError, UnicodeDecodeError) as error:
            raise AnswerRefused(str(error)) from None
        subject = f"Grill Board: {'revise' if revise else 'add'} {request['key']} in {relative}"
        commit = _write_and_commit(root, base, [(relative, path, mode, blob, text.encode())],
                                   subject, f"Published by {agent}." + (f" Reason: {reason}" if revise else ""))
        return {"status": "revised" if revise else "added", "commit": commit, "key": request["key"]}


def main(argv):
    """The existing ams-board entry also owns agent queue operations."""
    import argparse
    import sys
    from .answers import AnswerRefused

    parser = argparse.ArgumentParser(prog="ams-board")
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("add", "revise"):
        p = commands.add_parser(command)
        p.add_argument("--record", required=True)
        p.add_argument("--file", type=Path, required=True)
        p.add_argument("--by", required=True)
        if command == "revise":
            p.add_argument("--reason", required=True)
    for command in ("status", "pending"):
        commands.add_parser(command).add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = Path(_git(Path.cwd(), "rev-parse", "--show-toplevel").strip())
        if args.command in ("add", "revise"):
            request = json.loads(args.file.read_text())
            result = publish_request(root, args.record, request, agent=args.by,
                                     revise=args.command == "revise", reason=getattr(args, "reason", ""))
        else:
            from .cards import load_cards
            cards, failures = load_cards(root / "grill-board/cards")
            result = {"items": [{"file": c.file, "question": c.question, "source": c.fields.get("Source record"),
                                  "request_key": c.fields.get("Request key"), "revision": c.fields.get("Source revision"),
                                  "state": "earlier" if not c.source_current else "answered" if c.answer else "held" if c.flag else "pending",
                                  "answer": c.answer, "note": c.answer_note, "record": c.fields.get("Owner record")}
                                 for c in cards if args.command == "status" or c.source_current],
                      "issues": [{"source": r.file, "problems": r.problems} for r in failures]}
        print(json.dumps(result, indent=2))
    except (AnswerRefused, CardSourceError, OSError, ValueError) as error:
        print(f"Grill Board: {error}", file=sys.stderr)
        return 1
    return 0
