# ===========================================================
# 🌌 Neuraluxe-AI Monitor — Production Worker
# Purpose: Metrics, Analytics, Error Tracking & User Load
# ===========================================================

import os
import time
import logging
import redis
import requests
from datetime import datetime
from threading import Thread

# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("Neuraluxe-Monitor")

# -----------------------------
# Environment Variables
# -----------------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
ENABLE_USER_ANALYTICS = os.getenv("ENABLE_USER_ANALYTICS", "true").lower() == "true"
ENABLE_CRYPTO_ANALYTICS = os.getenv("ENABLE_CRYPTO_ANALYTICS", "true").lower() == "true"
ENABLE_ERROR_MONITORING = os.getenv("ENABLE_ERROR_MONITORING", "true").lower() == "true"

# -----------------------------
# Redis Connection
# -----------------------------
try:
    redis_client = redis.from_url(REDIS_URL)
    logger.info("Connected to Redis successfully.")
except Exception as e:
    logger.error(f"Redis connection failed: {e}")
    redis_client = None

# -----------------------------
# Dummy Metrics & Analytics
# -----------------------------
def track_user_activity():
    while True:
        try:
            if ENABLE_USER_ANALYTICS and redis_client:
                # Simulate user activity tracking
                active_users = int(redis_client.get("active_users") or 0)
                active_users += 1
                redis_client.set("active_users", active_users)
                logger.info(f"Active users count: {active_users}")
        except Exception as e:
            if ENABLE_ERROR_MONITORING:
                logger.error(f"User activity tracking error: {e}")
        time.sleep(30)  # every 30 seconds

def track_crypto_data():
    while True:
        try:
            if ENABLE_CRYPTO_ANALYTICS:
                # Fetch dummy crypto price
                response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd")
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"Crypto Prices: BTC ${data['bitcoin']['usd']} | ETH ${data['ethereum']['usd']}")
                else:
                    logger.warning("Failed to fetch crypto prices.")
        except Exception as e:
            if ENABLE_ERROR_MONITORING:
                logger.error(f"Crypto tracking error: {e}")
        time.sleep(60)  # every minute

def track_system_metrics():
    while True:
        try:
            if ENABLE_METRICS and redis_client:
                # Example: memory and CPU dummy metrics
                memory_usage = redis_client.info().get("used_memory_human", "0B")
                clients_connected = redis_client.info().get("connected_clients", 0)
                logger.info(f"System Metrics -> Memory: {memory_usage} | Redis Clients: {clients_connected}")
        except Exception as e:
            if ENABLE_ERROR_MONITORING:
                logger.error(f"System metrics error: {e}")
        time.sleep(45)

# -----------------------------
# Start Monitoring Threads
# -----------------------------
if __name__ == "__main__":
    logger.info("Starting Neuraluxe-AI Monitoring Worker...")

    threads = [
        Thread(target=track_user_activity, daemon=True),
        Thread(target=track_crypto_data, daemon=True),
        Thread(target=track_system_metrics, daemon=True)
    ]

    for t in threads:
        t.start()

    # Keep the main thread alive
    while True:
        time.sleep(60)