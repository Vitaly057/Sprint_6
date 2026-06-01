import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)

    def get_current_url(self):
        return self.driver.current_url

    def get_window_handles(self):
        return self.driver.window_handles

    def switch_to_window(self, window_handle):
        self.driver.switch_to.window(window_handle)

    def close_current_window(self):
        self.driver.close()

    @allure.step("Форматирование локатора с подстановкой значения")
    def format_locators(self, locator, value):
        method, selector = locator
        return method, selector.format(value)

    def wait_until_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_until_present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_until_invisible(self, locator):
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_new_window(self, original_handles):
        self.wait.until(lambda driver: len(driver.window_handles) > len(original_handles))

    def wait_url_contains(self, url_part):
        self.wait.until(EC.url_contains(url_part))

    def find_visible_element(self, locator):
        def _predicate(driver):
            for element in driver.find_elements(*locator):
                if element.is_displayed():
                    return element
            return False

        return self.wait.until(_predicate)

    @allure.step("Поиск элемента с ожиданием видимости")
    def find_element_with_wait(self, locator):
        return self.wait_until_visible(locator)

    @allure.step("Надежный клик на элемент")
    def reliable_click(self, locator):
        element = self.wait_until_clickable(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def click_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        element.click()

    @allure.step("Скролл до элемента")
    def scroll_to_element(self, locator):
        element = self.find_element_with_wait(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    @allure.step("Получение текста элемента")
    def get_text_from_element(self, locator):
        return self.find_element_with_wait(locator).text

    @allure.step("Надежное заполнение поля текстом")
    def send_keys_to_element(self, locator, text):
        element = self.wait_until_clickable(locator)
        element.clear()
        element.send_keys(text)

    def send_escape_to_element(self, locator):
        self.wait_until_clickable(locator).send_keys(Keys.ESCAPE)

    def is_element_present(self, locator):
        try:
            self.wait_until_present(locator)
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator):
        try:
            self.wait_until_visible(locator)
            return True
        except TimeoutException:
            return False
