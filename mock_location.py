"""
mock_location.py
Return random location coordinates (mock).
"""

import random

def get_location() -> tuple:
    return (round(random.uniform(-90, 90), 5), round(random.uniform(-180, 180), 5))