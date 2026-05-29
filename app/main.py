from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import Config
from app.database import Database
from app.storage import UrlStorage


app = FastAPI(title="URL Shortener")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

database = Database(Config.DB_PATH)
storage = UrlStorage(database, Config.MAX_URLS)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "urls": storage.get_all_urls(),
            "base_url": Config.BASE_URL,
            "short_url": None,
            "error": None,
            "max_urls": Config.MAX_URLS
        }
    )


@app.post("/shorten")
def shorten(request: Request, original_url: str = Form(...)):
    if not original_url.startswith("http://") and not original_url.startswith("https://"):
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "urls": storage.get_all_urls(),
                "base_url": Config.BASE_URL,
                "short_url": None,
                "error": "URL должен начинаться с http:// или https://",
                "max_urls": Config.MAX_URLS
            }
        )

    item = storage.shorten_url(original_url)
    short_url = f"{Config.BASE_URL}/{item.short_code}"

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "urls": storage.get_all_urls(),
            "base_url": Config.BASE_URL,
            "short_url": short_url,
            "error": None,
            "max_urls": Config.MAX_URLS
        }
    )


@app.get("/{short_code}")
def redirect_to_original(short_code: str):
    item = storage.add_click(short_code)

    if item is None:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")

    return RedirectResponse(url=item.original_url)