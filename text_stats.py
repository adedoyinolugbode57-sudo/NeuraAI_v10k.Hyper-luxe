"""
text_stats.py
Analyze text statistics.
"""

def word_count(text: str) -> int:
    return len(text.split())

def char_count(text: str) -> int:
    return len(text)