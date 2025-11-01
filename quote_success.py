"""
quote_success.py
Return quotes about success, achievement, and growth.
"""

import random

QUOTES = [
    "Success usually comes to those who are too busy to be looking for it.",
    "Don’t be afraid to give up the good to go for the great.",
    "I find that the harder I work, the more luck I seem to have.",
    "Success is not how high you have climbed, but how you make a positive difference to the world.",
    "The road to success and the road to failure are almost exactly the same.",
    "Success is walking from failure to failure with no loss of enthusiasm.",
    "The secret of success is to do the common thing uncommonly well.",
    "Opportunities don't happen. You create them.",
    "Don’t let the fear of losing be greater than the excitement of winning.",
    "Success is not in what you have, but who you are.",
    "If you really look closely, most overnight successes took a long time.",
    "The only place where success comes before work is in the dictionary.",
    "Success is the sum of small efforts repeated day in and day out.",
    "Some people dream of success, while others wake up and work hard at it.",
    "Success is getting what you want. Happiness is wanting what you get."
]

def get_quote() -> str:
    return random.choice(QUOTES)