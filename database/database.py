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

        self.connection.commit()

    def execute(self, sql, params=()):

        self.cursor.execute(sql, params)

        self.connection.commit()

    def query(self, sql, params=()):

        self.cursor.execute(sql, params)

        return self.cursor.fetchall()

    def close(self):

        self.connection.close()