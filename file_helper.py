"""
file_helper.py
Independent file reading/writing helpers.
"""

import os

def read_text_file(path: str) -> str:
    if not os.path.exists(path): return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_text_file(path: str, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)