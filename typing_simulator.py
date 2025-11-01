"""
typing_simulator.py
Simulate typing delays.
"""

import time
import random

def simulate_typing(min_sec: float = 0.5, max_sec: float = 2.0):
    time.sleep(random.uniform(min_sec, max_sec))