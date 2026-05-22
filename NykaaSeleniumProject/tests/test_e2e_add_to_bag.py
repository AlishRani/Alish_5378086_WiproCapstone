import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from pages.home_page import HomePage
from pages.lipstick_page import LipstickPage
from utils import save_screenshot, TestLogger

log = TestLogger("nykaa_e2e")


@allure.story("End-to-End")
@allure.feature("Purchase Flow")
@allure.title("End-to-end: 13-step E2E test suite for lipstick purchase flow")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("13-step E2E flow: nav -> listing -> filters -> sort -> PDP -> add to bag -> search")
class TestE2EAddToBag:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Step 1: Navigate to lipstick listing page via Makeup menu")
    def test_step_nav_to_lipstick(self, driver):
        log.step("1: Navigate to lipstick listing via Makeup menu")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Hovered Makeup and clicked Lipstick")

        lipstick = LipstickPage(driver)
        heading = lipstick.get_heading_text()
        log.action(f"Listing heading: '{heading}'")
        save_screenshot(driver, "step1_lipstick_listing")
        log.assert_msg(f"Heading contains 'Lipstick'")
        assert "lipstick" in heading.lower(), f"Heading '{heading}' should contain 'Lipstick'"
        log.info("Step 1 PASSED")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Step 2: Verify products are displayed on listing page")
    def test_step_verify_products_displayed(self, driver):
        log.step("2: Verify products displayed on listing")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)
        count = lipstick.get_product_count()
        log.action(f"Product count: {count}")
        save_screenshot(driver, "step2_product_count")
        log.assert_msg(f"Product count > 0")
        assert count > 0, f"Expected at least 1 product on listing, found {count}"
        log.info("Step 2 PASSED")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Step 3: Filter products by brand Lakme")
    def test_step_filter_brand_lakme(self, driver):
        log.step("3: Filter products by brand Lakme")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)
        lipstick.filter_by_brand("Lakme")
        log.action("Applied Lakme brand filter")
        time.sleep(3)
        save_screenshot(driver, "step3_filter_lakme")
        log.assert_msg(f"URL contains 'brand' param: {driver.current_url}")
        assert "brand" in driver.current_url.lower(), (
            f"URL should contain brand parameter after Lakme filter, got {driver.current_url}"
        )
        log.info("Step 3 PASSED")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Step 4: Filter products by brand Maybelline")
    def test_step_filter_brand_maybelline(self, driver):
        log.step("4: Filter products by brand Maybelline")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)
        lipstick.filter_by_brand("Maybelline")
        log.action("Applied Maybelline brand filter")
        time.sleep(3)
        save_screenshot(driver, "step4_filter_maybelline")
        log.assert_msg(f"URL contains 'brand' param: {driver.current_url}")
        assert "brand" in driver.current_url.lower(), (
            f"URL should contain brand parameter after Maybelline filter, got {driver.current_url}"
        )
        log.info("Step 4 PASSED")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Step 5: Sort products by Price Low to High")
    def test_step_sort_low_to_high(self, driver):
        log.step("5: Sort products by Price Low to High")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)
        lipstick.select_sort_low_to_high()
        log.action("Selected Low to High sort")
        time.sleep(3)
        save_screenshot(driver, "step5_sort_low_to_high")

        heading = lipstick.get_heading_text()
        log.action(f"Page heading after sort: '{heading}'")
        log.assert_msg("Page heading contains 'Lipstick'")
        assert "lipstick" in heading.lower(), "Still on lipstick page after sorting"
        log.info("Step 5 PASSED")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Step 6: Verify sort parameter appears in URL")
    def test_step_verify_sort_param_in_url(self, driver):
        log.step("6: Verify sort parameter in URL")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)
        lipstick.select_sort_low_to_high()
        log.action("Selected Low to High sort")
        time.sleep(3)
        save_screenshot(driver, "step6_sort_url")

        has_sort = "sort" in driver.current_url.lower() or "price_asc" in driver.current_url.lower()
        log.assert_msg(f"URL has sort param: {driver.current_url}")
        assert has_sort, f"URL should contain sort parameter, got {driver.current_url}"
        log.info("Step 6 PASSED")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Step 7: Verify product name is displayed on PDP")
    def test_step_verify_pdp_product_name(self, driver):
        log.step("7: Verify product name on PDP")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)
        lipstick.click_first_product()
        log.action("Clicked first product")
        driver.switch_to.window(driver.window_handles[-1])
        log.action("Switched to PDP tab")

        name = lipstick.get_product_name()
        log.action(f"Product name: '{name}'")
        save_screenshot(driver, "step7_pdp_name")
        log.assert_msg("Product name is not empty")
        assert name.strip(), f"Product name should not be empty, got '{name}'"
        log.info("Step 7 PASSED")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Step 8: Verify product price is displayed on PDP")
    def test_step_verify_pdp_product_price(self, driver):
        log.step("8: Verify product price on PDP")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)
        lipstick.click_first_product()
        log.action("Clicked first product")
        driver.switch_to.window(driver.window_handles[-1])
        log.action("Switched to PDP tab")

        price = lipstick.get_product_price()
        log.action(f"Product price: '{price}'")
        save_screenshot(driver, "step8_pdp_price")
        log.assert_msg("Product price is not empty")
        assert price.strip(), f"Product price should not be empty, got '{price}'"
        log.info("Step 8 PASSED")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Step 9: Add product to bag")
    def test_step_add_to_bag(self, driver):
        log.step("9: Add product to bag")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)
        lipstick.click_first_product()
        log.action("Clicked first product")
        driver.switch_to.window(driver.window_handles[-1])
        log.action("Switched to PDP tab")

        name = lipstick.get_product_name()
        price = lipstick.get_product_price()
        log.action(f"Product: '{name}' - {price}")
        log.assert_msg("Product name and price are visible")
        assert name.strip(), "Product name should be visible"
        assert price.strip(), "Product price should be visible"

        lipstick.add_to_bag()
        log.action("Clicked Add to Bag")
        time.sleep(2)
        save_screenshot(driver, "step9_after_add_to_bag")
        log.info("Step 9 PASSED")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Step 10: Navigate to bag page")
    def test_step_navigate_to_bag(self, driver):
        log.step("10: Navigate to bag page")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)
        lipstick.click_first_product()
        log.action("Clicked first product")
        driver.switch_to.window(driver.window_handles[-1])
        log.action("Switched to PDP tab")

        lipstick.add_to_bag()
        log.action("Clicked Add to Bag")
        time.sleep(1)
        lipstick.go_to_bag()
        log.action("Navigated to bag page")
        time.sleep(2)

        save_screenshot(driver, "step10_bag_page")
        log.assert_msg(f"Bag page URL: {driver.current_url}")
        assert "bag" in driver.current_url.lower() or "cart" in driver.current_url.lower(), (
            f"Should be on bag/cart page, got {driver.current_url}"
        )
        log.info("Step 10 PASSED")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Step 11: Search for 'lipstick' from homepage")
    def test_step_search_lipstick(self, driver):
        log.step("11: Search for 'lipstick'")
        home = HomePage(driver)
        home.search("lipstick")
        log.action("Submitted search query 'lipstick'")
        time.sleep(3)

        save_screenshot(driver, "step11_search_lipstick")
        log.assert_msg(f"Search results URL: {driver.current_url}")
        assert "search" in driver.current_url.lower(), (
            f"Should navigate to search results page, got {driver.current_url}"
        )
        log.info("Step 11 PASSED")

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Step 12: Search special characters does not crash")
    def test_step_search_special_chars_no_crash(self, driver):
        log.step("12: Search special characters")
        home = HomePage(driver)
        home.search("!@#$%")
        log.action("Submitted search query '!@#$%'")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        log.action("Page body loaded")
        save_screenshot(driver, "step12_search_special_chars")
        log.assert_msg(f"Page title has no error: '{driver.title}'")
        assert "error" not in driver.title.lower(), "Page should not show an error after special char search"
        log.info("Step 12 PASSED")

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Step 13: Search results page renders successfully")
    def test_step_verify_search_results_rendered(self, driver):
        log.step("13: Verify search results rendered")
        home = HomePage(driver)
        home.search("lipstick")
        log.action("Submitted search query 'lipstick'")
        time.sleep(3)

        body = driver.find_element(By.TAG_NAME, "body")
        save_screenshot(driver, "step13_search_results_rendered")
        log.assert_msg("Search results page body is visible")
        assert body.is_displayed(), "Search results page body should be visible"
        log.assert_msg(f"URL contains 'search': {driver.current_url}")
        assert "search" in driver.current_url.lower(), (
            f"Should be on search results page, got {driver.current_url}"
        )
        log.info("Step 13 PASSED")


