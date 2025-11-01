"""
clipboard_utils.py
Independent clipboard utilities for Neuraluxe-AI.
"""
try:
    import pyperclip
except ImportError:
    pyperclip = None

def copy_to_clipboard(text: str):
    if pyperclip:
        pyperclip.copy(text)
        return True
    return False