from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class CartPage(BasePage):

    PROCEED_BUTTON = (
        By.XPATH,
        "//span[contains(text(),'Proceed')]"
    )

    QUANTITY_DROPDOWN = (
        By.TAG_NAME,
        "select"
    )

    def switch_to_cart_iframe(self):

        time.sleep(5)

        frames = self.driver.find_elements(By.TAG_NAME, "iframe")

        self.driver.switch_to.frame(frames[0])

    def click_proceed(self):

        self.click_element(self.PROCEED_BUTTON)