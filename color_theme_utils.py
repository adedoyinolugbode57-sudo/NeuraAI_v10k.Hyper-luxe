"""
color_theme_utils.py
Independent color/theme utilities for Neuraluxe-AI.
"""
THEMES = {
    "dark": {"bg": "#000000", "fg": "#FFFFFF"},
    "light": {"bg": "#FFFFFF", "fg": "#000000"},
}

def get_theme(name="dark"):
    return THEMES.get(name, THEMES["dark"])