"""
cli_utils.py
Independent command line helpers.
"""

def prompt_input(message: str) -> str:
    return input(message + ": ")

def confirm(message: str) -> bool:
    resp = input(message + " (y/n): ").lower()
    return resp in ("y", "yes")