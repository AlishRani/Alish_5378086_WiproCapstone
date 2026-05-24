# ============================================================================
# Feature  : Nykaa Lipstick Purchase – End to End Flow
# Module   : Makeup
# SubModule: Lipstick
# ============================================================================

Feature: Nykaa E2E Purchase Flow - Makeup / Lipstick
  Ek user Nykaa homepage se shuru karke lipstick purchase funnel ke
  har page par successfully pahunche.
  Har page ek alag test case hai aur apna screenshot leta hai.

  Background:
    Given Chrome browser open hai

  # ──────────────────────────────────────────────────────────────────────────
  Scenario: TC-E2E-01 Homepage successfully load hoti hai
    When user "https://www.nykaa.com/" par navigate karta hai
    Then page ka title ya URL mein "nykaa" hona chahiye
    And page 404 ya error nahi dikhani chahiye
    And screenshot liya jaye "TC_E2E_01_homepage"

  # ──────────────────────────────────────────────────────────────────────────
  Scenario: TC-E2E-02 Lip Makeup Category page load hoti hai
    When user Lip Makeup category page kholta hai
    Then page successfully load honi chahiye
    And page mein lip ya makeup content hona chahiye
    And screenshot liya jaye "TC_E2E_02_lip_makeup_category"

  # ──────────────────────────────────────────────────────────────────────────
  Scenario: TC-E2E-03 Lipstick Sub-Category page load hoti hai
    When user Lipstick sub-category page kholta hai
    Then page successfully load honi chahiye
    And page mein lipstick content hona chahiye
    And screenshot liya jaye "TC_E2E_03_lipstick_subcategory"

  # ──────────────────────────────────────────────────────────────────────────
  Scenario: TC-E2E-04 Lipstick Search Results page load hoti hai
    When user "lipstick" search karta hai
    Then search results page load honi chahiye
    And results mein lipstick products hone chahiye
    And screenshot liya jaye "TC_E2E_04_search_results"

  # ──────────────────────────────────────────────────────────────────────────
  Scenario: TC-E2E-05 Lipstick Product Detail page load hoti hai
    When user Lakme lipstick product detail page kholta hai
    Then product page successfully load honi chahiye
    And page mein product content hona chahiye
    And screenshot liya jaye "TC_E2E_05_product_detail"

  # ──────────────────────────────────────────────────────────────────────────
  Scenario: TC-E2E-06 Add to Bag button product page par dikh raha hai
    When user Lakme lipstick product detail page kholta hai
    Then page mein Add to Bag button hona chahiye
    And Add to Bag button click kiya jaye
    And screenshot liya jaye "TC_E2E_06_add_to_bag"

  # ──────────────────────────────────────────────────────────────────────────
  Scenario: TC-E2E-07 Shopping Cart page load hoti hai
    When user Shopping Cart page kholta hai
    Then cart page successfully load honi chahiye
    And page mein cart ya payment related content hona chahiye
    And screenshot liya jaye "TC_E2E_07_cart_page"

  # ──────────────────────────────────────────────────────────────────────────
  Scenario: TC-E2E-08 Proceed to Buy se Checkout ya Login page par pahunche
    When user Shopping Cart page kholta hai
    And user Proceed to Buy click karta hai
    Then user checkout ya login page par pahunche
    And screenshot liya jaye "TC_E2E_08_proceed_to_checkout"

  # ──────────────────────────────────────────────────────────────────────────
  Scenario: TC-E2E-09 Login Page - Payment Gate final step load hoti hai
    When user Login page kholta hai
    Then login page successfully load honi chahiye
    And page mein login form hona chahiye
    And screenshot liya jaye "TC_E2E_09_login_page"
