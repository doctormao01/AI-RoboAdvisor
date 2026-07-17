"""
Portfolio Engine
AI Robo Advisor
"""

import json
from pathlib import Path

from core.ranking_engine import RankingEngine


class PortfolioEngine:

    def __init__(self, capital=4000.0):
        self.capital = float(capital)
        self.ranking = RankingEngine()

    def build(self, limit=5):

        ranking = self.ranking.top(limit)

        if not ranking:
            return []

        total_power = sum(item["score"] ** 2 for item in ranking)

        portfolio = []

        for item in ranking:

            weight = (item["score"] ** 2) / total_power

            amount = round(self.capital * weight, 2)

            close = item["close"]

            shares = round(amount / close, 6) if close else 0.0

            portfolio.append({
                "symbol": item["symbol"],
                "score": item["score"],
                "price": close,
                "weight": round(weight * 100, 2),
                "amount": amount,
                "shares": shares,
                "date": item["date"]
            })

        return portfolio

    def save(self, portfolio,
             filename="portfolio/portfolio.json"):

        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(portfolio, f, indent=4)

    def print(self, portfolio):

        print()
        print("=" * 78)
        print(" AI ROBO ADVISOR PORTFOLIO ")
        print("=" * 78)
        print(f'{"ETF":<8} {"Score":>6} {"Peso%":>8} {"Importo":>12} {"Quote":>12}')
        print("-" * 78)

        for p in portfolio:
            print(
                f'{p["symbol"]:<8}'
                f'{p["score"]:>6.1f}'
                f'{p["weight"]:>8.2f}'
                f'{p["amount"]:>12.2f}'
                f'{p["shares"]:>12.4f}'
            )

        print("=" * 78)

    def run(self, capital=None):

        if capital is not None:
            self.capital = float(capital)

        portfolio = self.build()

        self.print(portfolio)

        self.save(portfolio)

        return portfolio

    def close(self):
        self.ranking.close()
