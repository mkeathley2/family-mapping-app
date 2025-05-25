@echo off
echo ========================================
echo    Family Mapping App - Starting...
echo ========================================
echo.

REM Check if Docker is running
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running or not installed!
    echo Please install Docker Desktop and make sure it's running.
    echo Download from: https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo Docker is running - Good!
echo.

REM Create datasets directory if it doesn't exist
if not exist "datasets" (
    echo Creating datasets directory...
    mkdir datasets
)

echo Starting Family Mapping App...
echo This may take a few minutes the first time (downloading application)
echo.

REM Stop any existing container
docker stop family-mapping-app >nul 2>&1
docker rm family-mapping-app >nul 2>&1

REM Pull latest image and run
docker run -d ^
    --name family-mapping-app ^
    -p 8765:8765 ^
    -v "%cd%\datasets:/app/datasets" ^
    --restart unless-stopped ^
    mkeathley75028/family-mapping-app:latest

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    SUCCESS! App is now running!
    echo ========================================
    echo.
    echo Open your web browser and go to:
    echo    http://localhost:8765
    echo.
    echo To stop the app, run: stop-app-hub.bat
    echo.
    echo The app will continue running in the background
    echo until you stop it or restart your computer.
    echo.
    echo Your data will be saved in the 'datasets' folder
    echo and will persist between app restarts.
    echo.
) else (
    echo.
    echo ERROR: Failed to start the application!
    echo Please check the error messages above.
    echo.
)

pause 