"""Transactional, local reservation and receipt ledger. This module makes no network calls."""
from __future__ import annotations
import json, os, sqlite3
from contextlib import contextmanager, closing
from datetime import datetime
from pathlib import Path
from .common import PolicyError, amount, canonical, digest, utcnow
from .catalog import catalog, estimate
from .policy import validate_plan, check_approval, public_url

class Ledger:
    def __init__(self, path: str | Path):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
        with closing(self._connect()) as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS budgets (group_id TEXT PRIMARY KEY, credits_cap TEXT NOT NULL,
                words_cap INTEGER NOT NULL,calls_cap INTEGER NOT NULL,credits_reserved TEXT NOT NULL,
                words_reserved INTEGER NOT NULL,calls_reserved INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY,plan_hash TEXT NOT NULL,group_id TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS claims (claim_key TEXT PRIMARY KEY,run_id TEXT NOT NULL,action_id TEXT NOT NULL,
                plan_hash TEXT NOT NULL,tool TEXT NOT NULL,effect TEXT NOT NULL,status TEXT NOT NULL,
                args_hash TEXT NOT NULL,receipt TEXT,external_id TEXT,created_at TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT,claim_key TEXT NOT NULL,
                kind TEXT NOT NULL,recorded_at TEXT NOT NULL,evidence TEXT NOT NULL,evidence_sha256 TEXT NOT NULL);
            ''')
        try:os.chmod(self.path,0o600)
        except OSError:pass

    def _connect(self):
        db=sqlite3.connect(self.path,timeout=30);db.row_factory=sqlite3.Row
        db.execute('PRAGMA busy_timeout=30000');return db

    @contextmanager
    def _transaction(self):
        db=self._connect()
        try:
            db.execute('BEGIN IMMEDIATE');yield db;db.commit()
        except Exception:db.rollback();raise
        finally:db.close()

    @staticmethod
    def _action(plan: dict, action_id: str) -> dict:
        matches=[a for a in plan.get('actions',[]) if a.get('id')==action_id]
        if len(matches)!=1:raise PolicyError('Action ID is missing or ambiguous')
        return matches[0]

    @staticmethod
    def _key(plan: dict, action: dict) -> str:
        if catalog()[action['tool']]['effect']=='read':return 'read:'+digest([plan['run_id'],action['id']])
        return 'effect:'+digest([plan['scope'].get('account_ref','default'),plan['scope'].get('brand_id'),
                                  public_url(plan['scope']['domain'] if '://' in plan['scope']['domain'] else 'https://'+plan['scope']['domain']),action['operation_key']])

    @staticmethod
    def _event(db, key, kind, now, evidence):
        db.execute('INSERT INTO events(claim_key,kind,recorded_at,evidence,evidence_sha256) VALUES(?,?,?,?,?)',
                   (key,kind,now.isoformat(),canonical(evidence),digest(evidence)))

    def claim(self, plan: dict, action_id: str, approval: dict | None = None, now: datetime | None = None) -> dict:
        now=now or utcnow();validate_plan(plan,now);check_approval(plan,approval,now)
        action=self._action(plan,action_id);key=self._key(plan,action);ph=digest(plan)
        cost=estimate(action['tool'],action.get('arguments',{}),action.get('writer_word_reservation',0))
        caps=plan.get('limits',{});cc=str(amount(caps.get('platform_credits','0')));wc=caps.get('writer_words',0);mc=caps.get('max_calls',20)
        with self._transaction() as db:
            run=db.execute('SELECT * FROM runs WHERE run_id=?',(plan['run_id'],)).fetchone()
            if run and run['plan_hash']!=ph:raise PolicyError('Run ID is already bound to another plan; do not mutate a running plan')
            existing=db.execute('SELECT * FROM claims WHERE claim_key=?',(key,)).fetchone()
            if existing:raise PolicyError(f'Operation already claimed ({existing["status"]}); reconcile, never blindly reissue')
            for dep in action.get('depends_on',[]):
                depkey=self._key(plan,self._action(plan,dep));row=db.execute('SELECT * FROM claims WHERE claim_key=?',(depkey,)).fetchone()
                depaction=self._action(plan,dep)
                verification_read=(row is not None and row['status']=='recorded' and row['effect']!='read'
                    and catalog()[action['tool']]['effect']=='read'
                    and action['tool']==depaction.get('verification',{}).get('tool')
                    and (not row['external_id'] or action.get('arguments',{}).get('articleId')==row['external_id']))
                if not row or row['plan_hash']!=ph or (row['status']!='verified' and not (row['effect']=='read' and row['status']=='recorded') and not verification_read):
                    raise PolicyError(f'Dependency {dep} has no successful verified/observed evidence')
            group=db.execute('SELECT * FROM budgets WHERE group_id=?',(plan['budget_group'],)).fetchone()
            if group:
                if amount(group['credits_cap'])!=amount(cc) or group['words_cap']!=wc or group['calls_cap']!=mc:
                    raise PolicyError('Budget group ceilings are immutable; changing them needs a separately authorized cycle')
                cr=amount(group['credits_reserved']);wr=group['words_reserved'];nr=group['calls_reserved']
            else:cr=amount('0');wr=0;nr=0
            if cr+cost['credits']>amount(cc) or wr+cost['words']>wc or nr+1>mc:raise PolicyError('Shared local reservation budget is exhausted')
            if not group:
                db.execute('INSERT INTO budgets VALUES(?,?,?,?,?,?,?)',(plan['budget_group'],cc,wc,mc,'0',0,0))
            db.execute('UPDATE budgets SET credits_reserved=?,words_reserved=?,calls_reserved=? WHERE group_id=?',
                       (str(cr+cost['credits']),wr+cost['words'],nr+1,plan['budget_group']))
            db.execute('INSERT OR IGNORE INTO runs VALUES(?,?,?)',(plan['run_id'],ph,plan['budget_group']))
            db.execute('INSERT INTO claims VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                (key,plan['run_id'],action_id,ph,action['tool'],catalog()[action['tool']]['effect'],'claimed',digest(action.get('arguments',{})),None,None,now.isoformat()))
            self._event(db,key,'claim',now,{'action':action,'approval_sha256':digest(approval) if approval else None})
        return {'status':'claimed','claim_key':key,'call':{'tool':action['tool'],'arguments':action.get('arguments',{})},
                'reservation':{'platform_credits':str(cost['credits']),'writer_words':cost['words']},
                'notice':'No network call made. Invoke this exact call in your authenticated host once, then record its result.'}

    def _claimed(self, db, plan, action):
        key=self._key(plan,action);row=db.execute('SELECT * FROM claims WHERE claim_key=?',(key,)).fetchone()
        if not row or row['plan_hash']!=digest(plan):raise PolicyError('No claim matches this exact plan/action')
        return key,row

    def record(self, plan: dict, action_id: str, receipt: dict, now: datetime | None = None) -> dict:
        now=now or utcnow();action=self._action(plan,action_id)
        if not isinstance(receipt,dict) or receipt.get('tool')!=action['tool'] or 'data' not in receipt:
            raise PolicyError('Receipt must include the original tool and actual observed data')
        outcome=receipt.get('outcome')
        if outcome not in ('success','failure','uncertain','partial'):raise PolicyError('Receipt outcome must be success/failure/uncertain/partial')
        external=receipt.get('external_id')
        if external is not None and (not isinstance(external,str) or not external):raise PolicyError('external_id must be a nonempty string when present')
        if outcome=='success' and action['tool']=='create_article_in_koala_writer' and not external:raise PolicyError('Persist the returned article ID before marking creation observed')
        if action['tool']=='edit_article' and external and external!=action['arguments']['articleId']:raise PolicyError('Edited article identity does not match the approved action')
        canonical(receipt)
        with self._transaction() as db:
            key,row=self._claimed(db,plan,action)
            if row['status']!='claimed':raise PolicyError('A receipt already exists; reconcile ambiguous results without replacing history')
            state='recorded' if outcome=='success' else outcome
            db.execute('UPDATE claims SET status=?,receipt=?,external_id=? WHERE claim_key=?',(state,canonical(receipt),external,key))
            self._event(db,key,'record',now,receipt)
        return {'status':state,'claim_key':key,'notice':'Reservations remain held, including failures and ambiguous outcomes.'}

    def reconcile(self, plan: dict, action_id: str, receipt: dict, now: datetime | None = None) -> dict:
        """Attach found-result evidence to an uncertain/partial claim; never make a retry executable."""
        now=now or utcnow();action=self._action(plan,action_id)
        if not isinstance(receipt,dict) or receipt.get('tool')!=action['tool'] or receipt.get('outcome')!='success' or 'data' not in receipt or not receipt.get('reconciliation_evidence'):
            raise PolicyError('Reconciliation requires success evidence for the original operation and a traceable read-back reference')
        external=receipt.get('external_id')
        if external is not None and (not isinstance(external,str) or not external):raise PolicyError('external_id must be a nonempty string when present')
        if action['tool']=='edit_article' and external and external!=action['arguments']['articleId']:raise PolicyError('Edited article identity does not match the approved action')
        if action['tool']=='create_article_in_koala_writer' and not external:raise PolicyError('Recover the existing article ID; do not create a replacement')
        canonical(receipt)
        with self._transaction() as db:
            key,row=self._claimed(db,plan,action)
            if row['status'] not in ('uncertain','partial'):raise PolicyError('Only uncertain/partial operations can be reconciled')
            if row['external_id'] and row['external_id']!=external:raise PolicyError('Reconciliation changed the known external identity')
            db.execute('UPDATE claims SET status=?,receipt=?,external_id=? WHERE claim_key=?',('recorded',canonical(receipt),external,key))
            self._event(db,key,'reconcile',now,receipt)
        return {'status':'recorded','claim_key':key,'notice':'Recovered existing operation; no retry, refund or network action occurred.'}

    def verify(self, plan: dict, action_id: str, evidence: dict, now: datetime | None = None) -> dict:
        now=now or utcnow();action=self._action(plan,action_id);expected=action.get('verification',{})
        if not isinstance(evidence,dict) or not expected or evidence.get('tool')!=expected.get('tool'):
            raise PolicyError('Read-back tool does not match the approved verification contract')
        observed=evidence.get('observed',{})
        if not isinstance(observed,dict) or any(k not in observed or digest(observed[k])!=digest(v) for k,v in expected.get('checks',{}).items()):
            raise PolicyError('Read-back checks did not all pass')
        with self._transaction() as db:
            key,row=self._claimed(db,plan,action)
            if row['status']!='recorded':raise PolicyError('Only successfully recorded operations can be verified')
            if row['external_id'] and row['external_id']!=evidence.get('external_id'):raise PolicyError('Read-back identity differs from the execution receipt')
            db.execute('UPDATE claims SET status=? WHERE claim_key=?',('verified',key));self._event(db,key,'verify',now,evidence)
        return {'status':'verified','claim_key':key,'notice':'Local evidence contract passed. Caller-supplied evidence is not a remote attestation.'}

    def status(self) -> dict:
        with closing(self._connect()) as db:
            groups=[dict(r) for r in db.execute('SELECT * FROM budgets ORDER BY group_id')]
            claims=[dict(r) for r in db.execute('SELECT run_id,action_id,tool,effect,status,external_id FROM claims ORDER BY created_at,claim_key')]
            events=db.execute('SELECT COUNT(*) FROM events').fetchone()[0]
        return {'budget_groups':groups,'actions':claims,'event_count':events,
                'notice':'Reserved estimates only. Not an account balance, receipt authenticity check or global exactly-once guarantee.'}
