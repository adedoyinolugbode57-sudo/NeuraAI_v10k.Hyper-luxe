"""
text_utils.py
Independent text utilities for Neuraluxe-AI.
"""
def capitalize_words(text):
    return " ".join(word.capitalize() for word in text.split())