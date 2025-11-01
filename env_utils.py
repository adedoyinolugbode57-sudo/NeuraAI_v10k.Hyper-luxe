"""
env_utils.py
Independent environment utilities for Neuraluxe-AI.
"""
import os

def get_env(key: str, default=None):
    return os.environ.get(key, default)

def set_env(key: str, value: str):
    os.environ[key] = value