"""
emoji_counter.py
Count emojis in text.
"""

import re

def count_emojis(text: str) -> int:
    return len(re.findall(r'[\U0001F600-\U0001F64F]', text))