#!/usr/bin/env bash
# Comprehensive quality check script for calculatorCICD
# This script runs all quality checks: tests, linting, type checking, formatting

set -e  # Exit immediately if any command fails

echo "🚀 Starting calculatorCICD Quality Checks..."
echo "============================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Make sure we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    print_warning "Virtual environment not detected. Activating..."
    if [ -f "venv/Scripts/activate" ]; then
        # Windows
        source venv/Scripts/activate
    elif [ -f "venv/bin/activate" ]; then
        # Linux/Mac
        source venv/bin/activate
    else
        print_error "Virtual environment not found. Please create one first."
        exit 1
    fi
fi

# 1. Run the main application
print_status "Running main application..."
python src/__main__.py
print_success "Main application completed"
echo ""

# 2. Run tests with coverage
print_status "Running tests with coverage..."
pytest -v
print_success "All tests passed"
echo ""

# 3. Check code formatting with Black
print_status "Checking code formatting with Black..."
if black --check src tests; then
    print_success "Code formatting is correct"
else
    print_warning "Code formatting issues found. Run 'black src tests' to fix."
fi
echo ""

# 4. Run linting with flake8
print_status "Running linting with flake8..."
if flake8 src tests; then
    print_success "No linting issues found"
else
    print_error "Linting issues found. Please fix them."
fi
echo ""

# 5. Run type checking with mypy
print_status "Running type checking with mypy..."
if mypy src --ignore-missing-imports; then
    print_success "No type checking issues found"
else
    print_error "Type checking issues found. Please fix them."
fi
echo ""

# Summary
echo "============================================="
print_success "🎉 All quality checks completed!"
echo -e "${BLUE}📊 Summary:${NC}"
echo "   ✓ Application runs successfully"
echo "   ✓ All tests pass"
echo "   ✓ Code formatting checked"
echo "   ✓ Linting completed"
echo "   ✓ Type checking completed"
echo ""
echo -e "${YELLOW}💡 Tip: Run this script before committing code!${NC}"