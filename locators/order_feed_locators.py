from selenium.webdriver.common.by import By


class OrderFeedLocators:
    # Основные элементы
    FIRST_ORDER_IN_FEED = (By.XPATH, "(//div[contains(@class, 'OrderHistory_textBox__')])[1]//p[contains(@class, 'digits-default')]")
    ORDER_DETAILS = (By.XPATH, "//p[@class='text text_type_main-medium mb-8' and text()='Cостав']")
    FIRST_ORDER_IN_HISTORY = (By.XPATH, "(//div[contains(@class, 'OrderHistory_textBox__')])[1]//p[contains(@class, 'digits-default')]")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[contains(@class, 'AppHeader_header__linkText__3q_va') and text()='Личный Кабинет']")
    ORDER_HISTORY_TAB = (By.XPATH, "//a[contains(@href, 'order-history')]")  # Вкладка "История заказов"
    HOME_LOGO = (By.XPATH, "//a[@href='/']")

    # Счетчики
    COMPLETED_ALL_TIME = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p[contains(@class, 'digits-large')]")
    COMPLETED_TODAY = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p[contains(@class, 'digits-large')]")

    # Конструктор бургера
    CRATER_BUN = (By.XPATH, "//img[contains(@class, 'BurgerIngredient_ingredient__image__3e-07') and @alt='Краторная булка N-200i']")
    BURGER_CREATION_WINDOW = (By.XPATH, "//span[contains(@class, 'constructor-element__text') and contains(., 'Перетяните булочку')]")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "button.button_button__33qZ0.button_button_type_primary__1O7Bx.button_button_size_large__G21Vg")

    # Номер заказа
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title') and contains(@class, 'text_type_digits-large')]")
    ORDER_ITEMS = (By.XPATH, "//div[contains(@class, 'OrderHistory_textBox__')]")
    ORDER_NUMBER_IN_MODAL = (By.XPATH, "//p[contains(@class, 'digits-large')]")
    ORDER_NUMBER_PLACEHOLDER = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title') and text()='9999']")

    # Раздел "В работе"
    IN_PROGRESS_SECTION = (By.XPATH, "//p[contains(text(), 'В работе')]")
    IN_PROGRESS_ORDERS_LIST = (By.XPATH, "//p[contains(text(), 'В работе')]/following-sibling::ul")
    IN_PROGRESS_ORDER_ITEMS = (By.XPATH, "//p[contains(text(), 'В работе')]/following-sibling::ul/li[contains(@class, 'text_type_digits-default')]")

    # Для авторизации
    USER_ORDER_IN_FEED = (By.XPATH, "//div[contains(@class, 'OrderHistory_link__')]")
    LOGIN_INPUT = (By.XPATH, "//input[@type='text' and @name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")