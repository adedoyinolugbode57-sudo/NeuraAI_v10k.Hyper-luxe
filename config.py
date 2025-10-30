# config.py
"""
Central config for NeuraAI_v10k.HyperLuxe
Read secrets from environment. Use .env locally for convenience.
"""
import os
from pathlib import Path
from typing import Optional

# optionally load .env in local dev
try:
    from dotenv import load_dotenv
    load_dotenv()  # safe no-op on environments without .env
except Exception:
    pass

PROJECT_ROOT = Path(__file__).parent.resolve()

# OpenAI
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
NEURA_MODEL: str = os.getenv("NEURA_MODEL", "gpt-4o-mini")

# Database (Postgres)
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")  # preferred
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Redis (optional)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Runtime flags
ENABLE_TTS = os.getenv("ENABLE_TTS", "false").lower() == "true"
ENABLE_IMAGE_PROVIDER = os.getenv("ENABLE_IMAGE_PROVIDER", "false").lower() == "true"

# Files
CHAT_LOGS_PATH = os.getenv("CHAT_LOGS_PATH", str(PROJECT_ROOT / "data" / "chat_logs.json"))
MEMORY_STORE_PATH = os.getenv("MEMORY_STORE_PATH", str(PROJECT_ROOT / "data" / "memory_store.json"))

# App
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))
ADMIN_TOKEN = os.getenv("NEURA_ADMIN_TOKEN", "change_me_admin_token")
# Premium Hyperluxe Options
ENABLE_NEON_UI: bool = os.getenv("ENABLE_NEON_UI", "true").lower() == "true"
MAX_CONCURRENT_REQUESTS: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR