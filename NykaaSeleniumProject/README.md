# Nykaa Selenium Test Suite

Automated test suite for [nykaa.com](https://www.nykaa.com) using Selenium WebDriver + pytest + Allure Report.

## Tech Stack

| Tool | Version |
|---|---|
| Python | 3.11 |
| Selenium | 4.28 |
| pytest | 8.3 |
| Allure | 2.16 / 2.37 |
| WebDriver Manager | 4.0 |

## Project Structure

```
nykaa-tests/
├── conftest.py                  # Fixtures: driver init (5s timeout), logo click, failure screenshot
├── pytest.ini                   # pytest + Allure config
├── requirements.txt             # Python dependencies
├── utils.py                     # Screenshot helper for Allure
├── pages/
│   ├── home_page.py             # POM: homepage nav (Makeup hover → Lipstick click), search
│   └── lipstick_page.py         # POM: listing, filters, sort, product detail, add to bag
├── tests/
│   ├── test_nav_lipstick.py     # ✅ Positive: hover Makeup → click Lipstick → verify heading
│   ├── test_filter_brand.py     # ✅ Positive: filter by Lakme brand → URL has brand param
│   ├── test_sort_price.py       # ✅ Positive: sort Low to High → verify sort applied
│   ├── test_product_detail.py   # ✅ Positive: click product → PDP shows name + price
│   ├── test_search_invalid.py   # ❌ Negative: search "!@#$%" → results page loads without error
│   └── test_e2e_add_to_bag.py   # 🔁 E2E: nav → PDP → verify details → click Add to Bag
└── allure-report/               # Generated Allure HTML report
```

## Test Cases

| # | Type | Test Name | What It Validates |
|---|---|---|---|
| 1 | ✅ Positive | `test_nav_lipstick` | Hover "Makeup" → click "Lipstick" → heading contains "Lipstick" |
| 2 | ✅ Positive | `test_filter_brand` | Filter by brand "Lakme" → URL contains brand parameter |
| 3 | ✅ Positive | `test_sort_price` | Sort by Price Low to High → heading still shows lipstick page |
| 4 | ✅ Positive | `test_product_detail` | Click first product → PDP shows product name (`<h1>`) + price (`₹`) |
| 5 | ❌ Negative | `test_search_invalid` | Search special chars `!@#$%` → search results page loads without error |
| 6 | 🔁 E2E | `test_e2e_add_to_bag` | Nav → listing → PDP → verify name & price → click Add to Bag |

## Quick Start

```bash
# 1. Install dependencies
cd nykaa-tests
pip install -r requirements.txt

# 2. Run all tests
pytest

# 3. Run with Allure
pytest --alluredir=allure-results

# 4. View Allure report
allure serve allure-results

# Or open static report
open allure-report/index.html
```

## Key Implementation Details

### Page Load Strategy
- `set_page_load_timeout(5)` — driver fails fast if page doesn't load in 5s
- Catches timeout → calls `window.stop()` to proceed with partial DOM
- Clicks the Nykaa logo after load to dismiss any transient overlays

### Navigation Flow
- Makeup link located by href (`/sp/makeup-clp-desktop/makeup`) — avoids matching brand links like "Makeup Revolution"
- Lipstick link has `target="_blank"` → switches to new tab after click
- 1s sleep after hover for mega-menu animation

### Locator Strategy
| Element | Locator |
|---|---|
| Makeup nav link | `//a[contains(@href,'/sp/makeup-clp-desktop/makeup')]` |
| Lipstick link | `//a[@href='/makeup/lips/lipstick/c/249']` |
| Product links | `//a[contains(@href,'/p/')]` |
| Product name | `<h1>` tag (PDP) |
| Product price | `//span[contains(text(),'₹')]` |
| Add to Bag | `//button[contains(text(),'Add to Bag')]` |
| Search box | `input[name='search-suggestions-nykaa']` |

### Screenshots
Every test captures step screenshots attached to Allure:
- Listing page, before/after filter, before/after sort, PDP, search result, Add to Bag
- On test failure, auto-captures screenshot via `pytest_runtest_makereport` hook

## Allure Report Features

- **Behaviors** — grouped by Story (Navigation, Filtering, Sorting, etc.)
- **Categories** — product defects vs test defects
- **Environment** — Browser, OS, Python, Selenium versions
- **Timeline** — test execution duration
- **Graphs** — pass/fail statistics
