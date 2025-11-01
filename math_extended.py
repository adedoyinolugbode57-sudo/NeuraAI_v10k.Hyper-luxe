"""
math_extended.py
Independent advanced math helpers.
"""

import math

def factorial(n: int) -> int:
    return math.factorial(n)

def is_prime(n: int) -> bool:
    if n < 2: return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True"""
math_extended.py
Independent advanced math helpers.
"""

import math

def factorial(n: int) -> int:
    return math.factorial(n)

def is_prime(n: int) -> bool:
    if n < 2: return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True