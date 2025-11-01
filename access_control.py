"""
access_control.py
Manage admin, premium, or guest permissions.
"""

PERMISSIONS = {
    "admin": ["all"],
    "premium": ["chat", "voice", "theme"],
    "guest": ["chat"]
}

def has_permission(user_role: str, action: str) -> bool:
    return action in PERMISSIONS.get(user_role, [])