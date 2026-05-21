from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

import time


class LoginPage(BasePage):

    SIGN_IN_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Sign in')]"
    )

    MOBILE_INPUT = (
        By.XPATH,
        "//input[@type='tel']"
    )

    SEND_OTP_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Send OTP')]"
    )

    def click_sign_in(self):

        sign_in = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                self.SIGN_IN_BUTTON
            )
        )

        sign_in.click()

    def enter_mobile(self, mobile):

        mobile_field = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                self.MOBILE_INPUT
            )
        )

        mobile_field.clear()

        mobile_field.send_keys(mobile)

    def click_send_otp(self):

        send_otp = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                self.SEND_OTP_BUTTON
            )
        )

        send_otp.click()