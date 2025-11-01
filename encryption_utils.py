"""
encryption_utils.py
Independent string encryption helpers.
"""

import base64

def encrypt(text: str) -> str:
    return base64.b64encode(text.encode()).decode()

def decrypt(enc_text: str) -> str:
    return base64.b64decode(enc_text.encode()).decode()