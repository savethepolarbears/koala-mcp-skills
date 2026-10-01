"""Reviewed conservative input contracts; live MCP definitions remain authoritative."""
from __future__ import annotations
import math, re, uuid
from datetime import date
from decimal import Decimal
from functools import lru_cache
from pathlib import Path
from typing import Any
from .common import PolicyError, amount, natural, load_json

CATALOG_PATH = Path(__file__).resolve().parents[2] / 'references/tools.json'

@lru_cache(maxsize=1)
def catalog() -> dict[str, dict]:
    return {item['name']: item for item in load_json(CATALOG_PATH)['tools']}

def contract_validate(value: Any, schema: dict, path: str = 'arguments') -> None:
    """Validate only the JSON Schema subset used in our reviewed contracts, not arbitrary JSON Schema."""
    if 'anyOf' in schema:
        for branch in schema['anyOf']:
            try: contract_validate(value, branch, path); return
            except PolicyError: pass
        raise PolicyError(f'{path}: does not match any accepted input shape')
    kind = schema.get('type')
    valid = {'object':isinstance(value,dict),'array':isinstance(value,list),
             'string':isinstance(value,str),'boolean':type(value) is bool,
             'integer':type(value) is int,
             'number':type(value) in (int,float) and (not isinstance(value,float) or math.isfinite(value))}
    if kind and not valid.get(kind,False): raise PolicyError(f'{path}: expected {kind}')
    if 'enum' in schema and value not in schema['enum']: raise PolicyError(f'{path}: invalid choice')
    if kind == 'object':
        properties = schema.get('properties',{})
        missing = set(schema.get('required',[])) - value.keys()
        if missing: raise PolicyError(f'{path}: missing {sorted(missing)}')
        if schema.get('additionalProperties') is False:
            extra = value.keys() - properties.keys()
            if extra: raise PolicyError(f'{path}: unreviewed fields {sorted(extra)}; inspect live schema')
        if len(value) < schema.get('minProperties',0): raise PolicyError(f'{path}: too few fields')
        for key, child in value.items():
            if key in properties: contract_validate(child,properties[key],f'{path}.{key}')
    elif kind == 'array':
        if len(value) < schema.get('minItems',0) or len(value) > schema.get('maxItems',10**9):
            raise PolicyError(f'{path}: array length outside reviewed bounds')
        for index, child in enumerate(value): contract_validate(child,schema.get('items',{}),f'{path}[{index}]')
    elif kind == 'string':
        if len(value) < schema.get('minLength',0) or len(value) > schema.get('maxLength',10**9):
            raise PolicyError(f'{path}: string length outside reviewed bounds')
        if schema.get('pattern') and not re.search(schema['pattern'],value): raise PolicyError(f'{path}: invalid pattern')
        if schema.get('format') == 'uuid':
            try: uuid.UUID(value)
            except ValueError as exc: raise PolicyError(f'{path}: expected a discovered UUID, not a made-up identifier') from exc
        if schema.get('format') == 'date':
            try:
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value): raise ValueError()
                date.fromisoformat(value)
            except ValueError as exc: raise PolicyError(f'{path}: expected YYYY-MM-DD') from exc
    elif kind in ('number','integer'):
        if value < schema.get('minimum',-math.inf) or value > schema.get('maximum',math.inf):
            raise PolicyError(f'{path}: number outside reviewed bounds')

def validate_arguments(tool: str, arguments: dict, *, live_schema_reviewed: bool = False) -> None:
    if tool not in catalog(): raise PolicyError(f'Unknown/unreviewed Koala tool: {tool}')
    if not isinstance(arguments,dict): raise PolicyError('Tool arguments must be an object')
    item = catalog()[tool]
    if item['contract_status'].startswith('opaque'):
        if live_schema_reviewed is not True or not arguments:
            raise PolicyError(f'{tool}: opaque connector input; inspect live schema and explicitly record review')
        return
    contract_validate(arguments,item['input_contract'])

def estimate(tool: str, arguments: dict, writer_word_reservation: int = 0) -> dict:
    if tool not in catalog(): raise PolicyError(f'Unknown/unreviewed Koala tool: {tool}')
    cost = catalog()[tool]['cost']; kind = cost['kind']; credits = Decimal(0)
    if kind == 'fixed': credits = amount(cost['credits'])
    elif kind == 'per_unique_seed':
        seeds = arguments.get('keywords',[])
        if not isinstance(seeds,list) or not seeds or any(not isinstance(s,str) or not s.strip() for s in seeds):
            raise PolicyError('Seed keywords must be nonblank strings')
        credits = amount(cost['credits']) * len(set(s.strip() for s in seeds))
    elif kind == 'image':
        quality = arguments.get('quality','fast')
        if quality not in ('fast','quality'): raise PolicyError('Unrecognized image quality')
        credits = amount(cost[quality])
    return {'credits':credits,'words':natural(writer_word_reservation,'writer_word_reservation')}
