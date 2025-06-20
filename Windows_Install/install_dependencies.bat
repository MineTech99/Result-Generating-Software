@echo off
REM This batch file automates the installation of required Python packages (pandas, Pillow).
REM It assumes Python is already installed and added to your system's PATH.
REM If Python is not found, the script will guide you to install it manually.

echo.
echo =========================================================
echo  Automated Python Package Installer for Image Generator
echo =========================================================
echo.

REM --- Step 1: Check for Python Installation ---
echo Checking for Python installation...
python --version >NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Python is not found or not added to your system's PATH.
    echo Please install Python first from the official website:
    echo        https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During Python installation, make sure to check the box
    echo            "Add Python.exe to PATH" or "Add Python 3.x to PATH".
    echo.
    echo After installing Python, please run this batch file again.
    echo.
    pause
    goto :eof
) else (
    echo Python found. Version:
    python --version
    echo.
)

REM --- Step 2: Request Administrator Privileges (if not already running as admin) ---
REM This part tries to re-run the script as administrator if it's not already.
REM This is often crucial for global pip installations.
NET SESSION >NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Requesting Administrator privileges to install packages...
    powershell -Command "Start-Process '%~dpnx0' -Verb RunAs"
    goto :eof
) else (
    echo Running with Administrator privileges.
)
echo.

REM --- Step 3: Upgrade pip (Python's package installer) ---
echo Upgrading pip to ensure it's up-to-date...
python -m pip install --upgrade pip
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to upgrade pip. This might be due to internet issues
    echo or a problem with your Python installation.
    pause
    goto :eof
) else (
    echo pip upgraded successfully.
)
echo.

REM --- Step 4: Install Required Packages ---
echo Installing required Python packages (pandas, Pillow, openpyxl, colorama)...
python -m pip install pandas Pillow openpyxl colorama
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install one or more packages.
    echo Please check your internet connection or review the errors above.
    pause
    goto :eof
) else (
    echo All required packages installed successfully!
)
echo.

REM --- Step 5: Inform User and Offer to Run the Main Script ---
echo Installation and setup complete!
echo You can now run the main Python script for image generation.

REM --- Optional: Automatically run your main.py script ---
REM Uncomment the following two lines (remove 'REM ') if you want the batch file
REM to automatically run your 'main.py' script after successfully installing everything.
REM This assumes main.py is in the same directory as this batch file.
REM echo Running the main image generation script (main.py)...
REM python main.py
REM IF %ERRORLEVEL% NEQ 0 (
REM    echo ERROR: Failed to run main.py. Please check the script for issues.
REM ) else (
REM    echo main.py executed successfully.
REM )
REM echo.

echo Press any key to exit this installer.
pause
goto :eof

:eof