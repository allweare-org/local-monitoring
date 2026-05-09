import sqlite3
from datetime import datetime

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self._init_table()

    def _init_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            timestamp TEXT,
            voltage REAL,
            current REAL,
            power REAL
        )
        """)

    def insert(self, data):
        self.conn.execute("""
        INSERT INTO readings VALUES (?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            data.get("voltage"),
            data.get("current"),
            data.get("power")
        ))
        self.conn.commit()
