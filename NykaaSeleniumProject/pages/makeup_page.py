"""Nykaa Makeup Category Page Object."""
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("nykaa")


class MakeupPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    PAGE_HEADING      = (By.CSS_SELECTOR, "h1, [class*='heading'], [class*='pageTitle']")
    LIPSTICK_SUBCAT   = (By.XPATH,
        "//a[contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'lipstick')]"
        " | //*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'lipstick') "
        "       and (self::a or self::button or self::li)]"
    )
    PRODUCT_CARDS     = (By.CSS_SELECTOR,
        "[class*='product-card'], [class*='productCard'], [class*='ProductCard'], "
        "[class*='product_card'], article[class*='product']"
    )
    PRODUCT_NAMES     = (By.CSS_SELECTOR,
        "[class*='product-name'], [class*='productName'], [class*='ProductName'], "
        "[class*='product_name'], [class*='product-title'], h3[class*='product']"
    )
    PRODUCT_PRICES    = (By.CSS_SELECTOR,
        "[class*='product-price'], [class*='ProductPrice'], [class*='price'], "
        "span[class*='price'], [class*='priceContainer']"
    )
    ADD_TO_BAG_BTN    = (By.CSS_SELECTOR,
        "button[class*='add-to-bag'], button[class*='addToBag'], "
        "button[class*='AddToBag'], button[class*='add_to_bag'], "
        "button[class*='atb'], [data-testid*='add-to-bag']"
    )
    FIRST_PRODUCT     = (By.CSS_SELECTOR,
        "[class*='product-card']:first-child a, [class*='productCard']:first-child a, "
        "a[class*='product']:first-of-type, [class*='ProductCard']:first-child a"
    )
    FILTER_SECTION    = (By.CSS_SELECTOR,
        "[class*='filter'], [class*='Filter'], [class*='sidebar'], aside"
    )
    SORT_DROPDOWN     = (By.CSS_SELECTOR,
        "[class*='sort'], [class*='Sort'], select[name*='sort'], "
        "[class*='sortBy'], [data-testid*='sort']"
    )
    BREADCRUMB        = (By.CSS_SELECTOR,
        "[class*='breadcrumb'], [class*='Breadcrumb'], nav[aria-label*='breadcrumb']"
    )
    LOAD_MORE_BTN     = (By.CSS_SELECTOR,
        "button[class*='load-more'], button[class*='loadMore'], "
        "[class*='LoadMore'], button[class*='show-more']"
    )
    PRICE_FILTER      = (By.XPATH,
        "//*[contains(@class,'filter')]//*[contains(text(),'Price') or contains(text(),'price')]"
    )
    BRAND_FILTER_ITEM = (By.CSS_SELECTOR,
        "[class*='filter'] [class*='item']:first-child, "
        "[class*='filterItem']:first-child, [class*='brandItem']:first-child"
    )
    NO_RESULTS_MSG    = (By.CSS_SELECTOR,
        "[class*='no-result'], [class*='noResult'], [class*='empty'], "
        "[class*='notFound'], [class*='zero-result']"
    )

    # ── Actions ───────────────────────────────────────────────────────────────
    def open_makeup(self):
        self.open("/beauty/makeup-c-3")
        logger.info("[MAKEUP] Makeup page opened")
        self.close_popup_if_present()
        return self

    def open_lipstick(self):
        self.open("/beauty/lips/lipstick-c-959")
        logger.info("[MAKEUP] Lipstick page opened")
        self.close_popup_if_present()
        return self

    def click_lipstick_subcategory(self):
        logger.info("[MAKEUP] Clicking Lipstick subcategory")
        try:
            self.scroll_to_element(self.LIPSTICK_SUBCAT)
            self.click(self.LIPSTICK_SUBCAT)
        except Exception:
            self.open_lipstick()
        return self

    def get_product_count(self) -> int:
        count = self.get_elements_count(self.PRODUCT_CARDS)
        logger.info(f"[MAKEUP] Product cards visible: {count}")
        return count

    def get_product_names(self) -> list:
        els   = self.get_all_elements(self.PRODUCT_NAMES)
        names = [el.text.strip() for el in els if el.text.strip()]
        logger.info(f"[MAKEUP] {len(names)} product names collected")
        return names

    def get_product_prices(self) -> list:
        els    = self.get_all_elements(self.PRODUCT_PRICES)
        prices = [el.text.strip() for el in els if el.text.strip()]
        return prices

    def click_first_product(self):
        logger.info("[MAKEUP] Clicking first product")
        try:
            cards = self.get_all_elements(self.PRODUCT_CARDS)
            if cards:
                link = cards[0].find_element(*("tag name", "a")) if hasattr(cards[0], "find_element") else None
                if link:
                    self.driver.execute_script("arguments[0].click();", link)
                    return self
        except Exception:
            pass
        self.js_click(self.FIRST_PRODUCT)
        return self

    def is_makeup_page(self) -> bool:
        url = self.get_current_url().lower()
        return "makeup" in url or "beauty" in url

    def is_lipstick_page(self) -> bool:
        url = self.get_current_url().lower()
        return "lipstick" in url or "lips" in url

    def is_filter_section_visible(self) -> bool:
        return self.is_element_visible(self.FILTER_SECTION)

    def is_sort_option_visible(self) -> bool:
        return self.is_element_visible(self.SORT_DROPDOWN)

    def are_products_displayed(self) -> bool:
        count = self.get_product_count()
        return count > 0

    def search_lipstick_directly(self):
        """Navigate directly to search results for lipstick."""
        self.open("/search/result/?q=lipstick&root=search&searchType=Manual&sourcepage=home")
        logger.info("[MAKEUP] Opened lipstick search results")
        self.close_popup_if_present()
        return self
