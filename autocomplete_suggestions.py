"""
autocomplete_suggestions.py
Suggest next words or phrases.
"""

SUGGESTIONS = {
    "hello": ["there", "world", "friend"],
    "how": ["are", "is", "do"]
}

def suggest(prefix: str):
    return SUGGESTIONS.get(prefix.lower(), [])