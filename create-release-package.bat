@echo off
echo ========================================
echo   Creating Release Package for Users
echo ========================================
echo.

REM Create release directory
if exist "release-package" (
    echo Removing existing release package...
    rmdir /s /q "release-package"
)

echo Creating release package directory...
mkdir "release-package"

REM Copy user files
echo Copying user files...
copy "start-app-hub.bat" "release-package\"
copy "stop-app-hub.bat" "release-package\"
copy "start-app-hub.sh" "release-package\"
copy "stop-app-hub.sh" "release-package\"
copy "DOCKER_SETUP.md" "release-package\README.md"

REM Create a simple instruction file
echo Creating quick start instructions...
(
echo # Family Mapping App - Quick Start
echo.
echo ## Windows Users:
echo 1. Install Docker Desktop from: https://www.docker.com/products/docker-desktop
echo 2. Double-click `start-app-hub.bat`
echo 3. Open browser to: http://localhost:8765
echo 4. To stop: Double-click `stop-app-hub.bat`
echo.
echo ## Mac/Linux Users:
echo 1. Install Docker Desktop from: https://www.docker.com/products/docker-desktop
echo 2. Open Terminal in this folder
echo 3. Run: `./start-app-hub.sh`
echo 4. Open browser to: http://localhost:8765
echo 5. To stop: Run `./stop-app-hub.sh`
echo.
echo ## Need Help?
echo See README.md for detailed instructions and troubleshooting.
echo.
echo Your data will be saved in a 'datasets' folder that will be created automatically.
) > "release-package\QUICK-START.md"

echo.
echo ========================================
echo   Release package created successfully!
echo ========================================
echo.
echo Files are ready in the 'release-package' folder.
echo You can zip this folder and upload it to GitHub releases.
echo.
pause 