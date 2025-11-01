"""
quote_motivation.py
Return motivational and inspiring quotes.
"""

import random

QUOTES = [
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Don’t watch the clock; do what it does. Keep going.",
    "Success doesn’t just find you. You have to go out and get it.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Little things make big days.",
    "Don’t stop when you’re tired. Stop when you’re done.",
    "It’s going to be hard, but hard does not mean impossible.",
    "Push yourself, because no one else is going to do it for you.",
    "Sometimes we’re tested not to show our weaknesses, but to discover our strengths.",
    "The key to success is to focus on goals, not obstacles.",
    "Don’t wait for opportunity. Create it.",
    "Success is not in what you have, but who you are.",
    "Your limitation—it’s only your imagination.",
    "Do something today that your future self will thank you for."
]

def get_quote() -> str:
    return random.choice(QUOTES)