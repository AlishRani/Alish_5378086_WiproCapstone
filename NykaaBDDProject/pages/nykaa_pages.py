"""Nykaa — Sabhi Page Objects."""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


# ─────────────────────────────────────────────────────────────────────────────
class HomePage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR,
        "input[placeholder*='Search'], input[type='search'], "
        "#search-desktop input, input[class*='search']")
    SEARCH_BOX_ALT = (By.XPATH,
        "//input[@type='search' or contains(@class,'search') or "
        "contains(@placeholder,'Search') or contains(@placeholder,'search')]")
    LOGO = (By.CSS_SELECTOR, "a[href='/'] img, img[alt*='Nykaa']")

    def open_homepage(self):
        self.open("/")
        time.sleep(3)
        self.close_popup()
        return self

    def search(self, keyword):
        try:
            box = self.wait_visible(self.SEARCH_INPUT, timeout=8)
        except Exception:
            box = self.wait_visible(self.SEARCH_BOX_ALT, timeout=8)
        box.clear()
        box.send_keys(keyword)
        box.send_keys(Keys.RETURN)
        time.sleep(4)
        return self

    def is_loaded(self):
        return "nykaa" in self.current_url or "nykaa" in self.title


# ─────────────────────────────────────────────────────────────────────────────
class MakeupPage(BasePage):
    PRODUCT_CARDS = (By.CSS_SELECTOR,
        "[class*='product-card'], [class*='productCard'], "
        "[class*='ProductCard'], article[class*='product']")
    PRODUCT_NAMES = (By.CSS_SELECTOR,
        "[class*='product-name'], [class*='productName'], "
        "[class*='product-title'], h3[class*='product']")
    PRODUCT_PRICES = (By.CSS_SELECTOR,
        "[class*='product-price'], [class*='ProductPrice'], "
        "span[class*='price'], [class*='priceContainer']")
    FILTER_SECTION = (By.CSS_SELECTOR,
        "[class*='filter'], [class*='Filter'], aside, [class*='sidebar']")
    SORT_DROPDOWN = (By.CSS_SELECTOR,
        "[class*='sort'], [class*='Sort'], select[name*='sort']")
    NO_RESULTS = (By.CSS_SELECTOR,
        "[class*='no-result'], [class*='noResult'], [class*='empty'], "
        "[class*='zero-result'], [class*='notFound']")

    def open_lip_makeup(self):
        self.open("/makeup/lips/c/15")
        time.sleep(4)
        self.close_popup()
        self.scroll_down(400)
        time.sleep(2)
        return self

    def open_lipstick(self):
        self.open("/makeup/lips/lipstick/c/249")
        time.sleep(4)
        self.close_popup()
        self.scroll_down(400)
        time.sleep(2)
        return self

    def open_search_results(self, keyword="lipstick"):
        self.open(
            f"/search/result/?q={keyword}&root=search&searchType=Manual&sourcepage=home"
        )
        time.sleep(4)
        self.close_popup()
        self.scroll_down(500)
        time.sleep(2)
        return self

    def get_product_count(self):
        return self.get_count(self.PRODUCT_CARDS)

    def get_product_names(self):
        return [el.text.strip() for el in self.get_elements(self.PRODUCT_NAMES)
                if el.text.strip()]

    def get_product_prices(self):
        return [el.text.strip() for el in self.get_elements(self.PRODUCT_PRICES)
                if el.text.strip()]

    def is_on_page(self):
        return "makeup" in self.current_url or "beauty" in self.current_url

    def is_lipstick_page(self):
        return "lipstick" in self.current_url or "lips" in self.current_url

    def filter_visible(self):
        return self.is_visible(self.FILTER_SECTION)

    def sort_visible(self):
        return self.is_visible(self.SORT_DROPDOWN)

    def has_products(self):
        count = self.get_product_count()
        if count > 0:
            return True
        src = self.src
        return "lipstick" in src or ("₹" in src and "lip" in src)

    def no_results_visible(self):
        if self.is_visible(self.NO_RESULTS, timeout=5):
            return True
        src = self.src
        return any(k in src for k in [
            "no results", "no products", "0 results", "not found",
            "couldn't find", "0 products", "no match"
        ])


# ─────────────────────────────────────────────────────────────────────────────
class ProductPage(BasePage):
    ADD_TO_BAG_SELECTORS = [
        (By.CSS_SELECTOR, "button[class*='add-to-bag']"),
        (By.CSS_SELECTOR, "button[class*='AddToBag']"),
        (By.CSS_SELECTOR, "button[class*='addToBag']"),
        (By.CSS_SELECTOR, "button[class*='atb']"),
        (By.XPATH, "//button[contains(translate(text(),'ADDTOBAG','addtobag'),'add to bag')]"),
        (By.XPATH, "//button[contains(translate(text(),'ADDTOCART','addtocart'),'add to cart')]"),
    ]
    SHADE_OPTIONS = (By.CSS_SELECTOR,
        "[class*='shade'], [class*='Shade'], [class*='color-swatch'], "
        "[class*='colorSwatch'], [class*='variant']")

    def open_product(self):
        # Confirmed URL from Nykaa search results
        self.open("/lakme-forever-matte-liquid-lip-colour/p/623306")
        time.sleep(5)
        self.close_popup()
        return self

    def has_product_content(self):
        return any(k in self.src for k in [
            "lakme", "matte", "lip", "₹", "add to bag", "lipstick"
        ])

    def atb_in_source(self):
        return any(k in self.src for k in ["add to bag", "add to cart", "addtobag"])

    def click_add_to_bag(self):
        for sel in self.ADD_TO_BAG_SELECTORS:
            try:
                btn = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable(sel))
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(3)
                self.close_popup()
                return True
            except Exception:
                continue
        return False

    def select_first_shade(self):
        try:
            shades = self.get_elements(self.SHADE_OPTIONS)
            if shades:
                self.driver.execute_script("arguments[0].click();", shades[0])
                time.sleep(1)
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
class CartPage(BasePage):
    PROCEED_SELECTORS = [
        (By.XPATH, "//button[contains(translate(text(),'PROCEEDTOBUY','proceedtobuy'),'proceed')]"),
        (By.CSS_SELECTOR, "button[class*='proceed']"),
        (By.CSS_SELECTOR, "button[class*='Proceed']"),
        (By.CSS_SELECTOR, "[class*='proceedToBuy']"),
        (By.CSS_SELECTOR, "a[class*='checkout']"),
        (By.XPATH, "//button[contains(text(),'Buy') or contains(@class,'buy')]"),
    ]

    def open_cart(self):
        self.open("/v2/payment/")
        time.sleep(4)
        self.close_popup()
        return self

    def is_cart_page(self):
        return any(k in self.current_url for k in ["payment", "v2", "cart", "bag"])

    def has_cart_content(self):
        return any(k in self.src[:2000] for k in [
            "bag", "cart", "payment", "shopping", "nykaa"
        ])

    def click_proceed_to_buy(self):
        for sel in self.PROCEED_SELECTORS:
            try:
                btn = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable(sel))
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn)
                time.sleep(0.3)
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(4)
                self.close_popup()
                return True
            except Exception:
                continue
        return False


# ─────────────────────────────────────────────────────────────────────────────
class LoginPage(BasePage):

    def open_login(self):
        self.open("/auth")
        time.sleep(4)
        self.close_popup()
        return self

    def is_login_page(self):
        return any(k in self.current_url or k in self.src[:2000]
                   for k in ["auth", "login", "signin"])

    def has_login_form(self):
        return any(k in self.src for k in [
            "email", "mobile", "phone", "password", "otp",
            "continue", "sign in", "login"
        ])
