"""
Configuration constants for GAPP application.

This module contains all configuration values, constants, URLs, and magic numbers
extracted from the codebase for better maintainability.
"""

from pathlib import Path
from enum import Enum

# ============================================================================
# PATHS AND DIRECTORIES
# ============================================================================

# Application data directory
DATA_PATH = Path.home() / "Documents" / "GAPP"

# Log file paths
ERROR_LOG_FILE = DATA_PATH / "error.log"
GENERAL_LOG_FILE = DATA_PATH / "logging.log"

# Credentials storage
CREDENTIALS_FILE = DATA_PATH / "data.dat"

# ============================================================================
# GPRO URLS
# ============================================================================

GPRO_BASE_URL = "https://gpro.net/gb"
GPRO_HOME_URL = f"{GPRO_BASE_URL}/"
GPRO_LOGIN_URL = f"{GPRO_BASE_URL}/Login.asp"
GPRO_DRIVER_PROFILE_URL = f"{GPRO_BASE_URL}/DriverProfile.asp"
GPRO_TRACK_DETAILS_URL = f"{GPRO_BASE_URL}/TrackDetails.asp"
GPRO_RACE_SETUP_URL = f"{GPRO_BASE_URL}/RaceSetup.asp"
GPRO_UPDATE_CAR_URL = f"{GPRO_BASE_URL}/UpdateCar.asp"
GPRO_TECH_DIRECTOR_URL = f"{GPRO_BASE_URL}/TechDProfile.asp"
GPRO_STAFF_URL = f"{GPRO_BASE_URL}/StaffAndFacilities.asp"
GPRO_SUPPLIERS_URL = f"{GPRO_BASE_URL}/Suppliers.asp"

# ============================================================================
# DRIVER AND CAR CONSTANTS
# ============================================================================

# XPath pattern to extract driver ID from home page
DRIVER_ID_XPATH = "normalize-space(//a[contains(@href, 'DriverProfile.asp?ID=')]/@href)"

# ============================================================================
# WEAR THRESHOLDS
# ============================================================================

# Wear percentage thresholds for UI color coding
WEAR_THRESHOLD_CRITICAL = 90  # Red warning
WEAR_THRESHOLD_WARNING = 80   # Orange warning

# ============================================================================
# UI STYLES
# ============================================================================

class WearStatus(Enum):
    """Enum for wear status label styles."""
    NORMAL = "Black.Label"
    WARNING = "Orange.Label"
    CRITICAL = "Red.Label"


# ============================================================================
# DEFAULT VALUES
# ============================================================================

# Default setup values
DEFAULT_SETUP_VALUE = "000"

# Default weather and session
DEFAULT_WEATHER = "Dry"
DEFAULT_SESSION = "Race"

# Default strategy values
DEFAULT_WEAR_PERCENTAGE = "20"
DEFAULT_LAPS = 1

# Default fuel load display
DEFAULT_FUEL_LOWER = "0 L"
DEFAULT_FUEL_UPPER = "1 L"

# ============================================================================
# WEB SCRAPING CONSTANTS
# ============================================================================

# Selenium wait times (in seconds)
LOGIN_WAIT_TIME = 1
PAGE_LOAD_WAIT_TIME = 2

# Form field names
LOGIN_USERNAME_FIELD = "textLogin"
LOGIN_PASSWORD_FIELD = "textPassword"
LOGIN_BUTTON_ID = "LogonFake"

# Login validation text
LOGIN_FAILURE_TEXT = "Invalid credentials"

# ============================================================================
# CAR PARTS
# ============================================================================

# List of all car parts in order
CAR_PARTS = [
    'Chassis', 'Engine', 'FWing', 'RWing', 'Underbody',
    'Sidepods', 'Cooling', 'Gearbox', 'Brakes',
    'Suspension', 'Electronics'
]

CAR_PARTS_DISPLAY = [
    'Chassis', 'Engine', 'Front Wing', 'Rear Wing', 'Underbody',
    'Sidepods', 'Cooling', 'Gearbox', 'Brakes',
    'Suspension', 'Electronics'
]

# ============================================================================
# TYRE COMPOUNDS
# ============================================================================

TYRE_COMPOUNDS = ['Extra Soft', 'Soft', 'Medium', 'Hard', 'Rain']
TYRE_COMPOUNDS_SHORT = ['Extra', 'Soft', 'Medium', 'Hard', 'Rain']

# ============================================================================
# CALCULATION CONSTANTS
# ============================================================================

# Tyre supplier factors
TYRE_SUPPLIER_FACTORS = {
    "Pipirelli": 1,
    "Avonn": 8,
    "Yokomama": 3,
    "Dunnolop": 4,
    "Contimental": 8,
    "Badyear": 7
}

# Tyre compound supplier factors
TYRE_COMPOUND_SUPPLIER_FACTORS = {
    "Pipirelli": 0,
    "Avonn": 0.015,
    "Yokomama": 0.05,
    "Dunnolop": 0.07,
    "Contimental": 0.07,
    "Badyear": 0.09
}

# Track wear levels
TRACK_WEAR_LEVELS = {
    "Very low": 0,
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Very high": 4
}

# Wear factors for different tyre compounds
WEAR_FACTORS = [
    0.998163750229071,  # Extra Soft
    0.997064844817654,  # Soft
    0.996380346554349,  # Medium
    0.995862526048112,  # Hard
    0.996087854384523   # Rain
]

# Part level factors for wear calculation
PART_LEVEL_FACTORS = [
    1.0193, 1.0100, 1.0073, 1.0053, 1.0043,
    1.0037, 1.0043, 1.0097, 1.0052
]

# Base wear constant
BASE_WEAR = 129.776458172062

# Fuel calculation constant
FUEL_TIME_COEFFICIENT = 0.0025

# Compound calculation constants
COMPOUND_CALC_CORNER_FACTOR = 0.00018
COMPOUND_CALC_TEMP_BASE = 50

# ============================================================================
# LOGGING
# ============================================================================

# Log format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%y-%m-%d %H:%M'

# ============================================================================
# VALIDATION
# ============================================================================

# Regex patterns for input validation
PATTERN_INTEGER = r'\d+'
PATTERN_FLOAT = r'\d+\.?\d*'

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_wear_status(wear_value: int) -> WearStatus:
    """
    Determine the wear status based on wear value.
    
    Args:
        wear_value: The wear percentage value
        
    Returns:
        WearStatus enum indicating the severity level
    """
    if wear_value >= WEAR_THRESHOLD_CRITICAL:
        return WearStatus.CRITICAL
    elif wear_value >= WEAR_THRESHOLD_WARNING:
        return WearStatus.WARNING
    return WearStatus.NORMAL


def ensure_data_directory() -> None:
    """Ensure the data directory exists, creating it if necessary."""
    DATA_PATH.mkdir(parents=True, exist_ok=True)


def extract_driver_id_from_url(url_string: str) -> int:
    """
    Extract driver ID from a GPRO driver profile URL.
    
    Args:
        url_string: URL string containing driver ID (e.g., "DriverProfile.asp?ID=20325")
        
    Returns:
        Driver ID as integer
        
    Raises:
        ValueError: If driver ID cannot be extracted from URL
    """
    import re
    match = re.search(r'ID=(\d+)', url_string)
    if match:
        return int(match.group(1))
    raise ValueError(f"Could not extract driver ID from URL: {url_string}")
