"""
validation_utils.py
Independent input validation utilities for Neuraluxe-AI.
"""
import re

def is_email(text: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", text) is not None

def is_numeric(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False