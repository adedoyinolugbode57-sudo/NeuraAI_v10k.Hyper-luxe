"""
analyze_logs.py
Analyzes stress_test_multi_bot.py logs and visualizes performance over time.
"""

import os
import re
from datetime import datetime
import matplotlib.pyplot as plt


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "stress_test_report.txt")


def parse_logs():
    """Extracts test results and timestamps from the log file."""
    if not os.path.exists(LOG_FILE):
        print("⚠️ No logs found. Run stress_test_multi_bot.py first.")
        return []

    pattern = r"Runtime: (\d+\.\d+)s.*?Bots Tested: (\d+).*?Average Profit per Trade: \$([\d\.]+)"
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    matches = re.findall(pattern, text, re.S)
    timestamps = re.findall(r"\[(.*?)\]", text)

    results = []
    for i, m in enumerate(matches):
        runtime, bots, profit = m
        ts = timestamps[i] if i < len(timestamps) else "Unknown"
        results.append({
            "timestamp": ts,
            "runtime": float(runtime),
            "bots": int(bots),
            "profit": float(profit)
        })
    return results


def show_summary(data):
    if not data:
        print("No data to analyze.")
        return

    avg_runtime = sum(d["runtime"] for d in data) / len(data)
    avg_profit = sum(d["profit"] for d in data) / len(data)
    total_tests = len(data)

    print("\n🧠 Neuraluxe-AI Stress Log Summary")
    print("─────────────────────────────────────")
    print(f"📅 Total Tests: {total_tests}")
    print(f"⏱️ Avg Runtime: {avg_runtime:.2f}s")
    print(f"💹 Avg Profit per Trade: ${avg_profit:.2f}")
    print(f"🤖 Last Test Bots: {data[-1]['bots']}")
    print(f"🕓 Last Test Time: {data[-1]['timestamp']}")
    print("─────────────────────────────────────\n")


def plot_results(data):
    if not data:
        return
    timestamps = [datetime.strptime(d["timestamp"], "%Y-%m-%d %H:%M:%S") for d in data]
    profits = [d["profit"] for d in data]
    runtimes = [d["runtime"] for d in data]

    plt.figure(figsize=(10, 6))
    plt.title("📈 Neuraluxe-AI Stress Performance Trends")
    plt.plot(timestamps, profits, label="Avg Profit ($)", marker="o")
    plt.plot(timestamps, runtimes, label="Runtime (s)", linestyle="--")
    plt.xlabel("Test Timestamp")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data = parse_logs()
    show_summary(data)
    plot_results(data)