"""
quote_love.py
Return quotes about love and romance.
"""

import random

QUOTES = [
    "Love all, trust a few, do wrong to none.",
    "The best thing to hold onto in life is each other.",
    "We accept the love we think we deserve.",
    "Being deeply loved by someone gives you strength, while loving someone deeply gives you courage.",
    "Love is composed of a single soul inhabiting two bodies.",
    "Where there is love there is life.",
    "Love doesn’t make the world go round. Love is what makes the ride worthwhile.",
    "Love is when the other person's happiness is more important than your own.",
    "To love and be loved is to feel the sun from both sides.",
    "Love is that condition in which the happiness of another person is essential to your own.",
    "The giving of love is an education in itself.",
    "You yourself, as much as anybody in the entire universe, deserve your love and affection.",
    "Love recognizes no barriers. It jumps hurdles, leaps fences, penetrates walls to arrive at its destination full of hope.",
    "We are most alive when we’re in love.",
    "True love stories never have endings."
]

def get_quote() -> str:
    return random.choice(QUOTES)