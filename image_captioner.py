"""
image_captioner.py
Generate captions for images using a mock AI engine.
"""

import random

CAPTION_TEMPLATES = [
    "A stunning view of {}.",
    "An artistic capture of {}.",
    "A vibrant scene featuring {}.",
    "A breathtaking image of {} in its full glory.",
    "A beautiful portrayal of {}."
]

IMAGE_KEYWORDS = {
    "mountain": ["mountains", "peaks", "highlands"],
    "beach": ["ocean", "sand", "waves"],
    "city": ["skyscrapers", "streets", "urban life"],
    "forest": ["trees", "nature", "greenery"],
    "sunset": ["sky", "horizon", "twilight"],
    "animal": ["wildlife", "creature", "beast"],
}

def caption_image(image_path: str, keyword: str = None) -> str:
    """
    Generates a mock AI-style caption based on a keyword.
    If keyword is not provided, one is randomly chosen.
    """
    if not keyword or keyword not in IMAGE_KEYWORDS:
        keyword = random.choice(list(IMAGE_KEYWORDS.keys()))
    
    topic = random.choice(IMAGE_KEYWORDS[keyword])
    template = random.choice(CAPTION_TEMPLATES)
    
    return template.format(topic)

# Example usage
if __name__ == "__main__":
    print(caption_image("sunset.jpg"))
    print(caption_image("mountain.png", keyword="mountain"))"""
image_captioner.py
Generate captions for images using a mock AI engine.
"""

import random

CAPTION_TEMPLATES = [
    "A stunning view of {}.",
    "An artistic capture of {}.",
    "A vibrant scene featuring {}.",
    "A breathtaking image of {} in its full glory.",
    "A beautiful portrayal of {}."
]

IMAGE_KEYWORDS = {
    "mountain": ["mountains", "peaks", "highlands"],
    "beach": ["ocean", "sand", "waves"],
    "city": ["skyscrapers", "streets", "urban life"],
    "forest": ["trees", "nature", "greenery"],
    "sunset": ["sky", "horizon", "twilight"],
    "animal": ["wildlife", "creature", "beast"],
}

def caption_image(image_path: str, keyword: str = None) -> str:
    """
    Generates a mock AI-style caption based on a keyword.
    If keyword is not provided, one is randomly chosen.
    """
    if not keyword or keyword not in IMAGE_KEYWORDS:
        keyword = random.choice(list(IMAGE_KEYWORDS.keys()))
    
    topic = random.choice(IMAGE_KEYWORDS[keyword])
    template = random.choice(CAPTION_TEMPLATES)
    
    return template.format(topic)

# Example usage
if __name__ == "__main__":
    print(caption_image("sunset.jpg"))
    print(caption_image("mountain.png", keyword="mountain"))