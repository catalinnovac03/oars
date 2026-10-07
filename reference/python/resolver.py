"""Experimental OARS 0.4-draft fixture resolver, not an enforcement engine.

See docs/DECISIONS.md for conventions beyond the source and trust preconditions.
Inputs are already schema-validated, externally accepted Core records.
"""
from datetime import datetime


def instant(value):
    return datetime.fromisoformat(value.upper().replace('Z', '+00:00'))


def contains(period, time):
    t = instant(time)
    return instant(period['from']) <= t and (
        'until' not in period or t < instant(period['until']))


def semantic_errors(record):
    errors = []
    for path, period in [('/effective', record['effective']),
                         ('/assessment/effective', record['assessment'].get('effective'))]:
        if period and 'until' in period and instant(period['until']) <= instant(period['from']):
            errors.append((path, 'period_order'))
    grants = record['authority_envelope']['grants']
    ids = [g['authority_ref'] for g in grants]
    if len(ids) != len(set(ids)):
        errors.append(('/authority_envelope/grants', 'duplicate_authority'))
    rel = record['record'].get('relationship')
    if rel and rel['ref'] == record['record']['id']:
        errors.append(('/record/relationship', 'self_relationship'))
    return errors


def scope_pair(record):
    return (record['scope']['subject']['id'], record['scope']['context']['id'])


def same_period(a, b):
    return (instant(a['from']) == instant(b['from']) and
            ('until' in a) == ('until' in b) and
            ('until' not in a or instant(a['until']) == instant(b['until'])))


def resolve(case):
    """Resolve grants without modifying data or evaluating external policies."""
    records, q = case['records'], case['query']
    pair = (q['subject'], q['context'])
    matching = [r for r in records if scope_pair(r) == pair]
    if not matching:
        return {'result': 'UNKNOWN_SCOPE'}
    uncertain = {'result': 'INDETERMINATE'}
    scope_ids = {r['scope']['id'] for r in matching}
    if len(scope_ids) != 1:
        return uncertain
    scope_id = next(iter(scope_ids))
    if any(r['scope']['id'] == scope_id and scope_pair(r) != pair for r in records):
        return uncertain
    # Validate the selected scope's history as a graph, never sort by issue time.
    by_id = {}
    for r in matching:
        rid = r['record']['id']
        if rid in by_id or semantic_errors(r):
            return uncertain
        by_id[rid] = r
    # A selected ID reused outside its scope is also ambiguous.
    if any(r['record']['id'] in by_id and scope_pair(r) != pair for r in records):
        return uncertain
    edges = {}
    for rid, r in by_id.items():
        rel = r['record'].get('relationship')
        if not rel:
            continue
        target = by_id.get(rel['ref'])
        if target is None:
            if case.get('allow_missing_history') and not any(
                    t['record']['id'] == rel['ref'] for t in records):
                continue
            return uncertain
        if instant(r['record']['issued_at']) <= instant(target['record']['issued_at']):
            return uncertain
        if rel['type'] == 'corrects' and not same_period(r['effective'], target['effective']):
            return uncertain
        edges[rid] = rel['ref']
    for rid in edges:
        seen = set()
        node = rid
        while node in edges:
            if node in seen:
                return uncertain
            seen.add(node)
            node = edges[node]
    active = {rid for rid, r in by_id.items() if contains(r['effective'], q['time'])}
    suppressed = set()
    for rid in active:
        node = rid
        while node in edges:
            node = edges[node]
            suppressed.add(node)
    survivors = active - suppressed
    if len(survivors) != 1:
        return uncertain
    chosen = by_id[next(iter(survivors))]
    grants = [g for g in chosen['authority_envelope']['grants'] if g['authority_ref'] == q['authority']]
    if not grants:
        return {'result': 'NOT_GRANTED_BY_ENVELOPE', 'constraints': []}
    grant = grants[0]
    human = grant.get('human_authorization', {}).get('required', False)
    policy = bool(grant.get('policy_refs'))
    constraints = (['human_authorization'] if human else []) + (['policy'] if policy else [])
    result = ('GRANTED_SUBJECT_TO_HUMAN_AUTHORIZATION' if human else
              'GRANTED_SUBJECT_TO_POLICY' if policy else 'GRANTED')
    return {'result': result, 'constraints': constraints}


def correlate(case):
    """Separate fixture mapping diagnostic; trust labels are not authentication."""
    q = case['query']
    scope_ids = {r['scope']['id'] for r in case['records']
                 if scope_pair(r) == (q['subject'], q['context'])}
    if len(scope_ids) != 1:
        return {'status': 'INDETERMINATE'}
    sid = next(iter(scope_ids))
    subjects = [b for b in case.get('subject_bindings', [])
                if b['scope_ref'] == sid and contains(b['effective'], q['time'])]
    authorities = [b for b in case.get('authority_bindings', [])
                   if b['scope_ref'] == sid and b['authority_ref'] == q['authority']
                   and contains(b['effective'], q['time'])]
    if not subjects or not authorities:
        return {'status': 'UNMAPPED'}
    trusted = set(case.get('trusted_asserted_by', []))
    if any(b.get('asserted_by') not in trusted for b in subjects + authorities):
        return {'status': 'UNTRUSTED'}
    if len(subjects) != 1 or len(authorities) != 1:
        return {'status': 'INDETERMINATE'}
    return {'status': 'MAPPED', 'implementation_ref': subjects[0]['implementation']['ref'],
            'target_ref': authorities[0]['target']['ref']}
