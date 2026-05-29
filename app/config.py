import os

class Config:
    MAX_URLS = int(os.getenv("MAX_URLS", 5))
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    DB_PATH = os.getenv("DB_PATH", "urls.db")