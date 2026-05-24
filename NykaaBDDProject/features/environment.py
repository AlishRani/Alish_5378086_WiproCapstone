"""
environment.py — Behave ka conftest.
Before/After hooks: driver setup, screenshot on fail, logging, allure attach.
"""
import os
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
SS_DIR      = os.path.join(BASE_DIR, "screenshots")
LOG_DIR     = os.path.join(BASE_DIR, "logs")
ALLURE_DIR  = os.path.join(BASE_DIR, "reports", "allure-results")

for d in [SS_DIR, LOG_DIR, ALLURE_DIR]:
    os.makedirs(d, exist_ok=True)


# ─── Logger ───────────────────────────────────────────────────────────────────
def setup_logger():
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    logfile = os.path.join(LOG_DIR, f"test_run_{ts}.log")
    logger  = logging.getLogger("nykaa")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        fh = logging.FileHandler(logfile, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(fmt)

        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger


# ─── Behave Hooks ─────────────────────────────────────────────────────────────
def before_all(context):
    context.logger = setup_logger()
    context.logger.info("=" * 60)
    context.logger.info("   Nykaa BDD Test Suite Started")
    context.logger.info("=" * 60)


def before_scenario(context, scenario):
    context.logger.info(f"\n[SCENARIO START] {scenario.name}")

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
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.implicitly_wait(10)
    context.driver.set_page_load_timeout(30)

    # Scenario mein current screenshot path store karne ke liye
    context.last_screenshot = None


def after_step(context, step):
    """Har failed step pe screenshot lo."""
    if step.status == "failed":
        _take_screenshot(context, f"FAILED_{step.name[:50]}")
        context.logger.error(f"[STEP FAILED] {step.name}")


def after_scenario(context, scenario):
    """Scenario ke baad driver close karo."""
    status = "PASSED" if scenario.status == "passed" else "FAILED"
    context.logger.info(f"[SCENARIO {status}] {scenario.name}")
    try:
        context.driver.quit()
    except Exception:
        pass


def after_all(context):
    context.logger.info("=" * 60)
    context.logger.info("   Nykaa BDD Test Suite Completed")
    context.logger.info("=" * 60)


# ─── Helper ───────────────────────────────────────────────────────────────────
def _take_screenshot(context, label):
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in label)
    path = os.path.join(SS_DIR, f"{safe}_{ts}.png")
    try:
        context.driver.save_screenshot(path)
        context.last_screenshot = path
        context.logger.info(f"[SCREENSHOT] {path}")
    except Exception as e:
        context.logger.warning(f"[SCREENSHOT FAILED] {e}")
    return path
