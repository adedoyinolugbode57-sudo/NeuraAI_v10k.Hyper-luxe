"""
data_utils.py
Independent data utilities for Neuraluxe-AI.
"""
def filter_dict(d: dict, keys: list):
    return {k: d[k] for k in keys if k in d}

def merge_dicts(*dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result