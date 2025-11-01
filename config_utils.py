"""
config_utils.py
Independent configuration utilities for Neuraluxe-AI.
"""
import json
import os

def load_config(path: str):
    if not os.path.isfile(path):
        return {}
    with open(path, 'r') as f:
        return json.load(f)

def save_config(path: str, data: dict):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)