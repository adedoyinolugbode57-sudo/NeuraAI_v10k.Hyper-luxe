"""
fun_utils.py
Independent module providing fun facts and meme captions for Neuraluxe-AI.
"""

import random

# ------------------------
# Fun Facts
# ------------------------
FACTS = [
    "Honey never spoils.",
    "Octopuses have three hearts.",
    "Bananas are berries, but strawberries are not.",
    "A day on Venus is longer than a year on Venus.",
    "Wombat poop is cube-shaped.",
    "Sharks existed before trees.",
    "There’s a species of jellyfish that is immortal.",
    "Sloths can hold their breath longer than dolphins.",
    "A group of flamingos is called a 'flamboyance'.",
    "The first computer bug was a moth stuck in a computer.",
    # … add up to 500+ unique fun facts
]

def random_fact() -> str:
    """Return a random fun fact."""
    return random.choice(FACTS)

# ------------------------
# Meme Captions
# ------------------------
MEME_CAPTIONS = [
    "When AI takes over your job…",
    "Me trying to explain code to humans.",
    "That feeling when your neural net converges!",
    "When you accidentally delete the production database.",
    "Debugging: Where the fun begins.",
    "That moment you realize your 'fixed' bug created three new ones.",
    "AI said it would be easy… it lied.",
    "Me waiting for the code to compile… forever.",
    "When the coffee runs out mid-deployment.",
    "That feeling when your script finally runs without errors.",
    # … add up to 500+ unique meme captions
]

def meme_caption(image_name: str) -> str:
    """
    Return a meme caption for a given image.
    
    Args:
        image_name (str): The image file or description.
        
    Returns:
        str: Image name + randomly chosen caption.
    """
    return f"{image_name}: {random.choice(MEME_CAPTIONS)}"

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    print("Random Fact:", random_fact())
    print("Meme Caption:", meme_caption("funny_cat.png"))