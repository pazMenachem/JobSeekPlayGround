#!/bin/bash
echo "Activating Job Scraper Virtual Environment..."

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo ""
    echo "❌ ERROR: This script must be SOURCED, not executed!"
    echo ""
    echo "Use this command instead:"
    echo "  source ./activate.sh"
    echo ""
    echo "The 'source' command runs the script in the current shell,"
    echo "allowing environment changes to persist."
    echo ""
    exit 1
fi

# Check if already in virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Virtual environment is already active: $VIRTUAL_ENV"
    echo "You can now run: python main.py"
    echo ""
    echo "To deactivate later, run: deactivate"
    echo ""
    return 0
fi

# Check for virtual environment directory
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: python install.py"
    return 1
fi

# Try to activate virtual environment
if [ -f "venv/Scripts/activate" ]; then
    # Windows Git Bash
    echo "Using Windows Git Bash activation..."
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    # Unix-like systems (Linux, Mac, WSL)
    echo "Using Unix-style activation..."
    source venv/bin/activate
else
    echo "Error: Could not find activation script!"
    echo "Virtual environment may be corrupted."
    echo "Please run: python install.py"
    return 1
fi

# Verify activation
if [ -n "$VIRTUAL_ENV" ]; then
    echo ""
    echo "✅ Virtual environment activated successfully!"
    echo "Environment: $VIRTUAL_ENV"
    echo "Python: $(which python)"
    echo ""
    echo "You can now run: python main.py"
    echo ""
    echo "To deactivate later, run: deactivate"
    echo ""
else
    echo ""
    echo "❌ Failed to activate virtual environment!"
    echo "Please check your installation and try again."
    echo ""
    return 1
fi
