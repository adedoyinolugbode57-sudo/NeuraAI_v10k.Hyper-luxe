"""
chat_limiter.py
Independent utility for Neuraluxe-AI to enforce daily chat limits
and keep a short-term history of recent messages.
"""

import time
from collections import defaultdict, deque

# Limits
DAILY_LIMIT = 200        # Max responses per user per 24h
WAIT_HOURS = 12          # Wait time to reset if exceeded
HISTORY_SIZE = 10        # Number of past messages to recall

# Stores user data: {email: {"count": int, "last_reset": timestamp, "history": deque}}
_user_data = defaultdict(lambda: {"count": 0, "last_reset": time.time(), "history": deque(maxlen=HISTORY_SIZE)})

def _reset_if_needed(user_email: str):
    """Reset the user's count if 24 hours have passed since last reset."""
    now = time.time()
    user = _user_data[user_email]
    if now - user["last_reset"] > 24*3600:
        user["count"] = 0
        user["last_reset"] = now

def can_chat(user_email: str) -> bool:
    """Check if user can chat within daily limit."""
    _reset_if_needed(user_email)
    return _user_data[user_email]["count"] < DAILY_LIMIT

def record_chat(user_email: str, prompt: str, response: str):
    """Record a user's chat interaction."""
    _reset_if_needed(user_email)
    user = _user_data[user_email]
    user["count"] += 1
    user["history"].append({"prompt": prompt, "response": response, "timestamp": time.time()})

def get_user_history(user_email: str, last_n: int = 5):
    """Return last N chat interactions for the user."""
    _reset_if_needed(user_email)
    user = _user_data[user_email]
    return list(user["history"])[-last_n:]