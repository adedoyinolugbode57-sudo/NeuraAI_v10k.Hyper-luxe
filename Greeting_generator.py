"""
greeting_generator.py
Generate greetings based on time of day.
"""

import datetime

def generate_greeting(name: str) -> str:
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return f"Good morning, {name}!"
    elif 12 <= hour < 18:
        return f"Good afternoon, {name}!"
    else:
        return f"Good evening, {name}!"