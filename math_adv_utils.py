"""
math_adv_utils.py
Independent advanced math utilities for Neuraluxe-AI.
"""
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def linear_scale(x, old_min, old_max, new_min, new_max):
    return ((x - old_min)/(old_max - old_min))*(new_max - new_min) + new_min