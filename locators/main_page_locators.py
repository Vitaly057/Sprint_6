from selenium.webdriver.common.by import By


class MainPageLocators:
    # Кнопки "Заказать"
    TOP_ORDER_BUTTON = (By.XPATH, ".//button[@class='Button_Button__ra12g' and text()='Заказать']")
    BOTTOM_ORDER_BUTTON = (
        By.XPATH,
        ".//button[@class='Button_Button__ra12g Button_UltraBig__UU3Lp' and text()='Заказать']",
    )

    # Логотипы
    SAMOKAT_LOGO = (By.XPATH, ".//img[@alt='Scooter']")
    YANDEX_LOGO = (By.XPATH, ".//img[@alt='Yandex']")

    # Аккордеон "Вопросы о важном"
    QUESTION_LOCATOR = (By.XPATH, ".//div[@id='accordion__heading-{}']")
    ANSWER_LOCATOR = (By.XPATH, ".//div[@id='accordion__panel-{}']/p")
