@echo off
REM This script runs your main.py and keeps the window open.

echo.
echo ===========================================
echo  Starting Image Generation Script (main.py)
echo ===========================================
echo.

REM Change directory to where this batch file is located
cd /d "%~dp0"

REM Run the Python script
python main.py

REM Keep the window open after the script finishes or encounters an error
echo.
echo Script finished. Press any key to close this window.
pause > NUL