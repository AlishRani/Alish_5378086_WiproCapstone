"""Base Page Object – all page classes inherit from this."""
import logging
import os
from datetime import datetime

import allure
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
logger         = logging.getLogger("nykaa")


class BasePage:
    BASE_URL = "https://www.nykaa.com"
    WAIT     = 15

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, self.WAIT)

    # ── Navigation ─────────────────────────────────────────────────────────────
    def open(self, path: str = ""):
        url = self.BASE_URL + path
        logger.info(f"[NAV] Opening: {url}")
        self.driver.get(url)
        return self

    def get_title(self) -> str:
        return self.driver.title

    def get_current_url(self) -> str:
        return self.driver.current_url

    # ── Wait helpers ───────────────────────────────────────────────────────────
    def wait_for_element(self, locator, timeout: int = None):
        t = timeout or self.WAIT
        return WebDriverWait(self.driver, t).until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator, timeout: int = None):
        t = timeout or self.WAIT
        return WebDriverWait(self.driver, t).until(EC.element_to_be_clickable(locator))

    def wait_for_visible(self, locator, timeout: int = None):
        t = timeout or self.WAIT
        return WebDriverWait(self.driver, t).until(EC.visibility_of_element_located(locator))

    def wait_for_url_contains(self, text: str, timeout: int = None):
        t = timeout or self.WAIT
        return WebDriverWait(self.driver, t).until(EC.url_contains(text))

    # ── Actions ────────────────────────────────────────────────────────────────
    def click(self, locator):
        el = self.wait_for_clickable(locator)
        try:
            el.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", el)
        logger.debug(f"[CLICK] {locator}")
        return self

    def type_text(self, locator, text: str):
        el = self.wait_for_visible(locator)
        el.clear()
        el.send_keys(text)
        logger.debug(f"[TYPE] '{text}' → {locator}")
        return self

    def get_text(self, locator) -> str:
        return self.wait_for_visible(locator).text.strip()

    def is_element_visible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_present(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def scroll_to_element(self, locator):
        el = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        return el

    def hover(self, locator):
        el = self.wait_for_element(locator)
        ActionChains(self.driver).move_to_element(el).perform()
        logger.debug(f"[HOVER] {locator}")
        return self

    def get_elements_count(self, locator) -> int:
        try:
            return len(self.driver.find_elements(*locator))
        except Exception:
            return 0

    def get_all_elements(self, locator):
        return self.driver.find_elements(*locator)

    # ── Screenshot ─────────────────────────────────────────────────────────────
    def take_screenshot(self, name: str) -> str:
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe     = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        path     = os.path.join(SCREENSHOT_DIR, f"{safe}_{ts}.png")
        self.driver.save_screenshot(path)
        logger.info(f"[SCREENSHOT] {path}")
        allure.attach.file(path, name=name, attachment_type=allure.attachment_type.PNG)
        return path

    # ── JS helpers ─────────────────────────────────────────────────────────────
    def js_click(self, locator):
        el = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].click();", el)
        return self

    def scroll_down(self, pixels: int = 400):
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")

    def close_popup_if_present(self):
        """Dismiss generic overlays / login modals."""
        dismiss_selectors = [
            (By.CSS_SELECTOR, "button.css-1x39bm7"),           # login modal close
            (By.CSS_SELECTOR, "[class*='modalClose']"),
            (By.CSS_SELECTOR, "[aria-label='Close']"),
            (By.XPATH, "//button[contains(@class,'close')]"),
            (By.CSS_SELECTOR, ".css-1rjbe5s"),                  # promo banner close
        ]
        for sel in dismiss_selectors:
            try:
                btn = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(sel))
                self.driver.execute_script("arguments[0].click();", btn)
                logger.info(f"[POPUP] Closed popup via {sel}")
                return True
            except Exception:
                pass
        return False
