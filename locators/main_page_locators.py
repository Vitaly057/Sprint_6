from selenium.webdriver.common.by import By

class MainPageLocators:
    # Кнопки "Заказать"
    TOP_ORDER_BUTTON = (By.XPATH, ".//button[@class='Button_Button__ra12g' and text()='Заказать']")
    BOTTOM_ORDER_BUTTON = (By.XPATH, "//button[text()='Заказать' and contains(@class, 'Button_Middle__1CSJM')]")

    # Логотипы
    SAMOKAT_LOGO = (By.XPATH, ".//img[@alt='Scooter']")
    YANDEX_LOGO = (By.XPATH, ".//img[@alt='Yandex']")

    # Аккордеон "Вопросы о важном"
    QUESTION_LOCATOR = (By.XPATH, ".//div[@id='accordion__heading-{}']")
    ANSWER_LOCATOR = (By.XPATH, ".//div[@id='accordion__panel-{}']/p")
    # Для скролла до нужного вопроса (можно использовать первый вопрос)
    QUESTION_TO_SCROLL = (By.XPATH, ".//div[@id='accordion__heading-0']")