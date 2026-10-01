#!/usr/bin/env python3
"""Preview-first global skills installer. No network, hooks, credentials or MCP-config edits."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, sys, tempfile
from pathlib import Path

VERSION='0.1.0'
OWNER='koala-mcp-skills'
MANIFEST='.koala-install.json'
TARGETS={'codex':'.agents/skills','claude-code':'.claude/skills',
         'gemini-cli':'.gemini/skills','antigravity':'.gemini/config/skills',
         'antigravity-app':'.gemini/antigravity/skills','codex-store':'.codex/skills',
         'cursor':'.cursor/skills'}
HUBS=['codex','antigravity','antigravity-app','claude-code','codex-store']
STARTER=['koala-core','koala-connect','koala-budget','koala-opportunity-research',
         'koala-content-decay','koala-content-plan','koala-editorial-qa','koala-queue-operations']
RESEARCH=STARTER+['koala-brand-audit','koala-competitor-analysis','koala-onpage-audit',
                 'koala-internal-links','koala-ai-visibility','koala-link-prospecting',
                 'koala-prospect-audit','koala-affiliate-research','koala-seasonal-content',
                 'koala-performance-review','koala-schema-watch']

class InstallError(ValueError):pass

SYSTEM_SYMLINKS={Path('/var'),Path('/tmp'),Path('/etc')}

def no_symlinks(path: Path) -> None:
    for part in [path,*path.parents]:
        if part in SYSTEM_SYMLINKS:continue
        if part.is_symlink():raise InstallError(f'Refusing symlink path: {part}')

def ignored(path: Path) -> bool:
    return '__pycache__' in path.parts or path.suffix in {'.pyc','.pyo'} or path.name=='.DS_Store'

def fingerprints(root: Path) -> dict[str,str]:
    """Include all non-generated files, reject symlinks and special filesystem entries."""
    if root.is_symlink() or not root.is_dir():raise InstallError(f'Not a regular skill directory: {root}')
    result={}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():raise InstallError(f'Refusing symlink inside skill: {path}')
        if ignored(path.relative_to(root)):continue
        if path.is_file():
            if path.name==MANIFEST:continue
            result[path.relative_to(root).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
        elif not path.is_dir():raise InstallError(f'Refusing special filesystem entry: {path}')
    if 'SKILL.md' not in result:raise InstallError(f'Missing SKILL.md in {root}')
    return result

def owned_clean(dest: Path, name: str) -> dict:
    marker=dest/MANIFEST
    if not marker.is_file() or marker.is_symlink():raise InstallError(f'Foreign skill directory; will not overwrite: {dest}')
    try:data=json.loads(marker.read_text())
    except (OSError,ValueError) as exc:raise InstallError(f'Invalid ownership manifest: {dest}') from exc
    if not isinstance(data,dict) or data.get('owner')!=OWNER or data.get('skill')!=name or not isinstance(data.get('files'),dict):
        raise InstallError(f'Invalid ownership manifest: {dest}')
    if fingerprints(dest)!=data['files']:
        raise InstallError(f'Local modifications or extra files detected; preserve/move them before replacement: {dest}')
    return data

def install(repo: Path, home: Path, agents: list[str], *, profile: str='starter',
            skills: list[str] | None=None, apply: bool=False, uninstall: bool=False) -> dict:
    repo=Path(repo).absolute();home=Path(home).absolute();no_symlinks(home)
    if not agents:raise InstallError('Select at least one --agent')
    if any(a not in TARGETS for a in agents):raise InstallError('Unknown agent')
    if profile not in {'starter','research','all'}:raise InstallError('Unknown profile')
    available={p.name:p for p in (repo/'skills').iterdir() if p.is_dir()}
    selected=set(skills if skills else (list(available) if profile=='all' else RESEARCH if profile=='research' else STARTER))
    if not uninstall:selected.add('koala-core')
    if not selected or not selected<=available.keys():raise InstallError('Unknown skill; names must match a bundled skill exactly')
    jobs=[]
    for agent in dict.fromkeys(agents):
        base=home/TARGETS[agent];no_symlinks(base)
        for name in sorted(selected):
            source=available[name];no_symlinks(source)
            hashes=fingerprints(source);dest=base/name;no_symlinks(dest)
            exists=dest.exists();old=owned_clean(dest,name) if exists else None
            op=('remove' if exists else 'absent') if uninstall else ('unchanged' if old and old['files']==hashes else 'replace' if exists else 'install')
            jobs.append({'agent':agent,'skill':name,'operation':op,'destination':str(dest),
                         'source':str(source),'hashes':hashes})
    # Entire selection is checked before the first write. Per-directory swaps are atomic;
    # all completed swaps are rolled back if a later swap raises. No protection against
    # an adversarial local process concurrently modifying the installation directories.
    committed=[];staging=[]
    try:
        if apply:
            for job in jobs:
                if job['operation'] in {'unchanged','absent'}:continue
                dest=Path(job['destination']);dest.parent.mkdir(parents=True,exist_ok=True)
                no_symlinks(dest)
                if dest.exists():owned_clean(dest,job['skill'])
                stage=Path(tempfile.mkdtemp(prefix='.koala-stage-',dir=dest.parent));staging.append(stage)
                new=stage/'new';backup=stage/'previous'
                if not uninstall:
                    shutil.copytree(job['source'],new,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.pyo','.DS_Store',MANIFEST))
                    if fingerprints(new)!=job['hashes']:raise InstallError('Source changed while copying; retry after stopping concurrent edits')
                    (new/MANIFEST).write_text(json.dumps({'owner':OWNER,'version':VERSION,'skill':job['skill'],'files':job['hashes']},indent=2)+'\n')
                had_old=dest.exists()
                if had_old:os.replace(dest,backup)
                try:
                    if not uninstall:os.replace(new,dest)
                except BaseException:
                    if had_old:os.replace(backup,dest)
                    raise
                committed.append((dest,backup,had_old))
    except BaseException:
        for dest,backup,had_old in reversed(committed):
            if dest.exists():shutil.rmtree(dest)
            if had_old:os.replace(backup,dest)
        raise
    finally:
        for stage in staging:
            if stage.exists():shutil.rmtree(stage)
    return {'applied':apply,'uninstall':uninstall,'version':VERSION,
            'actions':[{k:v for k,v in j.items() if k not in {'source','hashes'}} for j in jobs],
            'notice':'Skills only. No network calls, host hooks or MCP configuration changes. Restart the host/session to rediscover skills.'}

def main(argv: list[str] | None=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--agent',action='append',choices=TARGETS,help='Target host agent; repeat as needed')
    p.add_argument('--all-hubs',action='store_true',help='Install to all 5 canonical hubs')
    p.add_argument('--profile',choices=['starter','research','all'],default='starter')
    p.add_argument('--skill',action='append',help='Exact skill name; repeat as needed. Install also includes koala-core.')
    p.add_argument('--home',type=Path,default=Path.home(),help='Alternate home for isolated testing')
    p.add_argument('--apply',action='store_true',help='Perform the previewed file copies/removals')
    p.add_argument('--uninstall',action='store_true',help='Remove only clean installer-owned skills selected above')
    a=p.parse_args(argv)
    agents=list(dict.fromkeys((a.agent or [])+(HUBS if a.all_hubs else [])))
    if not agents:
        p.error('Select at least one --agent or pass --all-hubs')
    try:
        print(json.dumps(install(Path(__file__).resolve().parents[1],a.home,agents,profile=a.profile,skills=a.skill,apply=a.apply,uninstall=a.uninstall),indent=2));return 0
    except (InstallError,OSError) as exc:
        print(json.dumps({'status':'blocked','error':str(exc)}),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
