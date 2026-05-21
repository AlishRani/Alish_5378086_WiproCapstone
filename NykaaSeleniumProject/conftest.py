'''import pytest
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config import BASE_URL

# ADD THIS
from log_utils import logger


# Browser Setup
@pytest.fixture
def setup():

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    logger.info("Launching Browser")

    driver.get(BASE_URL)

    logger.info(f"Opening URL: {BASE_URL}")

    yield driver

    logger.info("Closing Browser")

    driver.quit()


# Screenshot Capture for Pass and Fail
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):

    outcome = yield
    rep = outcome.get_result()

    # Capture screenshot after test execution
    if rep.when == "call":

        driver = item.funcargs["setup"]

        # Create screenshots folder
        os.makedirs("screenshots", exist_ok=True)

        # Time stamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Test Status
        status = "PASSED" if rep.passed else "FAILED"

        # Screenshot Name
        screenshot_name = (
            f"screenshots/{item.name}_{status}_{timestamp}.png"
        )

        # Save Screenshot
        driver.save_screenshot(screenshot_name)

        logger.info(f"Screenshot saved: {screenshot_name}")

        print(f"\nScreenshot saved: {screenshot_name}")'''


import pytest
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config import BASE_URL

# LOGGER IMPORT
from utilities.log_utils import logger


# ======================================================
# Browser Setup
# ======================================================

@pytest.fixture
def setup():

    logger.info("Launching Chrome Browser")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    logger.info("Chrome Browser Launched Successfully")

    driver.get(BASE_URL)

    logger.info(f"Opened URL: {BASE_URL}")

    yield driver

    logger.info("Closing Browser")

    driver.quit()

    logger.info("Browser Closed Successfully")


# ======================================================
# Screenshot Capture for Pass and Fail
# ======================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):

    outcome = yield
    rep = outcome.get_result()

    # Capture Screenshot After Test Execution
    if rep.when == "call":

        driver = item.funcargs["setup"]

        # Create Screenshot Folder
        os.makedirs("screenshots", exist_ok=True)

        # Timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Test Status
        status = "PASSED" if rep.passed else "FAILED"

        # Screenshot Name
        screenshot_name = (
            f"screenshots/{item.name}_{status}_{timestamp}.png"
        )

        # Save Screenshot
        driver.save_screenshot(screenshot_name)

        print(f"\nScreenshot saved: {screenshot_name}")

        logger.info(f"Screenshot saved: {screenshot_name}")

        # Logging Test Result
        if rep.passed:

            logger.info(f"{item.name} PASSED")

        elif rep.failed:

            logger.error(f"{item.name} FAILED")

        elif rep.skipped:

            logger.warning(f"{item.name} SKIPPED")