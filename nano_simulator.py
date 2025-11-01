"""
nano_simulator.py
Simulate nanoscale interactions (mock science simulation).
"""

import random

ELEMENTS = ["Hydrogen", "Carbon", "Oxygen", "Nitrogen", "Gold", "Silver"]
REACTIONS = ["bond", "break", "fuse", "vibrate", "rotate"]

def simulate_interaction(atom1: str, atom2: str) -> str:
    """Return a simulated nanoscale interaction."""
    reaction = random.choice(REACTIONS)
    return f"{atom1} and {atom2} {reaction} at nanoscale."

def random_simulation(steps: int = 10) -> list:
    """Run a random nanoscale simulation."""
    results = []
    for _ in range(steps):
        a1 = random.choice(ELEMENTS)
        a2 = random.choice(ELEMENTS)
        results.append(simulate_interaction(a1, a2))
    return results

# Example usage
if __name__ == "__main__":
    for line in random_simulation(15):
        print(line)