"""
password_utils.py
Independent password utilities for Neuraluxe-AI.
"""
import random
import string

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choices(chars, k=length))

def is_strong(password: str):
    return len(password) >= 8 and any(c.isdigit() for c in password)