"""
logging_utils.py
Independent logging utilities for Neuraluxe-AI.
"""
import logging

def setup_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s - %(message)s'))
        logger.addHandler(ch)
    return logger