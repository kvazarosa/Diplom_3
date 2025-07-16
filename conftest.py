import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data import Urls, TestData
from locators.main_page_locators import MainPageLocators


@pytest.fixture(params=["Chrome", "Firefox"])
def driver(request):
    if request.param == "Chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
    else:
        options = webdriver.FirefoxOptions()
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        options.set_preference("layout.css.devPixelsPerPx", "1.0")
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()

    driver.get(Urls.HOME_PAGE_URL)
    yield driver
    driver.quit()


@pytest.fixture
def auth_user(driver):
    login_url = f"{Urls.HOME_PAGE_URL}{Urls.AUTHORIZATION_PAGE_URL}"
    driver.get(login_url)
    wait = WebDriverWait(driver, 15)
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='name']")))
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
    email_input.send_keys(TestData.VALID_EMAIL)
    password_input.send_keys(TestData.VALID_PASSWORD)
    login_button.click()
    wait.until(EC.url_to_be(Urls.HOME_PAGE_URL))
    return driver


@pytest.fixture(autouse=True)
def close_modals(driver):
    yield
    try:
        driver.find_element(*MainPageLocators.CROSS_WINDOW).click()
    except:
        pass

