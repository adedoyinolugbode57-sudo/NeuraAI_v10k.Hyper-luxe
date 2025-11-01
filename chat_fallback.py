"""
chat_fallback.py
Provides limited daily chatbot responses (mock/fallback) with history tracking.

- Uses chat_limiter.py for daily limits
- Returns canned responses when limit is reached
- Keeps last N responses for recall
"""

import random
from chat_limiter import can_chat, record_chat, get_user_history

# Predefined canned responses
CANNED_RESPONSES = [
    "I'm thinking... please wait a moment.",
    "Interesting! Let's continue.",
    "Hmm, can you clarify that?",
    "I have a suggestion you might like.",
    "Let's break this down into steps.",
    "Could you provide more context?",
    "That’s an excellent question!",
    "I can help with that in a moment.",
    "Here's an idea you could try.",
    "Let's explore this together."
]

def fallback_response(prompt: str) -> str:
    """Return a random canned response for a prompt."""
    r = random.choice(CANNED_RESPONSES)
    return f"{r} (fallback for: {prompt[:50]})"

def chat_with_limit(user_email: str, prompt: str) -> str:
    """
    Process chat for a user with daily limit enforced.
    Returns either a normal or fallback response.
    """
    if can_chat(user_email):
        # Simulate generating a response (replace with AI call if desired)
        response = fallback_response(prompt)
        record_chat(user_email, prompt, response)
        return response
    else:
        # Limit reached
        history = get_user_history(user_email, last_n=3)
        return f"You've reached your daily chat limit. Try again later.\nLast interactions: {history}"