#!/usr/bin/env python3
"""Run the complete offline acceptance suite without installing anything globally."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main() -> int:
    commands=[['-m','unittest','discover','-s','tests','-v'],['scripts/validate_repo.py'],['scripts/evaluate.py']]
    for args in commands:
        print('\n>>> '+sys.executable+' '+' '.join(args),flush=True)
        result=subprocess.run([sys.executable,*args],cwd=ROOT)
        if result.returncode:return result.returncode
    print('\nAll offline checks passed. Live host loading, OAuth and LLM behavior remain separate tests.')
    return 0

if __name__=='__main__':raise SystemExit(main())
