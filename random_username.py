"""
random_username.py
Generate random usernames.
"""

import random
import string

def generate_username(length: int = 8) -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))