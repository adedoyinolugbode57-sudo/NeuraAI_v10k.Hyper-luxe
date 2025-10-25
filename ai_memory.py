"""
ai_memory.py
NeuraAI Hyperluxe – Persistent conversation memory system.
"""

import json, os, time

MEMORY_FILE = "memory_store.json"
MAX_MEMORY = 15  # last 15 messages

def _load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory[-MAX_MEMORY:], f, indent=2)

def remember(role, text):
    memory = _load_memory()
    memory.append({
        "role": role,
        "text": text,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    _save_memory(memory)

def recall():
    return _load_memory()

def clear_memory():
    _save_memory([])