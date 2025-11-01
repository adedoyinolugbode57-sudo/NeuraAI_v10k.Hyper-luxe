"""
random_util.py
Independent random utilities.
"""

import random
import string

def rand_hex(length: int = 8) -> str:
    return ''.join(random.choice("0123456789abcdef") for _ in range(length))

def rand_string(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))