# Nykaa Selenium + Pytest Automation Framework

**Module:** Makeup | **Sub-Module:** Lipstick

---

## Project Structure

```
nykaa_automation/
│
├── conftest.py                          ← Fixtures, screenshot hook, logger setup
├── pytest.ini                           ← Pytest config (HTML + Allure + log settings)
├── requirements.txt                     ← Python dependencies
├── run_tests.sh                         ← One-shot run script
│
├── pages/                               ← Page Object Model (POM)
│   ├── base_page.py                     ← Shared helpers (wait, click, screenshot…)
│   ├── home_page.py                     ← Nykaa homepage
│   ├── makeup_page.py                   ← Makeup / Lipstick category page
│   ├── product_page.py                  ← Product detail page
│   ├── cart_page.py                     ← Shopping cart / bag
│   └── checkout_page.py                 ← Login & Checkout / Payment pages
│
├── tests/
│   ├── test_e2e_homepage_to_payment.py  ← End-to-End: Homepage → Payment (1 test)
│   └── test_makeup.py                   ← Makeup module: 4 positive + 2 negative
│
├── screenshots/                         ← Auto-saved PNG screenshots
├── logs/                                ← Auto-generated log files
└── reports/
    ├── html/report.html                 ← pytest-html report
    └── allure-results/                  ← Allure raw results (JSON + screenshots)
```

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.9+ |
| Google Chrome | latest |
| pip | latest |
| allure CLI (optional) | 2.x |

---

## Setup & Run

### 1 – Install dependencies
```bash
cd nykaa_automation
pip install -r requirements.txt
```

### 2 – Run ALL tests
```bash
pytest tests/
```

### 3 – Run only E2E test
```bash
pytest tests/test_e2e_homepage_to_payment.py -v
```

### 4 – Run only Makeup module tests
```bash
pytest tests/test_makeup.py -v
```

### 5 – Run by marker
```bash
pytest -m smoke        # quick sanity (TC-01, TC-04, E2E)
pytest -m regression   # full regression suite
```

### 6 – Using the shell script (Linux/macOS)
```bash
chmod +x run_tests.sh
./run_tests.sh           # all tests
./run_tests.sh makeup    # makeup only
./run_tests.sh e2e       # e2e only
./run_tests.sh smoke     # smoke only
```

---

## Reports

### HTML Report
Auto-generated at `reports/html/report.html`.  
Open in any browser after test run.

### Allure Report
1. Raw results land in `reports/allure-results/`.
2. Install allure CLI once:
   ```bash
   npm install -g allure-commandline
   # or: brew install allure
   ```
3. Generate & open:
   ```bash
   allure generate reports/allure-results -o reports/allure-html --clean
   allure open reports/allure-html
   ```

### Logs
Timestamped log file written to `logs/test_run_YYYYMMDD_HHMMSS.log` each run.  
Also streamed to console at INFO level.

### Screenshots
Every test saves a screenshot automatically.  
Failed tests get an extra `_FAILED_` screenshot.  
All screenshots are embedded in the Allure report.  
Location: `screenshots/<test_name>_<PASSED|FAILED>_<timestamp>.png`

---

## Test Cases

### test_e2e_homepage_to_payment.py

| # | Test | Severity |
|---|------|----------|
| E2E | Homepage → Makeup → Lipstick → Product → Cart → Payment/Login | BLOCKER |

### test_makeup.py – Positive (4)

| # | Test | Severity |
|---|------|----------|
| TC-01 | Lipstick category page loads | CRITICAL |
| TC-02 | Products displayed with names/prices | CRITICAL |
| TC-03 | Filter/Sort options visible | NORMAL |
| TC-04 | Search 'lipstick' returns results | CRITICAL |

### test_makeup.py – Negative (2)

| # | Test | Severity |
|---|------|----------|
| TC-05 | Gibberish search returns no results | NORMAL |
| TC-06 | Invalid product URL shows error/redirect | NORMAL |
