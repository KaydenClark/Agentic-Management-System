"""Local r1 intake, scoring and immutable manual-loop evidence (S-002).

Validates supplied records, not their truth. Makes no model calls.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from fractions import Fraction
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

RUBRIC = {'revision': 'r1', 'sha256': '96636d4a5e70cacbb0b94fd079340f02ed0f09b121b6498c1c70eebeb13b0578', 'checkVersion': 1}
# IDs/classes are the approved 47-check r1 inventory, not new scored criteria.
_CRITICAL = {'A01-01','A01-02','A01-03','A01-05','A01-06','A01-07',
             'A04-03','A04-04','A04-05','A04-06','A06-02','A06-03','A06-05','A09-02'}
CHECKS = {f'A{area:02}-{n:02}': ('Critical' if f'A{area:02}-{n:02}' in _CRITICAL else 'Quality')
          for area, count in enumerate((7,6,4,7,4,5,4,3,4,3), 1) for n in range(1,count+1)}
EVIDENCE_TYPES = {'harness-inspection', 'observed-use', 'behavioral-test'}
GAPS = {'Unknown', 'Unrun', 'refused', 'interrupted', 'missing'}


class Refused(ValueError):
    """Input or a transition does not meet the frozen assessment contract."""


def require(condition, message):
    if not condition:
        raise Refused(message)


def text(value, name):
    require(isinstance(value, str) and bool(value.strip()), f'{name} is required')
    return value


def revision(value, name):
    require(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{40}', value) is not None,
            f'{name} requires a full commit/hash revision')
    return value


def evidence(items, expected, name):
    require(isinstance(items, list), f'{name} must be an evidence list')
    for item in items:
        require(isinstance(item, dict), f'{name}: malformed evidence')
        require(item.get('type') in EVIDENCE_TYPES, f'{name}: unknown evidence type')
        require(item.get('revision') == expected, f'{name}: evidence revision mismatch')
        text(item.get('locator'), f'{name} locator')
    return bool(items)


def _validate(p):
    require(isinstance(p, dict) and p.get('schema') == 1, 'schema must be 1')
    for key in ('assessmentId','failureId','assessedAt'):
        text(p.get(key), key)
    try:
        stamp = datetime.fromisoformat(p['assessedAt'])
        require(stamp.utcoffset() is not None, 'assessedAt needs a timezone')
    except ValueError as exc:
        raise Refused('assessedAt must be an ISO timestamp with timezone') from exc
    require(p.get('rubric') == RUBRIC, 'rubric must be approved r1, check version 1')
    require(p.get('scope') in ('whole','bounded'), 'scope must be whole or bounded')
    require(type(p.get('attempt')) is int and 0 <= p['attempt'] <= 3, 'attempt must be baseline 0 or candidate 1..3')
    for key in ('candidate','baseline','skillsCommit','inventoryRevision'):
        revision(p.get(key), key)
    c = p.get('conditions')
    require(isinstance(c, dict), 'conditions are required')
    for key in ('host','workerModel','effort'):
        text(c.get(key), 'conditions.' + key)
    for key in ('tools','loadedArtifacts'):
        require(isinstance(c.get(key),list) and bool(c[key]), 'conditions.' + key + ' is required')
        for value in c[key]:
            text(value, 'conditions.' + key)
    evaluator = p.get('evaluator')
    require(isinstance(evaluator,dict), 'evaluator is required')
    text(evaluator.get('model'), 'evaluator.model')
    revision(evaluator.get('promptRevision'), 'evaluator.promptRevision')
    require(evaluator.get('qualification') in ('qualified','unqualified'), 'evaluator qualification is required')
    eq = evidence(evaluator.get('qualificationEvidence',[]), p['candidate'], 'qualification')
    require(evaluator['qualification'] != 'qualified' or eq, 'qualified evaluator needs qualification evidence')
    require(evaluator['qualification'] != 'qualified' or evaluator['model'].lower() not in ('unknown','unavailable'), 'qualified evaluator needs exact model identity')
    inv = p.get('inventory')
    require(isinstance(inv,list), 'frozen inventory is required')
    by_id = {}
    for check in inv:
        require(isinstance(check,dict), 'malformed inventory check')
        cid = check.get('id')
        require(cid in CHECKS and cid not in by_id, f'unknown or duplicate check: {cid}')
        cls = check.get('class')
        require(cls == CHECKS[cid] or (CHECKS[cid] == 'Quality' and cls == 'Regression'), f'{cid}: original class cannot change')
        if cls == 'Regression':
            proof = check.get('baselineEvidence',[])
            require(evidence(proof,p['baseline'],f'{cid} baseline'), f'{cid}: Regression needs baseline pass evidence')
            require(all(item.get('result') == 'Yes' and item.get('qualification') == 'qualified' for item in proof), f'{cid}: baseline must record a qualified pass')
        by_id[cid] = check
    excluded = p.get('excludedChecks')
    require(isinstance(excluded,dict), 'excludedChecks must justify the inventory boundary')
    require(set(by_id).isdisjoint(excluded) and set(by_id) | set(excluded) == set(CHECKS), 'inventory/exclusions must cover all 47 checks')
    for why in excluded.values():
        text(why, 'exclusion reason')
    if p['scope'] == 'whole':
        require({int(cid[1:3]) for cid in by_id} == set(range(1,11)), 'bounded inventory cannot claim whole scope')
    runs = p.get('runs')
    require(isinstance(runs,list) and len(runs) == 3, 'exactly three runs are required')
    seen = set()
    for run in runs:
        require(isinstance(run,dict), 'malformed run')
        rid = text(run.get('runId'), 'runId')
        require(rid not in seen, 'duplicate runId')
        seen.add(rid)
        require(isinstance(run.get('rows'),list), 'run rows must be a list')
    return by_id


def _run(p, run, inv):
    supplied = {}
    for row in run['rows']:
        require(isinstance(row,dict), 'malformed check row')
        cid = row.get('id')
        require(cid in inv and cid not in supplied, f'unknown or duplicate row: {cid}')
        require(row.get('result') in {'Yes','No','N/A'} | GAPS, f'{cid}: invalid result')
        if 'class' in row:
            require(row['class'] == inv[cid]['class'], f'{cid}: row class differs from frozen inventory')
        supplied[cid] = row
    rows = []
    for cid, check in inv.items():
        row = supplied.get(cid, {'id':cid, 'result':'missing', 'evidence':[]})
        result = row['result']
        if result == 'N/A':
            text(row.get('reason'), f'{cid} N/A reason')
            rows.append({'id':cid,'class':check['class'],'result':'N/A','reason':row['reason'], 'complete':True, 'qualified':True})
            continue
        has_proof = evidence(row.get('evidence',[]),p['candidate'],cid)
        complete = has_proof and result in ('Yes','No')
        qualified = row.get('qualification') == 'qualified' and p['evaluator']['qualification'] == 'qualified'
        rows.append({'id':cid,'class':check['class'],'result':result if complete else 'No',
                     'reportedResult':result, 'complete':complete, 'qualified':qualified,
                     'evidence':row.get('evidence',[]), 'reason':row.get('reason','')})
    applicable = [r for r in rows if r['result'] != 'N/A']
    return {'runId':run['runId'], 'rows':rows, 'passed':sum(r['result']=='Yes' for r in applicable),
            'applicable':len(applicable),
            'runPassed':all(r['result']=='Yes' for r in applicable if r['class'] in ('Critical','Regression')),
            'criticalFailure':any(r['class']=='Critical' and r['result']=='No' for r in applicable)}


def _findings(p, runs, previous):
    findings = {f['findingId']:dict(f) for f in previous}
    for old in p.get('historicalFindings',[]):
        require(isinstance(old,dict), 'malformed historical finding')
        fid = text(old.get('findingId'),'historical findingId')
        require(old.get('checkId') is None or old['checkId'] in CHECKS, 'unknown historical check')
        cid = old.get('checkId')
        if cid and old.get('class') is not None:
            require(old['class'] == CHECKS[cid] or (CHECKS[cid] == 'Quality' and old['class'] == 'Regression'), 'historical class cannot be demoted')
        if fid not in findings:
            findings[fid] = {**old, 'status':'open'}
    for run in runs:
        for row in run['rows']:
            if row['result'] != 'No':
                continue
            cid = row['id']
            fid = f"{p['failureId']}:{cid}"
            old = findings.get(fid)
            if old:
                old.update(status='recurred' if old['status'] in ('verified-resolved','recurred') else 'open', lastCandidate=p['candidate'])
            else:
                findings[fid] = {'findingId':fid, 'checkId':cid, 'class':row['class'], 'status':'open',
                                 'sourceRunId':run['runId'], 'candidate':p['candidate'], 'lastCandidate':p['candidate']}
    rejected = []
    seen = set()
    for retest in p.get('retests',[]):
        require(isinstance(retest,dict), 'malformed retest')
        fid = text(retest.get('findingId'),'retest findingId')
        require(fid not in seen, 'duplicate retest')
        seen.add(fid)
        finding = findings.get(fid)
        require(finding is not None, 'retest names an unknown finding')
        original = retest.get('originalCheckId')
        regressions = retest.get('regressionCheckIds',[])
        require(isinstance(regressions,list) and len(set(regressions)) == len(regressions), 'invalid regression check list')
        require(bool(regressions) or bool(retest.get('regressionExclusionReason','').strip()), 'retest needs affected regressions or justified exclusion')
        checks = [original, *regressions]
        ok = (retest.get('revision') == p['candidate'] and original == finding.get('checkId')
              and p['candidate'] != finding.get('candidate')
              and finding.get('class') in ('Critical','Regression','Quality')
              and all(any(r['id']==cid and r['result']=='Yes' and r['complete'] and r['qualified']
                          for r in run['rows']) for run in runs for cid in checks))
        if ok:
            finding.update(status='verified-resolved', resolvedAt=p['assessmentId'], repairedRevision=p['candidate'])
        else:
            rejected.append({'findingId':fid,'reason':'missing qualified three-run retest or revision mismatch'})
    return list(findings.values()), rejected


def score(p, previous_findings=()):
    """Compute an r1 result without modifying the packet or any external state."""
    inv = _validate(p)
    runs = [_run(p,r,inv) for r in p['runs']]
    findings, rejected = _findings(p,runs,previous_findings)
    passed = sum(r['passed'] for r in runs)
    applicable = sum(r['applicable'] for r in runs)
    ratio = Fraction(100*passed,applicable) if applicable else None
    passing = sum(r['runPassed'] for r in runs)
    level = ('Broken','Functional','Stable','Excellent')[passing]
    if any(r['criticalFailure'] for r in runs):
        level = 'Broken'
    complete = all(row['complete'] for run in runs for row in run['rows'])
    qualified = (p['evaluator']['qualification']=='qualified' and
                 all(row['qualified'] for run in runs for row in run['rows']))
    blocking = any(f.get('class') not in ('Critical','Regression','Quality') or
                   (f['status'] != 'verified-resolved' and f['class'] in ('Critical','Regression')) for f in findings)
    accepted = bool(applicable and level in ('Stable','Excellent') and complete and qualified and not blocking)
    return {'assessmentId':p['assessmentId'],'candidate':p['candidate'],'scope':p['scope'],
            'alignment':{'passed':passed,'applicable':applicable,
                         'percentageNumerator':ratio.numerator if ratio is not None else None,
                         'percentageDenominator':ratio.denominator if ratio is not None else None},
            'level':level,'passingRuns':passing,'evidenceState':'complete' if complete else 'incomplete',
            'qualification':'qualified' if qualified else 'unqualified','assessmentAccepted':accepted,
            # Behavioral useful-benefit comparison is outside this scorer.
            'retentionAccepted':False,'runs':runs,'findings':findings,'rejectedRetests':rejected}


def _encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',',':'), ensure_ascii=False).encode()


def _frozen(p):
    return {k:p[k] for k in ('failureId','baseline','rubric','scope','inventory','excludedChecks','inventoryRevision','conditions')} | {
        'evaluator':{k:v for k,v in p['evaluator'].items() if k != 'qualificationEvidence'}}


def read_records(store):
    """Read immutable packets and recompute every result; never trust totals."""
    records = []
    folder = Path(store)
    for file in sorted(folder.glob('*.json')):
        require(not file.is_symlink(), 'record symlinks are refused')
        try:
            envelope = json.loads(file.read_text())
        except (OSError,ValueError) as exc:
            raise Refused(f'unreadable local record: {file.name}') from exc
        require(isinstance(envelope,dict) and isinstance(envelope.get('packet'),dict), 'malformed record')
        records.append(envelope)
    ordered = sorted(records, key=lambda r:(r['packet'].get('failureId',''),r['packet'].get('attempt',-1)))
    prior = {}
    for record in ordered:
        p = record['packet']
        require(type(p.get('attempt')) is int, 'malformed recorded attempt')
        history = prior.setdefault(p['failureId'],[])
        expected = _transition(p, history)
        require(record.get('result') == expected, 'record result differs from recomputed history')
        require((folder / _filename(p['assessmentId'])).is_file(), 'record identity differs from filename')
        history.append(record)
    return ordered


def _transition(p, history):
    if history:
        require(_frozen(p) == _frozen(history[0]['packet']), 'frozen comparison changed; qualify and authorize a new grader/rubric series')
        last = history[-1]['packet']['attempt']
        require(last < 3, 'three candidate attempts exhausted; stop and report')
        require(p['attempt'] == last+1, 'attempt must continue history; rename/repair cannot reset it')
    else:
        require(p['attempt'] == 0, 'record baseline attempt 0 before candidates')
    previous = history[-1]['result']['findings'] if history else []
    r = score(p, previous)
    r['attempt'] = p['attempt']
    r['nextAction'] = ('baseline-recorded' if p['attempt']==0 else
                       'compare-benefit' if r['assessmentAccepted'] else
                       'stop' if p['attempt']==3 else 'revise')
    return r


def _filename(assessment_id):
    return hashlib.sha256(text(assessment_id,'assessmentId').encode()).hexdigest()+'.json'


@contextmanager
def _locked(folder):
    lock = folder / '.record-lock'
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise Refused('store is locked; inspect the interrupted writer before retrying') from exc
    try:
        yield
    finally:
        lock.rmdir()


def record(p, store):
    """Append one immutable local packet, preserving baseline and failed attempts."""
    _validate(p)  # retests are evaluated only after loading the prior findings
    folder = Path(store)
    require(not folder.is_symlink(), 'store symlinks are refused')
    folder.mkdir(parents=True, exist_ok=True)
    with _locked(folder):
        records = read_records(folder)
        for old in records:
            if old['packet']['assessmentId'] == p['assessmentId']:
                require(old['packet'] == p, 'assessmentId is immutable; use a new ID for new evidence')
                return old['result']
        history = [r for r in records if r['packet']['failureId'] == p['failureId']]
        result = _transition(p, history)
        envelope = {'packet':p,'result':result}
        dest = folder / _filename(p['assessmentId'])
        # Interrupted exclusive writes remain visibly malformed, never passed.
        with dest.open('xb') as out:
            out.write(_encoded(envelope) + b'\n')
        return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    for cmd in ('score','record'):
        p = sub.add_parser(cmd)
        p.add_argument('packet',type=Path)
        if cmd == 'record':
            p.add_argument('--store',type=Path,default=Path('.local/assessments'))
    p = sub.add_parser('list')
    p.add_argument('--store',type=Path,default=Path('.local/assessments'))
    args = parser.parse_args(argv)
    try:
        if args.command == 'list':
            result = read_records(args.store)
        else:
            packet = json.loads(args.packet.read_text())
            result = score(packet) if args.command == 'score' else record(packet,args.store)
        print(json.dumps(result,indent=2))
        return 0
    except (Refused,OSError,ValueError,TypeError,KeyError) as exc:
        print(f'assessment refused: {exc}',file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
