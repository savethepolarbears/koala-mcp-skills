"""Offline policy validation. Never treats this module as remote authorization."""
from __future__ import annotations
import ipaddress, re
from datetime import date, datetime, timedelta, timezone
from urllib.parse import urlsplit, parse_qsl
from typing import Any
from .common import PolicyError, amount, natural, digest, timestamp, utcnow
from .catalog import catalog, validate_arguments, estimate

ACTION_FIELDS = {'id','tool','arguments','depends_on','operation_key','writer_word_reservation',
                 'verification','integration_review','accept_live_settings','live_schema_reviewed','rationale'}
MODE_EFFECTS = {'read-only':{'read'},'draft':{'read','generate','edit','generate_image','cancel'},
               'connected-write':{'read','generate','edit','generate_image','cancel','schedule','schedule_update','submit'}}
GENERATION = {'create_article_in_koala_writer','schedule_articles','update_scheduled_articles'}
SECRET_KEYS = re.compile(r'^(authorization|password|api[_-]?key|access[_-]?token|refresh[_-]?token|cookie|secret)$', re.I)
SIGNED_KEYS = re.compile(r'(^x-amz-|^x-goog-|^token$|^access_token$|^key$|^signature$|^sig$)', re.I)

def public_url(value: str) -> str:
    """Syntactic screening only; the real fetcher must defend DNS rebinding and redirects."""
    try: parsed = urlsplit(value); host = (parsed.hostname or '').lower().rstrip('.'); _ = parsed.port
    except ValueError as exc: raise PolicyError('Malformed URL') from exc
    if parsed.scheme not in ('https','http') or not host or parsed.username or parsed.password:
        raise PolicyError('Only public HTTP(S) URLs without embedded credentials are permitted')
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        if re.fullmatch(r'[0-9.]+',host) or re.fullmatch(r'0x[0-9a-f]+',host) or '.' not in host or host.endswith(('.localhost','.local','.internal','.invalid')) or host == 'localhost':
            raise PolicyError('Private/local hostname is not allowed')
    else:
        if not ip.is_global: raise PolicyError('Private/reserved network address is not allowed')
    if any(SIGNED_KEYS.search(k) for k,_ in parse_qsl(parsed.query,keep_blank_values=True)):
        raise PolicyError('Signed or secret-bearing URL requires a separate trusted workflow; do not send it to Koala')
    return host

def _screen(value: Any, key: str = '') -> None:
    if SECRET_KEYS.match(key): raise PolicyError('Secrets must not enter tool arguments, plans or approvals')
    if isinstance(value,dict):
        for k,v in value.items(): _screen(v,k)
    elif isinstance(value,list):
        for v in value:_screen(v,key)
    elif isinstance(value,str):
        if value.startswith(('http://','https://','file://','ftp://')): public_url(value)
        elif key in {'url','pageUrl','articleUrl','referenceImages','urls'}: public_url(value)
        elif key in {'domain','target','yourDomain','competitor','amazonDomain'} and value:
            public_url('https://'+value if '://' not in value else value)

def _require_brand(args: dict, scope: dict, required: bool) -> None:
    explicit = args.get('brandId'); intended = scope.get('brand_id')
    if required and (not explicit or not intended): raise PolicyError('Resolve and pass an explicit brandId for brand tools')
    if explicit and explicit != intended: raise PolicyError('Cross-brand arguments do not match the locked scope')

def _date_pair(args: dict, now: datetime) -> None:
    if ('startDate' in args) != ('endDate' in args): raise PolicyError('Use startDate and endDate together')
    if 'startDate' in args:
        try:
            start, end = date.fromisoformat(args['startDate']),date.fromisoformat(args['endDate'])
        except (ValueError,TypeError) as exc: raise PolicyError('Invalid date range') from exc
        if start > end or end > now.date(): raise PolicyError('Performance dates must be ordered and not in the future')

