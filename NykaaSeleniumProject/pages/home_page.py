from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class HomePage(BasePage):

    SEARCH_BOX = (
        By.XPATH,
        "//input[contains(@placeholder,'Search')]"
    )

    def search_product(self, product):

        search = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                self.SEARCH_BOX
            )
        )

        search.clear()

        search.send_keys(product)