"""
multi_joke_loader.py
Dynamically load and serve jokes from multiple joke files.
Independent and ready for Neuraluxe-AI.
"""

import os
import random
import importlib.util

# Folder where joke files are stored
JOKE_FOLDER = "jokes"  # make sure all joke files are inside a folder named 'jokes'

def load_jokes_from_file(file_path: str):
    """Load the JOKES list from a Python file dynamically."""
    spec = importlib.util.spec_from_file_location("joke_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "JOKES") and isinstance(module.JOKES, list):
        return module.JOKES
    return []

def load_all_jokes():
    """Load jokes from all Python files in JOKE_FOLDER."""
    all_jokes = []
    if not os.path.isdir(JOKE_FOLDER):
        print(f"[Warning] Joke folder '{JOKE_FOLDER}' does not exist.")
        return all_jokes

    for filename in os.listdir(JOKE_FOLDER):
        if filename.endswith(".py"):
            file_path = os.path.join(JOKE_FOLDER, filename)
            jokes = load_jokes_from_file(file_path)
            all_jokes.extend(jokes)
    return all_jokes

class JokeProvider:
    """Serve random jokes from multiple joke files."""
    def __init__(self):
        self.jokes = load_all_jokes()

    def tell_joke(self):
        if not self.jokes:
            return "No jokes available!"
        return random.choice(self.jokes)

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    jp = JokeProvider()
    print(jp.tell_joke())