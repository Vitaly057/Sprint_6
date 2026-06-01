import allure
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators

class MainPage(BasePage):

    @allure.step("Клик на кнопку Заказать ({location})")
    def click_order_button(self, location="top"):
        if location == "top":
            self.click_top_order_button()
        else:
            self.click_bottom_order_button()

    @allure.step("Клик на вопрос с номером {num}")
    def click_to_question(self, num):
        locator_q_formatted = self.format_locators(MainPageLocators.QUESTION_LOCATOR, num)
        self.scroll_to_element(locator_q_formatted)
        self.reliable_click(locator_q_formatted)

    @allure.step("Получение текста ответа на вопрос {num}")
    def get_answer_text(self, num):
        locator_a_formatted = self.format_locators(MainPageLocators.ANSWER_LOCATOR, num)
        return self.get_text_from_element(locator_a_formatted)

    @allure.step("Клик на верхнюю кнопку Заказать")
    def click_top_order_button(self):
        self.reliable_click(MainPageLocators.TOP_ORDER_BUTTON)

    @allure.step("Клик на нижнюю кнопку Заказать")
    def click_bottom_order_button(self):
        self.reliable_click(MainPageLocators.BOTTOM_ORDER_BUTTON)

    @allure.step("Клик на логотип Самоката")
    def click_samokat_logo(self):
        self.reliable_click(MainPageLocators.SAMOKAT_LOGO)

    @allure.step("Клик на логотип Яндекса")
    def click_yandex_logo(self):
        self.reliable_click(MainPageLocators.YANDEX_LOGO)