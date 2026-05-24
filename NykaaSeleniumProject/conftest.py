import pytest
import allure
import os
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
LOG_DIR        = os.path.join(BASE_DIR, "logs")
HTML_REPORT    = os.path.join(BASE_DIR, "reports", "html", "report.html")
ALLURE_DIR     = os.path.join(BASE_DIR, "reports", "allure-results")

for d in [SCREENSHOT_DIR, LOG_DIR, os.path.dirname(HTML_REPORT), ALLURE_DIR]:
    os.makedirs(d, exist_ok=True)


# ─── Root Logger ──────────────────────────────────────────────────────────────
def setup_logger(name: str = "nykaa") -> logging.Logger:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file  = os.path.join(LOG_DIR, f"test_run_{timestamp}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(fmt)

        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger


logger = setup_logger()


# ─── Chrome Driver Fixture ─────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver(request):
    logger.info(f"[SETUP] Launching Chrome for: {request.node.name}")

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(10)
    drv.set_page_load_timeout(30)

    yield drv

    # ── Teardown: screenshot on failure ───────────────────────────────────────
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        _save_screenshot(drv, request.node.name, "FAILED")

    logger.info(f"[TEARDOWN] Closing Chrome for: {request.node.name}")
    drv.quit()


# ─── Hook: capture result & screenshot ────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep     = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call":
        driver = item.funcargs.get("driver")
        if driver:
            status = "PASSED" if rep.passed else "FAILED"
            path   = _save_screenshot(driver, item.name, status)
            if path:
                allure.attach.file(
                    path,
                    name=f"screenshot_{status}",
                    attachment_type=allure.attachment_type.PNG,
                )


# ─── Helper ───────────────────────────────────────────────────────────────────
def _save_screenshot(driver, test_name: str, status: str) -> str:
    ts        = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in test_name)
    filename  = f"{safe_name}_{status}_{ts}.png"
    path      = os.path.join(SCREENSHOT_DIR, filename)
    try:
        driver.save_screenshot(path)
        logger.info(f"[SCREENSHOT] Saved → {path}")
    except Exception as e:
        logger.warning(f"[SCREENSHOT] Could not save: {e}")
        return ""
    return path


# ─── Pytest-html extras ───────────────────────────────────────────────────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    yield


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "smoke: quick sanity tests",
    )
    config.addinivalue_line(
        "markers",
        "regression: full regression suite",
    )
