# GAPP Deployment Guide

Complete guide for building and distributing GAPP as a standalone executable.

---

## Quick Start

### For Linux/macOS:
```bash
./build.sh
```

### For Windows:
```cmd
build.bat
```

The executable will be created in the `dist/` folder.

---

## Prerequisites

### Developer Requirements (Building the Executable)

1. **Python 3.7+** installed
2. **pip** package manager
3. **Chrome Browser** (for testing)

### End User Requirements (Running the Executable)

1. **Chrome Browser** - Required for web scraping (Selenium)
2. **No Python required** - The executable is standalone

---

## Building Process

### Option 1: Automatic Build (Recommended)

**Linux/macOS:**
```bash
./build.sh
```

**Windows:**
```cmd
build.bat
```

This will:
1. Check Python installation
2. Install all dependencies
3. Install PyInstaller
4. Clean previous builds
5. Create standalone executable
6. Report build status and file size

### Option 2: Manual Build

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install PyInstaller
pip install pyinstaller

# 3. Build executable
pyinstaller --clean GAPP.spec

# 4. Find executable in dist/ folder
```

---

## Build Output

After successful build, you'll find:

```
dist/
├── GAPP          (Linux/macOS executable)
└── GAPP.exe      (Windows executable)
```

**Typical file size:** 50-100 MB (includes Python interpreter and all dependencies)

---

## Distribution

### What to Distribute

**Single File Distribution:**
- `dist/GAPP` (Linux/macOS) or `dist/GAPP.exe` (Windows)

That's it! The executable is completely standalone.

### Distribution Methods

1. **GitHub Releases**
   - Upload executable to GitHub releases
   - Users can download directly

2. **Cloud Storage**
   - Upload to Google Drive, Dropbox, etc.
   - Share download link

3. **Direct Transfer**
   - USB drive, email, etc.

---

## User Instructions

### Linux/macOS

```bash
# 1. Download GAPP executable
# 2. Make it executable (if needed)
chmod +x GAPP

# 3. Run it
./GAPP
```

### Windows

```
1. Download GAPP.exe
2. Double-click to run
```

**Note:** Windows may show a security warning for unsigned executables. Users should click "More info" → "Run anyway"

---

## Important Notes

### Chrome Browser Requirement

**Users MUST have Chrome browser installed** because:
- Selenium (web scraping library) uses Chrome
- ChromeDriver is bundled with the executable
- Application will fail without Chrome

### First Run

On first run, the application will:
1. Create application directories:
   - **Linux/macOS**: `~/.local/share/gapp/` (data) and `~/.config/gapp/` (config)
   - **Windows**: `%APPDATA%\GAPP\` (typically `C:\Users\<username>\AppData\Roaming\GAPP\`)
2. Create log files: `error.log`, `logging.log`
3. Prompt for GPRO credentials

### Antivirus Warnings

Some antivirus software may flag PyInstaller executables as suspicious:
- **This is a false positive**
- PyInstaller executables are often flagged
- Users can add exception or whitelist the file

To reduce false positives:
- Sign the executable (requires code signing certificate)
- Submit to antivirus vendors for whitelisting

---

## Customization

### Adding an Icon

1. Create or find an `.ico` file (Windows) or `.icns` (macOS)
2. Edit `GAPP.spec`:
   ```python
   icon='path/to/icon.ico'  # Windows
   icon='path/to/icon.icns'  # macOS
   ```
3. Rebuild

### Reducing File Size

Edit `GAPP.spec` to exclude more packages:
```python
excludes=[
    'matplotlib', 'numpy', 'pandas', 'PIL', 
    'PyQt5', 'scipy', 'pytest', 'IPython',
    # Add more packages you don't use
],
```

### Console Mode (for Debugging)

Edit `GAPP.spec`:
```python
console=True,  # Show console window (useful for debugging)
```

---

## Troubleshooting

### Build Issues

**"ModuleNotFoundError" during build:**
```bash
# Install missing package
pip install <package-name>

