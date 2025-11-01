"""
version_utils.py
Independent version utilities for Neuraluxe-AI.
"""
__version__ = "1.0.0"

def is_newer_version(current, new):
    return tuple(map(int, new.split("."))) > tuple(map(int, current.split(".")))