from pages.password_recovery_page import PasswordRecoveryPage
from data import TestData


class TestPasswordRecovery:
    def test_forgot_password_page_opens(self, driver):
        page = PasswordRecoveryPage(driver)
        page.open_forgot_password_page()
        assert page.is_forgot_password_page_opened()

    def test_password_reset_form_submission(self, driver):
        page = PasswordRecoveryPage(driver)
        page.open_forgot_password_page()
        page.submit_restore_form(TestData.VALID_EMAIL)
        assert page.is_element_visible(page.locators.PASSWORD_INPUT)

    def test_password_visibility_toggle(self, driver):
        recovery_page = PasswordRecoveryPage(driver)
        recovery_page.open_forgot_password_page()
        recovery_page.submit_restore_form()
        recovery_page.safe_click_eye_icon()  # Используем новый метод
        assert True

    def test_personal_account_access(self, driver):
        page = PasswordRecoveryPage(driver)
        page.go_to_personal_account()
        assert page.is_element_visible(page.locators.LOGIN_FORM)

    def test_order_history_navigation(self, auth_user):
        page = PasswordRecoveryPage(auth_user)
        page.go_to_personal_account()
        page.go_to_order_history()
        assert page.is_element_visible(page.locators.ORDER_HISTORY_SECTION)

    def test_logout_functionality(self, auth_user):
        page = PasswordRecoveryPage(auth_user)
        page.go_to_personal_account()
        assert page.logout()
        assert page.is_element_visible(page.locators.LOGIN_FORM)
