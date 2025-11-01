"""
quote_creativity.py
Return quotes about creativity, imagination, and innovation.
"""

import random

QUOTES = [
    "Creativity is intelligence having fun.",
    "You can’t use up creativity. The more you use, the more you have.",
    "Imagination is more important than knowledge.",
    "Every artist was first an amateur.",
    "Creativity takes courage.",
    "Think left and think right and think low and think high. Oh, the thinks you can think up if only you try!",
    "Logic will get you from A to B. Imagination will take you everywhere.",
    "To live a creative life, we must lose our fear of being wrong.",
    "Curiosity about life in all of its aspects, I think, is still the secret of great creative people.",
    "Do not quench your inspiration and your imagination; do not become the slave of your model.",
    "Creativity is allowing yourself to make mistakes. Art is knowing which ones to keep.",
    "Innovation distinguishes between a leader and a follower.",
    "An essential aspect of creativity is not being afraid to fail.",
    "Originality is the essence of true scholarship.",
    "The chief enemy of creativity is 'good' sense."
]

def get_quote() -> str:
    return random.choice(QUOTES)