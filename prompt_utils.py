"""
prompt_utils.py
Independent AI prompt utilities for Neuraluxe-AI.
"""
def sanitize_prompt(prompt: str):
    return prompt.strip().replace("\n", " ")

def shorten_prompt(prompt: str, max_length=256):
    return prompt[:max_length] + ("..." if len(prompt) > max_length else "")