"""
logger_color_utils.py
Independent colored logging for Neuraluxe-AI.
"""
def log_color(text, color="green"):
    colors = {"green":"\033[92m", "red":"\033[91m", "yellow":"\033[93m", "end":"\033[0m"}
    print(f"{colors.get(color,'')}{text}{colors['end']}")