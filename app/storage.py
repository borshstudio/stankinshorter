import random
import string
from datetime import datetime
from app.models import UrlItem


class UrlStorage:
    """
    Класс-хранилище ссылок.
    """

    def __init__(self, database, max_urls: int):
        self.database = database
        self.max_urls = max_urls

    def row_to_item(self, row):
        """
        Преобразует строку из базы данных в объект UrlItem.
        """

        if row is None:
            return None

        return UrlItem(
            id=row["id"],
            original_url=row["original_url"],
            short_code=row["short_code"],
            clicks=row["clicks"],
            created_at=row["created_at"]
        )

    def generate_code(self, length: int = 6) -> str:
        symbols = string.ascii_letters + string.digits

        while True:
            code = ""

            for _ in range(length):
                code += random.choice(symbols)

            if self.get_by_code(code) is None:
                return code

    def get_count(self) -> int:
        """
        Возвращает количество сохранённых ссылок.
        """

        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) AS count FROM urls")
        row = cursor.fetchone()

        connection.close()

        return row["count"]

    def shorten_url(self, original_url: str):
        """
        Создаёт короткую ссылку.
        """

        existing_item = self.get_by_original_url(original_url)

        if existing_item is not None:
            return existing_item

        if self.get_count() >= self.max_urls:
            self.delete_worst_url()

        short_code = self.generate_code()
        created_at = datetime.now().isoformat()

        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO urls (original_url, short_code, clicks, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (original_url, short_code, 0, created_at)
        )

        connection.commit()
        connection.close()

        return self.get_by_code(short_code)

    def get_by_code(self, short_code: str):
        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM urls
            WHERE short_code = ?
            """,
            (short_code,)
        )

        row = cursor.fetchone()
        connection.close()

        return self.row_to_item(row)

    def get_by_original_url(self, original_url: str):
        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM urls
            WHERE original_url = ?
            """,
            (original_url,)
        )

        row = cursor.fetchone()
        connection.close()

        return self.row_to_item(row)

    def add_click(self, short_code: str):
        """
        Увеличивает количество переходов по короткой ссылке.
        """

        item = self.get_by_code(short_code)

        if item is None:
            return None

        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE urls
            SET clicks = clicks + 1
            WHERE short_code = ?
            """,
            (short_code,)
        )

        connection.commit()
        connection.close()

        return self.get_by_code(short_code)

    def delete_worst_url(self):
        """
        Удаляет ссылку с наименьшим количеством переходов.
        Если таких несколько — удаляется самая старая.
        """

        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM urls
            ORDER BY clicks ASC, created_at ASC
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        if row is not None:
            cursor.execute(
                """
                DELETE FROM urls
                WHERE id = ?
                """,
                (row["id"],)
            )

        connection.commit()
        connection.close()

    def get_all_urls(self):
        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM urls
            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()
        connection.close()

        result = []

        for row in rows:
            result.append(self.row_to_item(row))

        return result

    def clear(self):
        """
        Очищает таблицу.
        Нужно для тестов.
        """

        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM urls")

        connection.commit()
        connection.close()