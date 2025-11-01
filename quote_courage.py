"""
quote_courage.py
Return quotes focused on bravery and overcoming challenges.
"""

import random

QUOTES = [
    "Courage is not the absence of fear, but the triumph over it.",
    "It takes courage to grow up and become who you really are.",
    "Do one thing every day that scares you.",
    "Courage is resistance to fear, mastery of fear—not absence of fear.",
    "You gain strength, courage, and confidence by every experience in which you really stop to look fear in the face.",
    "The only thing we have to fear is fear itself.",
    "Courage doesn’t mean you don’t get afraid. Courage means you don’t let fear stop you.",
    "Be brave enough to live life creatively.",
    "Everything you’ve ever wanted is on the other side of fear.",
    "Courage is the most important of all the virtues because, without courage, you can't practice any other virtue consistently.",
    "Life shrinks or expands in proportion to one's courage.",
    "Fortune favors the brave.",
    "Courage is grace under pressure.",
    "In the end, we only regret the chances we didn’t take.",
    "Be fearless in the pursuit of what sets your soul on fire."
]

def get_quote() -> str:
    return random.choice(QUOTES)