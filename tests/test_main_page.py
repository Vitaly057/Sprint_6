import allure
import pytest

from data import questions_answers
from pages.main_page import MainPage


@allure.feature("Главная страница")
class TestMainPage:

    @allure.title("Выпадающий список в разделе «Вопросы о важном»")
    @pytest.mark.parametrize("num, expected_text", questions_answers)
    def test_questions_and_answers(self, driver, num, expected_text):
        main_page = MainPage(driver)
        main_page.click_to_question(num)
        actual_text = main_page.get_answer_text(num)
        assert actual_text == expected_text, f"Текст ответа на вопрос {num} не совпадает"

    @allure.title("Логотип Самоката ведёт на главную страницу")
    def test_samokat_logo_redirect(self, driver):
        main_page = MainPage(driver)
        main_page.open_order_page()
        main_page.click_samokat_logo()
        assert main_page.is_main_page_opened()

    @allure.title("Логотип Яндекса открывает Дзен в новой вкладке")
    def test_yandex_logo_opens_dzen(self, driver):
        main_page = MainPage(driver)
        original_windows = main_page.get_window_handles()
        main_page.switch_to_dzen_tab(original_windows)
        assert main_page.is_dzen_opened()
        main_page.close_tab_and_switch_to(original_windows[0])
