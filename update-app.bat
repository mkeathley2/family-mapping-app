@echo off
echo ========================================
echo    Family Mapping App - Updating...
echo ========================================
echo.

REM Check if Docker is running
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running or not installed!
    echo Please install Docker Desktop and make sure it's running.
    echo.
    pause
    exit /b 1
)

echo Stopping current version...
docker-compose down

echo.
echo Pulling latest code from GitHub...
git pull origin main

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to pull updates from GitHub!
    echo Make sure you have git installed and internet connection.
    echo.
    pause
    exit /b 1
)

echo.
echo Rebuilding application with updates...
docker-compose build --no-cache

echo.
echo Starting updated application...
docker-compose up -d

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    UPDATE SUCCESSFUL!
    echo ========================================
    echo.
    echo Your app has been updated to the latest version.
    echo Open your web browser and go to:
    echo    http://localhost:8765
    echo.
    echo Your data has been preserved during the update.
    echo.
) else (
    echo.
    echo ERROR: Failed to start the updated application!
    echo Please check the error messages above.
    echo.
)

pause 