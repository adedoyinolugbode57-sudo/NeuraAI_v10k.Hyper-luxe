"""
uuid_helper.py
Independent UUID and ID generation utilities.
"""

import uuid

def make_id(prefix: str = "id") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def make_short_uuid() -> str:
    return uuid.uuid4().hex[:8]