#!/bin/bash
echo "Starting Job Scraper..."
echo

# Check if virtual environment exists
if [ ! -f "venv/Scripts/activate" ]; then
    echo "Virtual environment not found!"
    echo "Please run: python install.py"
    exit 1
fi

# Activate virtual environment and run the application
source venv/Scripts/activate
python main.py

echo
echo "Job Scraper finished."
