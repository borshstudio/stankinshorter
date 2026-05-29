from datetime import datetime


class UrlItem:
    """
    Класс одной сокращённой ссылки.
    """

    def __init__(
        self,
        id: int,
        original_url: str,
        short_code: str,
        clicks: int,
        created_at: str
    ):
        self.id = id
        self.original_url = original_url
        self.short_code = short_code
        self.clicks = clicks
        self.created_at = created_at