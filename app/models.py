from datetime import datetime


class UrlItem:
    """
    Класс одной сокращённой ссылки.
    """

    def __init__(self, original_url: str, short_code: str):
        self.original_url = original_url
        self.short_code = short_code
        self.clicks = 0
        self.created_at = datetime.now()

    def add_click(self):
        self.clicks += 1