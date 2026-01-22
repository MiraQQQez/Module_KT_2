# Автотесты Selenium + Pytest (вход в систему)

## Требования
- Python 3.10+
- Установленный браузер (Chrome/Firefox/Edge)

## Установка зависимостей
```bash
pip install -r requirements.txt
```

## Запуск тестов
### Chrome (по умолчанию)
```bash
pytest
```

### Headless (рекомендуется)
```bash
pytest --headless
```

### Firefox
```bash
pytest --browser firefox
```

### Edge
```bash
pytest --browser edge
```

### Базовый URL (если нужно заменить демо-сервер)
```bash
pytest --base-url http://localhost:8080
```

## Демо-приложение
В проекте есть простое демо-веб-приложение "маркетплейс" на Flask.

Важно:
- Тесты **сами поднимают** локальный сервер (через фикстуру `demo_server`).
- Отдельно запускать сервер **не требуется**.

## Структура проекта
- `conftest.py` — фикстуры pytest и опции `--browser`, `--base-url`
- `core/fixtures/browser_fixture.py` — класс `BrowserFixture` (создание WebDriver)
- `core/pages/*` — Page Object'ы
- `marketplace_app/` — демо-приложение маркетплейса (Flask)
- `tests/` — тесты
- `REPORT.md` — отчёт по заданию

## Примечания
- Selenium 4.6+ обычно сам управляет драйверами через Selenium Manager.
- Если драйвер не находится автоматически, добавьте соответствующий драйвер (chromedriver/geckodriver/msedgedriver) в `PATH`.
