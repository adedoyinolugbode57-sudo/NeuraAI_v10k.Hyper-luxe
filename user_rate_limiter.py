"""
user_rate_limiter.py
Limit users to a set number of requests per hour/day.
"""

from collections import defaultdict
import time

USER_LIMITS = defaultdict(list)  # user_id -> list of timestamps
MAX_REQUESTS = 200
TIME_WINDOW = 12 * 60 * 60  # 12 hours

def allow_request(user_id: str) -> bool:
    now = time.time()
    timestamps = USER_LIMITS[user_id]
    timestamps = [t for t in timestamps if now - t < TIME_WINDOW]
    if len(timestamps) >= MAX_REQUESTS:
        return False
    timestamps.append(now)
    USER_LIMITS[user_id] = timestamps
    return True