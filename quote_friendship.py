"""
quote_friendship.py
Return quotes about friendship and relationships.
"""

import random

QUOTES = [
    "A friend is someone who knows all about you and still loves you.",
    "Friendship is the only cement that will ever hold the world together.",
    "A real friend is one who walks in when the rest of the world walks out.",
    "Friends are the siblings God never gave us.",
    "True friendship comes when the silence between two people is comfortable.",
    "A single rose can be my garden... a single friend, my world.",
    "Friendship improves happiness and abates misery.",
    "There are no strangers here; only friends you haven’t yet met.",
    "A friend is one that knows you as you are, understands where you have been, accepts what you have become, and still, gently allows you to grow.",
    "Good friends are like stars. You don’t always see them, but you know they’re always there.",
    "Friendship is born at that moment when one person says to another, 'What! You too? I thought I was the only one.'",
    "Walking with a friend in the dark is better than walking alone in the light.",
    "Friendship is the golden thread that ties the heart of all the world.",
    "Life is partly what we make it, and partly what it is made by the friends we choose.",
    "Lots of people want to ride with you in the limo, but what you want is someone who will take the bus with you when the limo breaks down."
]

def get_quote() -> str:
    return random.choice(QUOTES)