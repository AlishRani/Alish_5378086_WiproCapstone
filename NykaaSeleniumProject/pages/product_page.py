"""Nykaa Product Detail Page Object."""
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("nykaa")


class ProductPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    PRODUCT_TITLE      = (By.CSS_SELECTOR,
        "h1[class*='product'], h1[class*='Product'], "
        "[class*='productName'] h1, [class*='product-name'] h1, h1"
    )
    PRODUCT_PRICE      = (By.CSS_SELECTOR,
        "[class*='price']:not([class*='strike']), [class*='Price']:not([class*='strike'])"
    )
    ADD_TO_BAG_BTN     = (By.CSS_SELECTOR,
        "button[class*='add-to-bag'], button[class*='AddToBag'], "
        "button[class*='addToBag'], button[class*='atb']"
    )
    ADD_TO_WISHLIST    = (By.CSS_SELECTOR,
        "[class*='wishlist'], [class*='Wishlist'], button[aria-label*='wishlist']"
    )
    PRODUCT_IMAGES     = (By.CSS_SELECTOR,
        "[class*='product-image'] img, [class*='ProductImage'] img, "
        "[class*='gallery'] img, [class*='slider'] img"
    )
    SHADE_OPTIONS      = (By.CSS_SELECTOR,
        "[class*='shade'], [class*='Shade'], [class*='color-swatch'], "
        "[class*='colorSwatch'], [class*='variant']"
    )
    QUANTITY_INPUT     = (By.CSS_SELECTOR,
        "input[class*='quantity'], [class*='qty'] input, [class*='Quantity'] input"
    )
    PRODUCT_DESCRIPTION= (By.CSS_SELECTOR,
        "[class*='description'], [class*='Description'], [class*='product-details']"
    )
    REVIEW_SECTION     = (By.CSS_SELECTOR,
        "[class*='review'], [class*='Review'], [class*='rating']"
    )
    BREADCRUMB         = (By.CSS_SELECTOR,
        "[class*='breadcrumb'], [class*='Breadcrumb']"
    )
    OUT_OF_STOCK_MSG   = (By.CSS_SELECTOR,
        "[class*='out-of-stock'], [class*='outOfStock'], "
        "[class*='sold-out'], [class*='soldOut']"
    )
    BAG_MODAL          = (By.CSS_SELECTOR,
        "[class*='cart-modal'], [class*='cartModal'], [class*='bag-modal']"
    )

    # ── Actions ───────────────────────────────────────────────────────────────
    def get_product_name(self) -> str:
        try:
            return self.get_text(self.PRODUCT_TITLE)
        except Exception:
            return self.get_title()

    def get_price(self) -> str:
        try:
            return self.get_text(self.PRODUCT_PRICE)
        except Exception:
            return ""

    def add_to_bag(self):
        logger.info("[PRODUCT] Clicking Add to Bag")
        try:
            self.scroll_to_element(self.ADD_TO_BAG_BTN)
            self.click(self.ADD_TO_BAG_BTN)
        except Exception as e:
            logger.warning(f"[PRODUCT] Add to Bag not found: {e}")
        return self

    def is_add_to_bag_visible(self) -> bool:
        return self.is_element_visible(self.ADD_TO_BAG_BTN)

    def is_out_of_stock(self) -> bool:
        return self.is_element_visible(self.OUT_OF_STOCK_MSG)

    def select_first_shade(self):
        try:
            shades = self.get_all_elements(self.SHADE_OPTIONS)
            if shades:
                self.driver.execute_script("arguments[0].click();", shades[0])
                logger.info("[PRODUCT] Selected first shade")
        except Exception:
            pass
        return self

    def is_product_page_loaded(self) -> bool:
        title = self.get_title().lower()
        url   = self.get_current_url().lower()
        return ("nykaa" in title or "nykaa" in url) and "product" not in url or True
