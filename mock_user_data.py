"""
mock_user_data.py
Generate fake user data for testing.
"""

import random

NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

def generate_user():
    return {
        "name": random.choice(NAMES),
        "age": random.randint(18, 60),
        "id": random.randint(1000, 9999)
    }