def validate_plan(plan: dict, now: datetime | None = None) -> dict:
    now = now or utcnow()
    if now.tzinfo is None: raise PolicyError('Clock must be timezone-aware')
    if not isinstance(plan,dict): raise PolicyError('Plan must be a JSON object')
    allowed={'version','run_id','budget_group','scope','limits','mode','actions','goal'}
    if set(plan)-allowed: raise PolicyError('Unrecognized plan fields')
    if plan.get('version') != 1 or type(plan.get('version')) is not int: raise PolicyError('Unsupported plan version')
    for field in ('run_id','budget_group'):
        if not isinstance(plan.get(field),str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:-]{0,159}',plan[field]):
            raise PolicyError(f'{field} must be a stable safe identifier')
    scope=plan.get('scope',{});limits=plan.get('limits',{});mode=plan.get('mode','read-only')
    if not isinstance(scope,dict) or not isinstance(limits,dict): raise PolicyError('scope and limits must be objects')
    if set(scope)-{'brand_id','domain','account_ref'}: raise PolicyError('Unrecognized scope fields')
    if 'account_ref' in scope and (not isinstance(scope['account_ref'],str) or not scope['account_ref'].strip()):
        raise PolicyError('account_ref must be a nonempty stable alias')
    if set(limits)-{'platform_credits','writer_words','max_calls'}: raise PolicyError('Unrecognized limit fields')
    if scope.get('brand_id') is not None and (not isinstance(scope['brand_id'],str) or not scope['brand_id'].strip()):
        raise PolicyError('brand_id must be null or a resolved nonblank identifier')
    if not isinstance(scope.get('domain'),str) or not scope['domain']: raise PolicyError('Explicit target domain is required')
    owned_host=public_url(scope['domain'] if '://' in scope['domain'] else 'https://'+scope['domain'])
    if mode not in MODE_EFFECTS: raise PolicyError('Mode must be read-only, draft or connected-write')
    cap=amount(limits.get('platform_credits','0'));word_cap=natural(limits.get('writer_words',0),'writer_words')
    max_calls=natural(limits.get('max_calls',20),'max_calls',1)
    actions=plan.get('actions')
    if not isinstance(actions,list) or not actions or len(actions)>min(max_calls,100): raise PolicyError('Use 1–100 bounded actions within max_calls')
    seen=set();total=amount('0');words=0;effects=set();items=[]
    for action in actions:
        if not isinstance(action,dict) or set(action)-ACTION_FIELDS: raise PolicyError('Unrecognized action shape')
        aid=action.get('id')
        if not isinstance(aid,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:-]{0,159}',aid) or aid in seen:
            raise PolicyError('Action IDs must be safe and unique')
        deps=action.get('depends_on',[])
        if not isinstance(deps,list) or any(not isinstance(d,str) or d not in seen for d in deps):
            raise PolicyError('Dependencies must reference earlier actions; cycles and missing actions are blocked')
        seen.add(aid);tool=action.get('tool');args=action.get('arguments',{})
        validate_arguments(tool,args,live_schema_reviewed=action.get('live_schema_reviewed',False))
        item=catalog()[tool];effect=item['effect'];effects.add(effect)
        if effect not in MODE_EFFECTS[mode]: raise PolicyError(f'{tool} is not permitted in {mode} mode')
        _require_brand(args,scope,item['scope']=='brand');_screen(args)
        if tool.startswith('get_gsc_'):
            _date_pair(args,now)
            if 'country' in args and not re.fullmatch(r'[A-Za-z]{3}',args['country']): raise PolicyError('GSC country uses alpha-3, not keyword-tool alpha-2')
        if tool in ('get_gsc_page_performance','get_gsc_indexing_status','request_indexing'):
            urls=args.get('urls',[args.get('pageUrl')])
            if any(public_url(u)!=owned_host for u in urls): raise PolicyError('Google URL is outside the explicitly locked host; use a separately verified scope')
        if tool=='get_ga4_page_performance' and not args['pagePath'].startswith('/'):
            raise PolicyError('GA4 pagePath must be a path beginning with /')
        if tool in ('get_page_content','get_page_html') and (('offset' in args)!=('contentHash' in args)):
            raise PolicyError('Chunk continuation requires both returned offset and contentHash')
        if tool=='audit_page_citation_readiness' and not args['urls']: raise PolicyError('Select at least one URL')
        reservation=natural(action.get('writer_word_reservation',0),'writer_word_reservation')
        if tool in GENERATION and reservation <= 0: raise PolicyError('Reserve future writer words using reviewed effective settings, including scheduling/updates')
        if tool not in GENERATION and reservation: raise PolicyError('Writer reservation applies only to generation/scheduling')
        attached=tool=='create_article_in_koala_writer' and (args.get('brandId') or args.get('projectId'))
        if attached or tool in ('schedule_articles','update_scheduled_articles'):
            if mode!='connected-write': raise PolicyError('Attached generation/scheduling can publish; connected-write authorization is required')
            review=action.get('integration_review',{})
            if not isinstance(review,dict):raise PolicyError('Integration review must be an object')
            checked=timestamp(review.get('checked_at',''))
            if checked > now or now-checked > timedelta(minutes=15):raise PolicyError('Integration review is stale; refresh effective settings immediately before writing')
            if review.get('arguments_sha256')!=digest(args) or review.get('effective_status') not in ('none','draft','publish') or not review.get('evidence_ref'):
                raise PolicyError('Bind known effective delivery settings and evidence to the exact argument hash')
        if tool in ('schedule_articles','update_scheduled_articles'):
            if action.get('accept_live_settings') is not True:raise PolicyError('Scheduled work inherits future live settings; explicit acceptance is required')
            batch=args.get('tasks',args.get('updates',[]))
            for row in batch:
                if row.get('scheduledDate') and date.fromisoformat(row['scheduledDate']) < now.date():raise PolicyError('Cannot schedule in the past')
        if tool=='create_article_in_koala_writer':
            kind=args.get('articleType','blog_post')
            required={'blog_post':'targetKeyword','listicle':'targetKeyword','amazon_product_roundup':'targetKeyword','service_page':'targetKeyword','youtube_video':'youTubeVideoUrl','rewrite_blog_post':'articleUrl','amazon_single_product_review':'asin'}[kind]
            if not args.get(required):raise PolicyError(f'{kind} requires {required}')
            if kind=='service_page' and not args.get('brandId'):raise PolicyError('Service pages require Brand DNA')
            if args.get('presetName') and not args.get('brandId'):raise PolicyError('A preset requires an explicit brand')
            if args.get('allowDuplicate'):raise PolicyError('This conservative helper does not bypass duplicate prevention; use a separately reviewed workflow')
            if args.get('extendedResearch') and not args.get('enableDeepResearch'):raise PolicyError('Extended Research requires Deep Research')
        if effect!='read':
            op=action.get('operation_key')
            if not isinstance(op,str) or not op.strip() or len(op)>200:raise PolicyError('Every effect requires a stable operation_key reused across retries/handoffs')
            verification=action.get('verification',{})
            if not isinstance(verification,dict) or verification.get('tool') not in item['verification_tools'] or not isinstance(verification.get('checks'),dict) or not verification['checks']:
                raise PolicyError('Every effect requires a planned read-back tool and nonempty verification checks')
        cost=estimate(tool,args,reservation);total+=cost['credits'];words+=cost['words']
        items.append({'id':aid,'tool':tool,'effect':effect,'credits':str(cost['credits']),'words':cost['words']})
    if total>cap or words>word_cap:raise PolicyError('Planned reservation exceeds the credit or writer-word ceiling')
    return {'plan_sha256':digest(plan),'credits':str(total),'words':words,'calls':len(actions),
            'effects':sorted(effects-{'read'}),'actions':items,'notice':'Estimated LOCAL reservations, not actual Koala billing or network authorization.'}

