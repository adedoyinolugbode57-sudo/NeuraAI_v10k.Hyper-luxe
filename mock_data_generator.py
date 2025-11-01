"""
mock_data_generator.py
Generate fake names, emails, addresses for testing.
"""

import random

FIRST_NAMES = ["John", "Jane", "Alex", "Maria", "Chris"]
LAST_NAMES = ["Smith", "Doe", "Johnson", "Brown", "Lee"]

def fake_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def fake_email() -> str:
    return f"{fake_name().replace(' ', '.').lower()}@example.com"

def fake_address() -> str:
    streets = ["Main St", "Broadway", "1st Ave", "2nd Ave", "Maple Rd"]
    return f"{random.randint(100,999)} {random.choice(streets)}, Cityville"