import allure
import pytest
from pages.main_page import MainPage
from pages.order_page import OrderPage
from data import order_data


@allure.feature("Заказ самоката")
class TestOrder:

    @allure.story("Позитивный сценарий заказа с разными наборами данных")
    @pytest.mark.parametrize("data", order_data)
    def test_positive_order_flow(self, driver, data):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        with allure.step(f"Нажимаем на кнопку заказа ({data['button_location']})"):
            main_page.click_order_button(location=data["button_location"])
            assert order_page.is_page_loaded(), "Не удалось перейти на страницу заказа"

        with allure.step("Заполняем информацию о клиенте"):
            order_page.fill_customer_info(
                data["name"], data["surname"], data["address"],
                data["metro"], data["phone"],
            )
            order_page.click_next()
            assert order_page.is_rental_step_loaded(), "Не удалось перейти к шагу аренды"

        with allure.step("Заполняем информацию об аренде"):
            order_page.fill_rental_info(
                data["date"], data["period"],
                data["color"], data["comment"],
            )
            order_page.click_order_button()

        with allure.step("Подтверждаем заказ и проверяем результат"):
            order_page.confirm_order()
            try:
                assert order_page.is_order_success_displayed(), (
                    "Сообщение об успешном заказе не появилось"
                )
            except AssertionError:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot_on_fail",
                    attachment_type=allure.attachment_type.PNG,
                )
                raise
