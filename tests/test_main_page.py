from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators


def test_click_on_designer(driver):
    main_page = MainPage(driver)
    (main_page
     .go_to_order_feed()
     .go_to_constructor())
    assert main_page.is_constructor_page_visible()

def test_click_on_order_feed(driver):
    main_page = MainPage(driver)
    main_page.go_to_order_feed()
    assert "feed" in driver.current_url


def test_ingredient_details_popup(driver):
    main_page = MainPage(driver)
    main_page.open_bun_details()
    main_page.close_modal()


def test_close_ingredient_popup(driver):
    main_page = MainPage(driver)
    (main_page
     .open_ingredient_details()
     .close_modal())
    assert main_page.is_element_visible(MainPageLocators.CONSTRUCTOR_BUTTON)

def test_ingredient_counter_increase(driver):
    main_page = MainPage(driver)
    initial_count = main_page.get_ingredient_counter_value()
    main_page.drag_bun_to_constructor()
    assert main_page.get_ingredient_counter_value() > initial_count


def test_create_order_by_authorized_user(auth_user):
    main_page = MainPage(auth_user)
    main_page.create_order()
    assert main_page.is_element_visible(MainPageLocators.TEXT_BEGAN_TO_BE_PREPARED)
