"""
array_utils.py
Independent array/list helpers.
"""

def flatten(lst: list) -> list:
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def unique(lst: list) -> list:
    return list(dict.fromkeys(lst))