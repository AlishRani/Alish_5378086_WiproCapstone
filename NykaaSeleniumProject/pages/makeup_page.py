from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class MakeupPage(BasePage):

    FIRST_PRODUCT = (
        By.XPATH,
        "(//a[contains(@href,'/p/')])[1]"
    )

    SHADE_OPTION = (
        By.XPATH,
        "(//button[contains(@class,'shade')])[1]"
    )

    ADD_TO_BAG = (
        By.XPATH,
        "//span[contains(text(),'Add to Bag')]"
    )

    PRODUCT_TITLE = (
        By.TAG_NAME,
        "h1"
    )

    def open_first_product(self):

        product = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.FIRST_PRODUCT)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            product
        )

        time.sleep(2)

        self.driver.execute_script(
            "arguments[0].click();",
            product
        )

    def select_shade(self):

        try:

            shade = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    self.SHADE_OPTION
                )
            )

            shade.click()

        except:

            print("Shade option not available")

    def add_product_to_bag(self):

        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time

        wait = WebDriverWait(self.driver, 30)

        # HANDLE NEW TAB
        all_tabs = self.driver.window_handles

        if len(all_tabs) > 1:
            self.driver.switch_to.window(all_tabs[-1])

        time.sleep(5)

        # SCROLL LITTLE DOWN
        self.driver.execute_script(
            "window.scrollBy(0,400);"
        )

        time.sleep(3)

        # MULTIPLE XPATHS
        add_to_bag_xpaths = [

            "//button[contains(.,'Add to Bag')]",

            "//span[contains(text(),'Add to Bag')]",

            "//button[contains(.,'Add to Cart')]",

            "//button[contains(@class,'add-to-bag')]",

            "//div[contains(text(),'Add to Bag')]",

        ]

        clicked = False

        for xpath in add_to_bag_xpaths:

            try:

                add_button = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            xpath
                        )
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    add_button
                )

                clicked = True

                print("Add To Bag Clicked")

                break

            except:
                continue

        if not clicked:
            print("Add To Bag Button Not Found")

            assert False

    def get_product_title(self):

        title = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                self.PRODUCT_TITLE
            )
        )

        return title.text