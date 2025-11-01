"""
random_color.py
Independent random color generator.
"""

import random

def random_hex_color() -> str:
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))