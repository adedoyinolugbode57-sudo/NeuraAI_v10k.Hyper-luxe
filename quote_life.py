"""
quote_life.py
Return quotes about life, purpose, and growth.
"""

import random

QUOTES = [
    "In the end, it’s not the years in your life that count. It’s the life in your years.",
    "Life is what happens when you’re busy making other plans.",
    "Get busy living or get busy dying.",
    "The purpose of life is a life of purpose.",
    "Life is really simple, but we insist on making it complicated.",
    "Do not take life too seriously. You will never get out of it alive.",
    "Life isn’t about finding yourself. Life is about creating yourself.",
    "Turn your wounds into wisdom.",
    "Life is short, and it is up to you to make it sweet.",
    "The biggest adventure you can take is to live the life of your dreams.",
    "Life is a journey that must be traveled no matter how bad the roads and accommodations.",
    "To live is the rarest thing in the world. Most people exist, that is all.",
    "Keep your eyes on the stars, and your feet on the ground.",
    "Life is made of ever so many partings welded together.",
    "Do not go where the path may lead, go instead where there is no path and leave a trail."
]

def get_quote() -> str:
    return random.choice(QUOTES)