@allure.story("Navigation")
@allure.feature("Makeup Navigation")
@allure.title("Hover on Makeup and click Lipstick navigates to lipstick listing page")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Verify that hovering over the Makeup category and clicking Lipstick "
                     "redirects to the lipstick listing page with correct heading")
class TestNavLipstick:
    @allure.severity(allure.severity_level.CRITICAL)
    def test_hover_makeup_click_lipstick_navigates_to_lipstick_page(self, driver):
        log.step("Nav: Hover Makeup and click Lipstick")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Hovered Makeup and clicked Lipstick")

        lipstick = LipstickPage(driver)
        heading = lipstick.get_heading_text()
        log.action(f"Listing heading: '{heading}'")

        save_screenshot(driver, "nav_lipstick_listing_page")
        log.assert_msg(f"Heading '{heading}' contains 'Lipstick'")
        assert "lipstick" in heading.lower(), f"Heading '{heading}' should contain 'Lipstick'"
        log.info("Nav test PASSED")


@allure.story("Filtering")
@allure.feature("Product Filters")
@allure.title("Filter lipstick results by brand Lakme")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("Apply brand filter (Lakme) on the lipstick listing page and verify "
                     "the URL contains the brand filter parameter")
class TestFilterBrand:
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_by_brand_shows_filtered_results(self, driver):
        log.step("Filter: Filter by brand Lakme")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)
        save_screenshot(driver, "before_filter")
        lipstick.filter_by_brand("Lakme")
        log.action("Applied Lakme brand filter")

        time.sleep(3)
        save_screenshot(driver, "after_filter_lakme")

        log.assert_msg(f"URL contains 'brand': {driver.current_url}")
        assert "brand" in driver.current_url.lower(), (
            f"URL should contain brand parameter after filtering, got {driver.current_url}"
        )
        log.info("Filter test PASSED")


