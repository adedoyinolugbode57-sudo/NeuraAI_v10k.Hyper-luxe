"""
link_validator.py
Check if URLs are valid (mock).
"""

def is_valid(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")