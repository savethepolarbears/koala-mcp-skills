#!/usr/bin/env python3
"""Repository shortcut to the self-contained koala-core CLI."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/koala-core/scripts'))
from koala_ops.cli import main
if __name__ == '__main__':raise SystemExit(main())
