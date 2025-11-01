"""
game_engine_utils.py
Helper utilities for AI-powered mini-games in Neuraluxe-AI.
"""

import random
import time
from typing import List, Tuple, Dict

# ------------------------
# Mini-game data
# ------------------------
MINI_GAMES = {
    "tic_tac_toe": {"players": 2, "board_size": 3},
    "guess_number": {"range": 100},
    "word_scramble": {"difficulty": "medium"},
    "memory_match": {"pairs": 10},
    "maze_solver": {"size": 5},
}

# ------------------------
# Game Engine Utilities
# ------------------------
def select_game() -> str:
    """Randomly select a mini-game."""
    game = random.choice(list(MINI_GAMES.keys()))
    print(f"[GameEngine] Selected mini-game: {game}")
    return game

# ------------------------
# Tic Tac Toe Helpers
# ------------------------
def create_board(size: int = 3) -> List[List[str]]:
    """Create a blank Tic Tac Toe board."""
    return [[" " for _ in range(size)] for _ in range(size)]

def print_board(board: List[List[str]]):
    """Print the Tic Tac Toe board."""
    for row in board:
        print("|".join(row))
        print("-" * (len(row) * 2 - 1))

def check_winner(board: List[List[str]], player: str) -> bool:
    """Check if a player has won."""
    size = len(board)
    # Check rows and columns
    for i in range(size):
        if all(board[i][j] == player for j in range(size)):
            return True
        if all(board[j][i] == player for j in range(size)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(size)):
        return True
    if all(board[i][size - 1 - i] == player for i in range(size)):
        return True
    return False

# ------------------------
# Guess Number Helpers
# ------------------------
def guess_number_game(max_value: int = 100) -> int:
    """Return a random number for guess the number game."""
    number = random.randint(1, max_value)
    print(f"[GameEngine] Number generated: {number}")
    return number

# ------------------------
# Word Scramble Helpers
# ------------------------
def scramble_word(word: str) -> str:
    """Return a scrambled version of a word."""
    letters = list(word)
    random.shuffle(letters)
    scrambled = "".join(letters)
    print(f"[GameEngine] Word '{word}' scrambled as '{scrambled}'")
    return scrambled

def pick_random_word(word_list: List[str]) -> str:
    """Pick a random word from a list."""
    word = random.choice(word_list)
    print(f"[GameEngine] Picked word: {word}")
    return word

# ------------------------
# Memory Match Helpers
# ------------------------
def create_memory_pairs(pairs: int = 10) -> List[str]:
    """Generate a list of pairs for memory match game."""
    values = [f"card{i}" for i in range(1, pairs + 1)]
    cards = values * 2
    random.shuffle(cards)
    return cards

# ------------------------
# Maze Solver Helpers
# ------------------------
def generate_maze(size: int = 5) -> List[List[int]]:
    """Generate a simple maze with 0 = empty, 1 = wall."""
    maze = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]
    maze[0][0] = 0  # Start
    maze[size - 1][size - 1] = 0  # End
    return maze

def print_maze(maze: List[List[int]]):
    for row in maze:
        print(" ".join(str(cell) for cell in row))

# ------------------------
# Game Loop
# ------------------------
def run_game(game_name: str):
    print(f"[GameEngine] Running game: {game_name}")
    if game_name == "tic_tac_toe":
        board = create_board()
        print_board(board)
    elif game_name == "guess_number":
        number = guess_number_game()
        print(f"[GameEngine] Number to guess: {number}")
    elif game_name == "word_scramble":
        word = pick_random_word(["python", "neuraluxe", "ai", "algorithm"])
        scrambled = scramble_word(word)
        print(f"[GameEngine] Scrambled word: {scrambled}")
    elif game_name == "memory_match":
        cards = create_memory_pairs()
        print(f"[GameEngine] Memory cards: {cards}")
    elif game_name == "maze_solver":
        maze = generate_maze()
        print_maze(maze)
    else:
        print("[GameEngine] Unknown game.")

# ------------------------
# Example
# ------------------------
if __name__ == "__main__":
    selected = select_game()
    run_game(selected)