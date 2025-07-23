from pages.password_recovery_page import PasswordRecoveryPage
from data import TestData
import allure


class TestPasswordRecovery:
    @allure.title("Открытие страницы восстановления пароля")
    @allure.description("Проверка доступности страницы восстановления пароля")
    def test_forgot_password_page_opens(self, driver):
        with allure.step("Открыть страницу восстановления пароля"):
            page = PasswordRecoveryPage(driver)
            page.open_forgot_password_page()
        with allure.step("Проверить отображение страницы"):
            assert page.is_forgot_password_page_opened()

    @allure.title("Отправка формы восстановления пароля")
    @allure.description("Проверка отправки формы с валидным email")
    def test_password_reset_form_submission(self, driver):
        with allure.step("Открыть страницу восстановления"):
            page = PasswordRecoveryPage(driver)
            page.open_forgot_password_page()
        with allure.step("Заполнить и отправить форму"):
            page.submit_restore_form(TestData.VALID_EMAIL)
        with allure.step("Проверить появление поля ввода пароля"):
            assert page.is_element_visible(page.locators.PASSWORD_INPUT)

    @allure.title("Переключение видимости пароля")
    @allure.description("Проверка работы иконки отображения пароля")
    def test_password_visibility_toggle(self, driver):
        with allure.step("Перейти на страницу смены пароля"):
            recovery_page = PasswordRecoveryPage(driver)
            recovery_page.open_forgot_password_page()
            recovery_page.submit_restore_form()
        with allure.step("Нажать на иконку глаза"):
            recovery_page.safe_click_eye_icon()
        with allure.step("Проверить что пароль видимый"):
            assert recovery_page.get_password_field_type() == "text"

    @allure.title("Доступ к личному кабинету")
    @allure.description("Проверка перехода в личный кабинет")
    def test_personal_account_access(self, driver):
        with allure.step("Перейти в личный кабинет"):
            page = PasswordRecoveryPage(driver)
            page.go_to_personal_account()
        with allure.step("Проверить отображение формы входа"):
            assert page.is_element_visible(page.locators.LOGIN_FORM)

    @allure.title("Навигация в историю заказов")
    @allure.description("Проверка перехода в историю заказов")
    def test_order_history_navigation(self, auth_user):
        with allure.step("Авторизоваться и перейти в ЛК"):
            page = PasswordRecoveryPage(auth_user)
            page.go_to_personal_account()
        with allure.step("Перейти в историю заказов"):
            page.go_to_order_history()
        with allure.step("Проверить отображение истории"):
            assert page.is_element_visible(page.locators.ORDER_HISTORY_SECTION)

    @allure.title("Выход из аккаунта")
    @allure.description("Проверка функционала выхода из учетной записи")
    def test_logout_functionality(self, auth_user):
        with allure.step("Перейти в личный кабинет"):
            page = PasswordRecoveryPage(auth_user)
            page.go_to_personal_account()
        with allure.step("Выйти из аккаунта"):
            assert page.logout()
        with allure.step("Проверить отображение формы входа"):
            assert page.is_element_visible(page.locators.LOGIN_FORM)
