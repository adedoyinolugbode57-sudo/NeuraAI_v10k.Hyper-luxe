def meme_caption(image_name: str) -> str:
    import random
    captions = [
        "When AI takes over your job…",
        "Me trying to explain code to humans.",
        "That feeling when your neural net converges!"
    ]
    return f"{image_name}: {random.choice(captions)}"