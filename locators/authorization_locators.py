from selenium.webdriver.common.by import By


class AuthorizationLocators:
    # Поля формы
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")

    # Другие элементы страницы авторизации
    REGISTER_LINK = (By.XPATH, "//a[contains(@href, 'register')]")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(@href, 'forgot-password')]")
