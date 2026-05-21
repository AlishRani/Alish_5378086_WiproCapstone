from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class CheckoutPage(BasePage):

    NAME_FIELD = (
        By.NAME,
        "name"
    )

    PHONE_FIELD = (
        By.NAME,
        "phoneNumber"
    )

    PINCODE_FIELD = (
        By.NAME,
        "postalCode"
    )

    ADDRESS_FIELD = (
        By.NAME,
        "address"
    )

    AREA_FIELD = (
        By.NAME,
        "roadArea"
    )

    SAVE_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Ship to this address')]"
    )

    PAYMENT_PAGE_TEXT = (
        By.TAG_NAME,
        "body"
    )

    def fill_name(self, name):

        self.enter_text(self.NAME_FIELD, name)

    def fill_phone(self, phone):

        self.enter_text(self.PHONE_FIELD, phone)

    def fill_pincode(self, pincode):

        self.enter_text(self.PINCODE_FIELD, pincode)

    def fill_address(self, address):

        self.enter_text(self.ADDRESS_FIELD, address)

    def fill_area(self, area):

        self.enter_text(self.AREA_FIELD, area)

    def save_address(self):

        self.click_element(self.SAVE_BUTTON)

    def complete_address(
            self,
            name,
            phone,
            pincode,
            address,
            area):

        time.sleep(3)

        self.fill_name(name)

        self.fill_phone(phone)

        self.fill_pincode(pincode)

        self.fill_address(address)

        self.fill_area(area)

        self.save_address()

    def get_payment_page_text(self):

        return self.get_text(self.PAYMENT_PAGE_TEXT)