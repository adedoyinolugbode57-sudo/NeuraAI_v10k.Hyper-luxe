"""
multi_bot_manager.py
Manages up to 50 AI trading bots per user with async control, scaling, and monitoring.
"""

import asyncio
import random
import time
from typing import Dict, List

class TradingBot:
    def __init__(self, bot_id: int, strategy: str):
        self.bot_id = bot_id
        self.strategy = strategy
        self.active = False
        self.balance = 10000.0
        self.profit_log = []
        self.start_time = None
    
    async def run(self):
        """Simulates trading cycles asynchronously."""
        self.active = True
        self.start_time = time.time()
        print(f"[BOT-{self.bot_id}] Started with strategy: {self.strategy}")
        try:
            while self.active:
                await asyncio.sleep(random.uniform(1.0, 3.0))
                profit = round(random.uniform(-100, 150), 2)
                self.balance += profit
                self.profit_log.append(profit)
                print(f"[BOT-{self.bot_id}] Profit tick: {profit} | Balance: {self.balance:.2f}")
        except asyncio.CancelledError:
            print(f"[BOT-{self.bot_id}] gracefully stopped.")
            self.active = False

    def stop(self):
        self.active = False
        print(f"[BOT-{self.bot_id}] Stopping...")

class MultiBotManager:
    def __init__(self, max_bots=50):
        self.max_bots = max_bots
        self.bots: Dict[int, TradingBot] = {}
        self.tasks: Dict[int, asyncio.Task] = {}
    
    def create_bot(self, strategy: str) -> str:
        """Create a new bot with a specific strategy."""
        if len(self.bots) >= self.max_bots:
            return "Bot limit reached. Upgrade required to deploy more bots."
        
        bot_id = len(self.bots) + 1
        bot = TradingBot(bot_id, strategy)
        self.bots[bot_id] = bot
        print(f"[MANAGER] Created bot #{bot_id} with strategy '{strategy}'")
        return f"Bot #{bot_id} ready."

    async def start_all(self):
        """Start all bots concurrently."""
        print("[MANAGER] Launching all bots...")
        for bot_id, bot in self.bots.items():
            if not bot.active:
                self.tasks[bot_id] = asyncio.create_task(bot.run())
        print(f"[MANAGER] {len(self.tasks)} bots are now running.")
    
    async def stop_all(self):
        """Stop all bots gracefully."""
        print("[MANAGER] Stopping all bots...")
        for bot in self.bots.values():
            bot.stop()
        for task in self.tasks.values():
            task.cancel()
        self.tasks.clear()
        await asyncio.sleep(1)
        print("[MANAGER] All bots stopped.")

    def bot_status_report(self) -> List[str]:
        """Return detailed status for all bots."""
        report = []
        for bot_id, bot in self.bots.items():
            uptime = (time.time() - bot.start_time) if bot.start_time else 0
            report.append(
                f"Bot {bot_id} | Strategy: {bot.strategy} | Balance: {bot.balance:.2f} | "
                f"Trades: {len(bot.profit_log)} | Uptime: {uptime:.1f}s"
            )
        return report

    def get_average_profit(self) -> float:
        """Calculate average profit across all bots."""
        total_profit = sum(sum(bot.profit_log) for bot in self.bots.values())
        total_trades = sum(len(bot.profit_log) for bot in self.bots.values())
        return total_profit / total_trades if total_trades else 0

    def remove_bot(self, bot_id: int) -> str:
        """Remove a bot by ID."""
        if bot_id not in self.bots:
            return f"Bot #{bot_id} not found."
        self.bots[bot_id].stop()
        self.bots.pop(bot_id)
        self.tasks.pop(bot_id, None)
        return f"Bot #{bot_id} removed."

    def quick_summary(self):
        """Short overview of current bot fleet."""
        return {
            "total_bots": len(self.bots),
            "active_bots": sum(1 for b in self.bots.values() if b.active),
            "avg_profit": round(self.get_average_profit(), 2)
        }

# Example usage
async def demo():
    manager = MultiBotManager(max_bots=50)
    strategies = ["scalping", "momentum", "mean_reversion", "arbitrage", "swing"]

    # Create 10 demo bots
    for i in range(10):
        manager.create_bot(random.choice(strategies))
    
    await manager.start_all()
    await asyncio.sleep(10)
    print("\n[REPORT]")
    for line in manager.bot_status_report():
        print(line)

    print("\n[SUMMARY]", manager.quick_summary())

    await manager.stop_all()

if __name__ == "__main__":
    asyncio.run(demo())