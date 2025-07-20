from selenium.webdriver.common.by import By


class PasswordRecoveryLocators:
    # Основные элементы
    RECOVERY_EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")

    # Кнопки и иконки
    RESTORE_BUTTON = (By.XPATH, "//button[contains(text(), 'Восстановить')]")
    EYE_ICON = (By.CSS_SELECTOR, "div.input__icon-action svg")
    PERSONAL_ACCOUNT_BTN = (By.XPATH, "//a[contains(@href, 'account')]")
    ORDER_HISTORY_BTN = (By.XPATH, "//a[contains(@href, 'order-history')]")
    LOGOUT_BTN = (By.XPATH, "//button[contains(text(), 'Выход')]")
    CURRENT_PASSWORD_INPUT = (By.XPATH, "//input[@type='password' and contains(@class, 'input__textfield')]")
    ENTER_NEW_PASSWORD = (By.XPATH, "//input[@type='password' and contains(@class, 'input__textfield')]")
    HIDDEN_PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    VISIBLE_PASSWORD_INPUT = (By.XPATH, "//input[@type='text']")
    PASSWORD_FIELD = (By.XPATH, "//input[contains(@class, 'input__textfield')]")

    # Проверочные элементы
    LOGIN_FORM = (By.CSS_SELECTOR, "input.input__textfield[name='name']")
    ORDER_HISTORY_SECTION = (By.CSS_SELECTOR, "ul.OrderHistory_profileList__374GU")



