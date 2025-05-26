@echo off
echo ========================================
echo    Family Mapping App - Standalone
echo ========================================
echo.
echo Starting the Family Mapping App...
echo This may take a moment to load.
echo.
echo Your web browser will open automatically.
echo If it doesn't, go to: http://localhost:8765
echo.
echo To stop the app, close this window.
echo ========================================
echo.

cd /d "%~dp0"
"FamilyMappingApp.exe"

pause 