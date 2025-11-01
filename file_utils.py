"""
file_utils.py
Independent file utilities for Neuraluxe-AI.
"""
import os

def file_exists(path: str) -> bool:
    return os.path.isfile(path)

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def read_text(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()