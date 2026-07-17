"""
Database Engine
AI Robo Advisor
"""

from pathlib import Path
import sqlite3

from config import DATABASE_FILE


class Database:

    def __init__(self):

        Path(DATABASE_FILE).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            DATABASE_FILE
        )

        self.cursor = self.connection.cursor()

    def initialize(self):

        # ==========================
        # TABELLA PREZZI
        # ==========================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT NOT NULL,

            date TEXT NOT NULL,

            open REAL,

            high REAL,

            low REAL,

            close REAL,

            volume REAL,

            provider TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(symbol,date)

        )
        """)

        # ==========================
        # TABELLA INDICATORI
        # ==========================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicators(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT NOT NULL,

            date TEXT NOT NULL,

            ema20 REAL,

            ema50 REAL,

            ema200 REAL,

            rsi REAL,

            macd REAL,

            signal REAL,

            histogram REAL,

            atr REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(symbol,date)

        )
        """)

        # ==========================
        # TABELLA AI SCORE
        # ==========================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT NOT NULL,

            date TEXT NOT NULL,

            score REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(symbol,date)

        )
        """)

        self.connection.commit()

    def execute(self, sql, params=()):

        self.cursor.execute(sql, params)

        self.connection.commit()

    def query(self, sql, params=()):

        self.cursor.execute(sql, params)

        return self.cursor.fetchall()

    def save_indicator(
        self,
        symbol,
        date,
        ema20,
        ema50,
        ema200,
        rsi,
        macd,
        signal,
        histogram,
        atr
    ):

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO indicators(

                symbol,
                date,
                ema20,
                ema50,
                ema200,
                rsi,
                macd,
                signal,
                histogram,
                atr

            )

            VALUES(?,?,?,?,?,?,?,?,?,?)

            """,
            (
                symbol,
                date,
                ema20,
                ema50,
                ema200,
                rsi,
                macd,
                signal,
                histogram,
                atr
            )
        )

        self.connection.commit()

    def save_score(
        self,
        symbol,
        date,
        score
    ):

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO scores(

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

        self.connection.commit()

    def close(self):

        self.connection.close()