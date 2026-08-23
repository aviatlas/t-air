#!/usr/bin/env bash
# Full pipeline plus both test suites. Run this before every commit.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== merge data parts"
python3 scripts/merge_parts.py
echo
echo "== build database"
python3 scripts/build_data.py
echo
echo "== database checks"
python3 scripts/test_build.py
echo
echo "== build single-file"
python3 scripts/build_single.py
echo
if [ -d node_modules/playwright ] || node -e "require('playwright')" 2>/dev/null; then
  echo "== interface checks"
  node scripts/test_ui.js
else
  echo "== WARNING: interface checks SKIPPED — playwright is not installed"
  echo "   npm install playwright && npx playwright install chromium"
  SKIPPED=1
fi
echo
if [ "${SKIPPED:-0}" = "1" ]; then
  echo "data is good; the interface was not tested"
else
  echo "all good"
fi
