#!/usr/bin/env python3
"""Build a deterministic ZIP from distribution paths, excluding private runtime/cache files."""
from __future__ import annotations
import argparse, hashlib, json, sys, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOP_FILES={'README.md','LICENSE','CHANGELOG.md','CONTRIBUTING.md','SECURITY.md','AGENTS.md',
           '.gitignore','.gitattributes','plugin.json','mcp.json','.mcp.json'}
TOP_DIRS={'skills','scripts','tests','catalog','examples','benchmarks','docs','.github','.claude-plugin','.codex-plugin','.agents','.cursor'}
SKIP_PARTS={'.git','.koala','__pycache__','.venv','venv','dist','node_modules','local-results'}

def distribution_files(root: Path) -> list[Path]:
    result=[]
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if rel.parts[0] not in TOP_DIRS and rel.as_posix() not in TOP_FILES:continue
        if any(x in SKIP_PARTS for x in rel.parts):continue
        if p.name.startswith('.env') or p.name in {'.DS_Store','.koala-install.json'} or p.suffix in {'.pyc','.pyo','.db','.sqlite','.sqlite3','.log'}:continue
        if p.is_symlink():raise ValueError(f'Refusing symlink in release: {rel}')
        if p.is_file():result.append(p)
    return result

def build(root: Path, output: Path) -> dict:
    files=distribution_files(root);output=Path(output)
    if output.resolve().is_relative_to(root.resolve()):raise ValueError('Build outside the repository to avoid recursive or accidental inclusion')
    if output.exists():raise ValueError('Output exists; choose a fresh path or remove the old archive explicitly')
    output.parent.mkdir(parents=True,exist_ok=True)
    prefix='koala-mcp-skills/';rows=[];payload=[]
    for p in files:
        data=p.read_bytes();name=p.relative_to(root).as_posix();rows.append(f'{hashlib.sha256(data).hexdigest()}  {name}')
        payload.append((prefix+name,data))
    payload.append((prefix+'MANIFEST.sha256',('\n'.join(rows)+'\n').encode()))
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(payload):
            info=zipfile.ZipInfo(name,date_time=(2026,10,1,0,0,0));info.create_system=3
            info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    sha=hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix+'.sha256').write_text(sha+'  '+output.name+'\n')
    return {'archive':str(output),'files':len(payload),'bytes':output.stat().st_size,'sha256':sha,
            'notice':'Deterministic package of allowlisted distribution paths. Inspect contents before publication; path filtering is not a comprehensive secret scanner.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    try:
        from validate_repo import validate
        result=validate(ROOT)
        if not result['passed']:raise ValueError('Repository validation failed: '+'; '.join(result['errors']))
        print(json.dumps(build(ROOT,a.output),indent=2))
    except (OSError,ValueError) as exc:
        print(json.dumps({'status':'blocked','error':str(exc)}),file=sys.stderr);raise SystemExit(1)
