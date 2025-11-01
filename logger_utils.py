"""
logger_utils.py
Independent logger utilities for Neuraluxe-AI.
"""
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Neuraluxe-AI")

def log_info(msg):
    logger.info(msg)

def log_error(msg):
    logger.error(msg)