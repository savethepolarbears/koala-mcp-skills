"""Public installer behavior tested against isolated temporary homes only."""
import importlib.util, json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('koala_installer',ROOT/'scripts/install.py')
installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)

class InstallerTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.home=Path(self.temp.name)/'home';self.home.mkdir()
 def tearDown(self):self.temp.cleanup()
 def run_install(self,**kw):
  return installer.install(ROOT,self.home,['codex'],skills=['koala-budget'],**kw)
 def test_preview_creates_nothing(self):
  result=self.run_install();self.assertFalse(result['applied']);self.assertEqual(list(self.home.iterdir()),[])
 def test_selected_installs_core_and_workflow(self):
  result=self.run_install(apply=True)
  self.assertEqual({x['skill'] for x in result['actions']},{'koala-core','koala-budget'})
  self.assertTrue((self.home/'.agents/skills/koala-core/scripts/koala.py').exists())
 def test_repeated_install_is_noop(self):
  self.run_install(apply=True);r=self.run_install(apply=True)
  self.assertTrue(all(x['operation']=='unchanged' for x in r['actions']))
 def test_foreign_directory_blocked_and_nothing_else_copied(self):
  dest=self.home/'.agents/skills/koala-budget';dest.mkdir(parents=True);(dest/'mine.txt').write_text('mine')
  with self.assertRaises(installer.InstallError):self.run_install(apply=True)
  self.assertFalse((self.home/'.agents/skills/koala-core').exists())
 def test_modified_owned_file_blocked(self):
  self.run_install(apply=True);(self.home/'.agents/skills/koala-budget/SKILL.md').write_text('custom')
  with self.assertRaises(installer.InstallError):self.run_install(apply=True)
 def test_untracked_file_blocks_upgrade(self):
  self.run_install(apply=True);(self.home/'.agents/skills/koala-budget/custom.txt').write_text('custom')
  with self.assertRaises(installer.InstallError):self.run_install(apply=True)
 def test_clean_uninstall_keeps_unselected_core(self):
  self.run_install(apply=True);self.run_install(apply=True,uninstall=True)
  self.assertFalse((self.home/'.agents/skills/koala-budget').exists())
  self.assertTrue((self.home/'.agents/skills/koala-core').exists())
 def test_modified_uninstall_blocked(self):
  self.run_install(apply=True);(self.home/'.agents/skills/koala-budget/SKILL.md').write_text('custom')
  with self.assertRaises(installer.InstallError):self.run_install(apply=True,uninstall=True)
 def test_preview_uninstall_does_not_delete(self):
  self.run_install(apply=True);self.run_install(uninstall=True)
  self.assertTrue((self.home/'.agents/skills/koala-budget').exists())
 def test_invalid_skill_cannot_traverse(self):
  with self.assertRaises(installer.InstallError):installer.install(ROOT,self.home,['codex'],skills=['../../outside'],apply=True)
 def test_invalid_agent(self):
  with self.assertRaises(installer.InstallError):installer.install(ROOT,self.home,['unknown'],apply=True)
 def test_symlink_target_blocked(self):
  (self.home/'.agents').symlink_to(Path(self.temp.name),target_is_directory=True)
  with self.assertRaises(installer.InstallError):self.run_install(apply=True)
 def test_source_symlink_blocked(self):
  fake=Path(self.temp.name)/'repo';(fake/'skills').mkdir(parents=True)
  (fake/'skills/koala-core').symlink_to(ROOT/'skills/koala-core',target_is_directory=True)
  with self.assertRaises(installer.InstallError):installer.install(fake,self.home,['codex'],skills=['koala-core'],apply=True)
 def test_corrupt_manifest_blocks(self):
  self.run_install(apply=True);(self.home/'.agents/skills/koala-budget/.koala-install.json').write_text('{}')
  with self.assertRaises(installer.InstallError):self.run_install(apply=True)
 def test_copied_core_runs_without_repository(self):
  self.run_install(apply=True)
  process=subprocess.run([sys.executable,str(self.home/'.agents/skills/koala-core/scripts/koala.py'),'demo'],capture_output=True,text=True,cwd=self.temp.name)
  self.assertEqual(process.returncode,0,process.stderr);self.assertEqual(json.loads(process.stdout)['network_calls'],0)
 def test_full_install_all_destinations(self):
  r=installer.install(ROOT,self.home,list(installer.TARGETS),profile='all',apply=True)
  self.assertEqual(len(r['actions']),26*len(installer.TARGETS))
  self.assertEqual(len(installer.HUBS),5)
 def test_antigravity_current_documented_path(self):
  self.assertEqual(installer.TARGETS['antigravity'],'.gemini/config/skills')
 def test_generated_bytecode_does_not_block_clean_uninstall(self):
  self.run_install(apply=True);cache=self.home/'.agents/skills/koala-budget/__pycache__';cache.mkdir();(cache/'test.pyc').write_bytes(b'cache')
  self.run_install(apply=True,uninstall=True)
 def test_uninstall_missing_is_noop(self):
  r=self.run_install(apply=True,uninstall=True);self.assertEqual(r['actions'][0]['operation'],'absent')

if __name__=='__main__':unittest.main()
