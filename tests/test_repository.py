"""Distribution checks exercise the same public scripts a local user runs."""
import importlib.util, json, subprocess, sys, tempfile, unittest, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py')
 obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj

class RepositoryTests(unittest.TestCase):
 def test_structural_validation(self):
  result=load('validate_repo').validate(ROOT)
  self.assertTrue(result['passed'],result['errors'])
  self.assertEqual(result['non_core_tool_coverage'],62)
 def test_policy_cases(self):
  result=load('evaluate').evaluate(ROOT)
  self.assertTrue(result['passed'],result)
  self.assertGreaterEqual(result['cases'],12)
  self.assertFalse(result['llm_evaluation'])
 def test_example_plans_validate(self):
  for name in ['read-only-plan.json','standalone-draft-plan.json']:
   run=subprocess.run([sys.executable,str(ROOT/'scripts/koala.py'),'check',str(ROOT/'examples'/name)],capture_output=True,text=True)
   self.assertEqual(run.returncode,0,run.stderr)
 def test_archive_is_reproducible_and_has_no_cache(self):
  package=load('package')
  with tempfile.TemporaryDirectory() as d:
   first=Path(d)/'a.zip';second=Path(d)/'b.zip'
   package.build(ROOT,first);package.build(ROOT,second)
   self.assertEqual(first.read_bytes(),second.read_bytes())
   with zipfile.ZipFile(first) as z:
    self.assertIsNone(z.testzip())
    self.assertIn('koala-mcp-skills/MANIFEST.sha256',z.namelist())
    self.assertIn('koala-mcp-skills/skills/koala-core/SKILL.md',z.namelist())
    self.assertTrue(all('__pycache__' not in x and not x.endswith('.pyc') for x in z.namelist()))
 def test_packager_refuses_symlinks(self):
  package=load('package')
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/'repo';root.mkdir();(root/'README.md').symlink_to(ROOT/'README.md')
   with self.assertRaises(ValueError):package.distribution_files(root)
 def test_source_has_no_network_transport(self):
  core=ROOT/'skills/koala-core/scripts/koala_ops'
  for path in core.glob('*.py'):
   text=path.read_text()
   self.assertNotIn('import requests',text);self.assertNotIn('import httpx',text)
   self.assertNotIn('urlopen(',text)

if __name__=='__main__':unittest.main()
