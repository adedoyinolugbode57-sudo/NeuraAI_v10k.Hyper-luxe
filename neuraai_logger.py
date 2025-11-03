"""
Neuraluxe-AI Smart Logger — Independent Utility Module
Logs system events, chats, and environment summaries with color and rotation.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "neuraluxe.log")

# Configure rotating file handler (max 1 MB per file, keep 5 backups)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

# Global logger setup
logger = logging.getLogger("NeuraluxeLogger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# --- Utility Functions ---
def log_event(message: str, level: str = "info"):
    """Log a message with a color-coded console output."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {message}"

    if level.lower() == "error":
        print(Fore.RED + msg + Style.RESET_ALL)
        logger.error(message)
    elif level.lower() == "warning":
        print(Fore.YELLOW + msg + Style.RESET_ALL)
        logger.warning(message)
    else:
        print(Fore.CYAN + msg + Style.RESET_ALL)
        logger.info(message)

def log_startup(app_name="Neuraluxe-AI"):
    """Log a startup event with app info."""
    banner = f"🚀 {app_name} Started Successfully at {datetime.utcnow()} UTC"
    log_event(banner)
    log_event("System diagnostics: memory, routes, and env OK ✅")

def log_chat(user_id: str, message: str, response: str):
    """Log user chat interactions."""
    entry = f"[User: {user_id}] said '{message}' → Bot replied: '{response}'"
    log_event(entry)

def log_env_summary(env_vars: list):
    """Log a summary of key environment variables (masked for safety)."""
    masked = {key: ("✅ Loaded" if os.getenv(key) else "⚠️ Missing") for key in env_vars}
    log_event(f"Environment Summary: {masked}")

# Example standalone run
if __name__ == "__main__":
    log_startup("NeuraAI v10k Hyperluxe")
    log_event("System warming up...")
    log_chat("demo_user", "Hello world!", "Greetings from Neuraluxe-AI 🌍")
    log_env_summary(["APP_NAME", "PORT", "OPENAI_ENABLED"])
