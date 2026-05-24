#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
# run_tests.sh – Install dependencies, run Nykaa test suite, generate reports
# Usage:
#   ./run_tests.sh              # run all tests
#   ./run_tests.sh smoke        # run only @smoke tests
#   ./run_tests.sh regression   # run only @regression tests
#   ./run_tests.sh e2e          # run only E2E test file
#   ./run_tests.sh makeup       # run only makeup test file
# ══════════════════════════════════════════════════════════════════════════════
set -e

MARKER="${1:-all}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║        Nykaa Selenium Automation – Test Runner       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── 1. Install dependencies ───────────────────────────────────────────────────
echo "▶ Installing Python dependencies…"
pip install -r requirements.txt -q

# ── 2. Create output directories ─────────────────────────────────────────────
mkdir -p screenshots reports/html reports/allure-results logs

# ── 3. Build pytest command ───────────────────────────────────────────────────
case "$MARKER" in
  smoke)      PYTEST_ARGS="-m smoke tests/" ;;
  regression) PYTEST_ARGS="-m regression tests/" ;;
  e2e)        PYTEST_ARGS="tests/test_e2e_homepage_to_payment.py" ;;
  makeup)     PYTEST_ARGS="tests/test_makeup.py" ;;
  *)          PYTEST_ARGS="tests/" ;;
esac

# ── 4. Run tests ──────────────────────────────────────────────────────────────
echo ""
echo "▶ Running tests: $PYTEST_ARGS"
echo ""
python -m pytest $PYTEST_ARGS || true   # don't fail script on test failure

# ── 5. Generate Allure HTML report ───────────────────────────────────────────
if command -v allure &>/dev/null; then
    echo ""
    echo "▶ Generating Allure HTML report…"
    allure generate reports/allure-results -o reports/allure-html --clean
    echo "   Allure report → reports/allure-html/index.html"
else
    echo ""
    echo "ℹ  allure CLI not found. To install:"
    echo "   npm install -g allure-commandline"
    echo "   (or brew install allure on macOS)"
fi

# ── 6. Summary ────────────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════"
echo "  Reports generated:"
echo "  • HTML     → $(pwd)/reports/html/report.html"
echo "  • Allure   → $(pwd)/reports/allure-results/"
echo "  • Logs     → $(pwd)/logs/"
echo "  • Screenshots → $(pwd)/screenshots/"
echo "══════════════════════════════════════════════════"
