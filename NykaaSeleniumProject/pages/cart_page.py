"""Nykaa Cart Page Object."""
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("nykaa")


class CartPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    CART_ITEMS         = (By.CSS_SELECTOR,
        "[class*='cart-item'], [class*='cartItem'], [class*='CartItem'], "
        "[class*='bag-item'], [class*='BagItem']"
    )
    PROCEED_TO_BUY     = (By.CSS_SELECTOR,
        "button[class*='proceed'], button[class*='Proceed'], "
        "a[class*='checkout'], a[class*='Checkout'], "
        "[class*='proceed-to-buy'], [class*='proceedToBuy']"
    )
    CART_TOTAL         = (By.CSS_SELECTOR,
        "[class*='total'], [class*='Total'], [class*='grand-total']"
    )
    REMOVE_ITEM_BTN    = (By.CSS_SELECTOR,
        "button[class*='remove'], [class*='Remove'], [aria-label*='remove'], "
        "[class*='delete'], [class*='Delete']"
    )
    EMPTY_CART_MSG     = (By.CSS_SELECTOR,
        "[class*='empty-cart'], [class*='emptyCart'], [class*='EmptyCart']"
    )
    APPLY_COUPON       = (By.CSS_SELECTOR,
        "input[placeholder*='coupon'], input[placeholder*='Coupon'], "
        "[class*='coupon'] input, [class*='Coupon'] input"
    )
    CART_HEADING       = (By.CSS_SELECTOR,
        "h1, h2, [class*='cart-title'], [class*='CartTitle'], [class*='bag-title']"
    )

    # ── Actions ───────────────────────────────────────────────────────────────
    def open_cart(self):
        self.open("/shoppingbag")
        logger.info("[CART] Cart page opened")
        self.close_popup_if_present()
        return self

    def get_cart_item_count(self) -> int:
        return self.get_elements_count(self.CART_ITEMS)

    def is_cart_empty(self) -> bool:
        return self.is_element_visible(self.EMPTY_CART_MSG)

    def click_proceed_to_buy(self):
        logger.info("[CART] Clicking Proceed to Buy")
        self.scroll_to_element(self.PROCEED_TO_BUY)
        self.click(self.PROCEED_TO_BUY)
        return self

    def get_cart_total(self) -> str:
        try:
            return self.get_text(self.CART_TOTAL)
        except Exception:
            return ""

    def is_cart_page(self) -> bool:
        url = self.get_current_url().lower()
        return "shoppingbag" in url or "cart" in url or "bag" in url
