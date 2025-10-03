# Data Migration Guide

## Path Changes (October 2025)

GAPP now uses industry-standard locations for storing application data and configuration files.

---

## New Locations

### Linux/macOS

**Data files (logs):**
- **Old**: `~/Documents/GAPP/`
- **New**: `~/.local/share/gapp/`

**Configuration (credentials):**
- **Old**: `~/Documents/GAPP/data.dat`
- **New**: `~/.config/gapp/credentials.dat`

### Windows

**Data files (logs & config):**
- **Old**: `%USERPROFILE%\Documents\GAPP\`
- **New**: `%APPDATA%\GAPP\` (typically `C:\Users\<username>\AppData\Roaming\GAPP\`)

**Credentials file:**
- **Old**: `Documents\GAPP\data.dat`
- **New**: `%APPDATA%\GAPP\credentials.dat`

---

## Why the Change?

The new paths follow operating system conventions:

1. **XDG Base Directory Specification** (Linux/macOS)
   - Cleaner home directory
   - Better multi-user support
   - Easier backup/sync

2. **Windows AppData** (Windows)
   - Standard location for application data
   - Proper roaming profile support
   - Hidden from casual browsing

---

## Migration Steps

### Automatic Migration (Recommended)

GAPP will automatically create the new directories on first run. However, you'll need to log in again with your credentials.

### Manual Migration (Keep Your Credentials)

If you want to preserve your saved credentials:

#### Linux/macOS

```bash
# Create new directories
mkdir -p ~/.local/share/gapp
mkdir -p ~/.config/gapp

# Copy credentials (if you had saved login)
if [ -f ~/Documents/GAPP/data.dat ]; then
    cp ~/Documents/GAPP/data.dat ~/.config/gapp/credentials.dat
fi

# Optional: Copy logs (if you want to preserve them)
if [ -f ~/Documents/GAPP/error.log ]; then
    cp ~/Documents/GAPP/error.log ~/.local/share/gapp/error.log
fi
if [ -f ~/Documents/GAPP/logging.log ]; then
    cp ~/Documents/GAPP/logging.log ~/.local/share/gapp/logging.log
fi

# Optional: Remove old directory
# rm -rf ~/Documents/GAPP
```

#### Windows

```cmd
REM Create new directories
mkdir "%APPDATA%\GAPP"

REM Copy credentials (if you had saved login)
if exist "%USERPROFILE%\Documents\GAPP\data.dat" (
    copy "%USERPROFILE%\Documents\GAPP\data.dat" "%APPDATA%\GAPP\credentials.dat"
)

REM Optional: Copy logs
if exist "%USERPROFILE%\Documents\GAPP\error.log" (
    copy "%USERPROFILE%\Documents\GAPP\error.log" "%APPDATA%\GAPP\error.log"
)
if exist "%USERPROFILE%\Documents\GAPP\logging.log" (
    copy "%USERPROFILE%\Documents\GAPP\logging.log" "%APPDATA%\GAPP\logging.log"
)

REM Optional: Remove old directory
REM rmdir /s /q "%USERPROFILE%\Documents\GAPP"
```

---

## What Happens to Old Files?

The old `~/Documents/GAPP/` (or `Documents\GAPP\`) directory is **NOT** automatically deleted. You can:

1. **Keep it** - No harm in leaving it there
2. **Delete it** - Once you've confirmed GAPP works with the new paths

---

## Troubleshooting

### "Can't find my credentials"

If GAPP asks for credentials again:
- The old `data.dat` wasn't migrated
- Simply re-enter your GPRO credentials
- GAPP will save them in the new location

### "Where are my logs?"

Check the new locations:
- **Linux/macOS**: `~/.local/share/gapp/*.log`
- **Windows**: `%APPDATA%\GAPP\*.log`

To view logs:

**Linux/macOS:**
```bash
tail -f ~/.local/share/gapp/error.log
```

**Windows:**
```cmd
type %APPDATA%\GAPP\error.log
```

### "I want the old paths back"

If you prefer the old behavior, edit `config.py`:

```python
# Replace the path functions with simple paths:
DATA_PATH = Path.home() / "Documents" / "GAPP"
CONFIG_PATH = DATA_PATH
CREDENTIALS_FILE = DATA_PATH / "data.dat"
```

---

## For Developers

### Testing Different Platforms

The path selection respects environment variables:

**Linux/macOS:**
```bash
export XDG_DATA_HOME=/custom/data/path
export XDG_CONFIG_HOME=/custom/config/path
python GAPP.py
```

**Windows:**
```cmd
set APPDATA=C:\Custom\Path
python GAPP.py
```

### Path Selection Logic

See `config.py` for the implementation:

```python
def _get_app_data_directory() -> Path:
    if sys.platform == "win32":
        return Path(os.getenv('APPDATA', Path.home() / "AppData" / "Roaming")) / "GAPP"
    else:
        xdg_data_home = os.getenv('XDG_DATA_HOME')
        return Path(xdg_data_home) / "gapp" if xdg_data_home else Path.home() / ".local" / "share" / "gapp"
```

---

## Benefits Summary

✅ **Cleaner home directory** - No application folders cluttering Documents  
✅ **OS conventions** - Follows Windows and Linux/macOS best practices  
✅ **Better organization** - Separate data and config directories  
✅ **Hidden by default** - AppData/dotfiles don't appear in normal browsing  
✅ **Backup friendly** - Standard locations for backup tools  
✅ **Multi-user ready** - Proper roaming profile support on Windows  

---

**Questions?** Open an issue on GitHub or contact the maintainer.
