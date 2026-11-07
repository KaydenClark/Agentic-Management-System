"""Versioned S-002 skill-audit evaluator. Historical r1 scoring stays separate."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import re

from ams import assessment

VERSION = 'skill-audit-v1'
CLASSES = ('Quality', 'Regression', 'Critical')
IDENTIFIER = r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}'
SKILL = r'[a-z0-9][a-z0-9-]{0,63}'
STAMP = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|\+00:00)'
require = assessment.require


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def token(value, name, pattern=IDENTIFIER):
    require(isinstance(value, str) and re.fullmatch(pattern, value) is not None,
            f'{name} has an invalid format')
    return value


def timestamp(value, name):
    token(value, name, STAMP)
    return datetime.fromisoformat(value).astimezone(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')


def counts(rows, check_class):
    applicable = [row for row in rows if row['class'] == check_class and row['result'] != 'N/A']
    return {'passed': sum(row['result'] == 'Yes' for row in applicable), 'total': len(applicable)}


def critical(count):
    return count['passed'] != count['total'] if count['total'] else None


# Bind each skill audit set to its version, source pins, evaluator and fixed check inventory.
def _contract(packet):
    require(isinstance(packet, dict) and packet.get('version') == VERSION,
            f'expected {VERSION} audit input')
    token(packet.get('audit_set_id'), 'audit_set_id')
    token(packet.get('skill'), 'skill', SKILL)
    for field in ('skills_commit', 'candidate', 'baseline'):
        assessment.revision(packet.get(field), field)
    require(assessment.same_artifact(packet.get('rubric'), assessment.RUBRIC),
            'shared checks must pin the approved r1 inventory')
    conditions = packet.get('conditions')
    require(isinstance(conditions, dict), 'frozen audit conditions are required')
    # Match Supabase's 64-character provider token before any run can enter the outbox.
    token(conditions.get('provider'), 'provider', r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}')
    token(conditions.get('model'), 'model', r'[A-Za-z0-9][A-Za-z0-9_.:/-]{0,127}')
    require(conditions.get('model_tier') in ('small', 'mid', 'high'), 'invalid model tier')
    for field in ('effort', 'host'):
        assessment.text(conditions.get(field), field)
    for field in ('tools', 'loaded_artifacts'):
        entries = conditions.get(field)
        require(isinstance(entries, list) and bool(entries), f'{field} must be recorded')
        for entry in entries:
            assessment.text(entry, field)
    # Evaluator eligibility needs an identified grader and evidence tied to the candidate.
    evaluator = packet.get('evaluator')
    require(isinstance(evaluator, dict), 'frozen evaluator is required')
    assessment.text(evaluator.get('model'), 'evaluator model')
    assessment.revision(evaluator.get('prompt_revision'), 'evaluator prompt revision')
    qualification = evaluator.get('qualification')
    require(qualification in ('qualified', 'unqualified'), 'invalid evaluator qualification')
    proof = assessment.evidence(evaluator.get('qualification_evidence', []),
                                packet['candidate'], 'evaluator qualification')
    if qualification == 'qualified':
        require(proof and evaluator['model'].lower() not in ('unknown', 'unavailable'),
                'qualified evaluator requires model identity and proof')
    # Shared checks retain their approved classes. Skill-specific additions cover regression or Critical checks.
    inventory = packet.get('inventory')
    require(isinstance(inventory, list), 'frozen audit inventory is required')
    checks = {}
    for check in inventory:
        require(isinstance(check, dict), 'invalid inventory check')
        check_id = token(check.get('id'), 'check ID')
        check_class = check.get('class')
        require(check_id not in checks and check_class in CLASSES, 'invalid or duplicate inventory check')
        shared_class = assessment.CHECKS.get(check_id)
        if shared_class or check_class == 'Quality':
            require(shared_class == check_class, 'shared checks retain their approved class')
        checks[check_id] = check_class
    fields = ('version', 'audit_set_id', 'skill', 'skills_commit', 'candidate', 'baseline',
              'rubric', 'conditions', 'evaluator', 'inventory')
    frozen = {field: packet[field] for field in fields}
    return checks, hashlib.sha256(canonical(frozen).encode()).hexdigest()


def _score_run(run, inventory, candidate):
    require(isinstance(run, dict), 'invalid audit run')
    run_id = token(run.get('audit_run_id'), 'audit_run_id')
    state = run.get('completion_state')
    require(state in ('completed', 'interrupted'), 'only actual completed or interrupted runs are recorded')
    completed_at = run.get('completed_at')
    if state == 'completed':
        completed_at = timestamp(completed_at, 'completed_at')
    else:
        require(completed_at is None, 'interrupted run cannot claim completion')
    supplied = {}
    require(isinstance(run.get('rows'), list), 'audit check rows must be a list')
    for row in run['rows']:
        require(isinstance(row, dict), 'invalid audit check row')
        check_id = token(row.get('id'), 'check ID')
        require(check_id in inventory and check_id not in supplied, 'unknown or duplicate audit check row')
        result = row.get('result')
        require(result in ('Yes', 'No', 'N/A') or result in assessment.GAPS, 'invalid check result')
        require(row.get('class', inventory[check_id]) == inventory[check_id], 'audit check class differs from inventory')
        supplied[check_id] = row
    # Score every frozen check in an actual run, even when the run stops early.
    # A justified N/A is excluded. Missing or unproved results count as No.
    rows = []
    for check_id, check_class in inventory.items():
        row = supplied.get(check_id, {'result': 'missing'})
        result = row['result']
        if result == 'N/A':
            assessment.text(row.get('reason'), 'N/A reason')
            complete = True
        else:
            proof = assessment.evidence(row.get('evidence', []), candidate, 'check evidence')
            complete = proof and result in ('Yes', 'No')
        rows.append(dict(row, id=check_id, **{'class': check_class},
                         reported_result=result, result=result if complete else 'No',
                         evidence_complete=complete))
    return {'audit_run_id': run_id, 'completion_state': state, 'completed_at': completed_at,
            'evidence_complete': state == 'completed' and all(row['evidence_complete'] for row in rows),
            'quality': counts(rows, 'Quality'), 'regression': counts(rows, 'Regression'),
            'critical_missed': critical(counts(rows, 'Critical')), 'rows': rows}


def score(packet):
    """Validate and score recorded evidence; make no model calls or acceptance claims."""
    inventory, contract_digest = _contract(packet)
    supplied = packet.get('runs')
    require(isinstance(supplied, list) and len(supplied) <= 3, 'audit set has at most three actual run records')
    runs = [_score_run(run, inventory, packet['candidate']) for run in supplied]
    require(len({run['audit_run_id'] for run in runs}) == len(runs), 'duplicate audit run ID')
    # Pool checks from actual runs, including interruptions. Only completed IDs count as completions.
    completed = [run for run in runs if run['completion_state'] == 'completed']
    rows = [row for run in runs for row in run['rows']]
    pooled = {name: counts(rows, name) for name in CLASSES}
    evidence_complete = len(completed) == 3 and all(run['evidence_complete'] for run in completed)
    has_checks = any(result['total'] for result in pooled.values())
    # A clean grade requires three fully evidenced runs with checks. The worst recorded miss sets severity.
    grade = 'Excellent' if evidence_complete and has_checks else None
    for check_class, level in zip(CLASSES, ('Stable', 'Functional', 'Broken')):
        if critical(pooled[check_class]):
            grade = level
    # A qualified evaluator can assess any grade. Only complete Stable or Excellent skills qualify here.
    # Repair acceptance and useful benefit remain separate decisions.
    evaluator_qualified = packet['evaluator']['qualification'] == 'qualified'
    qualified = evaluator_qualified and evidence_complete and grade in ('Excellent', 'Stable')
    return {'version': VERSION, 'audit_set_id': packet['audit_set_id'], 'contract_digest': contract_digest,
            'completed_audit_run_ids': [run['audit_run_id'] for run in completed],
            'quality': pooled['Quality'], 'regression': pooled['Regression'],
            'critical_missed': critical(pooled['Critical']), 'grade': grade,
            'evidence_complete': evidence_complete, 'evaluator_qualified': evaluator_qualified,
            'qualified': qualified, 'runs': runs}


def transport_rows(packet, result, *, is_test, is_public):
    """Project only allowlisted per-run fields; private rows and conditions stay local."""
    conditions = packet['conditions']
    return [
        {
            'audit_run_id': run['audit_run_id'], 'audit_set_id': result['audit_set_id'],
            'skill': packet['skill'], 'skills_commit': packet['skills_commit'],
            'contract_version': VERSION, 'contract_digest': result['contract_digest'],
            'provider': conditions['provider'], 'model': conditions['model'], 'model_tier': conditions['model_tier'],
            'quality_passed': run['quality']['passed'], 'quality_total': run['quality']['total'],
            'regression_passed': run['regression']['passed'], 'regression_total': run['regression']['total'],
            'critical_missed': run['critical_missed'], 'evidence_complete': run['evidence_complete'],
            'completion_state': run['completion_state'], 'completed_at': run['completed_at'],
            'is_test': is_test, 'is_public': is_public and run['completion_state'] == 'completed',
        }
        for run in result['runs']
    ]
