"""
list_utils.py
Independent list utilities for Neuraluxe-AI.
"""
def chunk_list(lst, size):
    return [lst[i:i+size] for i in range(0, len(lst), size)]

def flatten_list(nested):
    return [item for sublist in nested for item in sublist]