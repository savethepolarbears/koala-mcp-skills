from __future__ import annotations
import copy, json, sys, tempfile, unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/koala-core/scripts'))
from koala_ops.catalog import catalog, estimate, validate_arguments
from koala_ops.policy import PolicyError, validate_plan, approve, check_approval, digest
from koala_ops.ledger import Ledger
from koala_ops.analytics import periods, compare_metrics, classify_candidate

NOW = datetime(2026, 10, 1, 12, tzinfo=timezone.utc)
def plan(tool='get_usage', args=None, *, mode='read-only', credits='0', words=0):
    return {'version':1,'run_id':'sample-run','budget_group':'account-cycle-1',
      'scope':{'brand_id':None,'domain':'example.com'},
      'limits':{'platform_credits':credits,'writer_words':words,'max_calls':30},
      'mode':mode,'actions':[{'id':'a1','tool':tool,'arguments':args or {},'depends_on':[]}]}
def draft():
    p=plan('create_article_in_koala_writer', {'targetKeyword':'rain garden guide'},mode='draft',words=3000)
    p['actions'][0].update(operation_key='rain-garden-v1',writer_word_reservation=3000,
       verification={'tool':'get_article_content','checks':{'content_present':True}})
    return p

class CatalogTests(unittest.TestCase):
    def test_exact_tool_count(self): self.assertEqual(len(catalog()),62)
    def test_free_tool_count(self): self.assertEqual(sum(t['cost']['kind']=='free' for t in catalog().values()),23)
    def test_fractional_cost(self): self.assertEqual(str(estimate('get_page_html', {'url':'https://example.com'})['credits']),'0.1')
    def test_seed_cost(self): self.assertEqual(estimate('get_related_keywords',{'keywords':['a',' a ','b']})['credits'],2)
    def test_quality_image_cost(self): self.assertEqual(estimate('generate_image',{'prompt':'a tree','quality':'quality'})['credits'],8)
    def test_writer_words_not_credits(self):
        v=estimate('create_article_in_koala_writer',{'targetKeyword':'garden'},2000)
        self.assertEqual(v['credits'],0); self.assertEqual(v['words'],2000)
    def test_unknown_tool(self):
        with self.assertRaises(PolicyError): validate_arguments('publish_article',{})
    def test_coverage_batch_overflow(self):
        with self.assertRaises(PolicyError): validate_arguments('check_keyword_coverage',{'domain':'example.com','keywords':['x']*31})
    def test_volume_batch_overflow(self):
        with self.assertRaises(PolicyError): validate_arguments('get_keyword_volume',{'keywords':['x']*21})
    def test_unknown_field(self):
        with self.assertRaises(PolicyError): validate_arguments('get_usage',{'brandId':'wrong'})
    def test_missing_page(self):
        with self.assertRaises(PolicyError): validate_arguments('get_gsc_page_performance',{})
    def test_boolean_is_not_integer(self):
        with self.assertRaises(PolicyError): validate_arguments('list_recent_articles',{'limit':True})
    def test_opaque_contract_requires_review(self):
        with self.assertRaises(PolicyError): validate_arguments('amazon_product_details',{'asin':'B000000001'})

