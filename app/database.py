import sqlite3


class Database:

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.create_tables()

    def connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_tables(self):
        """
        Создаёт таблицу urls, если её ещё нет.
        """

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL UNIQUE,
                short_code TEXT NOT NULL UNIQUE,
                clicks INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_short_code
            ON urls(short_code)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_original_url
            ON urls(original_url)
            """
        )

        connection.commit()
        connection.close()