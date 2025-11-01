def detect_interruption(prev_msg: str, new_msg: str) -> bool:
    return len(new_msg.split()) < len(prev_msg.split()) / 2