from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--no-sandbox")  # Avoid issues in some environments

import time

# checkData
# This function will check to see if the user has selected "save credentials"
# If they have, it will store the credentials given in the data.dat file, otherwise it will erase that file
def checkData(filename, rememberCredentials, username, password):
    if rememberCredentials == 1:
        try:
            with open(filename, "w") as file:
                file.write("1\n")
                file.write(username + "\n")
                file.write(password + "\n")
        except Exception:
            pass
    else:
        try:
            open(filename, "w").close()
        except:
            pass


# checkLogin
# Takes login details and confirms they are correct, warning the user if something is amiss
def checkLogin(username, password):
    return True
    # Initialize WebDriver (Ensure you have chromedriver installed)
    driver = webdriver.Chrome()

    try:
        # Open the login page
        driver.get("https://gpro.net/gb/Login.asp")
        time.sleep(2)  # Wait for the page to load

        # **Debug Step 1: Print Form Fields**
        print("\n[DEBUG] Available input fields:")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        for inp in inputs:
            print(f"{inp.get_attribute('name')} - Type: {inp.get_attribute('type')}")

        # Input the username and password
        driver.find_element(By.NAME, "textLogin").send_keys(username)
        driver.find_element(By.NAME, "textPassword").send_keys(password)
        driver.find_element(By.ID, "LogonFake").click()

        # Wait for response to load
        time.sleep(1)

        response_html = driver.page_source
        if "Invalid credentials" in response_html:
            print("\n[DEBUG] Login failed! Check credentials.")
            return False
        else:
            print("\n[DEBUG] Login successful!")

        return True

    finally:
        driver.quit()  # Close browser


def login(driver, username, password):
    # Input the username and password
    driver.find_element(By.NAME, "textLogin").send_keys(username)
    driver.find_element(By.NAME, "textPassword").send_keys(password)
    driver.find_element(By.ID, "LogonFake").click()

    # Wait for response to load
    time.sleep(1)

    response_html = driver.page_source
    if "Invalid credentials" in response_html:
        print("\n[DEBUG] Login failed! Check credentials.")
        return False
    else:
        print("\n[DEBUG] Login successful!")

        return True
    
def checkSession(driver):
    # check if title contains "Sign in"
    if "Sign in" in driver.title:
        print("\n[DEBUG] Session expired or not logged in.")
        return False
    else:
        print("\n[DEBUG] Session is active.")
        return True