"""
quote_inspiration.py
Return general inspirational quotes.
"""

import random

QUOTES = [
    "The best way to predict the future is to invent it.",
    "Do what you can with what you have, where you are.",
    "Believe you can and you're halfway there.",
    "Dream big and dare to fail.",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Sometimes later becomes never. Do it now.",
    "Great things never come from comfort zones.",
    "Success doesn't just find you. You have to go out and get it.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Dream it. Wish it. Do it.",
    "Don't stop when you're tired. Stop when you're done.",
    "Little things make big days.",
    "It's going to be hard, but hard does not mean impossible.",
    "Don't wait for opportunity. Create it."
]

def get_quote() -> str:
    return random.choice(QUOTES)