def approve(plan: dict, actor: str, now: datetime | None = None, minutes: int = 30) -> dict:
    now=now or utcnow();summary=validate_plan(plan,now)
    if not isinstance(actor,str) or not actor.strip():raise PolicyError('Approval needs a named human/operator identity')
    natural(minutes,'approval minutes',1)
    if minutes>1440:raise PolicyError('Approval duration must not exceed 24 hours')
    return {'version':1,'plan_sha256':summary['plan_sha256'],'actor':actor,'created_at':now.isoformat(),
            'expires_at':(now+timedelta(minutes=minutes)).isoformat(),'effects':summary['effects'],
            'notice':'Self-declared local approval; not authenticated identity or Koala authorization. Agents must not approve their own actions.'}

def check_approval(plan: dict, approval: dict | None, now: datetime | None = None) -> None:
    now=now or utcnow();summary=validate_plan(plan,now)
    if not summary['effects']:return
    if not isinstance(approval,dict) or approval.get('plan_sha256')!=digest(plan):raise PolicyError('Missing or mismatched exact-plan approval')
    if not approval.get('actor'):raise PolicyError('Approval actor is missing')
    created=timestamp(approval.get('created_at',''));expires=timestamp(approval.get('expires_at',''))
    if created>now or expires<=now or expires<=created or expires-created>timedelta(hours=24):raise PolicyError('Approval is expired or invalid')
    if approval.get('effects')!=summary['effects']:raise PolicyError('Approval does not cover these effects')
