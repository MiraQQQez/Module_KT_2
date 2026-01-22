from __future__ import annotations

from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from core.pages.base_page import BasePage


@dataclass
class LoginPage(BasePage):
    """Page Object для страницы логина."""

    PATH = "/login"

    USERNAME_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    FLASH_MESSAGE = (By.ID, "flash")

    PROFILE_HEADER = (By.ID, "profile-header")
    USER_EMAIL_VALUE = (By.ID, "user-email")
    LOGOUT_BUTTON = (By.ID, "logout-button")

    def open_login(self) -> None:
        """Открыть страницу логина."""

        self.open(self.PATH)

    def login(self, username: str, password: str) -> None:
        """Войти в систему."""

        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

        WebDriverWait(self.driver, self.timeout_seconds).until(
            EC.any_of(
                EC.presence_of_element_located(self.FLASH_MESSAGE),
                EC.presence_of_element_located(self.LOGOUT_BUTTON),
            )
        )

    def logout(self) -> None:
        """Выйти из системы."""

        self.click(self.LOGOUT_BUTTON)

        WebDriverWait(self.driver, self.timeout_seconds).until(
            EC.presence_of_element_located(self.FLASH_MESSAGE)
        )

    def flash_message(self) -> str:
        """Сообщение об ошибке/успехе (верхний алерт)."""

        return self.wait_present(self.FLASH_MESSAGE).text.strip()

    def is_logged_in(self) -> bool:
        """Признак, что пользователь в защищённой зоне."""

        return self.is_visible_with_timeout(self.LOGOUT_BUTTON, 2) and self.is_visible_with_timeout(
            self.PROFILE_HEADER, 2
        )

    def current_user_email(self) -> str:
        """Email пользователя на странице профиля."""

        return self.wait_present(self.USER_EMAIL_VALUE).text.strip()
