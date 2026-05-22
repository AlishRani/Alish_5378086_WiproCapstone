from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class HomePage:
    URL = "https://www.nykaa.com"

    MAKEUP_LINK = (By.XPATH, "//a[contains(@href,'/sp/makeup-clp-desktop/makeup')]")
    LIPSTICK_LINK = (By.XPATH, "//a[@href='/makeup/lips/lipstick/c/249']")
    SEARCH_BOX = (By.NAME, "search-suggestions-nykaa")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.actions = ActionChains(driver)

    def open(self):
        self.driver.get(self.URL)

    def hover_makeup_and_click_lipstick(self):
        makeup = self.wait.until(EC.visibility_of_element_located(self.MAKEUP_LINK))
        self.actions.move_to_element(makeup).perform()
        import time
        time.sleep(1)
        lipstick = self.wait.until(EC.element_to_be_clickable(self.LIPSTICK_LINK))
        lipstick.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def search(self, query):
        search_box = self.wait.until(EC.visibility_of_element_located(self.SEARCH_BOX))
        search_box.clear()
        search_box.send_keys(query)
        search_box.submit()
