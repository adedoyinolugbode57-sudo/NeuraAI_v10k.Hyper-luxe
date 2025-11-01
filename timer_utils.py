"""
timer_utils.py
Independent timer utilities for Neuraluxe-AI.
"""
import time

class Timer:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time