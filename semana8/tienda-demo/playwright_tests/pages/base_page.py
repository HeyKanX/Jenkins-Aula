"""Operaciones comunes para las páginas Playwright de TiendaDemo."""
import os
from pathlib import Path

class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url=None):
        if url is None:
            url = (Path(__file__).resolve().parents[2] / "app" / "tienda_demo.html").as_uri()
        url = os.getenv("TIENDA_DEMO_URL", url)
        self.page.goto(url)

    def click(self, selector):
        self.page.locator(selector).click()

    def fill(self, selector, value):
        self.page.locator(selector).fill(value)

    def text(self, selector):
        return self.page.locator(selector).inner_text()

    def exists(self, selector):
        return self.page.locator(selector).count() > 0

    def visible(self, selector):
        return self.page.locator(selector).is_visible()

