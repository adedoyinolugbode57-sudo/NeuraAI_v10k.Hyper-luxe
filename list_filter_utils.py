"""
list_filter_utils.py
Independent list filter utilities for Neuraluxe-AI.
"""
def filter_even(lst):
    return [x for x in lst if x % 2 == 0]

def filter_odd(lst):
    return [x for x in lst if x % 2 != 0]