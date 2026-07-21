"""
Analytics Engine
AI Robo Advisor
"""

from datetime import datetime

from database.database import Database


class AnalyticsEngine:

    def __init__(self):

        self.db = Database()
        self.db.initialize()

    def save_snapshot(self, capital, portfolio):

        portfolio_value = round(
            sum(item["shares"] * item["price"] for item in portfolio),
            2
        )

        profit = round(
            portfolio_value - capital,
            2
        )

        profit_percent = round(
            (profit / capital) * 100,
            2
        ) if capital else 0

        self.db.save_portfolio_snapshot(
            snapshot_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            capital=capital,
            portfolio_value=portfolio_value,
            profit=profit,
            profit_percent=profit_percent
        )

        return {
            "capital": capital,
            "portfolio_value": portfolio_value,
            "profit": profit,
            "profit_percent": profit_percent
        }

    def history(self):

        return self.db.get_portfolio_history()

    def close(self):

        self.db.close()