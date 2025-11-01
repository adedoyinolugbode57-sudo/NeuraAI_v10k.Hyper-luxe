"""
retry_utils.py
Independent retry utilities for Neuraluxe-AI.
"""
import time

def retry(func, retries=3, delay=1, *args, **kwargs):
    for _ in range(retries):
        try:
            return func(*args, **kwargs)
        except:
            time.sleep(delay)
    return None