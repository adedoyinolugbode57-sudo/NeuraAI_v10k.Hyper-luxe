"""
json_utils.py
Independent JSON utilities for Neuraluxe-AI.
"""
import json

def pretty_json(data):
    return json.dumps(data, indent=2, ensure_ascii=False)

def parse_json(text: str):
    try:
        return json.loads(text)
    except:
        return None