import allure

from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from urls import BASE_URL, ORDER_PAGE_URL


class MainPage(BasePage):

    @allure.step("Переход на страницу заказа")
    def open_order_page(self):
        self.open(ORDER_PAGE_URL)

    def is_main_page_opened(self):
        return self.get_current_url() == BASE_URL

    @allure.step("Клик на кнопку Заказать ({location})")
    def click_order_button(self, location="top"):
        if location == "top":
            self.click_top_order_button()
        else:
            self.click_bottom_order_button()

    @allure.step("Клик на вопрос с номером {num}")
    def click_to_question(self, num):
        locator_q = self.format_locators(MainPageLocators.QUESTION_LOCATOR, num)
        self.scroll_to_element(locator_q)
        self.reliable_click(locator_q)

    @allure.step("Получение текста ответа на вопрос {num}")
    def get_answer_text(self, num):
        locator_a = self.format_locators(MainPageLocators.ANSWER_LOCATOR, num)
        return self.get_text_from_element(locator_a)

    @allure.step("Клик на верхнюю кнопку Заказать")
    def click_top_order_button(self):
        self.reliable_click(MainPageLocators.TOP_ORDER_BUTTON)

    @allure.step("Клик на нижнюю кнопку Заказать")
    def click_bottom_order_button(self):
        self.scroll_to_element(MainPageLocators.BOTTOM_ORDER_BUTTON)
        self.reliable_click(MainPageLocators.BOTTOM_ORDER_BUTTON)

    @allure.step("Клик на логотип Самоката")
    def click_samokat_logo(self):
        self.reliable_click(MainPageLocators.SAMOKAT_LOGO)

    @allure.step("Клик на логотип Яндекса")
    def click_yandex_logo(self):
        self.reliable_click(MainPageLocators.YANDEX_LOGO)

    @allure.step("Открыть Дзен в новой вкладке")
    def switch_to_dzen_tab(self, original_handles):
        self.click_yandex_logo()
        self.wait_for_new_window(original_handles)
        new_window = [
            handle for handle in self.get_window_handles()
            if handle not in original_handles
        ][0]
        self.switch_to_window(new_window)
        self.wait_url_contains("dzen.ru")

    def is_dzen_opened(self):
        return "dzen.ru" in self.get_current_url()

    @allure.step("Закрыть вкладку и вернуться на главную")
    def close_tab_and_switch_to(self, window_handle):
        self.close_current_window()
        self.switch_to_window(window_handle)
