# Nykaa BDD Automation — Behave + Selenium

**Module:** Makeup | **Sub-Module:** Lipstick | **Framework:** BDD (Behave)

---

## Project Structure

```
nykaa_bdd/
│
├── features/                                    ← Gherkin Feature Files
│   ├── e2e_homepage_to_payment.feature          ← E2E: 9 Scenarios (1 per page)
│   ├── makeup_lipstick.feature                  ← Makeup: 4 positive + 2 negative
│   ├── environment.py                           ← Before/After hooks (driver, logs, screenshot)
│   └── steps/
│       ├── e2e_steps.py                         ← Given/When/Then for E2E
│       └── makeup_steps.py                      ← Then steps for Makeup assertions
│
├── pages/                                       ← Page Object Model
│   ├── base_page.py                             ← Common helpers
│   └── nykaa_pages.py                           ← HomePage, MakeupPage, ProductPage, CartPage, LoginPage
│
├── screenshots/                                 ← Auto-saved PNGs
├── logs/                                        ← Auto-generated log files
├── reports/
│   ├── allure-results/                          ← Allure raw JSON
│   └── allure-html/                             ← Allure HTML report
│
├── requirements.txt
├── behave.ini
└── run_tests.sh
```

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Run Commands

| Command | Kya run hoga |
|---|---|
| `behave` | Sab features |
| `behave features/e2e_homepage_to_payment.feature` | Sirf E2E (9 scenarios) |
| `behave features/makeup_lipstick.feature` | Sirf Makeup (6 scenarios) |
| `behave --tags=@smoke` | Smoke tagged scenarios |
| `behave --tags=@positive` | Sirf positive tests |
| `behave --tags=@negative` | Sirf negative tests |
| `./run_tests.sh` | Sab + Allure report generate |
| `./run_tests.sh e2e` | E2E + Allure |
| `./run_tests.sh makeup` | Makeup + Allure |

---

## Allure Report

```bash
# Generate
allure generate reports/allure-results -o reports/allure-html --clean

# Open
allure open reports/allure-html
```

---

## Test Scenarios

### E2E — e2e_homepage_to_payment.feature (9 Scenarios)

| # | Scenario | URL |
|---|---|---|
| 01 | Homepage load | `nykaa.com/` |
| 02 | Lip Makeup Category | `/makeup/lips/c/15` |
| 03 | Lipstick Sub-Category | `/makeup/lips/lipstick/c/249` |
| 04 | Search Results | `/search/result/?q=lipstick` |
| 05 | Product Detail | `/lakme-forever-matte-liquid-lip-colour/p/623306` |
| 06 | Add to Bag | Same product page |
| 07 | Shopping Cart | `/v2/payment/` |
| 08 | Proceed to Checkout | Cart → redirect |
| 09 | Login / Payment Gate | `/auth` |

### Makeup — makeup_lipstick.feature (6 Scenarios)

| # | Type | Scenario |
|---|---|---|
| TC-MK-01 | ✅ Positive | Lipstick page load |
| TC-MK-02 | ✅ Positive | Products naam + price ke saath |
| TC-MK-03 | ✅ Positive | Filter/Sort visible |
| TC-MK-04 | ✅ Positive | Search results |
| TC-MK-05 | ❌ Negative | Galat keyword — no results |
| TC-MK-06 | ❌ Negative | Invalid URL — 404/redirect |

---

## BDD Layers

```
Feature File (.feature)   →  Plain English Gherkin (business readable)
        ↓
Step Definitions (.py)    →  Python code jo Gherkin steps execute karta hai
        ↓
Page Objects (.py)        →  Selenium actions (browser se interact karta hai)
        ↓
environment.py            →  Before/After hooks (driver, logs, screenshots)
```
