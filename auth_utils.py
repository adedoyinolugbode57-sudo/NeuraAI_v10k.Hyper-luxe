"""
auth_utils.py
Independent authentication utilities for Neuraluxe-AI.
"""
def check_admin(token: str, expected: str):
    return token == expected

def require_admin(fn):
    def wrapper(token, *args, **kwargs):
        if not check_admin(token, "neura-admin-2025"):
            raise PermissionError("Invalid admin token")
        return fn(*args, **kwargs)
    return wrapper