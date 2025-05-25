@echo off
echo ========================================
echo    Family Mapping App - Stopping...
echo ========================================
echo.

REM Stop the application
docker-compose down

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    App has been stopped successfully!
    echo ========================================
    echo.
    echo To start the app again, run: start-app.bat
    echo.
) else (
    echo.
    echo ERROR: Failed to stop the application!
    echo The app may not be running.
    echo.
)

pause 