from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


Locator = Tuple[str, str]


@dataclass
class BasePage:
    """Базовый класс Page Object.

    Содержит общие методы для навигации и ожиданий.
    """

    driver: WebDriver
    base_url: str
    timeout_seconds: int = 10

    def open(self, path: str) -> None:
        """Открыть страницу по относительному пути."""

        url = (self.base_url or "").rstrip("/") + "/" + path.lstrip("/")
        self.driver.get(url)

    def wait_visible(self, locator: Locator):
        """Дождаться, пока элемент станет видимым, и вернуть WebElement."""

        return WebDriverWait(self.driver, self.timeout_seconds).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_present(self, locator: Locator):
        """Дождаться, пока элемент появится в DOM, и вернуть WebElement."""

        return WebDriverWait(self.driver, self.timeout_seconds).until(
            EC.presence_of_element_located(locator)
        )

    def wait_clickable(self, locator: Locator):
        """Дождаться, пока элемент станет кликабельным, и вернуть WebElement."""

        return WebDriverWait(self.driver, self.timeout_seconds).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator: Locator) -> None:
        """Кликнуть по элементу."""

        self.wait_clickable(locator).click()

    def type(self, locator: Locator, text: str) -> None:
        """Ввести текст в поле ввода."""

        el = self.wait_visible(locator)
        el.clear()
        el.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        """Получить текст элемента."""

        return self.wait_visible(locator).text

    def is_visible(self, locator: Locator) -> bool:
        """Проверить, что элемент видим."""

        return self.is_visible_with_timeout(locator, timeout_seconds=1)

    def is_visible_with_timeout(self, locator: Locator, timeout_seconds: int) -> bool:
        """Проверить, что элемент видим за указанный таймаут."""

        try:
            WebDriverWait(self.driver, timeout_seconds).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False
