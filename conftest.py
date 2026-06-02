import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from urls import BASE_URL

_PROJECT_ROOT = Path(__file__).resolve().parent
_geckodriver_path = None


def _resolve_geckodriver_path():
    """Путь к geckodriver без повторных запросов к GitHub API."""
    global _geckodriver_path
    if _geckodriver_path:
        return _geckodriver_path

    env_path = os.getenv("GECKODRIVER_PATH")
    if env_path and Path(env_path).is_file():
        _geckodriver_path = env_path
        return _geckodriver_path

    local_driver = _PROJECT_ROOT / "geckodriver.exe"
    if local_driver.is_file():
        _geckodriver_path = str(local_driver)
        return _geckodriver_path

    wdm_cache = Path.home() / ".wdm" / "drivers" / "geckodriver"
    if wdm_cache.is_dir():
        cached = sorted(
            wdm_cache.rglob("geckodriver.exe"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        if cached:
            _geckodriver_path = str(cached[0])
            return _geckodriver_path

    _geckodriver_path = GeckoDriverManager().install()
    return _geckodriver_path


@pytest.fixture(scope="session")
def firefox_service():
    return Service(_resolve_geckodriver_path())


@pytest.fixture
def driver(firefox_service):
    options = FirefoxOptions()
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("-headless")

    browser = webdriver.Firefox(service=firefox_service, options=options)
    width = int(os.getenv("BROWSER_WIDTH", "1920"))
    height = int(os.getenv("BROWSER_HEIGHT", "1080"))
    browser.set_window_size(width, height)
    browser.get(os.getenv("BASE_URL", BASE_URL))

    yield browser
    browser.quit()
