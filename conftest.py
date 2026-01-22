import pytest

from core.fixtures.browser_fixture import BrowserFixture

from marketplace_app.app import create_app


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Выбор браузера: chrome | firefox | edge",
    )

    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск браузера в headless-режиме (без окна)",
    )

    parser.addoption(
        "--base-url",
        action="store",
        default="",
        help=(
            "Базовый URL тестируемого сайта. Если не указан, используется локальный демо-сервер." 
            " Пример: http://localhost:8080"
        ),
    )


@pytest.fixture(scope="function")
def browser(request):
    """Фикстура браузера на 1 тест.

    Делается function-scope, чтобы тесты были независимы и не ломали друг друга,
    если сессия WebDriver внезапно завершится.
    """

    browser_name = request.config.getoption("--browser")
    headless = bool(request.config.getoption("--headless"))
    factory = BrowserFixture(browser_name=browser_name, headless=headless)

    driver = factory.create_driver()
    driver.set_window_size(1400, 900)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(2)

    try:
        yield driver
    finally:
        try:
            driver.quit()
        except Exception:
            pass


@pytest.fixture(scope="session")
def demo_server() -> str:
    """Поднимает локальный демо-сервер маркетплейса и возвращает его base_url."""

    from threading import Thread

    from werkzeug.serving import make_server

    app = create_app()

    server = make_server("127.0.0.1", 0, app)
    port = int(server.server_port)

    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()


@pytest.fixture(scope="session")
def base_url(request, demo_server) -> str:
    """Базовый URL для Page Object'ов.

    По умолчанию используется локальный демо-сервер.
    Можно переопределить через параметр командной строки --base-url.
    """

    overridden = (request.config.getoption("--base-url") or "").strip()
    return overridden if overridden else demo_server
