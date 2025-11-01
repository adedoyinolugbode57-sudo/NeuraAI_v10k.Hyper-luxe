"""
mock_news.py
Return random news headlines (mock).
"""

import random

HEADLINES = [
    "AI changes the world!",
    "Stock market hits record highs.",
    "New species discovered in Amazon rainforest."
]

def get_headline() -> str:
    return random.choice(HEADLINES)