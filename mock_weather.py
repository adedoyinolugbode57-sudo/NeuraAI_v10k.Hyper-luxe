"""
mock_weather.py
Return random weather info (mock).
"""

import random

def get_weather(city: str) -> str:
    conditions = ["Sunny", "Cloudy", "Rainy", "Stormy", "Windy"]
    return f"{city}: {random.choice(conditions)}, {random.randint(15, 35)}°C"