"""
biome_generator.py
Create random biome simulations.
"""

import random

BIOMES = ["Desert", "Rainforest", "Tundra", "Savanna", "Wetlands", "Coral Reef", "Mountain"]
WEATHERS = ["sunny", "rainy", "stormy", "foggy", "snowy"]
FLORA = ["trees", "shrubs", "flowers", "grasses", "mosses"]
FAUNA = ["birds", "insects", "mammals", "reptiles", "fish"]

def generate_biome(name: str = None) -> dict:
    biome = name or random.choice(BIOMES)
    return {
        "biome": biome,
        "weather": random.choice(WEATHERS),
        "flora": random.sample(FLORA, 2),
        "fauna": random.sample(FAUNA, 2),
        "hazards": random.choice(["floods", "drought", "predators", "disease", "none"])
    }

def display_biome(b: dict):
    print(f"Biome: {b['biome']}")
    print(f" Weather: {b['weather']}")
    print(f" Flora: {b['flora']}")
    print(f" Fauna: {b['fauna']}")
    print(f" Hazards: {b['hazards']}")

# Example
if __name__ == "__main__":
    biome = generate_biome()
    display_biome(biome)