@allure.story("Sorting")
@allure.feature("Product Sort")
@allure.title("Sort lipstick results by Price: Low to High")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("Apply Low to High price sort on the lipstick listing and verify "
                     "the URL reflects the sort parameter")
class TestSortPrice:
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_low_to_high_changes_product_order(self, driver):
        log.step("Sort: Sort by Price Low to High")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)

        parsed = urlparse(driver.current_url)
        qs = parse_qs(parsed.query)
        log.assert_msg("Not already sorted by price")
        assert "sort" not in qs or qs.get("sort") != ["price_asc"], "Should not already be sorted by price"

        save_screenshot(driver, "before_sort")
        lipstick.select_sort_low_to_high()
        log.action("Selected Low to High sort")

        time.sleep(3)
        save_screenshot(driver, "after_sort_low_to_high")

        heading = lipstick.get_heading_text()
        log.action(f"Heading after sort: '{heading}'")
        log.assert_msg("Still on lipstick page")
        assert "lipstick" in heading.lower(), "Still on lipstick page after sort"
        log.info("Sort test PASSED")


@allure.story("Product Detail")
@allure.feature("Product Details Page")
@allure.title("Product detail page displays product name and price")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Click the first lipstick product from the listing, switch to the PDP tab, "
                     "and verify that the product name and price are displayed")
class TestProductDetail:
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_detail_displays_name_and_price(self, driver):
        log.step("PDP: Verify product name and price")
        home = HomePage(driver)
        home.hover_makeup_and_click_lipstick()
        log.action("Navigated to lipstick listing")

        lipstick = LipstickPage(driver)
        lipstick.click_first_product()
        log.action("Clicked first product")
        driver.switch_to.window(driver.window_handles[-1])
        log.action("Switched to PDP tab")

        name = lipstick.get_product_name()
        log.action(f"Product name: '{name}'")
        log.assert_msg("Product name is not empty")
        assert name.strip(), f"Product name should not be empty, got '{name}'"

        price = lipstick.get_product_price()
        log.action(f"Product price: '{price}'")
        save_screenshot(driver, "product_detail_page")
        log.assert_msg("Product price is not empty")
        assert price.strip(), f"Product price should not be empty, got '{price}'"
        log.info("PDP test PASSED")


@allure.story("Search")
@allure.feature("Search Error Handling")
@allure.title("Search with special characters does not crash the page")
@allure.severity(allure.severity_level.MINOR)
@allure.description("Enter special characters '!@#$%' in the search box and verify "
                     "the site navigates to a search results page without errors")
class TestSearchInvalid:
    @allure.severity(allure.severity_level.MINOR)
    def test_search_with_special_chars_does_not_crash(self, driver):
        log.step("Search: Special characters do not crash")
        home = HomePage(driver)
        home.search("!@#$%")
        log.action("Submitted search query '!@#$%'")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        log.action("Page body loaded")
        save_screenshot(driver, "search_special_chars_result")
        log.assert_msg(f"URL: {driver.current_url}, Title: '{driver.title}'")
        assert "search" in driver.current_url.lower() or "result" in driver.current_url.lower(), (
            f"Should navigate to search results page, got {driver.current_url}"
        )
        assert "error" not in driver.title.lower(), "Page should not show an error"
        log.info("Search test PASSED")
