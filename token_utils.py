"""
token_utils.py
Independent token utilities for Neuraluxe-AI.
"""
import secrets

def generate_token(length=32):
    return secrets.token_hex(length)