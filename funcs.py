from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from typing import Optional
import time
import logging

from config import (
    LOGIN_USERNAME_FIELD, LOGIN_PASSWORD_FIELD, LOGIN_BUTTON_ID,
    LOGIN_FAILURE_TEXT, LOGIN_WAIT_TIME
)

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--no-sandbox")  # Avoid issues in some environments

logger = logging.getLogger(__name__)


def checkData(filename: str, rememberCredentials: int, username: str, password: str) -> None:
    """
    Check if user wants to save credentials and store them accordingly.
    
    Args:
        filename: Path to the credentials file
        rememberCredentials: 1 to save, 0 to clear credentials
        username: User's email/username
        password: User's password
    """
    if rememberCredentials == 1:
        try:
            with open(filename, "w") as file:
                file.write("1\n")
                file.write(username + "\n")
                file.write(password + "\n")
            logger.info("Credentials saved successfully")
        except IOError as e:
            logger.error(f"Failed to save credentials: {e}")
        except Exception as e:
            logger.error(f"Unexpected error saving credentials: {e}")
    else:
        try:
            open(filename, "w").close()
            logger.info("Credentials file cleared")
        except IOError as e:
            logger.error(f"Failed to clear credentials file: {e}")


def checkLogin(username: str, password: str) -> bool:
    """
    Check if login credentials are valid by attempting to log in to GPRO.
    
    Args:
        username: User's email/username
        password: User's password
        
    Returns:
        True if login successful, False otherwise
        
    Note:
        Currently always returns True. This function should be implemented
        when login validation is needed.
    """
    # TODO: Implement actual login validation when needed
    logger.warning("checkLogin always returns True - implementation needed")
    return True


def login(driver: webdriver.Chrome, username: str, password: str) -> bool:
    """
    Perform login to GPRO using provided credentials.
    
    Args:
        driver: Selenium WebDriver instance
        username: User's email/username
        password: User's password
        
    Returns:
        True if login successful, False otherwise
        
    Raises:
        WebDriverException: If there's an issue with the web driver
    """
    try:
        # Input the username and password
        driver.find_element(By.NAME, LOGIN_USERNAME_FIELD).send_keys(username)
        driver.find_element(By.NAME, LOGIN_PASSWORD_FIELD).send_keys(password)
        driver.find_element(By.ID, LOGIN_BUTTON_ID).click()

        # Wait for response to load
        time.sleep(LOGIN_WAIT_TIME)

        response_html = driver.page_source
        if LOGIN_FAILURE_TEXT in response_html:
            logger.warning("Login failed - invalid credentials")
            return False
        else:
            logger.info("Login successful")
            return True
            
    except WebDriverException as e:
        logger.error(f"WebDriver error during login: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        raise

    
def checkSession(driver: webdriver.Chrome) -> bool:
    """
    Check if the current session is still active.
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        True if session is active, False if expired or not logged in
    """
    try:
        # Check if title contains "Sign in"
        if "Sign in" in driver.title:
            logger.info("Session expired or not logged in")
            return False
        else:
            logger.debug("Session is active")
            return True
    except WebDriverException as e:
        logger.error(f"Error checking session: {e}")
        return False