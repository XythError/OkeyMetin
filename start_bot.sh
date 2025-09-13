#!/bin/bash
echo "Starting Metin2 Okey Bot..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Launch the bot
python3 main.py
