"""
poll_results.py
Analyze poll results.
"""

def winner(poll: dict) -> str:
    if not poll:
        return "No votes yet"
    return max(poll, key=poll.get)