"""
Repository AI Score
"""


class ScoreRepository:

    def __init__(self, database):
        self.db = database

    def save(self, symbol, date, score):

        self.db.execute(
            """
            INSERT OR REPLACE INTO scores
            (
                symbol,
                date,
                score
            )

            VALUES(?,?,?)
            """,
            (
                symbol,
                date,
                score
            )
        )