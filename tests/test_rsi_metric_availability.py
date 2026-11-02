"""Public writer contract: unknown metrics retain reasons, never invented zeros."""
import pytest
from ams import rsi_rows
from test_rsi_rows import FakePostgrest, a_run, a_result, store

METRICS = ('cost_usd', 'input_tokens', 'output_tokens', 'turns', 'wall_seconds')

def unknown_row(run):
    return a_result(run, **dict.fromkeys(METRICS), metric_unknowns={
        key: {'reason': 'Subscription meter did not report this value',
              'source': 'evals/runs/trial-run-1.json'} for key in METRICS})

def test_unknown_metrics_roundtrip_without_becoming_zero():
    http = FakePostgrest()
    db = store(http)
    run = db.insert(rsi_rows.RUN_TABLE, a_run())
    row = unknown_row(run)
    saved = db.insert(rsi_rows.RESULT_TABLE, row)
    read = db.get(rsi_rows.RESULT_TABLE, saved['id'])
    assert all(read[key] is None for key in METRICS)
    assert read['metric_unknowns'] == row['metric_unknowns']
    changed = db.update(rsi_rows.RESULT_TABLE, read,
                        {'cost_usd': 0, 'metric_unknowns': {
                            k: v for k, v in read['metric_unknowns'].items() if k != 'cost_usd'}})
    assert changed['cost_usd'] == 0 and 'cost_usd' not in changed['metric_unknowns']

@pytest.mark.parametrize('metric', METRICS)
def test_omitted_metric_is_refused_even_with_an_unknown_reason(metric):
    row = unknown_row({'id': 1, **a_run()})
    del row[metric]
    with pytest.raises(rsi_rows.Refused, match=metric):
        rsi_rows.check_result(row)

@pytest.mark.parametrize('unknowns', [None, [], {}, {'cost_usd': {}},
    {'cost_usd': {'reason': ' ', 'source': 'log'}},
    {'cost_usd': {'reason': 'unavailable', 'source': ''}},
    {'cost_usd': {'reason': 2, 'source': 'log'}}])
def test_null_requires_a_nonblank_reason_and_source(unknowns):
    row = a_result({'id': 1, **a_run()}, cost_usd=None, metric_unknowns=unknowns)
    with pytest.raises(rsi_rows.Refused, match='metric_unknowns|cost_usd'):
        rsi_rows.check_result(row)

@pytest.mark.parametrize('metric', METRICS)
@pytest.mark.parametrize('value', [-1, True, float('nan'), float('inf')])
def test_bad_known_metrics_are_refused(metric, value):
    row = a_result({'id': 1, **a_run()}, **{metric: value})
    with pytest.raises(rsi_rows.Refused, match=metric):
        rsi_rows.check_result(row)

@pytest.mark.parametrize('metric', ['input_tokens', 'output_tokens', 'turns'])
def test_known_counts_cannot_be_fractional(metric):
    with pytest.raises(rsi_rows.Refused, match=metric):
        rsi_rows.check_result(a_result({'id': 1, **a_run()}, **{metric: 1.5}))

def test_known_values_cannot_also_be_labelled_unknown():
    with pytest.raises(rsi_rows.Refused, match='metric_unknowns|cost_usd'):
        rsi_rows.check_result(a_result({'id': 1, **a_run()}, metric_unknowns={
            'cost_usd': {'reason': 'unavailable', 'source': 'log'}}))

@pytest.mark.parametrize('metric', METRICS)
def test_oversized_measurements_are_refused_without_arithmetic_errors(metric):
    with pytest.raises(rsi_rows.Refused, match=metric):
        rsi_rows.check_result(a_result({'id': 1, **a_run()}, **{metric: 10**400}))
