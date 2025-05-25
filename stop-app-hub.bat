@echo off
echo ========================================
echo    Family Mapping App - Stopping...
echo ========================================
echo.

REM Stop and remove the container
docker stop family-mapping-app
docker rm family-mapping-app

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    App has been stopped successfully!
    echo ========================================
    echo.
    echo To start the app again, run: start-app-hub.bat
    echo.
    echo Your data in the 'datasets' folder has been preserved.
    echo.
) else (
    echo.
    echo ERROR: Failed to stop the application!
    echo The app may not be running.
    echo.
)

pause 