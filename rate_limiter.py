"""
rate_limiter.py
Limit requests per user/session.
"""

user_limits = {}
MAX_REQUESTS = 5

def can_proceed(user_id: str) -> bool:
    count = user_limits.get(user_id, 0)
    if count < MAX_REQUESTS:
        user_limits[user_id] = count + 1
        return True
    return False

# Example
if __name__ == "__main__":
    for i in range(7):
        print(can_proceed("user123"))