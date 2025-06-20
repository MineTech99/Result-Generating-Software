#!/bin/bash

# This script automates the installation of required Python packages for macOS.
# It checks for Python 3 and pip, then installs pandas, Pillow, openpyxl, and colorama.

echo ""
echo "========================================================="
echo " Automated Python Package Installer for macOS"
echo "========================================================="
echo ""
echo "This script will install Python packages required for the Image Generator."
echo "It requires an active internet connection."
echo ""

# --- Step 1: Check for Python 3 Installation ---
echo "1. Checking for Python 3 installation..."
# 'command -v' checks if a command exists. '&> /dev/null' suppresses output.
if ! command -v python3 &> /dev/null
then
    echo ""
    echo "---------------------------------------------------------"
    echo "  ERROR: Python 3 was not found."
    echo "---------------------------------------------------------"
    echo "  Please install Python 3. Recommended methods:"
    echo "  1. Using Homebrew (if you have it - open Terminal and paste this line):"
    echo "     /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "     Then run: brew install python"
    echo "  2. Download directly from python.org (simpler for non-tech users):"
    echo "     Visit https://www.python.org/downloads/macos/ and download the latest installer."
    echo ""
    echo "  After installing Python 3, please run this script again."
    echo "  Press any key to exit."
    read -n 1 -s # Read a single character silently
    exit 1 # Exit with an error code
else
    echo "  Python 3 found. Version:"
    python3 --version # Display Python 3 version
    echo ""
fi

# --- Step 2: Check for pip3 (Python 3's package installer) ---
echo "2. Checking for pip3 (Python's package installer)..."
if ! command -v pip3 &> /dev/null
then
    echo ""
    echo "---------------------------------------------------------"
    echo "  WARNING: pip3 was not found."
    echo "---------------------------------------------------------"
    echo "  Attempting to install pip3..."
    # 'python3 -m ensurepip' ensures pip is available. '--default-pip' installs if missing.
    python3 -m ensurepip --default-pip
    if [ $? -ne 0 ]; then # Check the exit status of the previous command
        echo "  ERROR: Failed to install pip3. Please check your internet connection or Python 3 installation."
        echo "  Press any key to exit."
        read -n 1 -s
        exit 1
    else
        echo "  pip3 installed successfully."
    fi
    echo ""
fi

# --- Step 3: Upgrade pip3 ---
echo "3. Upgrading pip3 to ensure it's up-to-date..."
python3 -m pip install --upgrade pip # Upgrade pip
if [ $? -ne 0 ]; then
    echo ""
    echo "---------------------------------------------------------"
    echo "  ERROR: Failed to upgrade pip3."
    echo "---------------------------------------------------------"
    echo "  Please check your internet connection or your Python 3 installation."
    echo "  Press any key to exit."
    read -n 1 -s
    exit 1
else
    echo "  pip3 upgraded successfully."
    echo ""
fi

# --- Step 4: Install Required Python Packages ---
echo "4. Installing required Python packages (pandas, Pillow, openpyxl, colorama)..."
# Using '--user' to install packages into your user's home directory.
# This avoids needing administrator (sudo) privileges and keeps system Python clean.
python3 -m pip install --user pandas Pillow openpyxl colorama
if [ $? -ne 0 ]; then
    echo ""
    echo "---------------------------------------------------------"
    echo "  ERROR: Failed to install one or more packages."
    echo "---------------------------------------------------------"
    echo "  Please check your internet connection or review the errors above."
    echo "  If you continue to face issues, you might try running:"
    echo "  sudo python3 -m pip install pandas Pillow openpyxl colorama"
    echo "  (which will ask for your macOS password)"
    echo "  Press any key to exit."
    read -n 1 -s
    exit 1
else
    echo ""
    echo "========================================================="
    echo "  All required packages installed successfully!"
    echo "========================================================="
    echo ""
fi

# --- Step 5: Inform User and Offer to run the main script ---
echo "Installation and setup complete!"
echo "You can now run the Python script from this folder by typing:"
echo "python3 main.py"
echo "Make sure your 'Input' folder (containing your CSV, image, and font) is in the same directory as 'main.py'."
echo ""
echo "Press any key to exit this installer."
read -n 1 -s # Read a single character silently
echo "" # For a clean newline after the pause