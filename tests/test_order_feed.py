from locators.order_feed_locators import OrderFeedLocators
from pages.order_feed_page import OrderFeedPage

class TestOrderFeed:
    def test_order_details_window_opens_on_click(self, driver):
        page = OrderFeedPage(driver)
        page.go_to_order_feed()
        page.click_first_order()
        assert page.is_element_visible(OrderFeedLocators.ORDER_DETAILS), "Элемент 'Cостав' не отображается на странице"

    def test_user_orders_appear_in_feed(self, auth_user):
        page = OrderFeedPage(auth_user)

        # 1. Переходим в ленту заказов и получаем номер первого заказа
        page.go_to_order_feed()
        feed_order_number = page.get_first_order_number(from_feed=True)
        print(f"Номер в ленте: #{feed_order_number}")

        # 2. Переходим в историю заказов
        page.go_to_order_history_via_account()
        history_order_number = page.get_first_order_number(from_feed=False)
        print(f"Номер в истории: #{history_order_number}")

        # 3. Сравниваем номера
        assert feed_order_number == history_order_number, (
            f"Номера не совпадают! Лента: #{feed_order_number}, История: #{history_order_number}"
        )

    def test_all_time_counter_increases(self, auth_user):
        page = OrderFeedPage(auth_user)
        page.go_to_order_feed()
        initial_count = page.get_counters()[0]
        print(f"Начальное значение счетчика: {initial_count}")
        page.go_to_home_page()
        order_number_text = page.create_burger_order()
        print(f"Создан заказ {order_number_text}")
        order_number = int(order_number_text.replace("№", ""))
        assert order_number > initial_count, (f"Номер заказа ({order_number}) должен быть больше последнего счетчика ({initial_count})")

    def test_today_counter_increases(self, auth_user):
        page = OrderFeedPage(auth_user)
        page.go_to_order_feed()
        initial_today_count = page.get_counters()[1]
        print(f"Начальное значение счетчика 'за сегодня': {initial_today_count}")
        page.go_to_home_page()
        order_number_text = page.create_burger_order()
        print(f"Создан заказ {order_number_text}")
        page.go_to_order_feed()
        new_today_count = page.get_counters()[1]
        print(f"Новое значение счетчика 'за сегодня': {new_today_count}")
        assert new_today_count > initial_today_count, (f"Счетчик 'за сегодня' не увеличился! Было: {initial_today_count}, Стало: {new_today_count}")

    def test_order_appears_in_progress(self, auth_user):
        page = OrderFeedPage(auth_user)
        page.go_to_home_page()
        order_number_text = page.create_burger_order()
        order_number = page.normalize_order_number(order_number_text)
        print(f"Создан заказ: {order_number}")
        page.go_to_order_feed()
        assert page.wait_for_order_in_progress(order_number, timeout=15), (f"Заказ {order_number} не появился в разделе 'В работе'")
