"""
thought_mapper.py
Visualize thought patterns (mock simulation).
"""

import random
from typing import List, Dict

IDEAS = ["creativity", "logic", "memory", "emotion", "intuition", "focus"]

def generate_thought_map(thoughts: List[str]) -> Dict[str, int]:
    """Convert a list of thoughts into a weighted map."""
    mapping = {}
    for thought in thoughts:
        mapping[thought] = random.randint(1, 10)
    return mapping

def display_map(mapping: Dict[str, int]):
    print("Thought Map:")
    for k, v in mapping.items():
        print(f" {k}: {v}")

# Example
if __name__ == "__main__":
    thoughts = random.sample(IDEAS, 5)
    map_data = generate_thought_map(thoughts)
    display_map(map_data)