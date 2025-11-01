"""
quote_health.py
Return quotes about health and wellness.
"""

import random

QUOTES = [
    "Health is the greatest gift, contentment the greatest wealth, faithfulness the best relationship.",
    "Take care of your body. It’s the only place you have to live.",
    "To keep the body in good health is a duty… otherwise we shall not be able to keep our mind strong and clear.",
    "A healthy outside starts from the inside.",
    "Happiness is the highest form of health.",
    "He who has health has hope; and he who has hope has everything.",
    "It is health that is real wealth and not pieces of gold and silver.",
    "The groundwork for all happiness is good health.",
    "Good health is not something we can buy. However, it can be an extremely valuable savings account.",
    "Health is a state of complete harmony of the body, mind and spirit.",
    "Your body deserves the best.",
    "Eat to live, don’t live to eat.",
    "Wellness is the natural state of my body.",
    "Every human being is the author of their own health or disease.",
    "Take care of your body; it’s the only place you have to live."
]

def get_quote() -> str:
    return random.choice(QUOTES)