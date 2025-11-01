"""
debug_tools.py
Advanced debugging utilities for Neuraluxe-AI.
"""

import logging
import traceback

def debug_response(prompt: str, response: str, context: dict = None) -> str:
    ctx_info = f"Context: {context}" if context else ""
    return (
        f"DEBUG INFO:\n"
        f"Prompt (first 50 chars): {prompt[:50]}\n"
        f"Response (first 50 chars): {response[:50]}\n"
        f"{ctx_info}\n"
        f"Traceback: {traceback.format_stack(limit=3)[-1]}"
    )

def setup_logger(name: str, level=logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger