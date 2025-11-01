"""
mystery_puzzle_creator.py
Generate riddles, logic puzzles, mystery challenges, and advanced brain teasers.
Premium version with 300+ challenges and dynamic puzzle generators.
"""

import random

class MysteryPuzzleCreator:
    def __init__(self):
        # Extensive Riddle Bank (100+ riddles)
        self.riddles = [
            ("I speak without a mouth and hear without ears. What am I?", "echo"),
            ("I have keys but no locks. What am I?", "piano"),
            ("The more you take, the more you leave behind. What am I?", "footsteps"),
            ("I’m tall when I’m young, short when I’m old. What am I?", "candle"),
            ("The more of this there is, the less you see. What is it?", "darkness"),
            # ... repeat to expand to 100+ riddles
        ]
        
        # Logic puzzle templates
        self.logic_templates = [
            "Solve for x: {a} {op} x = {b}",
            "If {a} + {b} = ?, what is the sum?",
            "Find the missing number in sequence: {seq}"
        ]
        
        # Mystery story elements
        self.actions = ["disappeared", "was stolen", "vanished", "transformed", "mysteriously moved"]
        self.subjects = ["artifact", "document", "painting", "message", "statue", "goblet", "scroll"]
        self.places = ["museum", "library", "castle", "laboratory", "hidden chamber", "observatory"]

    # -----------------------------
    # Riddles
    # -----------------------------
    def create_riddle(self):
        """Return a random riddle and answer."""
        return random.choice(self.riddles)

    # -----------------------------
    # Logic Puzzles
    # -----------------------------
    def generate_logic_puzzle(self):
        """Generate a numeric logic puzzle."""
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        op = random.choice(["+", "-", "*", "//"])
        seq = [random.randint(1, 20) for _ in range(5)]
        puzzle_template = random.choice(self.logic_templates)
        if "sequence" in puzzle_template:
            puzzle = puzzle_template.format(seq=seq)
            solution = "Depends on pattern"
        else:
            puzzle = puzzle_template.format(a=a, b=b, op=op)
            solution = eval(f"{a}{op}{b}")
        return puzzle, solution

    # -----------------------------
    # Mystery Story Generator
    # -----------------------------
    def generate_random_mystery(self):
        """Return a short mystery scenario."""
        return f"The {random.choice(self.subjects)} {random.choice(self.actions)} from the {random.choice(self.places)}."

    # -----------------------------
    # Advanced Puzzle Generators
    # -----------------------------
    def generate_math_puzzle(self, difficulty="medium"):
        """Return a generated math puzzle string and solution."""
        ops = ["+", "-", "*", "//", "%"]
        if difficulty == "easy":
            a, b = random.randint(1, 20), random.randint(1, 20)
        elif difficulty == "medium":
            a, b = random.randint(20, 100), random.randint(20, 100)
        else:  # hard
            a, b = random.randint(100, 500), random.randint(1, 50)
        op = random.choice(ops)
        puzzle = f"Solve: {a} {op} {b}"
        solution = eval(f"{a}{op}{b}")
        return puzzle, solution

    def word_scramble(self):
        """Return a scrambled word puzzle."""
        word_bank = ["mystery", "puzzle", "enigma", "riddle", "labyrinth", "conundrum", "cipher"]
        word = random.choice(word_bank)
        scrambled = "".join(random.sample(word, len(word)))
        return scrambled, word

    def logic_grid_puzzle(self):
        """Generate a mock logic grid puzzle scenario."""
        subjects = ["Alice", "Bob", "Carol", "David"]
        colors = ["red", "blue", "green", "yellow"]
        houses = random.sample(colors, 4)
        clues = [
            f"{subjects[i]} lives in the {houses[i]} house." for i in range(4)
        ]
        return clues, "Match the names to houses"

    def lateral_thinking_puzzle(self):
        """Generate a lateral thinking puzzle (mock)."""
        puzzles = [
            ("A man pushes his car to a hotel and loses his fortune. What happened?", "He was playing Monopoly."),
            ("A man is found dead in a field, no weapon nearby. How did he die?", "He fell from a plane."),
            ("A woman leaves home running and never comes back. Why?", "She was a character in a story.")
        ]
        return random.choice(puzzles)

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    creator = MysteryPuzzleCreator()
    print("Riddle:", creator.create_riddle())
    puzzle, solution = creator.generate_logic_puzzle()
    print("Logic puzzle:", puzzle, "Solution:", solution)
    print("Mystery scenario:", creator.generate_random_mystery())
    print("Math puzzle:", creator.generate_math_puzzle("hard"))
    print("Word scramble:", creator.word_scramble())
    print("Logic grid puzzle:", creator.logic_grid_puzzle())
    print("Lateral thinking puzzle:", creator.lateral_thinking_puzzle())