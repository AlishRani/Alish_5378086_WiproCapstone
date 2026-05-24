"""Nykaa Home Page Object."""
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage

logger = logging.getLogger("nykaa")


class HomePage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    LOGO             = (By.CSS_SELECTOR, "a[href='/'] img, [class*='logo'] img, img[alt*='Nykaa']")
    SEARCH_INPUT     = (By.CSS_SELECTOR, "input[placeholder*='Search'], input[type='search'], #search-desktop input")
    SEARCH_BTN       = (By.CSS_SELECTOR, "button[class*='search'], [class*='searchIcon']")
    NAV_MAKEUP       = (By.XPATH,
        "//nav//*[contains(translate(text(),'MAKEUP','makeup'),'makeup')] | "
        "//a[contains(@href,'makeup')] | //li[contains(@class,'nav')]//*[text()='Makeup']")
    SIGNIN_BTN       = (By.CSS_SELECTOR,
        "[class*='signIn'], [class*='login'], a[href*='login'], button[class*='login']")
    CART_ICON        = (By.CSS_SELECTOR,
        "a[href*='cart'], [class*='cart'] a, [class*='Cart']")
    BANNER           = (By.CSS_SELECTOR, "[class*='banner'], [class*='hero'], [class*='slider']")
    CATEGORY_LINKS   = (By.CSS_SELECTOR, "nav a, [class*='navigation'] a, [class*='NavItem'] a")
    MAKEUP_NAV_LINK  = (By.XPATH,
        "//a[contains(@href, 'makeup') and not(contains(@href, 'http'))]"
        " | //a[normalize-space(text())='Makeup']"
        " | //*[@data-testid='nav-makeup']"
    )
    # Generic makeup search fallback
    SEARCH_BOX_ALT   = (By.XPATH, "//input[@type='search' or contains(@class,'search') or @placeholder]")

    def open_homepage(self):
        self.open("/")
        logger.info("[HOME] Homepage opened")
        self.close_popup_if_present()
        return self

    def search(self, keyword: str):
        logger.info(f"[HOME] Searching for: {keyword}")
        try:
            box = self.wait_for_visible(self.SEARCH_INPUT, timeout=10)
        except Exception:
            box = self.wait_for_visible(self.SEARCH_BOX_ALT, timeout=10)
        box.clear()
        box.send_keys(keyword)
        box.send_keys(Keys.RETURN)
        return self

    def click_makeup_nav(self):
        logger.info("[HOME] Clicking Makeup in nav")
        try:
            self.hover(self.MAKEUP_NAV_LINK)
            self.click(self.MAKEUP_NAV_LINK)
        except Exception:
            # Fallback: navigate directly
            self.open("/beauty/makeup-c-3")
        return self

    def is_loaded(self) -> bool:
        title = self.get_title().lower()
        url   = self.get_current_url().lower()
        return "nykaa" in title or "nykaa" in url

    def click_signin(self):
        self.click(self.SIGNIN_BTN)
        return self

    def get_cart_count(self) -> str:
        try:
            return self.get_text(self.CART_ICON)
        except Exception:
            return "0"
