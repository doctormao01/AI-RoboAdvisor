"""
Rebalance Engine
AI Robo Advisor
"""

import json
from pathlib import Path


class RebalanceEngine:

    def __init__(
        self,
        current_file="portfolio/current_portfolio.json",
        target_file="portfolio/target_portfolio.json",
        orders_file="portfolio/rebalance_orders.json",
    ):
        self.current_file = Path(current_file)
        self.target_file = Path(target_file)
        self.orders_file = Path(orders_file)

    def _load(self, path):
        if not path.exists():
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save(self, data):
        self.orders_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.orders_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def generate(self, tolerance=1.0):
        current = {p["symbol"]: p for p in self._load(self.current_file)}
        target = {p["symbol"]: p for p in self._load(self.target_file)}

        symbols = sorted(set(current) | set(target))
        orders = []

        for symbol in symbols:
            cur = current.get(symbol, {})
            tar = target.get(symbol, {})

            current_amount = float(cur.get("amount", 0.0))
            target_amount = float(tar.get("amount", 0.0))
            delta = round(target_amount - current_amount, 2)

            if abs(delta) <= tolerance:
                action = "HOLD"
            elif delta > 0:
                action = "BUY"
            else:
                action = "SELL"

            orders.append({
                "symbol": symbol,
                "action": action,
                "current_amount": round(current_amount, 2),
                "target_amount": round(target_amount, 2),
                "difference": delta,
            })

        self._save(orders)
        return orders

    def print(self, orders):
        print()
        print("=" * 78)
        print(" AI ROBO ADVISOR REBALANCE ")
        print("=" * 78)
        print(f'{"ETF":<8} {"AZIONE":<8} {"ATTUALE":>12} {"TARGET":>12} {"DELTA":>12}')
        print("-" * 78)
        for o in orders:
            print(
                f'{o["symbol"]:<8}'
                f'{o["action"]:<8}'
                f'{o["current_amount"]:>12.2f}'
                f'{o["target_amount"]:>12.2f}'
                f'{o["difference"]:>12.2f}'
            )
        print("=" * 78)

    def run(self):
        orders = self.generate()
        self.print(orders)
        return orders
