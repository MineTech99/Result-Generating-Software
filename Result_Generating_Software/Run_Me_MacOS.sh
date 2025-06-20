#!/bin/bash

# This script runs your main.py and keeps the terminal window open on macOS.

echo ""
echo "==========================================="
echo " Starting Image Generation Script (main.py)"
echo "==========================================="
echo ""

# Change directory to where this script is located
# This ensures main.py can be found, regardless of where you run the .sh file from.
cd "$(dirname "$0")"

# Run the Python script using python3 (recommended for modern Python on macOS)
python3 main.py

# Keep the terminal window open after the script finishes or encounters an error
echo ""
echo "Script finished. Press any key to close this window."
read -n 1 -s # Reads a single character silently, then exits.
echo "" # Adds a newline for cleaner output after the key press