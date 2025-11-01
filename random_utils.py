"""
random_utils.py
Independent random utilities for Neuraluxe-AI.
"""
import random
import string

def random_string(length: int = 8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_choice(choices):
    return random.choice(choices)