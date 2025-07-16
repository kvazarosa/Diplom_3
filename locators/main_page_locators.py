from selenium.webdriver.common.by import By

class MainPageLocators:
    # блок верхотуры
    STELLAR_BURGERS_LOGO = (By.CSS_SELECTOR, "div.AppHeader_header__logo__2D0X2")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[contains(@class, 'AppHeader_header__linkText') and text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[contains(@class, 'AppHeader_header__linkText') and text()='Лента Заказов']")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']")

    # блок конструктора
    TEXT_ASSEMBLE_BURGER = (By.XPATH, "//h1[contains(@class, 'text_type_main-large') and contains(text(), 'Соберите бургер')]")
    INGREDIENTS_SECTION = (By.CSS_SELECTOR, "section.BurgerIngredients_ingredients__1N8v2")
    INGREDIENT_ITEM = (By.XPATH, "//div[contains(@class, 'IngredientItem_ingredient__')][1]")
    CRATER_BUN = (By.XPATH, "//p[contains(@class, '__text__yp3dH') and contains(., 'булка')]")
    DROP_ZONE = (By.XPATH, "//span[contains(@class, 'constructor-element__text') and contains(text(), 'Перетяните булочку сюда')]")
    CHECKOUT_BUTTON = (By.XPATH, "//button[contains(@class, 'button_type_primary') and contains(text(), 'Оформить заказ')]")
    CLEAR_CONSTRUCTOR_BUTTON = (By.XPATH, "//button[contains(text(), 'Очистить конструктор')]")

    # модальный блок
    INGREDIENT_DETAILS_MODAL = (By.XPATH, "//h2[contains(@class, 'modal__title') and contains(text(), 'Детали ингредиента')]")
    MODAL_TITLE = (By.XPATH, "//h2[contains(@class, 'modal__title') and text()='Детали ингредиента']")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    CROSS_WINDOW = (By.CSS_SELECTOR, "button.Modal_modal__close_modified__3V5XS Modal_modal__close__TnseK")
    TEXT_BEGAN_TO_BE_PREPARED = (By.XPATH, "//p[contains(@class, 'main-small') and contains(text(), 'Ваш заказ начали готовить')]")

    # блок заказов
    COMPLETED_ALL_TIME_TEXT = (By.XPATH, "//p[@class='text text_type_main-medium' and contains(., 'все время')]")

    # блок личного кабинета
    PERSONAL_ACCOUNT = (By.XPATH, "//a[contains(@href, 'account/profile')]")
    ORDER_HISTORY = (By.XPATH, "//a[contains(@href, 'order-history')]")
    EXIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")

    # каунтер ингредиента
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "div.counter_counter__ZNLkj.counter_default__28sqi > p.counter_counter__num__3nue1")