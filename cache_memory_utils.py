"""
cache_memory_utils.py
Independent in-memory cache for Neuraluxe-AI.
"""
memory_store = {}

def set_memory(key, value):
    memory_store[key] = value

def get_memory(key, default=None):
    return memory_store.get(key, default)