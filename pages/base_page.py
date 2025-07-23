from selenium.common import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, timeout=3):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def send_text(self, locator, text, timeout=3):
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator, timeout=3):
        return self.find_element(locator, timeout).text

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def wait_for_element_to_be_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_url(self, url, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))

    def wait_for_url_contains(self, text, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.url_contains(text))

    def get_element_attribute(self, locator, attribute, timeout=3):
        return self.find_element(locator, timeout).get_attribute(attribute)

    def is_element_visible(self, locator, timeout=3):
        try:
            return self.find_element(locator, timeout).is_displayed()
        except:
            return False

    def get_current_url(self):
        return self.driver.current_url

    def url_contains(self, text):
        return text in self.get_current_url()

    def wait_for_element_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator),
                                                         message=f"Элемент {locator} не стал видимым за {timeout} сек")

    def wait_for_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator),
                                                         message=f"Элемент {locator} не стал кликабельным за {timeout} сек")

    def wait_for_element_invisible(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator),
                                                         message=f"Элемент {locator} не исчез за {timeout} сек")

    def click_element(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()

    def wait_for_element_present(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator),
                                                         message=f"Элемент {locator} не найден в DOM за {timeout} сек")

    def close_modal_if_present(self):
        if self.is_firefox():
            try:
                modal_overlay = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay__')]")
                close_button = (By.XPATH, "//button[contains(@class, 'Modal_close__')]")
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(modal_overlay))
                self.driver.find_element(*close_button).click()
                WebDriverWait(self.driver, 3).until(EC.invisibility_of_element_located(modal_overlay))
            except:
                pass

    def click_with_modal_handling(self, locator, overlay_locator=None, timeout=10):
        if overlay_locator and self.is_firefox():
            self.close_modal_if_present(overlay_locator)
        element = self.wait_for_element_clickable(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()

    def js_click(self, locator, timeout=10):
        element = self.wait_for_element_present(locator, timeout)
        self.driver.execute_script("arguments[0].click();", element)

    def is_page_opened(self, url_part, unique_locator, timeout=5):
        return (self.url_contains(url_part) and self.is_element_visible(unique_locator, timeout))

    def drag_and_drop(self, locator_from, locator_to):
        element_from = self.wait_for_element_visible(locator_from)
        element_to = self.wait_for_element_visible(locator_to)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element_from)

        if "chrome" in self.driver.capabilities['browserName'].lower():
            ActionChains(self.driver) \
                .click_and_hold(element_from) \
                .pause(1) \
                .move_to_element(element_to) \
                .pause(1) \
                .release() \
                .perform()
        else:
            self.driver.execute_script("""
                function createEvent(typeOfEvent) {
                    var event = document.createEvent("CustomEvent");
                    event.initCustomEvent(typeOfEvent, true, true, null);
                    event.dataTransfer = {
                        data: {},
                        setData: function(key, value) {
                            this.data[key] = value;
                        },
                        getData: function(key) {
                            return this.data[key];
                        }
                    };
                    return event;
                }

                function dispatchEvent(element, event, transferData) {
                    if (transferData !== undefined) {
                        event.dataTransfer = transferData;
                    }
                    if (element.dispatchEvent) {
                        element.dispatchEvent(event);
                    } else if (element.fireEvent) {
                        element.fireEvent("on" + event.type, event);
                    }
                }

                var source = arguments[0];
                var target = arguments[1];

                var dragStartEvent = createEvent('dragstart');
                dispatchEvent(source, dragStartEvent);

                var dropEvent = createEvent('drop');
                dispatchEvent(target, dropEvent, dragStartEvent.dataTransfer);

                var dragEndEvent = createEvent('dragend');
                dispatchEvent(source, dragEndEvent, dragStartEvent.dataTransfer);
            """, element_from, element_to)

    def safe_click(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент {locator} не стал кликабельным за {timeout} сек"
        )

        try:
            element.click()
        except:
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except:
                ActionChains(self.driver).move_to_element(element).click().perform()

    def is_firefox(self):
        return 'firefox' in self.driver.capabilities.get('browserName', '').lower()

    def find_elements(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator),
                                                             message=f"Элементы {locator} не найдены за {timeout} сек")
        except:
            return []

    def firefox_safe_click(self, locator, timeout=10):
        if self.is_firefox():
            self.close_modal_if_present()
            element = self.wait_for_element_clickable(locator, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.driver.execute_script("arguments[0].click();", element)
        else:
            self.click_element(locator, timeout)

    def safe_click_with_modal_wait(self, locator, timeout=10):
        try:
            if self.is_firefox():
                self.close_modal_if_present()
            element = self.wait_for_element_clickable(locator, timeout)
            try:
                element.click()
            except:
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                except:
                    ActionChains(self.driver).move_to_element(element).click().perform()
        except Exception as e:
            print(f"Ошибка при безопасном клике: {str(e)}")
            raise

    def close_all_modals(self):
        try:
            if self.is_firefox():
                for _ in range(3):
                    try:
                        modal = self.driver.find_element(By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")
                        close_btn = modal.find_element(By.XPATH, ".//button[contains(@class, 'Modal_modal__close')]")
                        self.driver.execute_script("arguments[0].click();", close_btn)
                        time.sleep(0.5)
                    except:
                        break

            close_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
            for btn in close_buttons:
                try:
                    self.driver.execute_script("arguments[0].click();", btn)
                    time.sleep(0.3)
                except:
                    continue

        except Exception as e:
            print(f"Ошибка при закрытии модальных окон: {str(e)}")

    def wait_and_find(self, locator, timeout=15):
        attempt = 0
        while attempt < 3:
            try:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            except StaleElementReferenceException:
                attempt += 1
                time.sleep(1)
        raise TimeoutException(f"Элемент {locator} не стабилизировался после 3 попыток")

    def wait_for_full_load(self, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete")
        except Exception as e:
            print(f"Страница не загрузилась полностью: {str(e)}")

    def reliable_scroll_to_element(self, element, max_attempts=3, delay=1):
        for attempt in range(max_attempts):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                           element)
                time.sleep(delay)
                if element.is_displayed():
                    return True
            except StaleElementReferenceException:
                print(f"Попытка {attempt + 1}: элемент устарел при прокрутке")
        return False

    def get_last_element_text(self, locator):
        elements = self.find_elements(locator)
        if not elements:
            raise NoSuchElementException(f"Элементы {locator} не найдены")
        return elements[-1].text

    def get_first_element_text(self, locator):
        return self.find_element(locator).text

    def scroll_to_bottom(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_last_visible_element(self, locator):
        elements = self.find_elements(locator)
        if not elements:
            raise NoSuchElementException(f"Элементы {locator} не найдены")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elements[-1])
        time.sleep(0.5)
        return elements[-1]
