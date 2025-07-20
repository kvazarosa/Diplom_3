from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = MainPageLocators

    def go_to_order_feed(self):
        self.safe_click(MainPageLocators.ORDER_FEED_BUTTON)
        return self

    def go_to_constructor(self):
        self.safe_click(MainPageLocators.CONSTRUCTOR_BUTTON)
        return self

    def open_ingredient_details(self):
        self.safe_click(MainPageLocators.CRATER_BUN)
        self.wait_for_element_visible(MainPageLocators.INGREDIENT_DETAILS_MODAL)
        return self

    def open_bun_details(self):
        return self.open_ingredient_details()

    def close_modal(self):
        self.safe_click(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.wait_for_element_invisible(MainPageLocators.INGREDIENT_DETAILS_MODAL)
        return self

    def close_all_modals(self):
        try:
            self.close_modal()
        except:
            pass
        return self

    def get_ingredient_counter_value(self):
        try:
            counter_text = self.get_element_text(MainPageLocators.INGREDIENT_COUNTER)
            return int(counter_text) if counter_text else 0
        except:
            return 0

    def reset_constructor(self):
        try:
            if self.get_ingredient_counter_value() > 0:
                self.click_element(MainPageLocators.CLEAR_CONSTRUCTOR_BUTTON)
                self.wait_for_element_invisible(MainPageLocators.INGREDIENT_COUNTER)
        except:
            pass
        return self

    def drag_bun_to_constructor(self):
        self.reset_constructor()
        initial_count = self.get_ingredient_counter_value()
        self.drag_and_drop(MainPageLocators.CRATER_BUN, MainPageLocators.DROP_ZONE)
        WebDriverWait(self.driver, 5).until(lambda d: self.get_ingredient_counter_value() != initial_count)
        return self

    def is_constructor_page_visible(self):
        return (
            self.is_element_visible(MainPageLocators.INGREDIENTS_SECTION) and
            self.is_element_visible(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        )

    def create_order(self):
        self.drag_bun_to_constructor()
        self.click_element(MainPageLocators.CHECKOUT_BUTTON)
        return self

    def is_order_feed_page_opened(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: "feed" in d.current_url
        )
        return "feed" in self.driver.current_url
