def generate_prompt(context: str) -> str:
    import random
    templates = [
        f"Explain {context} in simple terms.",
        f"List the pros and cons of {context}.",
        f"Make a story about {context}."
    ]
    return random.choice(templates)