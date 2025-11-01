"""
api_utils.py
Independent API utilities for Neuraluxe-AI.
"""
import requests

def get_json(url: str, params=None):
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"API GET Error: {e}")
        return None

def post_json(url: str, data=None):
    try:
        r = requests.post(url, json=data)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"API POST Error: {e}")
        return None