# ============================================================================
# Feature  : Nykaa Makeup Module – Lipstick Sub-Module
# Module   : Makeup
# SubModule: Lipstick
# ============================================================================

Feature: Nykaa Makeup Module - Lipstick Tests
  Makeup module ke lipstick sub-module ke liye positive aur negative test cases.

  Background:
    Given Chrome browser open hai

  # ══════════════════════════════════════════════════════════════════════════
  # POSITIVE TEST CASES (4)
  # ══════════════════════════════════════════════════════════════════════════

  @positive @smoke
  Scenario: TC-MK-01 Lipstick category page successfully load hoti hai
    When user Lipstick sub-category page kholta hai
    Then page successfully load honi chahiye
    And page mein lipstick content hona chahiye
    And screenshot liya jaye "TC_MK_01_lipstick_page_loaded"

  @positive @smoke
  Scenario: TC-MK-02 Lipstick products naam aur price ke saath display hote hain
    When user Lipstick sub-category page kholta hai
    And user page scroll karta hai
    Then products page par display hone chahiye
    And screenshot liya jaye "TC_MK_02_products_displayed"

  @positive
  Scenario: TC-MK-03 Filter aur Sort options lipstick page par visible hain
    When user Lipstick sub-category page kholta hai
    Then filter ya sort options page par hone chahiye
    And screenshot liya jaye "TC_MK_03_filter_sort_visible"

  @positive @smoke
  Scenario: TC-MK-04 Lipstick search karne par relevant results aate hain
    Given user Nykaa homepage par hai
    When user "lipstick" search karta hai
    Then search results page load honi chahiye
    And results mein lipstick products hone chahiye
    And screenshot liya jaye "TC_MK_04_search_results"

  # ══════════════════════════════════════════════════════════════════════════
  # NEGATIVE TEST CASES (2)
  # ══════════════════════════════════════════════════════════════════════════

  @negative
  Scenario: TC-MK-05 Galat keyword search karne par no results aata hai
    Given user Nykaa homepage par hai
    When user "xyzabcqwerty12345" search karta hai
    Then koi relevant product nahi dikhna chahiye ya no results message aana chahiye
    And screenshot liya jaye "TC_MK_05_no_results"

  @negative
  Scenario: TC-MK-06 Invalid product URL se error ya redirect hota hai
    When user "https://www.nykaa.com/p/999999999-fake-product-xyz" par navigate karta hai
    Then page ek valid product nahi dikhana chahiye
    And page 404 ya redirect honi chahiye
    And screenshot liya jaye "TC_MK_06_invalid_url"
