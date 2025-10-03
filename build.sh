#!/bin/bash
#
# Build script for GAPP executable
# Creates a standalone executable that can be distributed to users without Python
#

set -e  # Exit on error

echo "========================================="
echo "GAPP Build Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Python version: $PYTHON_VERSION"
echo ""

# Install/upgrade pip
echo "Updating pip..."
python3 -m pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip updated${NC}"
echo ""

# Install dependencies
echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt --quiet
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}Warning: requirements.txt not found${NC}"
fi
echo ""

# Install PyInstaller
echo "Installing PyInstaller..."
python3 -m pip install pyinstaller --quiet
echo -e "${GREEN}✓ PyInstaller installed${NC}"
echo ""

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist __pycache__
rm -f *.pyc
echo -e "${GREEN}✓ Clean complete${NC}"
echo ""

# Build executable
echo "Building GAPP executable..."
echo "This may take a few minutes..."
pyinstaller --clean GAPP.spec

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}Build successful!${NC}"
    echo -e "${GREEN}=========================================${NC}"
    echo ""
    echo "Executable location: dist/GAPP"
    echo ""
    
    # Check file size
    if [ -f "dist/GAPP" ]; then
        SIZE=$(du -h "dist/GAPP" | cut -f1)
        echo "Executable size: $SIZE"
    elif [ -f "dist/GAPP.exe" ]; then
        SIZE=$(du -h "dist/GAPP.exe" | cut -f1)
        echo "Executable size: $SIZE"
    fi
    
    echo ""
    echo "You can now distribute the executable to users."
    echo "Users do NOT need Python installed to run it."
    echo ""
    echo "Note: Make sure users have Chrome browser installed"
    echo "      (required for Selenium web scraping)"
    
else
    echo ""
    echo -e "${RED}=========================================${NC}"
    echo -e "${RED}Build failed!${NC}"
    echo -e "${RED}=========================================${NC}"
    echo ""
    echo "Check the error messages above for details."
    exit 1
fi
