"""
analytics_tracker.py
Track simple usage metrics.
"""

usage_data = {}

def log_usage(user_id: str, action: str):
    if user_id not in usage_data:
        usage_data[user_id] = []
    usage_data[user_id].append(action)

def get_user_actions(user_id: str):
    return usage_data.get(user_id, [])

# Example
if __name__ == "__main__":
    log_usage("user123", "sent_message")
    print(get_user_actions("user123"))