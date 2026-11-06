"""Freeze an actual routed-prose + native-Jot baseline before candidate tuning.

Run only on the prepared public snapshot. Route choices are recorded development
inputs selected from MEMORY, not an automated or independent answer judgment.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root, cases_path, output = map(Path, sys.argv[1:])
cases = json.loads(cases_path.read_text())
rows = []
for case in cases['cases']:
    maximum = cases['budget']['max_chars']
    navigation = ''
    if case['route']:
        # A bounded read along the human-selected MEMORY route, before native history.
        navigation = (root / case['route']).read_text().split('<!-- jot-entry -->')[0][:maximum // 2]
    result = subprocess.run(['node', str(root / 'workbench/tools/jot.mjs'), 'search', '--query', case['native_query'], '--limit', str(cases['budget']['limit']), '--max-chars', str(maximum // 2)], cwd=root, text=True, capture_output=True)
    native = json.loads(result.stdout)
    global_search = native
    if native['status'] != 'read' and case['route']:
        result = subprocess.run(['node', str(root / 'workbench/tools/jot.mjs'), 'read', '--page', case['route'], '--query', case['native_query'], '--limit', str(cases['budget']['limit']), '--max-chars', str(maximum // 2)], cwd=root, text=True, capture_output=True)
        native = json.loads(result.stdout)
    # Keep only complete native entries that fit the same overall output bound.
    row = {'id': case['id'], 'route': case['route'], 'navigation': navigation, 'entries': [], 'correction_context': [], 'native_total_matches': native.get('total_matches'), 'global_search_status': global_search['status'], 'global_search_error': global_search.get('error'), 'routed_read_status': native['status']}
    for name in ['entries', 'correction_context']:
        for entry in native.get(name, []):
            row[name].append(entry)
            if len(json.dumps(row, ensure_ascii=False, indent=2)) > maximum:
                row[name].pop()
                break
    row['context_chars'] = len(json.dumps(row, ensure_ascii=False, indent=2))
    row['source_hit'] = not case['expected_sources'] or case['route'] in case['expected_sources'] or any(e['page'] in case['expected_sources'] for e in row['entries'])
    row['jot_hit'] = None if not case.get('expected_jot') else any(e['id'] == case['expected_jot'] for e in row['entries'])
    rows.append(row)
manifest = json.loads((root / 'corpus-manifest.json').read_text())
report = {'version': 1, 'method': 'MEMORY route (recorded human selection) plus executable native Jot search', 'source_revision': cases['source_revision'], 'cases_sha256': hashlib.sha256(cases_path.read_bytes()).hexdigest(), 'cases_identity_sha256': hashlib.sha256(json.dumps(cases, sort_keys=True).encode()).hexdigest(), 'budget': cases['budget'], 'wiki_sha256': {p: h for p, h in manifest['files'].items() if p.startswith('workbench/wiki/') and '/archive/' not in p}, 'rows': rows, 'independent_answer_correctness': 'unmeasured', 'stale_answer_repetition': 'unmeasured', 'owner_correction_effort': 'unmeasured', 'limits': 'Development routes and keywords were inspected by the implementor. This records retrieved context, not independent answers or benefit. Held-out/fresh-agent evaluation belongs to TK-002W.'}
output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print('baseline captured:', [(r['id'], r['source_hit'], r['jot_hit'], r['context_chars']) for r in rows])
