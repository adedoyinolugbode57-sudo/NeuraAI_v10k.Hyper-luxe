"""
hash_utils.py
Independent hashing utilities for Neuraluxe-AI.
"""
import hashlib

def md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()