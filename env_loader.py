"""
env_loader.py
Independent .env loader for Neuraluxe-AI.
"""

import os

def load_env(path: str = ".env") -> dict:
    env_vars = {}
    if not os.path.exists(path):
        return env_vars
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                env_vars[key] = value
                os.environ[key] = value
    return env_vars