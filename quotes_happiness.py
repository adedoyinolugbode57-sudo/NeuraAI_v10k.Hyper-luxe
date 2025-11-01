"""
quote_happiness.py
Return quotes focused on happiness and positivity.
"""

import random

QUOTES = [
    "Happiness is not something ready-made. It comes from your own actions.",
    "For every minute you are angry you lose sixty seconds of happiness.",
    "Happiness is when what you think, what you say, and what you do are in harmony.",
    "Count your age by friends, not years. Count your life by smiles, not tears.",
    "The most important thing is to enjoy your life—to be happy—it's all that matters.",
    "Be happy for this moment. This moment is your life.",
    "Happiness depends upon ourselves.",
    "The purpose of our lives is to be happy.",
    "Happiness is a direction, not a place.",
    "Think of all the beauty still left around you and be happy.",
    "Happiness is not in the mere possession of money; it lies in the joy of achievement.",
    "If you want to be happy, be.",
    "Happiness is the art of never holding in your mind the memory of any unpleasant thing that has passed.",
    "Do more of what makes you happy.",
    "Spread love everywhere you go. Let no one ever come to you without leaving happier."
]

def get_quote() -> str:
    return random.choice(QUOTES)