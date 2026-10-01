"""Regression cases discovered during implementation review."""
import copy, tempfile, unittest
from pathlib import Path
from test_core import plan, draft, NOW
from koala_ops.common import PolicyError
from koala_ops.policy import public_url, validate_plan, approve
from koala_ops.ledger import Ledger

class ReviewRegressions(unittest.TestCase):
 def test_noncanonical_numeric_host_is_blocked(self):
  for host in ['127.1','2130706433','0x7f000001','0177.0.0.1']:
   with self.subTest(host=host),self.assertRaises(PolicyError):public_url('https://'+host+'/')
 def test_bad_port_is_blocked(self):
  with self.assertRaises(PolicyError):public_url('https://example.com:99999/')
 def test_empty_account_alias_is_blocked(self):
  p=plan();p['scope']['account_ref']=''
  with self.assertRaises(PolicyError):validate_plan(p,NOW)
 def test_default_limits_claim(self):
  p=plan();del p['limits']
  with tempfile.TemporaryDirectory() as d:self.assertEqual(Ledger(Path(d)/'state.db').claim(p,'a1',now=NOW)['status'],'claimed')
 def test_same_write_domain_spelling_does_not_bypass_deduplication(self):
  p=draft()
  with tempfile.TemporaryDirectory() as d:
   l=Ledger(Path(d)/'state.db');l.claim(p,'a1',approve(p,'human',NOW),NOW)
   p['run_id']='again';p['scope']['domain']='https://EXAMPLE.com/'
   with self.assertRaises(PolicyError):l.claim(p,'a1',approve(p,'human',NOW),NOW)
 def test_successful_reconciliation_preserves_key(self):
  p=draft();tool=p['actions'][0]['tool']
  with tempfile.TemporaryDirectory() as d:
   l=Ledger(Path(d)/'state.db');a=approve(p,'human',NOW);l.claim(p,'a1',a,NOW)
   l.record(p,'a1',{'tool':tool,'outcome':'uncertain','data':{}},NOW)
   result=l.reconcile(p,'a1',{'tool':tool,'outcome':'success','external_id':'job-1','data':{},'reconciliation_evidence':'local/readback.json'},NOW)
   self.assertEqual(result['status'],'recorded')
   with self.assertRaises(PolicyError):l.claim(p,'a1',a,NOW)
 def test_reconciliation_rejects_nonstring_identity(self):
  p=draft();tool=p['actions'][0]['tool']
  with tempfile.TemporaryDirectory() as d:
   l=Ledger(Path(d)/'state.db');l.claim(p,'a1',approve(p,'human',NOW),NOW)
   l.record(p,'a1',{'tool':tool,'outcome':'uncertain','data':{}},NOW)
   with self.assertRaises(PolicyError):l.reconcile(p,'a1',{'tool':tool,'outcome':'success','external_id':42,'data':{},'reconciliation_evidence':'local/readback.json'},NOW)
 def test_edit_reconciliation_cannot_change_article(self):
  p=plan('edit_article',{'articleId':'00000000-0000-4000-8000-000000000001','instruction':'Fix factual error'},credits='1')
  p['mode']='draft';p['actions'][0].update(operation_key='edit-1',verification={'tool':'get_article_content','checks':{'checked':True}})
  with tempfile.TemporaryDirectory() as d:
   l=Ledger(Path(d)/'state.db');l.claim(p,'a1',approve(p,'human',NOW),NOW)
   l.record(p,'a1',{'tool':'edit_article','outcome':'uncertain','data':{}},NOW)
   with self.assertRaises(PolicyError):l.reconcile(p,'a1',{'tool':'edit_article','outcome':'success','external_id':'different','data':{},'reconciliation_evidence':'local/readback.json'},NOW)


 def test_readback_dependency_can_follow_recorded_write(self):
  p=plan('edit_article',{'articleId':'00000000-0000-4000-8000-000000000001','instruction':'Fix factual error'},credits='1')
  p['mode']='draft';p['actions'][0].update(operation_key='edit-1',verification={'tool':'get_article_content','checks':{'checked':True}})
  p['actions'].append({'id':'readback','tool':'get_article_content','arguments':{'articleId':p['actions'][0]['arguments']['articleId']},'depends_on':['a1']})
  with tempfile.TemporaryDirectory() as d:
   l=Ledger(Path(d)/'state.db');a=approve(p,'human',NOW);l.claim(p,'a1',a,NOW)
   l.record(p,'a1',{'tool':'edit_article','outcome':'success','external_id':p['actions'][0]['arguments']['articleId'],'data':{}},NOW)
   self.assertEqual(l.claim(p,'readback',a,NOW)['status'],'claimed')
 def test_unrelated_read_cannot_advance_unverified_write(self):
  p=draft();p['actions'].append({'id':'other','tool':'get_usage','arguments':{},'depends_on':['a1']})
  with tempfile.TemporaryDirectory() as d:
   l=Ledger(Path(d)/'state.db');a=approve(p,'human',NOW);l.claim(p,'a1',a,NOW)
   l.record(p,'a1',{'tool':p['actions'][0]['tool'],'outcome':'success','external_id':'job-1','data':{}},NOW)
   with self.assertRaises(PolicyError):l.claim(p,'other',a,NOW)


 def test_sqlite_connections_are_closed(self):
  import gc, warnings
  gc.collect()
  with tempfile.TemporaryDirectory() as d:
   with warnings.catch_warnings(record=True) as observed:
    warnings.simplefilter('always',ResourceWarning)
    for i in range(3):Ledger(Path(d)/'state.db').status()
    gc.collect()
   self.assertFalse([w for w in observed if issubclass(w.category,ResourceWarning)],str(observed))

if __name__=='__main__':unittest.main()
