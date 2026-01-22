from core.pages.login_page import LoginPage


VALID_USERNAME = "user@example.com"
VALID_PASSWORD = "Password123!"


def test_login_success(browser, base_url):
    page = LoginPage(browser, base_url)
    page.open_login()

    page.login(VALID_USERNAME, VALID_PASSWORD)

    assert page.is_logged_in() is True
    assert page.current_user_email() == VALID_USERNAME


def test_login_invalid_password(browser, base_url):
    page = LoginPage(browser, base_url)
    page.open_login()

    page.login(VALID_USERNAME, "wrong_password")

    assert page.is_logged_in() is False
    assert "Неверный email или пароль" in page.flash_message()


def test_login_invalid_username(browser, base_url):
    page = LoginPage(browser, base_url)
    page.open_login()

    page.login("wrong_user@example.com", VALID_PASSWORD)

    assert page.is_logged_in() is False
    assert "Неверный email или пароль" in page.flash_message()


def test_login_empty_credentials(browser, base_url):
    page = LoginPage(browser, base_url)
    page.open_login()

    page.login("", "")

    assert page.is_logged_in() is False
    assert "Поля email и пароль обязательны" in page.flash_message()


def test_logout_after_login(browser, base_url):
    page = LoginPage(browser, base_url)
    page.open_login()

    page.login(VALID_USERNAME, VALID_PASSWORD)
    assert page.is_logged_in() is True

    page.logout()

    assert page.is_logged_in() is False
    assert "Вы вышли из системы" in page.flash_message()
