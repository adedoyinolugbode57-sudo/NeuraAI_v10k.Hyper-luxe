"""
date_utils.py
Independent date/time utilities for Neuraluxe-AI.
"""
from datetime import datetime, timedelta

def utc_now():
    return datetime.utcnow()

def add_days(dt: datetime, days: int):
    return dt + timedelta(days=days)

def format_iso(dt: datetime):
    return dt.isoformat() + "Z"