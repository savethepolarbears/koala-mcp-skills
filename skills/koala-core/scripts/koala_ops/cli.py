"""CLI entry point. Every command is offline; authenticated MCP calls belong to the host."""
from __future__ import annotations
import argparse, json, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path
from .common import PolicyError, load_json, write_json, digest
from .catalog import catalog
from .policy import validate_plan, approve
from .ledger import Ledger
from .analytics import periods, compare_metrics, classify_candidate


def schema_diff(observed: dict) -> dict:
    """Compare reviewed input shapes; missing tools can be permission-filtered, not removed."""
    if not isinstance(observed,dict):raise PolicyError('Expected a tools/list response object')
    rows=observed.get('result',observed).get('tools')
    if not isinstance(rows,list) or any(not isinstance(t,dict) or not isinstance(t.get('name'),str) for t in rows):
        raise PolicyError('Expected tools/list result.tools or tools array with names')
    if len({t['name'] for t in rows})!=len(rows):raise PolicyError('Duplicate observed tool names')
    current={t['name']:t for t in rows};known=catalog();changed={}
    for name in sorted(current.keys() & known.keys()):
        if known[name]['contract_status'].startswith('opaque'):continue
        live=current[name].get('inputSchema')
        if not isinstance(live,dict):changed[name]=['inputSchema unavailable'];continue
        local=known[name]['input_contract'];reasons=[]
        if set(live.get('properties',{}))!=set(local['properties']):reasons.append('parameter names differ')
        if set(live.get('required',[]))!=set(local['required']):reasons.append('required parameters differ')
        def shape(x):
            if isinstance(x,dict):return {k:shape(v) for k,v in x.items() if k not in {'description','title','default','$schema','additionalProperties'}}
            if isinstance(x,list):return [shape(v) for v in x]
            return x
        # Exact structural comparison is deliberately conservative; transcription differences need review too.
        if shape(live.get('properties',{}))!=shape(local['properties']):reasons.append('parameter types/constraints differ')
        if reasons:changed[name]=reasons
    return {'added_unreviewed':sorted(current.keys()-known.keys()),
            'missing_or_permission_filtered':sorted(known.keys()-current.keys()),'changed_needs_review':changed,
            'opaque_requires_live_review':[n for n in current.keys() & known.keys() if known[n]['contract_status'].startswith('opaque')],
            'notice':'This is a conservative local transcription comparison, not a claim that the provider changed. Missing tools may reflect permissions. Nothing was updated.'}


def demo() -> dict:
    """A fixture-only read/record loop; zero live tools, credits, accounts or network requests."""
    now=datetime(2026,10,1,12,tzinfo=timezone.utc)
    p={'version':1,'run_id':'offline-demo','budget_group':'synthetic-account-cycle',
       'scope':{'brand_id':None,'domain':'example.com'},'mode':'read-only',
       'limits':{'platform_credits':'1','writer_words':0,'max_calls':5},
       'actions':[{'id':'budget','tool':'get_usage','arguments':{},'depends_on':[]},
                  {'id':'inventory','tool':'get_sitemap','arguments':{'domain':'example.com','limit':100},'depends_on':['budget']}]}
    with tempfile.TemporaryDirectory(prefix='koala-demo-') as folder:
        ledger=Ledger(Path(folder)/'state.sqlite3')
        ledger.claim(p,'budget',now=now)
        ledger.record(p,'budget',{'tool':'get_usage','outcome':'success','data':{'fixture':True,'platform_credits':100}},now)
        ledger.claim(p,'inventory',now=now)
        ledger.record(p,'inventory',{'tool':'get_sitemap','outcome':'success','data':{'fixture':True,'returnedSlugCount':2,'slugs':['/rain-garden','/soil']}},now)
        duplicate_blocked=False
        try:ledger.claim(p,'inventory',now=now)
        except PolicyError:duplicate_blocked=True
        state=ledger.status()
    return {'simulation':True,'network_calls':0,'real_credits_spent':0,'real_writer_words_spent':0,
            'planned_reservation':validate_plan(p,now),'duplicate_claim_blocked':duplicate_blocked,
            'comparison':compare_metrics({'clicks':100,'impressions':1000},{'clicks':70,'impressions':900}),
            'intent_check':classify_candidate(' Rain Garden ',['rain garden'],None,[]),'ledger':state,
            'notice':'Synthetic fixture results only. This does not test Koala authentication, server execution or host skill loading.'}


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('demo',help='Run a zero-network synthetic demo')
    p=sub.add_parser('catalog',help='List reviewed tools or inspect one');p.add_argument('--tool');p.add_argument('--group')
    p=sub.add_parser('check',help='Validate and estimate a local plan');p.add_argument('plan')
    p=sub.add_parser('approve',help='Record a HUMAN-issued local exact-plan approval');p.add_argument('plan');p.add_argument('--by',required=True);p.add_argument('--minutes',type=int,default=30);p.add_argument('--out',required=True)
    p=sub.add_parser('claim',help='Reserve a call locally, without executing it');p.add_argument('plan');p.add_argument('action');p.add_argument('--approval');p.add_argument('--db',required=True)
    for command in ['record','verify','reconcile']:
        p=sub.add_parser(command,help='Record local execution/read-back evidence');p.add_argument('plan');p.add_argument('action');p.add_argument('evidence');p.add_argument('--db',required=True)
    p=sub.add_parser('status');p.add_argument('--db',required=True)
    p=sub.add_parser('periods');p.add_argument('--end',required=True);p.add_argument('--days',type=int,default=28)
    p=sub.add_parser('compare');p.add_argument('input')
    p=sub.add_parser('coverage');p.add_argument('input')
    p=sub.add_parser('schema-diff');p.add_argument('observed')
    p=sub.add_parser('hash');p.add_argument('input')
    args=parser.parse_args(argv)
    try:
        if args.command=='demo':result=demo()
        elif args.command=='catalog':
            if args.tool:
                if args.tool not in catalog():raise PolicyError('Unknown tool')
                result=catalog()[args.tool]
            else:result=[{'name':t['name'],'group':t['group'],'effect':t['effect'],'cost':t['cost']} for t in catalog().values() if not args.group or t['group']==args.group]
        elif args.command=='check':result=validate_plan(load_json(args.plan))
        elif args.command=='approve':
            result=approve(load_json(args.plan),args.by,minutes=args.minutes);write_json(args.out,result)
        elif args.command=='claim':result=Ledger(args.db).claim(load_json(args.plan),args.action,load_json(args.approval) if args.approval else None)
        elif args.command in ('record','verify','reconcile'):
            result=getattr(Ledger(args.db),args.command)(load_json(args.plan),args.action,load_json(args.evidence))
        elif args.command=='status':result=Ledger(args.db).status()
        elif args.command=='periods':result=periods(args.end,args.days)
        elif args.command=='compare':
            data=load_json(args.input);result=compare_metrics(data['previous'],data['current'])
        elif args.command=='coverage':
            data=load_json(args.input);result=classify_candidate(data['keyword'],data.get('planned_keywords',[]),data.get('coverage'),data.get('matched_urls',[]))
        elif args.command=='schema-diff':
            result=schema_diff(load_json(args.observed))
            print(json.dumps(result,indent=2,ensure_ascii=False))
            return 2 if result['added_unreviewed'] or result['changed_needs_review'] else 0
        else:result={'sha256':digest(load_json(args.input))}
        print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False));return 0
    except (PolicyError,OSError,KeyError,TypeError,ValueError) as exc:
        print(json.dumps({'status':'blocked','error':str(exc)},ensure_ascii=False),file=sys.stderr);return 2
