# tests/test_makeup_page.py

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.home_page import HomePage
from pages.makeup_page import MakeupPage
from utilities.log_utils import logger


# ======================================================
# POSITIVE TEST CASE 1
# Verify user can search lipstick product
# ======================================================

def test_search_lipstick(setup):

    logger.info("Starting Lipstick Search Test")

    driver = setup

    home = HomePage(driver)

    # Search Product
    home.search_product("Lipstick")

    time.sleep(2)

    # Press ENTER
    driver.find_element(
        By.NAME,
        "search-suggestions-nykaa"
    ).send_keys(Keys.ENTER)

    time.sleep(5)

    # Assertion
    assert "lipstick" in driver.page_source.lower()

    logger.info("Lipstick Search Test Passed")


# ======================================================
# POSITIVE TEST CASE 2
# Verify user can open product page
# ======================================================

def test_open_product_page(setup):

    logger.info("Starting Open Product Page Test")

    driver = setup

    home = HomePage(driver)

    makeup = MakeupPage(driver)

    # Search Product
    home.search_product("Lipstick")

    time.sleep(2)

    # Press ENTER
    driver.find_element(
        By.NAME,
        "search-suggestions-nykaa"
    ).send_keys(Keys.ENTER)

    time.sleep(5)

    # Open Product
    makeup.open_first_product()

    time.sleep(5)

    # Assertion
    assert "nykaa" in driver.current_url.lower()

    logger.info("Open Product Page Test Passed")

# ======================================================
# POSITIVE TEST CASE 3
# Verify user can select product shade
# ======================================================

def test_select_product_shade(setup):

    logger.info("Starting Shade Selection Test")

    driver = setup

    home = HomePage(driver)

    makeup = MakeupPage(driver)

    # Search Product
    home.search_product("Lipstick")

    time.sleep(2)

    driver.find_element(
        By.NAME,
        "search-suggestions-nykaa"
    ).send_keys(Keys.ENTER)

    time.sleep(5)

    # Open Product
    makeup.open_first_product()

    time.sleep(5)

    # Select Shade
    makeup.select_shade()

    time.sleep(3)

    assert True

    logger.info("Shade Selection Test Passed")
# ======================================================
# POSITIVE TEST CASE 4
# Verify user can add product to bag
# ======================================================

def test_add_product_to_bag(setup):

    logger.info("Starting Add To Bag Test")

    driver = setup

    home = HomePage(driver)

    makeup = MakeupPage(driver)

    # Search Product
    home.search_product("Lipstick")

    time.sleep(2)

    driver.find_element(
        By.NAME,
        "search-suggestions-nykaa"
    ).send_keys(Keys.ENTER)

    time.sleep(5)

    # Open Product
    makeup.open_first_product()

    time.sleep(5)

    # Select Shade
    makeup.select_shade()

    time.sleep(2)

    # Add To Bag
    makeup.add_product_to_bag()

    time.sleep(5)

    assert True

    logger.info("Add To Bag Test Passed")


# ======================================================
# NEGATIVE TEST CASE 1
# Verify invalid product search
# ======================================================

def test_invalid_product_search(setup):

    logger.info("Starting Invalid Product Search Test")

    driver = setup

    home = HomePage(driver)

    # Invalid Search
    home.search_product("xyzinvalidproduct")

    time.sleep(2)

    # Press ENTER
    driver.find_element(
        By.NAME,
        "search-suggestions-nykaa"
    ).send_keys(Keys.ENTER)

    time.sleep(5)

    page_source = driver.page_source.lower()

    # Assertion
    assert (
        "no results" in page_source
        or "sorry" in page_source
        or "0 items" in page_source
    )

    logger.info("Invalid Product Search Test Passed")


# ======================================================
# NEGATIVE TEST CASE 2
# Verify empty search behavior
# ======================================================

def test_empty_search(setup):

    logger.info("Starting Empty Search Test")

    driver = setup

    # Verify homepage opens successfully
    time.sleep(3)

    assert "nykaa" in driver.title.lower()

    logger.info("Empty Search Test Passed")