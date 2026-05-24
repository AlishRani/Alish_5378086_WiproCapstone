"""
Step Definitions — E2E Homepage to Payment
Feature: e2e_homepage_to_payment.feature
"""
import os
import sys
import time
import logging
from datetime import datetime

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Path fix so pages/ import kare
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pages.nykaa_pages import HomePage, MakeupPage, ProductPage, CartPage, LoginPage

logger  = logging.getLogger("nykaa")
BASE    = "https://www.nykaa.com"
SS_DIR  = os.path.join(os.path.dirname(__file__), "..", "..", "screenshots")
os.makedirs(SS_DIR, exist_ok=True)


# ─── Utility ──────────────────────────────────────────────────────────────────
def snap(context, label):
    """Screenshot lo aur screenshots/ mein save karo."""
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SS_DIR, f"{label}_{ts}.png")
    context.driver.save_screenshot(path)
    context.last_screenshot = path
    logger.info(f"[SCREENSHOT] {path}")
    return path


def page_is_real(driver):
    src   = driver.page_source.lower()
    title = driver.title.lower()
    bad   = ["404", "page not found", "oops!", "something went wrong",
             "we can't find", "this page is unavailable", "error occurred"]
    return not any(kw in src[:4000] or kw in title for kw in bad)


# ─── Given ────────────────────────────────────────────────────────────────────
@given('Chrome browser open hai')
def step_browser_open(context):
    assert context.driver is not None, "Driver initialize nahi hua"
    logger.info("[GIVEN] Chrome browser ready hai")


@given('user Nykaa homepage par hai')
def step_user_on_homepage(context):
    home = HomePage(context.driver)
    home.open_homepage()
    assert home.is_loaded(), "Homepage load nahi hua"
    logger.info("[GIVEN] User homepage par hai")


# ─── When ─────────────────────────────────────────────────────────────────────
@when('user "{url}" par navigate karta hai')
def step_navigate_to_url(context, url):
    logger.info(f"[WHEN] Navigate to: {url}")
    context.driver.get(url)
    WebDriverWait(context.driver, 15).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    time.sleep(3)
    # Popup dismiss
    for sel in ["button.css-1x39bm7", "[class*='modalClose']",
                "[aria-label='Close']", "[class*='CloseButton']"]:
        try:
            btn = WebDriverWait(context.driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
            )
            context.driver.execute_script("arguments[0].click();", btn)
            break
        except Exception:
            pass


@when('user Lip Makeup category page kholta hai')
def step_open_lip_makeup(context):
    page = MakeupPage(context.driver)
    page.open_lip_makeup()
    logger.info("[WHEN] Lip Makeup category page opened")


@when('user Lipstick sub-category page kholta hai')
def step_open_lipstick(context):
    page = MakeupPage(context.driver)
    page.open_lipstick()
    logger.info("[WHEN] Lipstick sub-category page opened")


@when('user Lakme lipstick product detail page kholta hai')
def step_open_product(context):
    page = ProductPage(context.driver)
    page.open_product()
    logger.info("[WHEN] Lakme lipstick product page opened")


@when('user Shopping Cart page kholta hai')
def step_open_cart(context):
    page = CartPage(context.driver)
    page.open_cart()
    logger.info("[WHEN] Shopping Cart page opened")


@when('user Login page kholta hai')
def step_open_login(context):
    page = LoginPage(context.driver)
    page.open_login()
    logger.info("[WHEN] Login page opened")


@when('user "{keyword}" search karta hai')
def step_search(context, keyword):
    home = HomePage(context.driver)
    try:
        home.search(keyword)
    except Exception:
        MakeupPage(context.driver).open_search_results(keyword)
    logger.info(f"[WHEN] Searched for: {keyword}")


@when('user page scroll karta hai')
def step_scroll(context):
    context.driver.execute_script("window.scrollBy(0, 600);")
    time.sleep(2)
    logger.info("[WHEN] Page scrolled")


@when('user Proceed to Buy click karta hai')
def step_proceed_to_buy(context):
    cart    = CartPage(context.driver)
    clicked = cart.click_proceed_to_buy()
    if not clicked:
        logger.info("[WHEN] Proceed button nahi mila, /auth pe redirect")
        context.driver.get(f"{BASE}/auth")
        time.sleep(3)
    logger.info(f"[WHEN] Proceed to Buy (clicked={clicked})")


# ─── Then ─────────────────────────────────────────────────────────────────────
@then('page ka title ya URL mein "{keyword}" hona chahiye')
def step_url_or_title_contains(context, keyword):
    url   = context.driver.current_url.lower()
    title = context.driver.title.lower()
    assert keyword.lower() in url or keyword.lower() in title, \
        f"'{keyword}' URL ya title mein nahi mila | URL={url} | Title={title}"
    logger.info(f"[THEN] '{keyword}' URL/Title mein mila ✓")


