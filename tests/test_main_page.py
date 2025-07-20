from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators
import allure


@allure.feature("Главная страница")
class TestMainPage:
    @allure.title("Переход в конструктор")
    @allure.description("Проверка перехода в раздел 'Конструктор' из других страниц")
    def test_click_on_designer(self, driver):
        allure.step("Инициализация главной страницы")
        main_page = MainPage(driver)
        allure.step("Переход в ленту заказов и возврат в конструктор")
        main_page.go_to_order_feed()
        allure.step("Возврат в конструктор через хедер")
        main_page.go_to_constructor()
        allure.step("Проверка видимости конструктора")
        assert main_page.is_constructor_page_visible()

    @allure.title("Переход в ленту заказов")
    @allure.description("Проверка перехода по клику на 'Лента заказов' в хедере")
    def test_click_on_order_feed(self, driver):
        allure.step("Инициализация главной страницы")
        main_page = MainPage(driver)
        allure.step("Клик на 'Лента заказов'")
        main_page.go_to_order_feed()
        allure.step("Проверка URL страницы")
        assert main_page.is_order_feed_page_opened()

    @allure.title("Открытие деталей ингредиента")
    @allure.description("Проверка отображения модального окна при клике на ингредиент")
    def test_ingredient_details_popup(self, driver):
        allure.step("Инициализация главной страницы")
        main_page = MainPage(driver)
        allure.step("Клик на ингредиент булки")
        main_page.open_bun_details()
        allure.step("Проверка видимости модального окна")
        assert main_page.is_element_visible(MainPageLocators.INGREDIENT_DETAILS_MODAL)

    @allure.title("Закрытие модального окна ингредиента")
    @allure.description("Проверка закрытия модального окна по крестику")
    def test_close_ingredient_popup(self, driver):
        allure.step("Инициализация главной страницы")
        main_page = MainPage(driver)
        allure.step("Открытие и закрытие модального окна")
        main_page.open_ingredient_details().close_modal()
        allure.step("Проверка доступности конструктора")
        assert main_page.is_element_visible(MainPageLocators.CONSTRUCTOR_BUTTON)

    @allure.title("Счетчик ингредиентов")
    @allure.description("Проверка увеличения счетчика при добавлении ингредиента")
    def test_ingredient_counter_increase(self, driver):
        allure.step("Инициализация главной страницы")
        main_page = MainPage(driver)
        allure.step("Получение начального значения счетчика")
        initial_count = main_page.get_ingredient_counter_value()
        allure.step("Добавление ингредиента в конструктор")
        main_page.drag_bun_to_constructor()
        allure.step("Проверка увеличения счетчика")
        assert main_page.get_ingredient_counter_value() > initial_count

    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Проверка оформления заказа после авторизации")
    def test_create_order_by_authorized_user(self, auth_user):
        allure.step("Инициализация главной страницы")
        main_page = MainPage(auth_user)
        allure.step("Создание заказа")
        main_page.create_order()
        allure.step("Проверка подтверждения заказа")
        assert main_page.is_element_visible(MainPageLocators.TEXT_BEGAN_TO_BE_PREPARED)
