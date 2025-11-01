#!/bin/bash

# PitchDeck Autopilot - Test Runner Script
# Runs complete test suite with coverage and audit

set -e  # Exit on error

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PitchDeck Autopilot - Comprehensive Test Suite"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if in correct directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing dependencies..."
    pip install -r requirements-dev.txt
fi

echo "📊 Step 1: Running Unit Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/test_text_cleaner.py tests/test_markdown_builder.py -v --tb=short
echo ""

echo "🔌 Step 2: Running API Contract Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/test_ai_analyzer.py -v -m api --tb=short
echo ""

echo "🔗 Step 3: Running Integration Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/test_integration.py tests/test_deck_parser.py -v --tb=short
echo ""

echo "🛡️  Step 4: Running Validation Guards"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/test_validation.py -v --tb=short
echo ""

echo "📈 Step 5: Running Full Suite with Coverage"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/ -v --cov=deckbrief --cov-report=html --cov-report=term-missing --tb=short
echo ""

echo "📊 Coverage report generated: htmlcov/index.html"
echo ""

echo "🔍 Step 6: Running Test Quality Audit"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python audit.py
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Test Suite Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 Artifacts:"
echo "  - Coverage HTML: htmlcov/index.html"
echo "  - Coverage data: .coverage"
echo ""
echo "💡 Next steps:"
echo "  - Review coverage report: open htmlcov/index.html"
echo "  - Run mutation tests: mutmut run"
echo "  - Check specific tests: pytest tests/test_<module>.py -v"
echo ""


