"""
math_random_utils.py
Independent math/random utilities for Neuraluxe-AI.
"""
import math
import random

def random_angle():
    return random.uniform(0, 360)

def distance_2d(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)