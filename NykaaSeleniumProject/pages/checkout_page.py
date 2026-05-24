"""Nykaa Login & Checkout Page Object."""
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("nykaa")


class LoginPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    EMAIL_INPUT   = (By.CSS_SELECTOR,
        "input[type='email'], input[name='email'], input[placeholder*='email' i], "
        "input[placeholder*='mobile' i], input[name='username']"
    )
    PASSWORD_INPUT= (By.CSS_SELECTOR,
        "input[type='password'], input[name='password']"
    )
    LOGIN_SUBMIT  = (By.CSS_SELECTOR,
        "button[type='submit'], button[class*='login'], [class*='LoginBtn'], "
        "button[class*='signin']"
    )
    ERROR_MSG     = (By.CSS_SELECTOR,
        "[class*='error'], [class*='Error'], [class*='invalid'], "
        "[class*='alert'], [aria-live='polite']"
    )
    LOGIN_HEADING = (By.CSS_SELECTOR,
        "h1, h2, [class*='login-title'], [class*='LoginTitle']"
    )
    GUEST_CHECKOUT= (By.CSS_SELECTOR,
        "[class*='guest'], [class*='Guest'], a[href*='guest']"
    )

    def open_login(self):
        self.open("/login")
        logger.info("[LOGIN] Login page opened")
        return self

    def is_login_page(self) -> bool:
        url = self.get_current_url().lower()
        return "login" in url or "signin" in url or "account" in url

    def get_error_message(self) -> str:
        try:
            return self.get_text(self.ERROR_MSG)
        except Exception:
            return ""


class CheckoutPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    CHECKOUT_HEADING   = (By.CSS_SELECTOR,
        "h1, h2, [class*='checkout-title'], [class*='CheckoutTitle']"
    )
    ADDRESS_SECTION    = (By.CSS_SELECTOR,
        "[class*='address'], [class*='Address'], [class*='delivery']"
    )
    PAYMENT_SECTION    = (By.CSS_SELECTOR,
        "[class*='payment'], [class*='Payment'], [class*='pay-section']"
    )
    ORDER_SUMMARY      = (By.CSS_SELECTOR,
        "[class*='order-summary'], [class*='OrderSummary'], [class*='summary']"
    )
    PAYMENT_OPTIONS    = (By.CSS_SELECTOR,
        "[class*='payment-option'], [class*='PaymentOption'], "
        "[class*='payment-method'], [class*='paymentMethod']"
    )
    PLACE_ORDER_BTN    = (By.CSS_SELECTOR,
        "button[class*='place-order'], button[class*='placeOrder'], "
        "button[class*='PlaceOrder'], [class*='pay-now'], button[class*='payNow']"
    )
    UPI_OPTION         = (By.XPATH,
        "//*[contains(translate(text(),'UPI','upi'),'upi') or contains(@class,'upi')]"
    )
    NET_BANKING_OPTION = (By.XPATH,
        "//*[contains(translate(text(),'NETBANKING','netbanking'),'net banking') "
        "    or contains(@class,'netbanking') or contains(@class,'net-banking')]"
    )

    def is_checkout_page(self) -> bool:
        url = self.get_current_url().lower()
        return "checkout" in url or "payment" in url or "order" in url or "address" in url

    def is_payment_section_visible(self) -> bool:
        return self.is_element_visible(self.PAYMENT_SECTION)

    def is_address_section_visible(self) -> bool:
        return self.is_element_visible(self.ADDRESS_SECTION)

    def get_page_heading(self) -> str:
        try:
            return self.get_text(self.CHECKOUT_HEADING)
        except Exception:
            return ""
