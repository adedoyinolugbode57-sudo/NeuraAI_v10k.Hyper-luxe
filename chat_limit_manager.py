"""
chat_limit_manager.py
Independent daily-limited chatbot manager for Neuraluxe-AI.

Features:
- Limit each user to N responses per 24 hours
- Reset limit after 12 hours
- Recall previous chat context
- Fully independent, no external dependencies
"""

import time
import threading
from collections import defaultdict, deque

# ------------------------
# Configuration
# ------------------------
MAX_RESPONSES_PER_DAY = 200
RESET_HOURS = 12

# ------------------------
# Data storage (in-memory)
# ------------------------
# Each user_email maps to a dict: {"count": int, "last_reset": timestamp, "history": deque}
_user_chat_data = defaultdict(lambda: {"count": 0, "last_reset": 0, "history": deque(maxlen=MAX_RESPONSES_PER_DAY)})

_lock = threading.Lock()

# ------------------------
# Utilities
# ------------------------
def _current_ts() -> int:
    return int(time.time())

def _reset_if_needed(user_email: str):
    data = _user_chat_data[user_email]
    now = _current_ts()
    if now - data["last_reset"] > RESET_HOURS * 3600:
        data["count"] = 0
        data["last_reset"] = now
        data["history"].clear()

# ------------------------
# Public API
# ------------------------
def can_send_response(user_email: str) -> bool:
    """Check if user can get a new response."""
    with _lock:
        _reset_if_needed(user_email)
        return _user_chat_data[user_email]["count"] < MAX_RESPONSES_PER_DAY

def record_response(user_email: str, prompt: str, response: str):
    """Record that a user has received a response."""
    with _lock:
        _reset_if_needed(user_email)
        data = _user_chat_data[user_email]
        if data["count"] < MAX_RESPONSES_PER_DAY:
            data["count"] += 1
            data["history"].append({"prompt": prompt, "response": response})
            return True
        return False

def get_user_history(user_email: str, last_n: int = 10):
    """Get the last N chats for the user."""
    with _lock:
        _reset_if_needed(user_email)
        return list(_user_chat_data[user_email]["history"])[-last_n:]

def responses_left(user_email: str) -> int:
    """Return how many responses are left today for the user."""
    with _lock:
        _reset_if_needed(user_email)
        return max(0, MAX_RESPONSES_PER_DAY - _user_chat_data[user_email]["count"])

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    user = "test@example.com"
    for i in range(205):
        if can_send_response(user):
            record_response(user, f"Prompt {i+1}", f"Response {i+1}")
            print(f"Sent response {i+1}")
        else:
            print(f"Daily limit reached at response {i+1}, wait {RESET_HOURS} hours")
            break

    print("History:", get_user_history(user, last_n=5))
    print("Responses left:", responses_left(user))