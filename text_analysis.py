"""
text_analysis.py
Independent text analysis helpers.
"""

def word_count(text: str) -> int:
    return len(text.split())

def char_count(text: str) -> int:
    return len(text)