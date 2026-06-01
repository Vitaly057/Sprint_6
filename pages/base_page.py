import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Форматирование локатора с подстановкой значения")
    def format_locators(self, locator, value):
        method, selector = locator
        return (method, selector.format(value))

    @allure.step("Поиск элемента с ожиданием видимости")
    def find_element_with_wait(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Надежный клик на элемент")
    def reliable_click(self, locator):
        """
        1. Ждет кликабельности.
        2. Скроллит к элементу.
        3. Кликает нативно; при ошибке — через JS.
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Скролл до элемента")
    def scroll_to_element(self, locator):
        element = self.find_element_with_wait(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    @allure.step("Получение текста элемента")
    def get_text_from_element(self, locator):
        element = self.find_element_with_wait(locator)
        return element.text

    @allure.step("Надежное заполнение поля текстом")
    def send_keys_to_element(self, locator, text):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)