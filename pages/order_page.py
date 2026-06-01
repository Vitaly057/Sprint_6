import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.order_page_locators import OrderPageLocators


class OrderPage(BasePage):

    def is_page_loaded(self):
        # Более лаконичный способ проверить наличие элемента
        return self.wait.until(EC.presence_of_element_located(OrderPageLocators.NAME_FIELD)) is not None

    def is_rental_step_loaded(self):
        return self.wait.until(EC.presence_of_element_located(OrderPageLocators.DATE_FIELD)) is not None

    @allure.step("Выбор станции метро: {metro_station}")
    def _select_metro_station(self, metro_station):
        metro_field = self.wait.until(
            EC.element_to_be_clickable(OrderPageLocators.METRO_FIELD)
        )
        metro_field.click()
        metro_field.clear()
        metro_field.send_keys(metro_station)

        metro_option = (
            OrderPageLocators.METRO_OPTION[0],
            OrderPageLocators.METRO_OPTION[1].format(metro_station),
        )
        try:
            self.reliable_click(metro_option)
        except TimeoutException as e: # <--- ИСПРАВЛЕННЫЙ ОТСТУП
            allure.attach(f"Не удалось выбрать станцию через клик. Падаем обратно на ввод. Ошибка: {e}", "Fallback Log",
                          attachment_type=allure.attachment_type.TEXT)
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
        self.wait.until(EC.visibility_of_element_located(OrderPageLocators.DATE_FIELD))

    @staticmethod
    def _to_data_day(date: str) -> str:
        """Преобразует 01.06.2026 в формат data-day календаря: 1.6.2026."""
        day, month, year = date.split(".")
        return f"{int(day)}.{int(month)}.{year}"

    def _close_datepicker(self):
        try:
            self.wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".react-datepicker"))
            )
        except TimeoutException:
            self.driver.find_element(*OrderPageLocators.DATE_FIELD).send_keys(Keys.ESCAPE)

    @allure.step("Выбор даты доставки: {date}")
    def _select_delivery_date(self, date: str):
        date_field = self.find_element_with_wait(OrderPageLocators.DATE_FIELD)
        date_field.click()
        date_field.clear()
        date_field.send_keys(date)

        data_day = self._to_data_day(date)
        day_locator = (
            OrderPageLocators.DATEPICKER_DAY[0],
            OrderPageLocators.DATEPICKER_DAY[1].format(data_day),
        )
        try:
            self.reliable_click(day_locator)
        except TimeoutException:
            date_field.send_keys(Keys.ENTER)
        self._close_datepicker()

    @allure.step("Выбор срока аренды: {period}")
    def _select_rental_period(self, period: str):
        dropdown = self.wait.until(
            lambda driver: next(
                (
                    element
                    for element in driver.find_elements(*OrderPageLocators.RENTAL_PERIOD_DROPDOWN)
                    if element.is_displayed()
                ),
                None,
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", dropdown
        )
        dropdown.click()
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.Dropdown-menu"))
        )

        period_locator = (
            By.XPATH,
            f"//div[contains(@class, 'Dropdown-option') and normalize-space()='{period}']",
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

    @allure.step("Проверка, что появилось сообщение об успешном заказе")
    def is_order_success_displayed(self):
        return self.find_element_with_wait(OrderPageLocators.SUCCESS_MODAL).is_displayed()
