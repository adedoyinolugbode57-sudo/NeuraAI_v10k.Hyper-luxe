"""
string_utils.py
Independent string manipulation helpers.
"""

def safe_truncate(text: str, length: int = 100) -> str:
    return text[:length] + "..." if len(text) > length else text

def to_snake_case(text: str) -> str:
    return '_'.join(text.replace('-', ' ').split()).lower()

def capitalize_words(text: str) -> str:
    return ' '.join(word.capitalize() for word in text.split())