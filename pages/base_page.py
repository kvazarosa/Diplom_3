from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator), message=f"Элемент {locator} не стал видимым за {timeout} сек")

    def wait_for_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator), message=f"Элемент {locator} не стал кликабельным за {timeout} сек")

    def wait_for_element_invisible(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator), message=f"Элемент {locator} не исчез за {timeout} сек")

    def click_element(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()

    def wait_for_element_present(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator), message=f"Элемент {locator} не найден в DOM за {timeout} сек")

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
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator), message=f"Элементы {locator} не найдены за {timeout} сек")
        except:
            return []
