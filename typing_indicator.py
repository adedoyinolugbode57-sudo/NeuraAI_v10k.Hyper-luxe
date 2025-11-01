"""
typing_indicator.py
Simulate bot typing indicator.
"""

import time

def show_typing(seconds: float = 2):
    print("Bot is typing...", end="", flush=True)
    time.sleep(seconds)
    print("\r" + " " * 20 + "\r", end="", flush=True)