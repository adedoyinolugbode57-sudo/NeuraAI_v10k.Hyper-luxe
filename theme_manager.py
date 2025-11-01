"""
theme_manager.py
Handle UI themes and transitions.
"""

available_themes = ["light", "dark", "neon", "retro"]
current_theme = "light"

def set_theme(theme_name: str):
    global current_theme
    if theme_name in available_themes:
        current_theme = theme_name
    return current_theme

def get_theme() -> str:
    return current_theme

# Example
if __name__ == "__main__":
    set_theme("neon")
    print(get_theme())