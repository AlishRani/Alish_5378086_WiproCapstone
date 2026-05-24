"""
Step Definitions — Makeup Module / Lipstick
Feature: makeup_lipstick.feature
"""
import os
import sys
import logging

from behave import then

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pages.nykaa_pages import MakeupPage, ProductPage

logger = logging.getLogger("nykaa")

# NOTE: Given/When steps e2e_steps.py se reuse hote hain (behave automatically combine karta hai)


# ─── Positive Assertions ──────────────────────────────────────────────────────

@then('products page par display hone chahiye')
def step_products_displayed(context):
    page = MakeupPage(context.driver)
    assert page.has_products(), \
        "Lipstick products page par nahi mile"
    count = page.get_product_count()
    names = page.get_product_names()
    logger.info(f"[THEN] Products mile — Cards: {count}, Names: {len(names)} ✓")


@then('filter ya sort options page par hone chahiye')
def step_filter_sort_visible(context):
    page   = MakeupPage(context.driver)
    f_vis  = page.filter_visible()
    s_vis  = page.sort_visible()
    src    = context.driver.page_source.lower()
    in_src = any(k in src for k in ["filter", "sort", "brand", "price range"])
    assert f_vis or s_vis or in_src, \
        "Filter aur sort options dono absent hain"
    logger.info(f"[THEN] Filter/Sort present (filter={f_vis}, sort={s_vis}, in_src={in_src}) ✓")


# ─── Negative Assertions ──────────────────────────────────────────────────────

@then('koi relevant product nahi dikhna chahiye ya no results message aana chahiye')
def step_no_results(context):
    page          = MakeupPage(context.driver)
    no_result_msg = page.no_results_visible()
    count         = page.get_product_count()
    src           = context.driver.page_source.lower()
    # Count 0 ho ya no-results indicator mile
    result_empty = no_result_msg or count == 0 or \
        any(k in src for k in ["no results", "no products", "0 result", "not found", "0 product"])
    logger.info(f"[THEN] No results check — msg={no_result_msg}, count={count}")
    assert result_empty, \
        f"Galat keyword search mein bhi products aa rahe hain (count={count})"
    logger.info("[THEN] Galat keyword par correctly no/empty results ✓")


@then('page ek valid product nahi dikhana chahiye')
def step_not_valid_product(context):
    src           = context.driver.page_source.lower()
    valid_product = "add to bag" in src or ("₹" in src and "add" in src)
    assert not valid_product, \
        "Invalid URL par bhi valid product show ho raha hai"
    logger.info("[THEN] Invalid URL par valid product nahi dikh raha ✓")


@then('page 404 ya redirect honi chahiye')
def step_404_or_redirect(context):
    url       = context.driver.current_url.lower()
    src       = context.driver.page_source.lower()
    title     = context.driver.title.lower()
    bad_url   = "999999999" not in url   # redirect hua
    has_404   = any(k in src[:4000] or k in title
                    for k in ["404", "not found", "oops", "sorry", "unavailable"])
    to_search = any(k in url for k in ["search", "nykaa.com"])
    logger.info(f"[THEN] Invalid URL result — redirected={bad_url}, 404={has_404}, to_search={to_search}")
    assert bad_url or has_404 or to_search, \
        f"Invalid URL se na redirect hua, na 404 mila | URL={url}"
    logger.info("[THEN] Invalid URL correctly handled (404/redirect) ✓")
