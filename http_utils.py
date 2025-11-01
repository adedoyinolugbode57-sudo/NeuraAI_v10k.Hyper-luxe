"""
http_utils.py
Independent HTTP utilities for Neuraluxe-AI.
"""
import requests

def is_url_alive(url: str) -> bool:
    try:
        return requests.head(url, timeout=5).status_code < 400
    except:
        return False