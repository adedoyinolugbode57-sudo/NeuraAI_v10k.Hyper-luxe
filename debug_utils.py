"""
debug_utils.py
Independent debug utilities for Neuraluxe-AI.
"""
def log_vars(**kwargs):
    for k, v in kwargs.items():
        print(f"[DEBUG] {k} = {v}")