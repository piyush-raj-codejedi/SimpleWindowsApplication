@echo off
echo Starting TestSky Flight Booking Application...
cd /d "%~dp0"
python app.py
if %errorlevel% neq 0 (
    echo.
    echo Application crashed with error code %errorlevel%.
    echo Check the error above for details.
)
pause
