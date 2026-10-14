#!/usr/bin/env python3
"""Validate CatalystIQ public archive. Python stdlib only."""
import datetime as dt, json, re, sys
from pathlib import Path

DATA=Path(sys.argv[1] if len(sys.argv)>1 else 'data/months.json')
BASE='CIQ-GEO-2026-10-14'
FIELDS=('direct','gaza','economic','maritime','diplomatic')
ALLOWED={'unknown','fragile','elevated','stable','deteriorating','improving','functioning','moderate','high','low','indeterminate','watch','active'}

def fail(message): raise ValueError(message)
def parse_date(d,field):
    if not isinstance(d,str): fail(f'{field} must be an ISO date')
    try: return dt.date.fromisoformat(d)
    except ValueError: fail(f'{field} has invalid date {d}')

try:
    doc=json.loads(DATA.read_text(encoding='utf8'))
    if doc.get('schema_version') != 1 or doc.get('baseline') != BASE: fail('Schema/baseline mismatch')
    entries=doc.get('snapshots')
    if not isinstance(entries,list) or not entries: fail('At least one snapshot is required')
    ids=set(); last=None; complete_months=set()
    for item in entries:
        key=item.get('id')
        if not isinstance(key,str) or key in ids: fail('IDs must be unique strings')
        ids.add(key)
        if not re.fullmatch(r'\d{4}-\d{2}',item.get('month','')): fail(f'Bad month for {key}')
        first=parse_date(item['month']+'-01','month')
        if last is not None and first<last: fail('Snapshots must be chronologically ordered')
        last=first
        period=item.get('period')
        if period not in ('complete','interim'): fail(f'Bad period for {key}')
        asof=parse_date(item.get('as_of'),'as_of')
        pub=parse_date(item.get('published'),'published')
        if asof>dt.date.today() or pub>dt.date.today(): fail(f'Future dates in {key}')
        if period=='complete':
            following=(first.replace(day=28)+dt.timedelta(days=4)).replace(day=1)
            if asof<following: fail(f'Completed month {key} assessed before month ended')
            if item['month'] in complete_months: fail(f'Duplicate completed month {key}')
            complete_months.add(item['month'])
        if asof<first: fail(f'As-of precedes month: {key}')
        if item.get('reference_baseline')!=BASE: fail(f'Wrong baseline in {key}')
        indicators=item.get('indicators')
        if not isinstance(indicators,dict) or not all(k in indicators for k in FIELDS): fail(f'Missing indicators in {key}')
        for k in FIELDS:
            v=indicators[k]
            if not isinstance(v,dict) or v.get('status') not in ALLOWED: fail(f'Bad status in {key}/{k}')
            if not isinstance(v.get('observation'),str) or len(v['observation'].strip())<8: fail(f'Empty observation in {key}/{k}')
        metrics=item.get('numeric_metrics')
        if not isinstance(metrics,dict): fail(f'Invalid metrics in {key}')
        for k,v in metrics.items():
            if v is None: fail(f'Unknown numeric metrics must be omitted, not null: {key}/{k}')
            if not isinstance(v,dict) or not isinstance(v.get('value'),(int,float)) or isinstance(v.get('value'),bool) or not v.get('unit') or not v.get('source_url'): fail(f'Metrics require measured value, unit, source_url: {key}/{k}')
        urls=item.get('sources')
        if not isinstance(urls,list) or len(urls)<2 or any(not isinstance(u,str) or not u.startswith('https://') for u in urls): fail(f'Sources missing or unsafe in {key}')
    anchor=entries[0]
    if anchor.get('id')!='2026-10-interim' or anchor.get('as_of')!='2026-10-14' or anchor.get('period')!='interim': fail('Founding baseline must remain the first snapshot')
    if len(entries)>1:
        if any(e.get('id')=='2026-10-interim' for e in entries[1:]): fail('Baseline duplicated')
    print(f'Validated {len(entries)} snapshot(s) in {DATA}')
except (ValueError,KeyError,TypeError,json.JSONDecodeError) as e:
    print(f'VALIDATION FAILED: {e}',file=sys.stderr)
    sys.exit(1)
