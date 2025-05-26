@echo off
echo ========================================
echo   Cross-Platform Standalone Packages
echo ========================================
echo.

echo This script helps you create standalone packages for all platforms.
echo.
echo IMPORTANT: You need to build each platform on its native system:
echo - Windows: Build on Windows (this script)
echo - macOS: Build on macOS using build-macos.sh
echo - Linux: Build on Linux using build-linux.sh
echo.

REM Create Windows package (current system)
echo Creating Windows package...
call create-standalone-package.bat

echo.
echo ========================================
echo   Windows Package Complete!
echo ========================================
echo.
echo To create packages for other platforms:
echo.
echo FOR macOS:
echo 1. Copy this project to a Mac
echo 2. Install Python and PyInstaller: pip install pyinstaller
echo 3. Run: ./build-macos.sh
echo.
echo FOR Linux:
echo 1. Copy this project to a Linux system
echo 2. Install Python and PyInstaller: pip install pyinstaller
echo 3. Run: ./build-linux.sh
echo.
echo OR use GitHub Actions for automated cross-platform builds!
echo.
pause 