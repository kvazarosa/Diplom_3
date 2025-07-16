from selenium.common import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from locators.password_recovery_locators import PasswordRecoveryLocators
from pages.base_page import BasePage
from data import Urls, TestData


class PasswordRecoveryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = PasswordRecoveryLocators()

    def open_forgot_password_page(self):
        self.driver.get(f"{Urls.HOME_PAGE_URL}{Urls.FORGOT_PASSWORD_URL}")
        self.wait_for_element_visible(self.locators.RECOVERY_EMAIL_INPUT)
        return self

    def is_forgot_password_page_opened(self):
        return (self.url_contains(Urls.FORGOT_PASSWORD_URL) and
                self.is_element_visible(self.locators.RECOVERY_EMAIL_INPUT))

    def submit_restore_form(self, email=TestData.VALID_EMAIL):
        self.wait_for_element_visible(self.locators.RECOVERY_EMAIL_INPUT)
        self.send_text(self.locators.RECOVERY_EMAIL_INPUT, email)
        self.click_element(self.locators.RESTORE_BUTTON)
        return self

    def is_reset_password_page_opened(self):
        return self.is_page_opened(Urls.RESET_PASSWORD_URL, PasswordRecoveryLocators.ENTER_NEW_PASSWORD)

    def toggle_password_visibility(self):
        initial_type = self.get_password_field_type()
        self.click_element(self.locators.EYE_ICON)
        WebDriverWait(self.driver, 5).until(lambda d: self.get_password_field_type() != initial_type or self._is_password_visible_via_css())
        return self

    def is_password_visible(self):
        try:
            return self.driver.execute_script("""
                const input = arguments[0];
                return input.type === 'text' || input.value.length > 0 && input.style.webkitTextSecurity === 'none';
            """, self.find_element(self.locators.CURRENT_PASSWORD_INPUT))
        except:
            return False

    def go_to_personal_account(self):
        if 'firefox' in self.driver.capabilities.get('browserName', '').lower():
            self._click_for_firefox(self.locators.PERSONAL_ACCOUNT_BTN)
        else:
            self._click_for_chrome(self.locators.PERSONAL_ACCOUNT_BTN)
        return self

    def is_login_page_opened(self):
        return self.is_element_visible(self.locators.LOGIN_FORM)

    def go_to_order_history(self):
        if 'firefox' in self.driver.capabilities.get('browserName', '').lower():
            self._click_for_firefox(self.locators.ORDER_HISTORY_BTN)
        else:
            self._click_for_chrome(self.locators.ORDER_HISTORY_BTN)
        return self

    def is_order_history_page_opened(self):
        return self.is_element_visible(self.locators.ORDER_HISTORY_CONTAINER)

    def logout(self):
        try:
            if 'firefox' in self.driver.capabilities.get('browserName', '').lower():
                self._click_for_firefox(self.locators.LOGOUT_BTN)
            else:
                self._click_for_chrome(self.locators.LOGOUT_BTN)
            return True
        except Exception as e:
            print(f"Ошибка при выходе: {str(e)}")
            return False

    def _enter_email(self, email):
        self.send_text(PasswordRecoveryLocators.EMAIL_INPUT, email)

    def _click_restore_button(self):
        self.click_element(PasswordRecoveryLocators.RESTORE_BUTTON)

    def is_on_authorization_page(self):
        return Urls.AUTHORIZATION_PAGE_URL in self.driver.current_url

    def _firefox_click(self, locator, timeout=10):
        element = self.wait_for_element_clickable(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

    def _safe_click(self, locator, timeout=10):
        if self.is_firefox():
            self._firefox_click(locator, timeout)
        else:
            self.click_element(locator)

    def _firefox_safe_click(self, locator):
        element = self.wait_for_element_clickable(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

    def _universal_click(self, locator):
        element = self.wait_for_element_clickable(locator)
        if self.is_firefox():
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.driver.execute_script("arguments[0].click();", element)
        else:
            element.click()

    def _click_for_firefox(self, locator):
        element = self.wait_for_element_clickable(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.execute_script("arguments[0].click();", element)

    def _click_for_chrome(self, locator):
        self.click_element(locator)

    def get_password_visibility_state(self):
        return self.get_element_attribute(self.locators.PASSWORD_INPUT,"type")

    def _get_recovery_email(self):
        return "default_recovery@example.com"

    def get_password_field_type(self):
        return self.get_element_attribute(self.locators.PASSWORD_INPUT, "type")

    def wait_for_password_field(self):
        return self.wait_for_element_visible(self.locators.PASSWORD_INPUT, timeout=5)

    def _is_password_visible_via_css(self):
        return self.driver.execute_script("return window.getComputedStyle(arguments[0]).webkitTextSecurity === 'none';", self.find_element(self.locators.PASSWORD_INPUT))

    def click_eye_icon(self):
        self.click_element(self.locators.EYE_ICON)

    def safe_click_eye_icon(self):
        try:
            self.click_element(self.locators.EYE_ICON)
        except ElementClickInterceptedException:
            self.close_modal_if_present()
            self.click_element(self.locators.EYE_ICON)
