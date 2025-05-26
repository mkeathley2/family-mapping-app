@echo off
echo ========================================
echo   Creating Standalone Package
echo ========================================
echo.

REM Create standalone package directory
if exist "standalone-package" (
    echo Removing existing package...
    rmdir /s /q "standalone-package"
)

echo Creating package directory...
mkdir "standalone-package"

REM Copy the executable
echo Copying executable...
copy "dist\FamilyMappingApp.exe" "standalone-package\"

REM Copy support files
echo Copying support files...
copy "START_HERE.bat" "standalone-package\"
copy "STANDALONE_README.md" "standalone-package\README.md"
copy "sample_family_addresses.csv" "standalone-package\"

REM Create version info
echo Creating version info...
(
echo Family Mapping App - Standalone Version
echo Version: v0.0.3-standalone
echo Build Date: %date% %time%
echo.
echo This package contains:
echo - FamilyMappingApp.exe ^(Main application^)
echo - START_HERE.bat ^(Double-click to run^)
echo - README.md ^(Instructions^)
echo - sample_family_addresses.csv ^(Example file^)
echo.
echo No installation required - just double-click START_HERE.bat!
) > "standalone-package\VERSION.txt"

REM Create zip file
echo Creating zip file...
if exist "family-mapping-app-standalone-v0.0.3.zip" del "family-mapping-app-standalone-v0.0.3.zip"
powershell -Command "Compress-Archive -Path 'standalone-package\*' -DestinationPath 'family-mapping-app-standalone-v0.0.3.zip' -Force"

echo.
echo ========================================
echo   Package created successfully!
echo ========================================
echo.
echo Files created:
echo - standalone-package\ ^(folder with all files^)
echo - family-mapping-app-standalone-v0.0.3.zip ^(ready for distribution^)
echo.
echo The zip file is ready to share with non-technical users!
echo They just need to:
echo 1. Download and extract the zip
echo 2. Double-click START_HERE.bat
echo 3. Use the app in their browser
echo.
pause 