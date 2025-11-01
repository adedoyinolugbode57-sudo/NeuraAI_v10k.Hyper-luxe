"""
cache_manager.py
Independent in-memory cache for any object.
"""

import threading
from collections import defaultdict
import time

_cache = {}
_cache_lock = threading.Lock()
_ttl = defaultdict(lambda: 3600)  # default TTL: 1 hour

def set_cache(key: str, value, ttl: int = None):
    with _cache_lock:
        _cache[key] = {"value": value, "ts": time.time()}
        if ttl: _ttl[key] = ttl

def get_cache(key: str, default=None):
    with _cache_lock:
        entry = _cache.get(key)
        if not entry: return default
        if time.time() - entry["ts"] > _ttl.get(key, 3600):
            del _cache[key]
            return default
        return entry["value"]

def clear_cache():
    with _cache_lock:
        _cache.clear()
        CACHE = {}
def set_cache(key: str, value: str) -> str:
    CACHE[key] = value
    return f"Cache set for {key}"