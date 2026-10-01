"""Small shared primitives: exact arithmetic, canonical JSON, and safe local I/O."""
from __future__ import annotations
import hashlib, json, os, tempfile
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

class PolicyError(ValueError):
    """A plan or state transition is not permitted by the local policy."""

def canonical(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise PolicyError('Input must be finite, serializable JSON') from exc

def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()

def amount(value: Any) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise PolicyError('Credit amount must be a nonnegative finite decimal')
    try: result = Decimal(str(value))
    except InvalidOperation as exc: raise PolicyError('Invalid decimal credit amount') from exc
    if not result.is_finite() or result < 0:
        raise PolicyError('Credit amount must be a nonnegative finite decimal')
    return result

def natural(value: Any, label: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise PolicyError(f'{label} must be an integer >= {minimum}')
    return value

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def timestamp(value: str) -> datetime:
    try: result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, AttributeError) as exc: raise PolicyError('Invalid timestamp') from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise PolicyError('Timestamps must include a timezone offset')
    return result.astimezone(timezone.utc)

def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result: raise PolicyError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result

def load_json(path: str | Path) -> Any:
    p = Path(path)
    if p.stat().st_size > 20_000_000: raise PolicyError('JSON file exceeds 20 MB local input limit')
    try:
        return json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(PolicyError('Nonfinite JSON number')))
    except (json.JSONDecodeError, UnicodeError) as exc: raise PolicyError(f'Invalid JSON: {p}') from exc

def write_json(path: str | Path, value: Any, *, overwrite: bool = False) -> None:
    """Write a private file atomically; do not overwrite approval/evidence by accident."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists() and not overwrite: raise PolicyError(f'Refusing to overwrite {p}')
    encoded = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
    fd, name = tempfile.mkstemp(prefix='.koala-', dir=p.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(encoded); stream.flush(); os.fsync(stream.fileno())
        os.chmod(name, 0o600)
        if overwrite:
            os.replace(name, p)
        else:
            # Link is exclusive: a concurrent writer cannot win between exists() and write.
            os.link(name, p); os.unlink(name)
    finally:
        if os.path.exists(name): os.unlink(name)
