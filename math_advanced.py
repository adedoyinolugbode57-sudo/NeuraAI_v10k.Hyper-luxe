"""
math_advanced.py
Independent advanced math helpers.
"""

import math

def factorial(n: int) -> int:
    return math.factorial(n)

def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a