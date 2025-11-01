"""
cache_utils.py
Independent cache utilities for Neuraluxe-AI.
"""
import time

class SimpleCache:
    def __init__(self):
        self.store = {}

    def set(self, key, value, ttl=None):
        expire = time.time() + ttl if ttl else None
        self.store[key] = (value, expire)

    def get(self, key):
        val = self.store.get(key)
        if not val:
            return None
        value, expire = val
        if expire and time.time() > expire:
            del self.store[key]
            return None
        return value