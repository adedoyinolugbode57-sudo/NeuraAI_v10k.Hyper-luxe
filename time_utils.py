"""
time_utils.py
Independent time utilities for Neuraluxe-AI.
"""
import time
from datetime import datetime

def current_timestamp():
    return int(time.time())

def format_datetime(ts=None, fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.fromtimestamp(ts or time.time()).strftime(fmt)