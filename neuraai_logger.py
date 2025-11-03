# ==========================================================
# 🌌 Neuraluxe-AI — Environment & System Logger
# Author: Joshua_Dav
# Purpose: Validate environment variables + structured logging
# ==========================================================

import os, sys, logging
from datetime import datetime
from dotenv import load_dotenv

# -----------------------------
# LOAD ENVIRONMENT
# -----------------------------
load_dotenv()

# -----------------------------
# LOGGING CONFIGURATION
# -----------------------------
LOG_FILE = "neuraai_startup.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
    ]
)

logger = logging.getLogger("NeuraAI_Logger")

# -----------------------------
# ENVIRONMENT SUMMARY
# -----------------------------
ENV_KEYS = [
    "APP_NAME", "APP_VERSION", "FLASK_ENV", "PORT",
    "DATABASE_URL", "VOICE_ENGINE", "TTS_LANG",
    "CACHE_TYPE", "CRYPTO_API", "OPENFDA_API_BASE",
    "NEURA_DEV_FREE_EMAIL", "OPENAI_ENABLED", "LOG_LEVEL"
]

def summarize_env():
    logger.info("🛰️  Booting Neuraluxe-AI Environment Check...")
    missing = []
    for key in ENV_KEYS:
        val = os.getenv(key)
        if val:
            if "KEY" in key or "PASS" in key:
                logger.info(f"{key} = ✅ [SECURE VALUE LOADED]")
            else:
                logger.info(f"{key} = {val}")
        else:
            logger.warning(f"{key} = ⚠️ Missing")
            missing.append(key)
    if not missing:
        logger.info("✅ All critical environment variables loaded successfully.")
    else:
        logger.warning(f"⚠️ Missing {len(missing)} keys: {', '.join(missing)}")

# -----------------------------
# STARTUP LOG ENTRY
# -----------------------------
def log_startup():
    logger.info("===========================================================")
    logger.info(f"🚀 Neuraluxe-AI Startup | Time: {datetime.utcnow().isoformat()} UTC")
    logger.info(f"🌍 Running in region: {os.getenv('DEPLOY_REGION', 'unknown')}")
    logger.info(f"📦 Version: {os.getenv('APP_VERSION', 'v10k')} | Stage: {os.getenv('PROJECT_STAGE', 'production')}")
    logger.info("===========================================================")
    summarize_env()

if __name__ == "__main__":
    log_startup()