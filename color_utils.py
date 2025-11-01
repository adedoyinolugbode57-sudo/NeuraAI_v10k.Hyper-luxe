"""
color_utils.py
Independent color and theme utilities.
"""

def rgb_to_hex(r: int, g: int, b: int) -> str:
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def hex_to_rgb(hex_code: str) -> tuple:
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def random_color_hex() -> str:
    import random
    return rgb_to_hex(random.randint(0,255), random.randint(0,255), random.randint(0,255))