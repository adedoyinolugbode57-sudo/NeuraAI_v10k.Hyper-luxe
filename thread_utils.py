"""
thread_utils.py
Independent threading utilities for Neuraluxe-AI.
"""
import threading

def start_thread(target, daemon=True):
    t = threading.Thread(target=target, daemon=daemon)
    t.start()
    return t