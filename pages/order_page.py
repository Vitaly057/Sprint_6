import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from locators.order_page_locators import OrderPageLocators
from pages.base_page import BasePage


class OrderPage(BasePage):

    @allure.step("Проверка загрузки страницы заказа")
    def is_page_loaded(self):
        return self.is_element_present(OrderPageLocators.NAME_FIELD)

    @allure.step("Проверка загрузки шага «Про аренду»")
    def is_rental_step_loaded(self):
        return self.is_element_visible(OrderPageLocators.DATE_FIELD)

    @allure.step("Выбор станции метро: {metro_station}")
    def _select_metro_station(self, metro_station):
        metro_field = self.wait_until_clickable(OrderPageLocators.METRO_FIELD)
        metro_field.click()
        metro_field.clear()
        metro_field.send_keys(metro_station)

        metro_option = self.format_locators(
            OrderPageLocators.METRO_OPTION, metro_station
        )
        try:
            self.reliable_click(metro_option)
        except TimeoutException:
            metro_field.send_keys(Keys.ARROW_DOWN)
            metro_field.send_keys(Keys.ENTER)

    @allure.step("Заполнение информации о клиенте")
    def fill_customer_info(self, name, surname, address, metro_station, phone):
        self.send_keys_to_element(OrderPageLocators.NAME_FIELD, name)
        self.send_keys_to_element(OrderPageLocators.SURNAME_FIELD, surname)
        self.send_keys_to_element(OrderPageLocators.ADDRESS_FIELD, address)
        self._select_metro_station(metro_station)
        self.send_keys_to_element(OrderPageLocators.PHONE_FIELD, phone)

    @allure.step("Клик на кнопку Далее")
    def click_next(self):
        self.reliable_click(OrderPageLocators.NEXT_BUTTON)
        self.wait_until_visible(OrderPageLocators.DATE_FIELD)

    @staticmethod
    def _to_data_day(date):
        day, month, year = date.split(".")
        return f"{int(day)}.{int(month)}.{year}"

    def _close_datepicker(self):
        if not self.wait_until_invisible(OrderPageLocators.DATEPICKER):
            self.send_escape_to_element(OrderPageLocators.DATE_FIELD)

    @allure.step("Выбор даты доставки: {date}")
    def _select_delivery_date(self, date):
        date_field = self.find_element_with_wait(OrderPageLocators.DATE_FIELD)
        date_field.click()
        date_field.clear()
        date_field.send_keys(date)

        day_locator = self.format_locators(
            OrderPageLocators.DATEPICKER_DAY,
            self._to_data_day(date),
        )
        try:
            self.reliable_click(day_locator)
        except TimeoutException:
            date_field.send_keys(Keys.ENTER)
        self._close_datepicker()

    @allure.step("Выбор срока аренды: {period}")
    def _select_rental_period(self, period):
        dropdown = self.find_visible_element(OrderPageLocators.RENTAL_PERIOD_DROPDOWN)
        self.click_element(dropdown)
        self.wait_until_present(OrderPageLocators.DROPDOWN_MENU)

        period_locator = self.format_locators(
            OrderPageLocators.RENTAL_PERIOD_OPTION, period
        )
        self.reliable_click(period_locator)

    @allure.step("Заполнение информации об аренде")
    def fill_rental_info(self, date, period, color, comment):
        self._select_delivery_date(date)
        self._select_rental_period(period)

        color_code = color.lower().replace("ё", "е")
        if color_code == "черный":
            self.reliable_click(OrderPageLocators.COLOR_BLACK)
        elif color_code == "серый":
            self.reliable_click(OrderPageLocators.COLOR_GREY)

        self.send_keys_to_element(OrderPageLocators.COMMENT_FIELD, comment)

    @allure.step("Клик на кнопку Заказать (финальная)")
    def click_order_button(self):
        self.reliable_click(OrderPageLocators.ORDER_BUTTON)

    @allure.step("Подтверждение заказа в диалоговом окне")
    def confirm_order(self):
        self.reliable_click(OrderPageLocators.CONFIRM_BUTTON)

    @allure.step("Проверка сообщения об успешном заказе")
    def is_order_success_displayed(self):
        return self.is_element_visible(OrderPageLocators.SUCCESS_MODAL)
