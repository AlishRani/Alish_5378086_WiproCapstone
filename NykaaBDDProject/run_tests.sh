#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
# run_tests.sh — Nykaa BDD Test Runner
#
# Usage:
#   ./run_tests.sh            # Sab tests run karo (E2E + Makeup)
#   ./run_tests.sh e2e        # Sirf E2E feature
#   ./run_tests.sh makeup     # Sirf Makeup feature
#   ./run_tests.sh smoke      # Sirf @smoke tagged scenarios
#   ./run_tests.sh positive   # Sirf @positive tagged scenarios
#   ./run_tests.sh negative   # Sirf @negative tagged scenarios
# ══════════════════════════════════════════════════════════════════════════════
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     Nykaa BDD (Behave + Selenium) Test Runner       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── 1. Install dependencies ───────────────────────────────────────────────────
echo "▶ Installing dependencies..."
pip install -r requirements.txt -q --break-system-packages 2>/dev/null || \
pip install -r requirements.txt -q

# ── 2. Create output dirs ─────────────────────────────────────────────────────
mkdir -p screenshots logs reports/allure-results reports/html

# ── 3. Build behave command ───────────────────────────────────────────────────
MARKER="${1:-all}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
HTML_REPORT="reports/html/report_${TIMESTAMP}.html"
ALLURE_DIR="reports/allure-results"

case "$MARKER" in
  e2e)      FEATURE="features/e2e_homepage_to_payment.feature" ;;
  makeup)   FEATURE="features/makeup_lipstick.feature" ;;
  smoke)    FEATURE="features/ --tags=@smoke" ;;
  positive) FEATURE="features/ --tags=@positive" ;;
  negative) FEATURE="features/ --tags=@negative" ;;
  *)        FEATURE="features/" ;;
esac

# ── 4. Run with Allure formatter ─────────────────────────────────────────────
echo "▶ Running: behave $FEATURE"
echo ""

behave $FEATURE \
  --format allure_behave.formatter:AllureFormatter \
  --outfile "$ALLURE_DIR" \
  --format pretty \
  || true

# ── 5. Generate HTML report via allure CLI ────────────────────────────────────
if command -v allure &>/dev/null; then
    echo ""
    echo "▶ Generating Allure HTML report..."
    allure generate "$ALLURE_DIR" -o reports/allure-html --clean
    echo "   ✓ Allure report → reports/allure-html/index.html"
else
    echo ""
    echo "ℹ  Allure CLI nahi mili. Install karo:"
    echo "   npm install -g allure-commandline"
fi

# ── 6. Summary ────────────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════════"
echo "  Output:"
echo "  • Allure Results  → $(pwd)/reports/allure-results/"
echo "  • Allure HTML     → $(pwd)/reports/allure-html/index.html"
echo "  • Screenshots     → $(pwd)/screenshots/"
echo "  • Logs            → $(pwd)/logs/"
echo "══════════════════════════════════════════════════════"
