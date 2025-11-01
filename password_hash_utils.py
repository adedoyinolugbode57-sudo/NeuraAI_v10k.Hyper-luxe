"""
password_hash_utils.py
Independent password hashing for Neuraluxe-AI.
"""
import hashlib

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()