class PolicyTests(unittest.TestCase):
    def test_free_read_works(self): self.assertEqual(validate_plan(plan(),NOW)['credits'],'0')
    def test_paid_read_over_budget(self):
        with self.assertRaises(PolicyError): validate_plan(plan('get_domain_authority',{'domain':'example.com'}),NOW)
    def test_paid_read_authorized_budget(self): validate_plan(plan('get_domain_authority',{'domain':'example.com'},credits='1'),NOW)
    def test_generation_read_only_blocked(self):
        p=draft();p['mode']='read-only'
        with self.assertRaises(PolicyError): validate_plan(p,NOW)
    def test_unreserved_words_blocked(self):
        p=draft();p['actions'][0]['writer_word_reservation']=0
        with self.assertRaises(PolicyError): validate_plan(p,NOW)
    def test_words_ceiling(self):
        p=draft();p['limits']['writer_words']=2000
        with self.assertRaises(PolicyError): validate_plan(p,NOW)
    def test_cross_brand_blocked(self):
        p=plan('get_brand_profile',{'brandId':'brand-b'});p['scope']['brand_id']='brand-a'
        with self.assertRaises(PolicyError): validate_plan(p,NOW)
    def test_implicit_brand_blocked(self):
        with self.assertRaises(PolicyError): validate_plan(plan('get_brand_profile'),NOW)
    def test_brand_explicit_allowed(self):
        p=plan('get_brand_profile',{'brandId':'brand-a'});p['scope']['brand_id']='brand-a';validate_plan(p,NOW)
    def test_attached_creation_requires_connected_write_mode(self):
        p=draft();p['scope']['brand_id']='brand-a';p['actions'][0]['arguments']['brandId']='brand-a'
        with self.assertRaises(PolicyError):validate_plan(p,NOW)
    def test_schedule_is_not_a_draft_list(self):
        p=plan('schedule_articles',{'brandId':'b','tasks':[{'title':'x','keyword':'x','rationale':'x','scheduledDate':'2026-10-08'}]},mode='draft',words=3000)
        p['scope']['brand_id']='b';p['actions'][0].update(operation_key='x',writer_word_reservation=3000)
        with self.assertRaises(PolicyError): validate_plan(p,NOW)
    def test_private_url_blocked(self):
        for url in ['http://127.0.0.1/a','http://169.254.169.254','https://localhost/a','file:///etc/passwd','https://user:password@example.com']:
            with self.subTest(url=url), self.assertRaises(PolicyError):validate_plan(plan('get_page_content',{'url':url},credits='1'),NOW)
    def test_signed_url_blocked(self):
        with self.assertRaises(PolicyError): validate_plan(plan('get_page_content',{'url':'https://example.com/x?token=secret'},credits='1'),NOW)
    def test_gsc_url_scope(self):
        p=plan('get_gsc_indexing_status',{'brandId':'b','urls':['https://example.com.evil.org/x']});p['scope']['brand_id']='b'
        with self.assertRaises(PolicyError):validate_plan(p,NOW)
    def test_gsc_country_three_letters(self):
        p=plan('get_gsc_search_performance',{'brandId':'b','country':'us'});p['scope']['brand_id']='b'
        with self.assertRaises(PolicyError):validate_plan(p,NOW)
    def test_gsc_date_pair(self):
        p=plan('get_gsc_search_performance',{'brandId':'b','startDate':'2026-09-01'});p['scope']['brand_id']='b'
        with self.assertRaises(PolicyError):validate_plan(p,NOW)
    def test_invalid_budget_values(self):
        for val in ['NaN','Infinity','-1',True]:
            p=plan();p['limits']['platform_credits']=val
            with self.subTest(val=val),self.assertRaises(PolicyError):validate_plan(p,NOW)
    def test_dependency_cycle_blocked(self):
        p=plan();p['actions'][0]['depends_on']=['a1']
        with self.assertRaises(PolicyError):validate_plan(p,NOW)
    def test_duplicate_action_ids(self):
        p=plan();p['actions']*=2
        with self.assertRaises(PolicyError):validate_plan(p,NOW)
    def test_unknown_mode(self):
        p=plan();p['mode']='unlimited'
        with self.assertRaises(PolicyError):validate_plan(p,NOW)
    def test_approval_hash_binding(self):
        p=draft();a=approve(p,'human',NOW,30);p['actions'][0]['arguments']['targetKeyword']='changed'
        with self.assertRaises(PolicyError):check_approval(p,a,NOW)
    def test_approval_expiry(self):
        p=draft();a=approve(p,'human',NOW,1)
        with self.assertRaises(PolicyError):check_approval(p,a,NOW+timedelta(minutes=2))
    def test_write_requires_approval(self):
        with self.assertRaises(PolicyError):check_approval(draft(),None,NOW)
    def test_read_no_approval(self):check_approval(plan(),None,NOW)
    def test_digest_order_independent(self):self.assertEqual(digest({'a':1,'b':2}),digest({'b':2,'a':1}))

class LedgerTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.db=Path(self.tmp.name)/'state.db'
    def tearDown(self):self.tmp.cleanup()
    def test_duplicate_claim_blocked(self):
        l=Ledger(self.db);p=plan();l.claim(p,'a1',None,NOW)
        with self.assertRaises(PolicyError):l.claim(p,'a1',None,NOW)
    def test_budget_shared_across_runs(self):
        l=Ledger(self.db);p=plan('get_domain_authority',{'domain':'example.com'},credits='1');l.claim(p,'a1',None,NOW);p['run_id']='other'
        with self.assertRaises(PolicyError):l.claim(p,'a1',None,NOW)
    def test_budget_group_limit_cannot_silently_increase(self):
        l=Ledger(self.db);p=plan();l.claim(p,'a1',None,NOW);p['run_id']='other';p['limits']['platform_credits']='10'
        with self.assertRaises(PolicyError):l.claim(p,'a1',None,NOW)
    def test_concurrent_claims_single_winner(self):
        l=Ledger(self.db);p=plan()
        def attempt(_):
            try:Ledger(self.db).claim(p,'a1',None,NOW);return True
            except PolicyError:return False
        with ThreadPoolExecutor(max_workers=4) as ex:self.assertEqual(sum(ex.map(attempt,range(4))),1)
    def test_uncertain_not_retryable(self):
        l=Ledger(self.db);p=draft();a=approve(p,'human',NOW,30);l.claim(p,'a1',a,NOW)
        l.record(p,'a1',{'tool':p['actions'][0]['tool'],'outcome':'uncertain','data':{}},NOW)
        with self.assertRaises(PolicyError):l.claim(p,'a1',a,NOW)
    def test_write_operation_key_survives_run_change(self):
        l=Ledger(self.db);p=draft();a=approve(p,'human',NOW,30);l.claim(p,'a1',a,NOW);p['run_id']='new';p['budget_group']='new-cycle'
        with self.assertRaises(PolicyError):l.claim(p,'a1',approve(p,'human',NOW,30),NOW)
    def test_receipt_wrong_tool_blocked(self):
        l=Ledger(self.db);p=plan();l.claim(p,'a1',None,NOW)
        with self.assertRaises(PolicyError):l.record(p,'a1',{'tool':'edit_article','outcome':'success','data':{}},NOW)
    def test_unclaimed_cannot_record(self):
        with self.assertRaises(PolicyError):Ledger(self.db).record(plan(),'a1',{'tool':'get_usage','outcome':'success','data':{}},NOW)
    def test_write_readback_required(self):
        l=Ledger(self.db);p=draft();l.claim(p,'a1',approve(p,'human',NOW,30),NOW)
        l.record(p,'a1',{'tool':p['actions'][0]['tool'],'outcome':'success','external_id':'job-1','data':{}},NOW)
        with self.assertRaises(PolicyError):l.verify(p,'a1',{'tool':'get_article_content','external_id':'job-2','observed':{'content_present':True}},NOW)
        result=l.verify(p,'a1',{'tool':'get_article_content','external_id':'job-1','observed':{'content_present':True}},NOW)
        self.assertEqual(result['status'],'verified')
    def test_dependency_requires_receipt(self):
        l=Ledger(self.db);p=plan();p['actions'].append({'id':'a2','tool':'get_usage','arguments':{},'depends_on':['a1']})
        with self.assertRaises(PolicyError):l.claim(p,'a2',None,NOW)
        l.claim(p,'a1',None,NOW);l.record(p,'a1',{'tool':'get_usage','outcome':'success','data':{'credits':10}},NOW);l.claim(p,'a2',None,NOW)

class AnalyticsTests(unittest.TestCase):
    def test_equal_inclusive_periods(self):
        v=periods('2026-09-28',28)
        self.assertEqual(v['current'],{'start':'2026-09-01','end':'2026-09-28'});self.assertEqual(v['previous'],{'start':'2026-08-04','end':'2026-08-31'})
    def test_leap_day_periods(self):self.assertEqual(periods('2024-03-01',2)['current']['start'],'2024-02-29')
    def test_zero_baseline_not_infinite(self):self.assertIsNone(compare_metrics({'clicks':0,'impressions':10},{'clicks':5,'impressions':20})['clicks_pct'])
    def test_missing_not_zero(self):self.assertIsNone(compare_metrics({}, {'clicks':5})['clicks_delta'])
    def test_ctr_derived(self):self.assertEqual(compare_metrics({'clicks':5,'impressions':100},{'clicks':20,'impressions':200})['ctr_current'],0.1)
    def test_exact_planned_duplicate_skipped(self):self.assertEqual(classify_candidate(' Rain Garden ',['rain garden'],None,[])['decision'],'skip')
    def test_unknown_coverage_investigate(self):self.assertEqual(classify_candidate('rain garden',[],None,[])['decision'],'investigate')
    def test_covered_requires_inspection(self):self.assertEqual(classify_candidate('rain garden',[],'covered',['https://example.com/gardens'])['decision'],'inspect-existing')
    def test_uncovered_not_proof(self):self.assertEqual(classify_candidate('rain garden',[],'uncovered',[])['decision'],'candidate-not-approved')

if __name__=='__main__':unittest.main()
