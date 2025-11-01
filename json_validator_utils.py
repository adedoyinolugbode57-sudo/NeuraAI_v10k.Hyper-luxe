"""
json_validator.py
Independent JSON validator for Neuraluxe-AI.
"""
import json

def is_valid_json(text):
    try:
        json.loads(text)
        return True
    except:
        return False