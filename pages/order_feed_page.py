from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from .base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators
from data import Urls
import time

class OrderFeedPage(BasePage):
    def go_to_order_feed(self):
        self.driver.get(f"{Urls.HOME_PAGE_URL}{Urls.ORDER_FEED_URL}")
        time.sleep(2)

    def click_first_order(self):
        try:
            orders = self.wait_for_any_element_visible(OrderFeedLocators.ORDER_ITEMS, timeout=20)

            if not orders:
                raise Exception("Не найдено ни одного заказа в ленте")
            first_order = orders[0]
            self.scroll_to_element(first_order)
            self.highlight_element(first_order)
            self.safe_click_element(first_order)
            self.wait_for_element_visible(OrderFeedLocators.ORDER_DETAILS, timeout=10)
        except Exception as e:
            self.driver.save_screenshot("click_order_error.png")
            raise Exception(f"Ошибка при клике на заказ: {str(e)}")

    def is_order_details_displayed(self):
        return self.is_element_visible(OrderFeedLocators.ORDER_DETAILS, timeout=10)

    def get_user_order_numbers(self):
        elements = self.find_elements(OrderFeedLocators.USER_ORDER_IN_FEED)
        return [el.text.split('#')[-1] for el in elements if el.text]

    def get_feed_orders(self):
        elements = self.find_elements(OrderFeedLocators.USER_ORDER_IN_FEED)
        return [el.text for el in elements if el.text]

    def get_counters(self):
        try:
            if self.is_firefox():
                self.driver.execute_script("window.scrollTo(0, 0)")
                time.sleep(1)
            timeout = 20 if self.is_firefox() else 10
            wait = WebDriverWait(self.driver, timeout)
            all_time_element = wait.until(EC.visibility_of_element_located(OrderFeedLocators.COMPLETED_ALL_TIME))
            today_element = wait.until(EC.visibility_of_element_located(OrderFeedLocators.COMPLETED_TODAY))
            self.highlight_element(all_time_element)
            self.highlight_element(today_element)
            all_time = int(all_time_element.text)
            today = int(today_element.text)
            return all_time, today
        except Exception as e:
            self.driver.save_screenshot("counters_error.png")
            raise Exception(f"Ошибка при получении счетчиков: {str(e)}")

    def create_burger_order(self):
        self.drag_and_drop(OrderFeedLocators.CRATER_BUN, OrderFeedLocators.BURGER_CREATION_WINDOW)
        time.sleep(1)
        self.click_element(OrderFeedLocators.CHECKOUT_BUTTON)
        try:
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(OrderFeedLocators.ORDER_NUMBER_PLACEHOLDER), "Placeholder номера заказа не исчез")
        except:
            pass
        order_element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(OrderFeedLocators.ORDER_NUMBER),"Номер заказа не появился за 15 секунд")
        return order_element.text

    def wait_for_elements_visible(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_any_elements_located(locator), message=f"Элементы {locator} не стали видимыми за {timeout} сек")
        except TimeoutException:
            return []

    def highlight_element(self, element):
        self.driver.execute_script("arguments[0].style.border='3px solid red';", element)
        time.sleep(0.5)

    def safe_click_element(self, element):
        try:
            element.click()
        except:
            try:
                ActionChains(self.driver).move_to_element(element).pause(0.5).click().perform()
            except:
                self.driver.execute_script("arguments[0].click();", element)

    def wait_for_any_element_visible(self, locator, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator), message=f"Элементы {locator} не найдены за {timeout} сек")           # Проверяем видимость каждого элемента
            for element in elements:
                if element.is_displayed():
                    return elements
            raise TimeoutException(f"Ни один элемент {locator} не стал видимым за {timeout} сек")
        except Exception as e:
            self.driver.save_screenshot("wait_elements_error.png")
            raise

    def go_to_personal_account(self):
        self.click_element(OrderFeedLocators.PERSONAL_ACCOUNT_BUTTON)
        self.wait_for_url_contains("account")
        return self

    def go_to_order_history(self):
        self.click_element(OrderFeedLocators.ORDER_HISTORY_TAB)
        self.wait_for_url_contains("/profile/orders")
        return self

    def get_first_order_number(self, from_feed=True):
        locator = OrderFeedLocators.FIRST_ORDER_IN_FEED if from_feed else OrderFeedLocators.FIRST_ORDER_IN_HISTORY
        order_element = self.wait_for_element_visible(locator, timeout=15)
        self.highlight_element(order_element)
        return order_element.text.replace("#", "").strip()

    def verify_orders_match(self):
        history_num = (self.go_to_personal_account()
                       .go_to_order_history()
                       .get_first_order_number(OrderFeedLocators.FIRST_ORDER_IN_HISTORY))
        feed_num = (self.go_to_order_feed()
                    .get_first_order_number(OrderFeedLocators.FIRST_ORDER_IN_FEED))
        return history_num == feed_num, history_num, feed_num

    def go_to_order_history_via_account(self):
        print("Шаг 1: Клик по кнопке 'Личный Кабинет'")
        account_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(OrderFeedLocators.PERSONAL_ACCOUNT_BUTTON), "Не удалось найти/кликнуть кнопку 'Личный Кабинет'")
        self.highlight_element(account_button)
        account_button.click()
        print("Шаг 2: Ожидание загрузки профиля")
        WebDriverWait(self.driver, 15).until(EC.url_contains("account/profile"),"Не произошел переход в профиль после 15 сек")
        print("Шаг 3: Клик по вкладке 'История заказов'")
        history_tab = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(OrderFeedLocators.ORDER_HISTORY_TAB),"Не найдена вкладка 'История заказов'")
        self.driver.execute_script("arguments[0].scrollIntoView();", history_tab)
        self.highlight_element(history_tab)
        history_tab.click()
        print("Шаг 4: Ожидание загрузки истории заказов")
        WebDriverWait(self.driver, 15).until(EC.url_contains("order-history"),"Не произошел переход в историю заказов после 15 сек")
        print("Шаг 5: Проверка отображения заказов")
        WebDriverWait(self.driver, 25).until(EC.visibility_of_element_located(OrderFeedLocators.FIRST_ORDER_IN_HISTORY),"Не отображаются заказы в истории после 25 сек")
        print("Успешный переход в историю заказов")
        return self

    def go_to_home_page(self):
        self.close_modal_if_present()
        try:
            self.driver.find_element(*OrderFeedLocators.HOME_LOGO).click()
        except ElementClickInterceptedException:
            self.close_modal_if_present()
            self.driver.find_element(*OrderFeedLocators.HOME_LOGO).click()
        self.wait_for_url(Urls.HOME_PAGE_URL)

    def get_in_progress_orders(self):
        try:
            self.wait_for_element_visible(OrderFeedLocators.IN_PROGRESS_SECTION, timeout=10)
            return [
                element.text.strip()
                for element in self.find_elements(OrderFeedLocators.IN_PROGRESS_ORDER_ITEMS)
            ]
        except Exception as e:
            print(f"Ошибка при получении заказов: {e}")
            return []

    def is_order_in_progress(self, order_number):
        try:
            normalized_order = ''.join([c for c in str(order_number) if c.isdigit()])
            self.wait_for_element_visible(OrderFeedLocators.IN_PROGRESS_SECTION, timeout=15)
            orders = self.find_elements(OrderFeedLocators.IN_PROGRESS_ORDER_ITEMS)
            current_orders = [''.join([c for c in item.text.strip() if c.isdigit()]) for item in orders]
            print(f"Ищем заказ {normalized_order} в списке: {current_orders}")
            return normalized_order in current_orders
        except Exception as e:
            print(f"Ошибка при проверке заказов в работе: {str(e)}")
            return False

    def is_first_in_progress(self, order_number):
        current_orders = self.get_in_progress_orders()
        if not current_orders:
            return False
        print(f"Первый заказ в работе: {current_orders[0]}, ожидаемый: {order_number}")
        return current_orders[0] == order_number

    def normalize_order_number(self, order_number):
        digits = ''.join([char for char in str(order_number) if char.isdigit()])
        return digits.lstrip('0') or '0'

    def wait_for_order_in_progress(self, order_number, timeout=15):
        normalized = self.normalize_order_number(order_number)

        def order_present(driver):
            try:
                orders = [
                    self.normalize_order_number(num)
                    for num in self.get_in_progress_orders()
                ]
                return normalized in orders
            except:
                return False

        return WebDriverWait(self.driver, timeout).until(order_present, message=f"Заказ {normalized} не появился в разделе 'В работе' за {timeout} сек")
