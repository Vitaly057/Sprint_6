import pytest
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

@pytest.fixture
def driver():
    options = FirefoxOptions()
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    driver.get(os.getenv('BASE_URL', 'https://qa-scooter.praktikum-services.ru/'))
    yield driver
    driver.quit()