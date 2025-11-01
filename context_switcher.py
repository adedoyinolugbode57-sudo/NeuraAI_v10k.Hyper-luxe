def switch_context(current_context: str, new_input: str) -> str:
    return f"Switching from '{current_context}' to new topic: {new_input[:30]}..."