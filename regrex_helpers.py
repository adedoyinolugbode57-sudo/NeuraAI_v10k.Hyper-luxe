"""
regex_helpers.py
Independent regex utilities for Neuraluxe-AI.
"""

import re

def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def is_valid_phone(phone: str) -> bool:
    pattern = r"^\+?\d{7,15}$"
    return re.match(pattern, phone) is not None

def is_valid_url(url: str) -> bool:
    pattern = r"^(https?://)?[\w.-]+\.[a-z]{2,}(/[\w./-]*)?$"
    return re.match(pattern, url) is not None