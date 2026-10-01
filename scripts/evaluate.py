#!/usr/bin/env python3
"""Execute deterministic policy fixtures. Does NOT run or score an LLM or live MCP server."""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/koala-core/scripts'))
from koala_ops.common import PolicyError
from koala_ops.policy import validate_plan

def evaluate(root: Path=ROOT) -> dict:
    cases=json.loads((root/'benchmarks/policy-cases.json').read_text())['cases'];results=[]
    for case in cases:
        observed='allow';reason='';summary=None
        try:summary=validate_plan(case['plan'],datetime.fromisoformat(case['clock']))
        except PolicyError as exc:observed='block';reason=str(exc)
        except Exception as exc:observed='crash';reason=type(exc).__name__+': '+str(exc)
        results.append({'id':case['id'],'expected':case['expected'],'observed':observed,
                        'passed':observed==case['expected'],'reason':reason,'summary':summary})
    return {'passed':all(x['passed'] for x in results),'cases':len(results),'passed_cases':sum(x['passed'] for x in results),
            'llm_evaluation':False,'network_calls':0,'results':results,
            'notice':'Deterministic local policy fixtures only. No host-agent scenario, OAuth flow or remote call was executed.'}

if __name__=='__main__':
    result=evaluate();print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
