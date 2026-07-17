"""
Ranking Engine
AI Robo Advisor
"""

import sqlite3

from config import DATABASE_FILE


class RankingEngine:

    def __init__(self):

        self.connection = sqlite3.connect(DATABASE_FILE)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def top(self, limit=10):

        self.cursor.execute(
            """
            SELECT

                s.symbol,
                s.score,
                p.close,
                s.date

            FROM scores s

            INNER JOIN prices p

                ON s.symbol = p.symbol
               AND s.date = p.date

            WHERE s.date = (

                SELECT MAX(date)

                FROM scores x

                WHERE x.symbol = s.symbol

            )

            ORDER BY s.score DESC

            LIMIT ?

            """,
            (limit,)
        )

        rows = self.cursor.fetchall()

        ranking = []

        for row in rows:

            ranking.append(
                {
                    "symbol": row["symbol"],
                    "score": float(row["score"]),
                    "close": float(row["close"]),
                    "date": row["date"]
                }
            )

        return ranking

    def print(self, limit=10):

        ranking = self.top(limit)

        print()
        print("=" * 70)
        print(" AI ROBO ADVISOR RANKING ")
        print("=" * 70)

        for position, item in enumerate(ranking, start=1):

            print(
                f"{position:>2}. "
                f"{item['symbol']:<8}"
                f"{item['score']:>6.1f}   "
                f"€ {item['close']:>9.2f}"
            )

        print("=" * 70)

    def close(self):

        self.connection.close()