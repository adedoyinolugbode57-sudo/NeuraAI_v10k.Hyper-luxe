def analyze_usage(user_data: list):
    total_sessions = len(user_data)
    avg_length = sum(len(s) for s in user_data) / max(1, total_sessions)
    return {"total_sessions": total_sessions, "avg_length": avg_length}