"""
math_utils.py
Independent advanced math helpers for Neuraluxe-AI.
"""

import math
import random
from typing import List, Optional

# ------------------------
# Basic helpers
# ------------------------
def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(max_val, value))

def round_decimal(value: float, places: int = 2) -> float:
    return round(value, places)

def percent_of(value: float, total: float) -> float:
    if total == 0: return 0
    return (value / total) * 100

# ------------------------
# Advanced calculations
# ------------------------
def average(values: List[float]) -> float:
    if not values: return 0
    return sum(values) / len(values)

def median(values: List[float]) -> float:
    if not values: return 0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
    return sorted_vals[mid]

def factorial(n: int) -> int:
    if n < 0: raise ValueError("Negative factorial not allowed")
    return math.factorial(n)

def deg_to_rad(degrees: float) -> float:
    return math.radians(degrees)

def rad_to_deg(radians: float) -> float:
    return math.degrees(radians)

# ------------------------
# Random & distributions
# ------------------------
def random_int(min_val: int, max_val: int) -> int:
    return random.randint(min_val, max_val)

def random_float(min_val: float, max_val: float) -> float:
    return random.uniform(min_val, max_val)

def random_choice(values: List) -> Optional[any]:
    if not values: return None
    return random.choice(values)

def random_sample(values: List, k: int) -> List:
    return random.sample(values, min(k, len(values)))

# ------------------------
# Trigonometry helpers
# ------------------------
def sin(degrees: float) -> float:
    return math.sin(math.radians(degrees))

def cos(degrees: float) -> float:
    return math.cos(math.radians(degrees))

def tan(degrees: float) -> float:
    return math.tan(math.radians(degrees))