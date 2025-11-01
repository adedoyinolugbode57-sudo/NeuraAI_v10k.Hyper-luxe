"""
cache_file_utils.py
Independent file caching for Neuraluxe-AI.
"""
import os
import pickle

def save_cache(path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def load_cache(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    return None