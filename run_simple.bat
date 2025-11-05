@echo off
echo ============================================================
echo STARTING GESTURE MATCHING - SINGLE WINDOW SIDE BY SIDE
echo ============================================================
echo.
echo Memastikan tidak ada Python process lain yang running...
echo.

REM Kill any existing Python processes (optional, uncomment if needed)
REM taskkill /F /IM python.exe /T 2>nul

echo Starting main_simple.py...
echo.
python main_simple.py

pause
