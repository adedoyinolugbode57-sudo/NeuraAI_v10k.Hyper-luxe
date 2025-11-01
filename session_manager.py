"""
session_manager.py
Handle user sessions.
"""

SESSIONS = {}  # user_id -> session data

def start_session(user_id: str):
    SESSIONS[user_id] = {"active": True}

def end_session(user_id: str):
    SESSIONS.pop(user_id, None)

def is_active(user_id: str) -> bool:
    return SESSIONS.get(user_id, {}).get("active", False)