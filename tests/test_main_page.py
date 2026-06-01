import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from data import questions_answers
from pages.main_page import MainPage
from urls import BASE_URL, ORDER_PAGE_URL

@allure.feature("Главная страница")
class TestMainPage:

    @allure.story("Выпадающий список в разделе «Вопросы о важном»")
    @pytest.mark.parametrize("num, expected_text", questions_answers)
    def test_questions_and_answers(self, driver, num, expected_text):
        main_page = MainPage(driver)
        main_page.click_to_question(num)
        actual_text = main_page.get_answer_text(num)
        assert actual_text == expected_text, f"Текст ответа на вопрос {num} не совпадает"

    @allure.story("Логотип Самоката ведёт на главную страницу")
    def test_samokat_logo_redirect(self, driver):
        main_page = MainPage(driver)
        driver.get(ORDER_PAGE_URL)
        main_page.click_samokat_logo()
        assert driver.current_url == BASE_URL

    @allure.story("Логотип Яндекса открывает Дзен в новой вкладке")
    def test_yandex_logo_opens_dzen(self, driver):
        main_page = MainPage(driver)
        original_windows = driver.window_handles
        main_page.click_yandex_logo()
        WebDriverWait(driver, 10).until(EC.new_window_is_opened(original_windows))
        new_window = [w for w in driver.window_handles if w not in original_windows][0]
        driver.switch_to.window(new_window)
        WebDriverWait(driver, 10).until(EC.url_contains("dzen.ru"))
        assert "dzen.ru" in driver.current_url
        driver.close()
        driver.switch_to.window(original_windows[0])