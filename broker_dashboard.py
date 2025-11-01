"""
Neuraluxe-AI Stress-Test Visual Dashboard
----------------------------------------
Real-time console dashboard for monitoring broker_adapter tests.
Integrates with test_broker_adapter.py or any async trading simulation.
"""

import asyncio
import random
import time
import statistics
from collections import deque
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich.live import Live
from rich.text import Text

console = Console()

# Metrics buffer
latencies = deque(maxlen=200)
success_count = 0
fail_count = 0
requests_count = 0
start_time = time.time()

# Visualization config
MAX_BOTS = 30
MAX_RATE = 60  # max orders/sec visual scale
REFRESH_INTERVAL = 0.2  # seconds

# Fake load generator for demo or offline mode
async def mock_broker_activity():
    global success_count, fail_count, requests_count
    while True:
        await asyncio.sleep(random.uniform(0.02, 0.1))
        latency = random.uniform(0.05, 0.4)
        latencies.append(latency)
        requests_count += 1
        if random.random() < 0.9:
            success_count += 1
        else:
            fail_count += 1


def render_dashboard():
    global success_count, fail_count, requests_count

    elapsed = max(time.time() - start_time, 1)
    total = success_count + fail_count
    rate = total / elapsed
    avg_latency = statistics.mean(latencies) if latencies else 0
    success_rate = (success_count / total * 100) if total else 0

    # Table for summary
    table = Table(expand=True)
    table.add_column("Metric", justify="left", style="cyan")
    table.add_column("Value", justify="right", style="bold white")

    table.add_row("🧠 Active Bots", f"{random.randint(20, MAX_BOTS)} / {MAX_BOTS}")
    table.add_row("⚡ Throughput", f"{rate:,.1f} req/sec")
    table.add_row("📈 Success Rate", f"{success_rate:.1f}%")
    table.add_row("⏱ Avg Latency", f"{avg_latency*1000:.1f} ms")
    table.add_row("✅ Success", str(success_count))
    table.add_row("❌ Failures", str(fail_count))

    # Load bar panel
    load_percent = min(rate / MAX_RATE, 1.0)
    bar_length = 40
    filled = int(bar_length * load_percent)
    bar = "█" * filled + "░" * (bar_length - filled)

    load_panel = Panel(
        Text(f"{bar}\nLoad: {load_percent*100:.1f}%", justify="center"),
        title="[bold magenta]System Load[/bold magenta]",
        border_style="magenta",
    )

    return Panel.fit(
        table, title="[bold blue]Neuraluxe-AI Broker Stress Dashboard[/bold blue]"
    ), load_panel


async def live_dashboard():
    """Continuously updates dashboard every REFRESH_INTERVAL seconds."""
    task = asyncio.create_task(mock_broker_activity())
    with Live(refresh_per_second=5, console=console, screen=True):
        while True:
            info_panel, load_panel = render_dashboard()
            layout = Table.grid(expand=True)
            layout.add_row(info_panel)
            layout.add_row(load_panel)
            console.print(layout)
            await asyncio.sleep(REFRESH_INTERVAL)
            console.clear()


if __name__ == "__main__":
    console.print("[bold green]🚀 Starting Neuraluxe-AI Broker Dashboard...[/bold green]")
    console.print("Press Ctrl+C to stop.\n")
    try:
        asyncio.run(live_dashboard())
    except KeyboardInterrupt:
        console.print("\n[bold red]⛔ Dashboard stopped by user.[/bold red]")