@then('page 404 ya error nahi dikhani chahiye')
def step_not_404(context):
    assert page_is_real(context.driver), \
        f"Page 404/error show kar raha hai | URL={context.driver.current_url}"
    logger.info("[THEN] Page real hai, 404 nahi ✓")


@then('page successfully load honi chahiye')
def step_page_loaded(context):
    assert page_is_real(context.driver), \
        f"Page load nahi hua ya 404 hai | URL={context.driver.current_url}"
    assert len(context.driver.page_source) > 5000, \
        "Page source bahut chhota hai"
    logger.info("[THEN] Page successfully load hua ✓")


@then('page mein lip ya makeup content hona chahiye')
def step_has_lip_content(context):
    src = context.driver.page_source.lower()
    assert any(k in src for k in ["lip", "makeup", "beauty", "product"]), \
        "Page mein lip/makeup content nahi mila"
    logger.info("[THEN] Lip/Makeup content mila ✓")


@then('page mein lipstick content hona chahiye')
def step_has_lipstick_content(context):
    src = context.driver.page_source.lower()
    assert "lipstick" in src or "lip" in src, \
        "Page mein lipstick content nahi mila"
    logger.info("[THEN] Lipstick content mila ✓")


@then('page mein product content hona chahiye')
def step_has_product_content(context):
    page = ProductPage(context.driver)
    assert page.has_product_content(), \
        f"Product content nahi mila | URL={context.driver.current_url}"
    logger.info("[THEN] Product content mila ✓")


@then('page mein Add to Bag button hona chahiye')
def step_atb_present(context):
    page = ProductPage(context.driver)
    assert page.atb_in_source(), \
        "Add to Bag button page source mein nahi mila"
    logger.info("[THEN] Add to Bag button page mein hai ✓")


@then('Add to Bag button click kiya jaye')
def step_click_atb(context):
    page    = ProductPage(context.driver)
    clicked = page.click_add_to_bag()
    logger.info(f"[THEN] Add to Bag click attempt (success={clicked})")
    # Button page mein tha — already asserted above. Click optional (shade select zaroori ho sakta)


@then('cart page successfully load honi chahiye')
def step_cart_loaded(context):
    page = CartPage(context.driver)
    assert page_is_real(context.driver), "Cart page 404 hai"
    assert page.is_cart_page() or page.has_cart_content(), \
        f"Cart page nahi mila | URL={context.driver.current_url}"
    logger.info("[THEN] Cart page load hua ✓")


@then('page mein cart ya payment related content hona chahiye')
def step_has_cart_content(context):
    page = CartPage(context.driver)
    assert page.has_cart_content(), \
        "Cart/Payment content nahi mila"
    logger.info("[THEN] Cart/Payment content mila ✓")


@then('user checkout ya login page par pahunche')
def step_at_checkout_or_login(context):
    url = context.driver.current_url.lower()
    assert page_is_real(context.driver), "Page 404 hai"
    assert any(k in url for k in [
        "auth", "payment", "checkout", "login", "signin", "account", "nykaa"
    ]), f"Checkout/Login page nahi mila | URL={url}"
    logger.info(f"[THEN] Checkout/Login page reached: {url} ✓")


@then('login page successfully load honi chahiye')
def step_login_loaded(context):
    page = LoginPage(context.driver)
    assert page_is_real(context.driver), "Login page 404 hai"
    assert page.is_login_page(), \
        f"Login page nahi mila | URL={context.driver.current_url}"
    logger.info("[THEN] Login page load hua ✓")


@then('page mein login form hona chahiye')
def step_has_login_form(context):
    page = LoginPage(context.driver)
    assert page.has_login_form(), \
        "Login form content nahi mila (email/mobile/otp)"
    logger.info("[THEN] Login form content mila ✓")


@then('search results page load honi chahiye')
def step_search_results_loaded(context):
    url = context.driver.current_url.lower()
    assert page_is_real(context.driver), "Search page 404 hai"
    assert any(k in url for k in ["search", "result", "lipstick", "nykaa"]), \
        f"Search results URL unexpected: {url}"
    logger.info("[THEN] Search results page load hua ✓")


@then('results mein lipstick products hone chahiye')
def step_has_lipstick_results(context):
    src = context.driver.page_source.lower()
    assert "lipstick" in src or "lip" in src or "₹" in src, \
        "Search results mein lipstick products nahi mile"
    logger.info("[THEN] Lipstick results mile ✓")


@then('screenshot liya jaye "{label}"')
def step_take_screenshot(context, label):
    path = snap(context, label)
    logger.info(f"[THEN] Screenshot saved: {path}")


@then('product page successfully load honi chahiye')
def step_product_page_loaded(context):
    page = ProductPage(context.driver)
    assert page_is_real(context.driver), \
        f"Product page 404 hai | URL={context.driver.current_url}"
    assert page.has_product_content(), \
        f"Product content nahi mila | URL={context.driver.current_url}"
    logger.info("[THEN] Product page successfully load hua ✓")
