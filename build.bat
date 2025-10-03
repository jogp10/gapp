@echo off
REM Build script for GAPP executable (Windows)
REM Creates a standalone executable that can be distributed to users without Python

echo =========================================
echo GAPP Build Script (Windows)
echo =========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Install/upgrade pip
echo Updating pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip updated
echo.

REM Install dependencies
echo Installing dependencies...
if exist requirements.txt (
    python -m pip install -r requirements.txt --quiet
    echo [OK] Dependencies installed
) else (
    echo Warning: requirements.txt not found
)
echo.

REM Install PyInstaller
echo Installing PyInstaller...
python -m pip install pyinstaller --quiet
echo [OK] PyInstaller installed
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
del /q *.pyc 2>nul
echo [OK] Clean complete
echo.

REM Build executable
echo Building GAPP executable...
echo This may take a few minutes...
echo.
pyinstaller --clean GAPP.spec

if errorlevel 1 (
    echo.
    echo =========================================
    echo Build failed!
    echo =========================================
    echo.
    echo Check the error messages above for details.
    pause
    exit /b 1
)

echo.
echo =========================================
echo Build successful!
echo =========================================
echo.
echo Executable location: dist\GAPP.exe
echo.

REM Show file size
if exist dist\GAPP.exe (
    for %%A in (dist\GAPP.exe) do echo Executable size: %%~zA bytes
)

echo.
echo You can now distribute GAPP.exe to users.
echo Users do NOT need Python installed to run it.
echo.
echo Note: Make sure users have Chrome browser installed
echo       (required for Selenium web scraping)
echo.
pause
