from locators.order_feed_locators import OrderFeedLocators
from pages.order_feed_page import OrderFeedPage
import allure


class TestOrderFeed:
    @allure.title("Отображение деталей заказа при клике")
    @allure.description("При клике на заказ в ленте должно открываться окно с деталями")
    def test_order_details_window_opens_on_click(self, driver):
        with allure.step("Открытие ленты заказов"):
            page = OrderFeedPage(driver)
            page.go_to_order_feed()
        with allure.step("Клик по первому заказу в ленте"):
            page.click_first_order()
        with allure.step("Проверка отображения деталей заказа"):
            assert page.is_element_visible(OrderFeedLocators.ORDER_DETAILS)

    @allure.title("Совпадение заказов в ленте и истории")
    @allure.description("Заказ должен отображаться одновременно в ленте и истории заказов")
    def test_user_orders_appear_in_feed(self, auth_user):
        with allure.step("Создание нового заказа"):
            page = OrderFeedPage(auth_user)
            page.create_order_and_get_number()
            page.close_order_modal()
        with allure.step("Получение номера из истории заказов"):
            history_num = page.get_last_order_from_history()
        with allure.step("Получение номера из ленты заказов"):
            feed_num = page.get_last_order_from_feed()
        with allure.step("Проверка совпадения номеров"):
            assert history_num == feed_num

    @allure.title("Увеличение счетчика 'Всего заказов'")
    @allure.description("При создании нового заказа счетчик 'Выполнено за все время' должен увеличиваться")
    def test_all_time_counter_increases(self, auth_user):
        with allure.step("Получение начального значения счетчика"):
            page = OrderFeedPage(auth_user)
            page.go_to_order_feed()
            initial_count = page.get_counters()[0]
        with allure.step("Создание нового заказа"):
            page.go_to_home_page()
            order_number_text = page.create_burger_order()
            order_number = int(order_number_text.replace("№", ""))
        with allure.step("Проверка увеличения счетчика"):
            assert order_number > initial_count

    @allure.title("Увеличение счетчика 'Сегодня заказов'")
    @allure.description("При создании нового заказа счетчик 'Выполнено за сегодня' должен увеличиваться")
    def test_today_counter_increases(self, auth_user):
        with allure.step("Получение начального значения счетчика"):
            page = OrderFeedPage(auth_user)
            page.go_to_order_feed()
            initial_today_count = page.get_counters()[1]
        with allure.step("Создание нового заказа"):
            page.go_to_home_page()
            order_number_text = page.create_burger_order()
            page.go_to_order_feed()
            new_today_count = page.get_counters()[1]
        with allure.step("Проверка увеличения счетчика"):
            assert new_today_count > initial_today_count

    @allure.title("Отображение заказа в разделе 'В работе'")
    @allure.description("Новый заказ должен отображаться в разделе 'В работе' ленты заказов")
    def test_order_appears_in_progress(self, auth_user):
        with allure.step("Создание нового заказа"):
            page = OrderFeedPage(auth_user)
            page.go_to_home_page()
            order_number_text = page.create_burger_order()
            order_number = page.normalize_order_number(order_number_text)
        with allure.step("Проверка отображения в разделе 'В работе'"):
            page.go_to_order_feed()
            assert page.wait_for_order_in_progress(order_number, timeout=15)
