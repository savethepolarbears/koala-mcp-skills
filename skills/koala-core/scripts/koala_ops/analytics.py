"""Deterministic arithmetic and exact-match intent triage, not SEO predictions."""
from __future__ import annotations
import re, unicodedata
from datetime import date, timedelta
from .common import PolicyError, amount, natural

def periods(end: str, days: int = 28) -> dict:
    natural(days,'days',1)
    if days>486:raise PolicyError('Use at most 486 days in a comparison period')
    try:last=date.fromisoformat(end)
    except ValueError as exc:raise PolicyError('end must be YYYY-MM-DD') from exc
    first=last-timedelta(days=days-1);previous_end=first-timedelta(days=1)
    return {'days_each':days,'current':{'start':first.isoformat(),'end':last.isoformat()},
            'previous':{'start':(first-timedelta(days=days)).isoformat(),'end':previous_end.isoformat()},
            'notice':'Inclusive calendar dates. Check property timezone, data freshness, completeness and identical filters separately.'}

def compare_metrics(previous: dict, current: dict) -> dict:
    if not isinstance(previous,dict) or not isinstance(current,dict):raise PolicyError('Metrics must be objects')
    def val(row,key):return None if row.get(key) is None else amount(row[key])
    result={}
    for key in ('clicks','impressions'):
        before,after=val(previous,key),val(current,key)
        result[f'{key}_delta']=None if before is None or after is None else float(after-before)
        result[f'{key}_pct']=None if before is None or after is None or before==0 else float((after-before)/before*100)
    for label,row in [('previous',previous),('current',current)]:
        clicks,impressions=val(row,'clicks'),val(row,'impressions')
        result[f'ctr_{label}']=None if clicks is None or impressions is None or impressions==0 else float(clicks/impressions)
    result['notice']='Missing values remain null. CTR is clicks/impressions, not an average of row CTRs. Changes do not establish causality.'
    return result

def normalize_intent(value: str) -> str:
    if not isinstance(value,str) or not value.strip():raise PolicyError('Intent must be a nonblank string')
    return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',value).casefold()).strip()

def classify_candidate(keyword: str, planned_keywords: list[str], coverage: str | None, matched_urls: list[str]) -> dict:
    normalized=normalize_intent(keyword)
    if normalized in {normalize_intent(k) for k in planned_keywords}:decision='skip';reason='Exact normalized intent already planned'
    elif coverage in ('covered','partial'):
        decision='inspect-existing' if matched_urls else 'investigate';reason='Review matched URLs and intent; coverage is a model judgment'
    elif coverage=='uncovered':decision='candidate-not-approved';reason='No match found in available data, not proof of absence or permission to generate'
    else:decision='investigate';reason='Coverage is unavailable or unrecognized; unknown is not uncovered'
    return {'keyword':keyword,'normalized':normalized,'decision':decision,'reason':reason,
            'matched_urls':matched_urls,'semantic_overlap':'not determined by this exact-match helper'}
