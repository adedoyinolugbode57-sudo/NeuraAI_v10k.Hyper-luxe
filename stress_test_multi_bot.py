"""
stress_test_multi_bot.py
Performance stress test for MultiBotManager (handles 50+ concurrent bots)
Now includes logging to logs/stress_test_report.txt
"""

import asyncio
import random
import time
import os
from datetime import datetime
from multi_bot_manager import MultiBotManager


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "stress_test_report.txt")


def log(message: str):
    """Append a timestamped line to the log file."""
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")


async def stress_test(duration=30, bots=50):
    """Runs a stress test for multiple concurrent bots."""
    print(f"🚀 Starting stress test: {bots} bots for {duration} seconds...")
    log(f"Starting stress test: {bots} bots for {duration}s")

    start_time = time.time()
    manager = MultiBotManager(max_bots=bots)

    strategies = ["scalping", "momentum", "mean_reversion", "arbitrage", "swing"]
    for i in range(bots):
        manager.create_bot(random.choice(strategies))

    await manager.start_all()
    await asyncio.sleep(duration)

    print("\n📊 Gathering stress test results...")
    log("Collecting test results...")

    avg_profit = manager.get_average_profit()
    summary = manager.quick_summary()

    report_lines = [
        "\n========= 🧠 STRESS TEST COMPLETE 🧠 =========",
        f"⏱️  Runtime: {round(time.time() - start_time, 2)}s",
        f"🤖  Bots Tested: {len(manager.bots)}",
        f"💹  Average Profit per Trade: ${avg_profit:.2f}",
        f"📈  Active Bots: {summary['active_bots']}",
        f"💰  System-Wide Avg Profit: {summary['avg_profit']}",
        "==============================================",
    ]

    for line in report_lines:
        print(line)
        log(line)

    await manager.stop_all()
    log("Stress test finished successfully.\n")


if __name__ == "__main__":
    asyncio.run(stress_test(duration=30, bots=50))