from selenium.webdriver.common.by import By

class OrderPageLocators:
    # Первая страница (Для кого самокат)
    NAME_FIELD = (By.XPATH, ".//input[@placeholder='* Имя']")
    SURNAME_FIELD = (By.XPATH, ".//input[@placeholder='* Фамилия']")
    ADDRESS_FIELD = (By.XPATH, ".//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_FIELD = (By.XPATH, ".//input[@placeholder='* Станция метро']")
    METRO_OPTION = (
        By.XPATH,
        "//div[contains(@class, 'select-search__row') and normalize-space()='{}']",
    )
    PHONE_FIELD = (By.XPATH, ".//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, ".//button[text()='Далее']")

    # Вторая страница (Про аренду)
    DATE_FIELD = (By.XPATH, ".//input[@placeholder='* Когда привезти самокат']")
    DATEPICKER_DAY = (By.XPATH, "//div[contains(@class, 'react-datepicker')]//td[@data-day='{}']")
    RENTAL_PERIOD_DROPDOWN = (By.CSS_SELECTOR, "div.Dropdown-control")
    COLOR_BLACK = (By.ID, "black")
    COLOR_GREY = (By.ID, "grey")
    COMMENT_FIELD = (By.XPATH, ".//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, ".//div[@class='Order_Buttons__1xGrp']/button[text()='Заказать']")
    CONFIRM_BUTTON = (By.XPATH, ".//button[text()='Да']")

    # Сообщение об успешном заказе
    SUCCESS_MODAL = (By.XPATH, ".//div[contains(@class, 'Order_ModalHeader') and text()='Заказ оформлен']")