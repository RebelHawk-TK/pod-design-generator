"""Simple JSON file cache with TTL."""

from __future__ import annotations

import json
import time
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / "dashboard_cache"


def _cache_path(key: str) -> Path:
    safe_key = key.replace("/", "_").replace("?", "_")
    return CACHE_DIR / f"{safe_key}.json"


def get_cached(key: str, ttl: int) -> dict | list | None:
    """Return cached data if fresh, else None. ttl in seconds."""
    path = _cache_path(key)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    if time.time() - data.get("_ts", 0) > ttl:
        return None
    return data.get("payload")


def set_cached(key: str, payload) -> None:
    """Write data to cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _cache_path(key)
    path.write_text(json.dumps({"_ts": time.time(), "payload": payload}))


def bust_cache() -> int:
    """Delete all cache files. Returns count deleted."""
    if not CACHE_DIR.exists():
        return 0
    count = 0
    for f in CACHE_DIR.glob("*.json"):
        f.unlink()
        count += 1
    return count
