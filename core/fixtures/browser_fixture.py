from __future__ import annotations

from dataclasses import dataclass

from selenium import webdriver


@dataclass(frozen=True)
class BrowserFixture:
    """Класс-обёртка над созданием WebDriver.

    Хранит выбранный браузер и умеет создавать соответствующий драйвер.
    """

    browser_name: str
    headless: bool = False

    def create_driver(self):
        """Создать драйвер для выбранного браузера."""

        name = (self.browser_name or "").strip().lower()

        if name in {"firefox", "ff"}:
            options = webdriver.FirefoxOptions()
            if self.headless:
                options.add_argument("-headless")
            return webdriver.Firefox(options=options)

        if name in {"chrome", "ch"}:
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            return webdriver.Chrome(options=options)

        if name in {"edge", "msedge"}:
            options = webdriver.EdgeOptions()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            return webdriver.Edge(options=options)

        raise ValueError(
            "Неизвестный браузер: '{0}'. Допустимые значения: chrome, firefox, edge".format(
                self.browser_name
            )
        )
