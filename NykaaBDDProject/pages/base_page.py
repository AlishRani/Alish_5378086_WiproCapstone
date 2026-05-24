"""Base Page Object — sabhi pages yahan se inherit karte hain."""
import logging
import os
from datetime import datetime

from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

logger = logging.getLogger("nykaa")


class BasePage:
    BASE_URL = "https://www.nykaa.com"
    WAIT     = 15

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, self.WAIT)

    def open(self, path=""):
        url = self.BASE_URL + path
        logger.info(f"[NAV] {url}")
        self.driver.get(url)
        self._wait_ready()
        return self

    def _wait_ready(self, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except Exception:
            pass

    def wait_visible(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator):
        el = self.wait_clickable(locator)
        try:
            el.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", el)
        return self

    def type_text(self, locator, text):
        el = self.wait_visible(locator)
        el.clear()
        el.send_keys(text)
        return self

    def get_text(self, locator):
        return self.wait_visible(locator).text.strip()

    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def scroll_down(self, px=400):
        self.driver.execute_script(f"window.scrollBy(0, {px});")

    def scroll_to(self, locator):
        el = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        return el

    def get_elements(self, locator):
        return self.driver.find_elements(*locator)

    def get_count(self, locator):
        return len(self.driver.find_elements(*locator))

    def close_popup(self):
        selectors = [
            (By.CSS_SELECTOR, "button.css-1x39bm7"),
            (By.CSS_SELECTOR, "[class*='modalClose']"),
            (By.CSS_SELECTOR, "[class*='CloseButton']"),
            (By.CSS_SELECTOR, "[class*='closeIcon']"),
            (By.CSS_SELECTOR, "[aria-label='Close']"),
            (By.CSS_SELECTOR, ".css-1rjbe5s"),
            (By.XPATH, "//button[contains(@class,'close') or contains(@class,'Close')]"),
        ]
        for sel in selectors:
            try:
                btn = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(sel))
                self.driver.execute_script("arguments[0].click();", btn)
                return True
            except Exception:
                pass
        return False

    def is_real_page(self):
        """404 / error page detect karo."""
        src   = self.driver.page_source.lower()
        title = self.driver.title.lower()
        bad   = ["404", "page not found", "oops!", "something went wrong",
                 "we can't find", "this page is unavailable", "error occurred"]
        for kw in bad:
            if kw in src[:4000] or kw in title:
                return False
        return True

    def screenshot(self, label):
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(SCREENSHOT_DIR, f"{label}_{ts}.png")
        self.driver.save_screenshot(path)
        logger.info(f"[SCREENSHOT] {path}")
        return path

    @property
    def current_url(self):
        return self.driver.current_url.lower()

    @property
    def title(self):
        return self.driver.title.lower()

    @property
    def src(self):
        return self.driver.page_source.lower()
