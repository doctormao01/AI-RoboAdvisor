"""
Portfolio History
AI Robo Advisor
"""

import sqlite3

from config.config import DATABASE_FILE


class PortfolioHistory:

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.cursor = self.conn.cursor()

        self.initialize()

    def initialize(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS portfolio_history
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                date TEXT NOT NULL,

                capital REAL NOT NULL,

                portfolio_value REAL NOT NULL,

                profit REAL NOT NULL,

                profit_percent REAL NOT NULL
            )
            """
        )

        self.conn.commit()

    def save_snapshot(
        self,
        date,
        capital,
        portfolio_value,
        profit,
        profit_percent,
    ):

        self.cursor.execute(
            """
            INSERT INTO portfolio_history
            (
                date,
                capital,
                portfolio_value,
                profit,
                profit_percent
            )
            VALUES
            (
                ?,?,?,?,?,?
            )
            """,
            (
                date,
                capital,
                portfolio_value,
                profit,
                profit_percent,
            ),
        )

        self.conn.commit()

    def get_history(self):

        self.cursor.execute(
            """
            SELECT
                date,
                capital,
                portfolio_value,
                profit,
                profit_percent
            FROM portfolio_history
            ORDER BY id
            """
        )

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()