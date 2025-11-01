"""
dict_utils.py
Independent dict utilities for Neuraluxe-AI.
"""
def invert_dict(d):
    return {v: k for k, v in d.items()}

def merge_dicts(*dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result