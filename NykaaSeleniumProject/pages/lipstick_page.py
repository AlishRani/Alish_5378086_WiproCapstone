from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


class LipstickPage:
    PAGE_HEADING = (By.TAG_NAME, "h1")
    PRODUCT_LINKS = (By.XPATH, "//a[contains(@href,'/p/')]")
    FIRST_PRODUCT_LINK = (By.XPATH, "(//a[contains(@href,'/p/')])[1]")

    ADD_TO_BAG_BUTTON = (By.XPATH, "//button[contains(text(),'Add to Bag')] | //span[contains(text(),'Add to Bag')]/..")
    BAG_ICON = (By.CSS_SELECTOR, "[class*='bag'] a, [class*='Bag'] a, a[href*='bag'], a[href*='Bag']")

    SORT_LOW_TO_HIGH = (By.XPATH, "//*[contains(text(),'Low to High')]")
    SORT_DROPDOWN = (By.XPATH, "//*[contains(text(),'Popularity')] | //*[contains(text(),'Sort')]")

    BRAND_FILTER = (By.XPATH, "//*[contains(text(),'Brand')]")
    LAKME_CHECKBOX = (By.XPATH, "//*[contains(text(),'Lakme')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.actions = ActionChains(driver)

    def get_heading_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.PAGE_HEADING)).text

    def click_first_product(self):
        link = self.wait.until(EC.element_to_be_clickable(self.FIRST_PRODUCT_LINK))
        link.click()

    def get_product_name(self):
        return self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text

    def get_product_price(self):
        return self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(),'₹')]")
        )).text

    def add_to_bag(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_BAG_BUTTON)).click()

    def go_to_bag(self):
        try:
            self.wait.until(EC.element_to_be_clickable(self.BAG_ICON)).click()
        except TimeoutException:
            self.driver.get("https://www.nykaa.com/checkout/cart")

    def is_item_in_bag(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH,
                                                "//*[contains(@class,'item')] | "
                                                "//*[contains(@class,'cart')] | "
                                                "//*[contains(@class,'product')]"))
            )
            return True
        except TimeoutException:
            return False

    def click_proceed_to_checkout(self):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Proceed')] | //a[contains(text(),'Proceed')]")
        )).click()

    def is_login_page_displayed(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH,
                                                "//input[@type='email'] | "
                                                "//input[@type='password'] | "
                                                "//*[contains(text(),'Login')]"))
            )
            return True
        except TimeoutException:
            return False

    def get_product_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_LINKS))

    def select_sort_low_to_high(self):
        try:
            sort = self.driver.find_element(*self.SORT_DROPDOWN)
            self.driver.execute_script("arguments[0].click();", sort)
            self.wait.until(EC.element_to_be_clickable(self.SORT_LOW_TO_HIGH)).click()
        except Exception:
            self.driver.get("https://www.nykaa.com/makeup/lips/lipstick/c/249?sort=price_asc")

    def filter_by_brand(self, brand="Lakme"):
        try:
            brand_btn = self.driver.find_element(*self.BRAND_FILTER)
            self.driver.execute_script("arguments[0].click();", brand_btn)
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//*[contains(text(),'{brand}')]")
            )).click()
        except Exception:
            self.driver.get(
                f"https://www.nykaa.com/makeup/lips/lipstick/c/249?brand={brand}&root=nav_4"
            )
