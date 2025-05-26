@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    GitHub Release Creator
echo ========================================
echo.

REM Get version from user
set /p VERSION="Enter version (e.g., v0.0.4): "
if "%VERSION%"=="" (
    echo Error: Version is required!
    pause
    exit /b 1
)

REM Get release title
set /p TITLE="Enter release title (or press Enter for default): "
if "%TITLE%"=="" (
    set "TITLE=Family Mapping App %VERSION% - New Release"
)

echo.
echo Creating release for version: %VERSION%
echo Title: %TITLE%
echo.

REM Create release package
echo Step 1: Creating release package...
call create-release-package.bat

REM Create zip file
echo Step 2: Creating zip file...
if exist "family-mapping-app-%VERSION%.zip" del "family-mapping-app-%VERSION%.zip"
powershell -Command "Compress-Archive -Path 'release-package\*' -DestinationPath 'family-mapping-app-%VERSION%.zip' -Force"

REM Create release notes file
echo Step 3: Creating release notes...
(
echo # Family Mapping App %VERSION% 🎉
echo.
echo ## 🚀 New Release
echo.
echo ### ✨ What's New
echo.
echo - Add your new features here
echo - Bug fixes and improvements
echo - Performance enhancements
echo.
echo ### 🚀 Quick Start
echo.
echo 1. **Install Docker Desktop** from [docker.com](https://www.docker.com/products/docker-desktop^)
echo 2. **Download** the `family-mapping-app-%VERSION%.zip` file below
echo 3. **Extract** and double-click the start script for your OS
echo 4. **Open** http://localhost:8765 in your browser
echo 5. **Start mapping** your family addresses! 🗺️
echo.
echo ### 📋 System Requirements
echo.
echo - Docker Desktop (Windows/Mac^) or Docker Engine (Linux^)
echo - 4GB RAM minimum
echo - 1GB free disk space
echo - Modern web browser
echo.
echo ### 🔧 Technical Details
echo.
echo - **Docker Image**: `mkeathley75028/family-mapping-app:%VERSION%`
echo - **Port**: 8765
echo - **Data Storage**: Local `datasets` folder
echo.
echo ### 🙏 Support
echo.
echo If you encounter any issues:
echo 1. Check the troubleshooting section in README.md
echo 2. Make sure Docker Desktop is running
echo 3. Open an issue with specific error messages
echo.
echo ---
echo.
echo **Download the zip file below and start mapping your family connections today!** 🗺️❤️
) > "RELEASE_NOTES_%VERSION%.md"

REM Commit and tag
echo Step 4: Committing changes and creating tag...
git add .
git commit -m "Release %VERSION%"
git tag %VERSION%
git push origin master
git push origin %VERSION%

REM Create GitHub release
echo Step 5: Creating GitHub release...
& "C:\Program Files\GitHub CLI\gh.exe" release create %VERSION% family-mapping-app-%VERSION%.zip --title "%TITLE%" --notes-file "RELEASE_NOTES_%VERSION%.md"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    SUCCESS! Release created!
    echo ========================================
    echo.
    echo Release URL: https://github.com/mkeathley2/family-mapping-app/releases/tag/%VERSION%
    echo.
    echo Don't forget to:
    echo 1. Update Docker image: docker build -t mkeathley75028/family-mapping-app:%VERSION% .
    echo 2. Push to Docker Hub: docker push mkeathley75028/family-mapping-app:%VERSION%
    echo 3. Update latest tag: docker tag mkeathley75028/family-mapping-app:%VERSION% mkeathley75028/family-mapping-app:latest
    echo 4. Push latest: docker push mkeathley75028/family-mapping-app:latest
    echo.
) else (
    echo.
    echo ERROR: Failed to create GitHub release!
    echo.
)

pause 