# Rebuild
pyinstaller --clean GAPP.spec
```

**"Permission denied" on Linux/macOS:**
```bash
chmod +x build.sh
./build.sh
```

### Runtime Issues

**"Chrome not found" error:**
- User needs to install Chrome browser
- Make sure Chrome is in system PATH

**Application won't start:**
- Check `error.log` in:
  - **Linux/macOS**: `~/.local/share/gapp/error.log`
  - **Windows**: `%APPDATA%\GAPP\error.log`
- Run from terminal to see error messages:
  ```bash
  ./dist/GAPP  # Linux/macOS
  dist\GAPP.exe  # Windows
  ```

**Selenium errors:**
- Update Chrome to latest version
- ChromeDriver version may be incompatible

---

## Advanced Options

### Creating Platform-Specific Builds

**Cross-compilation is NOT supported.** To create executables for different platforms:

1. **Windows executable** → Build on Windows
2. **macOS executable** → Build on macOS
3. **Linux executable** → Build on Linux

### GitHub Actions (Automated Builds)

Create `.github/workflows/build.yml` for automated builds on commit:

```yaml
name: Build GAPP

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build executable
      run: pyinstaller --clean GAPP.spec
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: GAPP-${{ matrix.os }}
        path: dist/
```

---

## File Structure

```
gapp/
├── GAPP.py              # Main application
├── calcs.py             # Calculation functions
├── config.py            # Configuration
├── data.py              # Track data
├── funcs.py             # Helper functions
├── requirements.txt     # Python dependencies
├── GAPP.spec           # PyInstaller configuration
├── build.sh            # Linux/macOS build script
├── build.bat           # Windows build script
├── README.md           # Project documentation
├── REFACTORING.md      # Refactoring documentation
└── DEPLOYMENT.md       # This file
```

After build:
```
gapp/
├── build/              # Temporary build files (can delete)
├── dist/               # Final executable(s)
│   └── GAPP / GAPP.exe
└── __pycache__/        # Python cache (can delete)
```

---

## Version Management

### Updating the Application

1. Update version in code
2. Rebuild executable
3. Distribute new version to users

### Version Numbering

Add version to `config.py`:
```python
VERSION = "2.0.0"
```

Display in GUI (add to `GAPP.py`):
```python
from config import VERSION
root.title(f"GAPP v{VERSION}")
```

---

## Security Considerations

### Code Signing

**Windows:**
- Purchase code signing certificate
- Use SignTool to sign `.exe`
- Reduces antivirus false positives
- Builds user trust

**macOS:**
- Requires Apple Developer account ($99/year)
- Use `codesign` to sign application
- Required for distribution on macOS 10.15+

### Credentials Storage

The application stores credentials in:
- **Linux/macOS**: `~/.config/gapp/credentials.dat`
- **Windows**: `%APPDATA%\GAPP\credentials.dat`

**Security notes:**
- Credentials are stored in plain text
- File is readable only by user (Unix permissions)
- Consider encryption for production use

---

## Support

### For Developers

Issues building? Check:
1. Python version (3.7+)
2. All dependencies installed
3. PyInstaller version (latest)
4. Review build logs

### For End Users

Application issues? Check:
1. Chrome browser installed
2. Log files in application data directory:
   - **Linux/macOS**: `~/.local/share/gapp/*.log`
   - **Windows**: `%APPDATA%\GAPP\*.log`
3. Valid GPRO credentials
4. Internet connection

---

## FAQ

**Q: Why is the executable so large?**  
A: It includes Python interpreter, all libraries, and dependencies. Typical size is 50-100 MB.

**Q: Can I run on systems without Python?**  
A: Yes! That's the whole point. The executable is standalone.

**Q: Does it work offline?**  
A: No, it needs internet to scrape GPRO website.

**Q: Can I modify the executable?**  
A: No, but you can modify the source code and rebuild.

**Q: Why does antivirus flag it?**  
A: PyInstaller executables are often flagged. It's a false positive.

**Q: Can I distribute this commercially?**  
A: Check the license. GAPP appears to be open source.

---

## License

Same as main GAPP project. See repository for details.

---

**Last Updated:** October 3, 2025  
**PyInstaller Version:** 6.0+  
**Python Version:** 3.7+
