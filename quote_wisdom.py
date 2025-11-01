"""
quote_wisdom.py
Return quotes focused on wisdom and knowledge.
"""

import random

QUOTES = [
    "The only true wisdom is in knowing you know nothing.",
    "Knowing yourself is the beginning of all wisdom.",
    "The journey of a thousand miles begins with one step.",
    "Wisdom is not a product of schooling but of the lifelong attempt to acquire it.",
    "Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment.",
    "An investment in knowledge pays the best interest.",
    "Patience is the companion of wisdom.",
    "The invariable mark of wisdom is to see the miraculous in the common.",
    "It is the mark of an educated mind to be able to entertain a thought without accepting it.",
    "Turn your face to the sun and the shadows fall behind you.",
    "Wisdom begins in wonder.",
    "The mind is everything. What you think you become.",
    "Knowing others is intelligence; knowing yourself is true wisdom.",
    "Do not go where the path may lead, go instead where there is no path and leave a trail.",
    "The fool doth think he is wise, but the wise man knows himself to be a fool."
]

def get_quote() -> str:
    return random.choice(QUOTES)