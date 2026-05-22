import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utils import take_screenshot


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(5)
    try:
        driver.get("https://www.nykaa.com")
    except Exception:
        driver.execute_script("window.stop();")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.logo"))
    ).click()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        from pathlib import Path
        log_dir = Path(__file__).parent / "logs"
        if log_dir.exists():
            log_files = sorted(log_dir.glob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)
            if log_files:
                latest = log_files[0]
                with open(latest) as f:
                    allure.attach(f.read(), name="test_log", attachment_type=allure.attachment_type.TEXT)
        if report.failed:
            driver = item.funcargs.get("driver")
            if driver:
                take_screenshot(driver, f"{item.name}_failed")
