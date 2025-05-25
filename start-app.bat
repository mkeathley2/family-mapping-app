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

REM Check if docker-compose is available
docker-compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: docker-compose is not available!
    echo Please make sure Docker Desktop is properly installed.
    echo.
    pause
    exit /b 1
)

echo Starting Family Mapping App...
echo This may take a few minutes the first time (downloading dependencies)
echo.

REM Start the application
docker-compose up -d

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    SUCCESS! App is now running!
    echo ========================================
    echo.
    echo Open your web browser and go to:
    echo    http://localhost:8765
    echo.
    echo To stop the app, run: stop-app.bat
    echo.
    echo The app will continue running in the background
    echo until you stop it or restart your computer.
    echo.
) else (
    echo.
    echo ERROR: Failed to start the application!
    echo Please check the error messages above.
    echo.
)

pause 