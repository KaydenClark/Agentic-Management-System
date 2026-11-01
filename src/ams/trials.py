"""Private trial preparation and honest local runtime evidence (S-002).

This CLI never calls a model. Execution facts are neither graded trial rows nor
Alignment assessments. Supplied evidence validates structurally, not as truth.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

from ams.assessment import Refused, require, same_artifact
from ams import trial_runtime as runtime
from ams.trial_inputs import (SCOPE, _hash, _no_links, digest, encoded, fixture_identity,
                              grader_reference, load, materialize, validate_manifest, worker_prompt)


def execution_evidence(identity, result, source, source_digest):
    """Allowlisted public-safe summary; raw prompts/responses remain private."""
    require(isinstance(identity, str) and re.fullmatch('[A-Za-z0-9][A-Za-z0-9._-]{0,100}', identity),
            'safe evidence identity required')
    require(source in ('external-cli-smoke', 'adapter-execution'), 'execution source required')
    _hash(source_digest)
    require(result.get('model') == runtime.MODEL and result.get('provider') == 'firstParty'
            and result.get('effort') == runtime.EFFORT and result.get('tools') == []
            and result.get('mcpServers') == [], 'execution boundary not established')
    row = {'schema': 1, 'kind': 'execution-fact', 'id': identity, 'scope': SCOPE,
           'source': source, 'sourceDigest': source_digest, 'model': runtime.MODEL,
           'provider': 'firstParty', 'effort': runtime.EFFORT, 'tools': [], 'mcpServers': [],
           'usage': result['usage'], 'equivalentApiCostUsd': result['equivalentApiCostUsd'],
           'actualSubscriptionCostUsd': None, 'actualSubscriptionCostAvailability': 'unknown',
           'semanticQualification': 'unqualified', 'controlledTrial': False, 'improvement': False}
    validate_evidence(row)
    return row


def validate_evidence(row):
    common = {'schema', 'kind', 'id', 'scope'}
    require(isinstance(row, dict) and type(row.get('schema')) is int and row['schema'] == 1,
            'invalid evidence schema')
    require(isinstance(row.get('id'), str) and re.fullmatch('[A-Za-z0-9][A-Za-z0-9._-]{0,100}', row['id']),
            'invalid evidence identity')
    require(row.get('scope') == SCOPE, 'evidence scope changed')
    if row.get('kind') == 'execution-fact':
        fields = common | {'source', 'sourceDigest', 'model', 'provider', 'effort', 'tools',
                           'mcpServers', 'usage', 'equivalentApiCostUsd', 'actualSubscriptionCostUsd',
                           'actualSubscriptionCostAvailability', 'semanticQualification', 'controlledTrial', 'improvement'}
        require(set(row) == fields, 'unsafe or missing evidence fields')
        _hash(row['sourceDigest'])
        require(row['source'] in ('external-cli-smoke', 'adapter-execution')
                and row['model'] == runtime.MODEL and row['provider'] == 'firstParty'
                and row['effort'] == runtime.EFFORT and row['tools'] == row['mcpServers'] == [],
                'execution provenance changed')
        require(row['actualSubscriptionCostUsd'] is None and row['actualSubscriptionCostAvailability'] == 'unknown'
                and row['semanticQualification'] == 'unqualified'
                and row['controlledTrial'] is False and row['improvement'] is False,
                'execution fact cannot certify trials, qualification or benefit')
        usage = row['usage']
        require(isinstance(usage, dict) and set(usage) == {'inputTokens', 'outputTokens', 'cacheReadInputTokens', 'cacheCreationInputTokens'},
                'unsafe provider usage fields')
        for count in usage.values():
            runtime._count(count)
        cost = row['equivalentApiCostUsd']
        require(type(cost) in (int, float) and math.isfinite(cost) and cost >= 0, 'invalid equivalent API cost')
    elif row.get('kind') == 'bootstrap-preflight':
        fields = common | {'manifestDigest', 'reference', 'shell', 'readyForControlledTrials', 'gates'}
        require(set(row) == fields, 'unsafe or missing preflight fields')
        _hash(row['manifestDigest'])
        ref = row['reference']
        require(isinstance(ref, dict) and set(ref) == {'referenceDigest', 'promptDigest', 'sourceRevision', 'qualification'},
                'unsafe grader summary')
        for key in ('referenceDigest', 'promptDigest'):
            _hash(ref[key])
        _hash(ref['sourceRevision'], 40)
        require(ref['qualification'] in ('qualified', 'unqualified'), 'invalid grader qualification')
        shell = row['shell']
        require(isinstance(shell, dict) and shell.get('scope') == 'host-command-canaries'
                and shell.get('status') in ('passed', 'failed', 'unavailable'), 'invalid shell observation')
        if shell['status'] == 'unavailable':
            require(set(shell) == {'scope', 'status', 'reason'} and shell['reason'] in (
                'macOS-only probe', 'sandbox command unavailable', 'enclosing sandbox refuses nested Seatbelt'),
                'unsafe shell diagnostic')
        else:
            require(set(shell) == {'scope', 'status', 'checks'} and isinstance(shell['checks'], dict)
                    and set(shell['checks']) == set(runtime.CANARIES)
                    and all(type(v) is bool for v in shell['checks'].values())
                    and (shell['status'] == 'passed') == all(shell['checks'].values()), 'inconsistent shell observations')
        expected = ['frozen-series-not-released']
        if ref['qualification'] != 'qualified': expected.append('semantic-grader-unqualified')
        if shell['status'] != 'passed': expected.append('host-command-preflight-not-passed')
        require(row['readyForControlledTrials'] is False and row['gates'] == expected, 'bootstrap cannot release controlled trials')
    else:
        raise Refused('unknown evidence kind')


def read_evidence(store):
    store = Path(store); _no_links(store)
    result = []
    for path in sorted(store.glob('*.json')):
        envelope = load(path)
        require(isinstance(envelope, dict) and set(envelope) == {'record', 'digest'}, 'invalid evidence envelope')
        row = envelope['record']; validate_evidence(row)
        require(envelope['digest'] == digest(row), 'evidence digest changed')
        require(path.name == hashlib.sha256(row['id'].encode()).hexdigest()+'.json', 'evidence filename/identity changed')
        result.append(row)
    return result


def save_evidence(row, store):
    validate_evidence(row)
    folder = Path(store); _no_links(folder)
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    read_evidence(folder)
    path = folder/(hashlib.sha256(row['id'].encode()).hexdigest()+'.json')
    if path.exists():
        require(same_artifact(load(path)['record'], row), 'evidence identity is immutable')
        return path.name
    envelope = {'record': row, 'digest': digest(row)}
    with path.open('xb') as output:
        output.write(encoded(envelope)+b'\n')
    path.chmod(0o600)
    return path.name


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    material = commands.add_parser('materialize'); material.add_argument('manifest', type=Path)
    material.add_argument('worker', type=Path); material.add_argument('--reset', action='store_true')
    preflight = commands.add_parser('preflight'); preflight.add_argument('worker', type=Path)
    preflight.add_argument('--reference', type=Path, required=True); preflight.add_argument('--id', required=True)
    preflight.add_argument('--store', type=Path, default=Path('.local/trial-evidence'))
    readback = commands.add_parser('readback'); readback.add_argument('--store', type=Path, default=Path('.local/trial-evidence'))
    args = parser.parse_args(argv)
    try:
        if args.command == 'materialize': result = materialize(args.manifest, args.worker, reset=args.reset)
        elif args.command == 'readback': result = read_evidence(args.store)
        else:
            manifest_digest = fixture_identity(args.worker)
            ref = grader_reference(args.reference, args.worker)
            shell = runtime.shell_preflight(args.worker)
            gates = ['frozen-series-not-released']
            if ref['qualification'] != 'qualified': gates.append('semantic-grader-unqualified')
            if shell['status'] != 'passed': gates.append('host-command-preflight-not-passed')
            result = {'schema': 1, 'kind': 'bootstrap-preflight', 'id': args.id, 'scope': SCOPE,
                      'manifestDigest': manifest_digest, 'reference': ref, 'shell': shell,
                      'readyForControlledTrials': False, 'gates': gates}
            save_evidence(result, args.store)
        print(json.dumps(result, indent=2))
        return 0
    except (Refused, OSError, ValueError, TypeError, KeyError):
        print('trial preparation refused: invalid, unavailable or changed input; preserve evidence before retry', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
