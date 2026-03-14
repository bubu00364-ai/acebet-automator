from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

def setup_driver():
    """Sets up the Selenium WebDriver in headless mode."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox") # Required for running in some environments like Replit
    chrome_options.add_argument("--disable-dev-shm-usage") # Required for running in some environments like Replit
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--log-level=3") # Suppress console logs from Chrome itself

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10) # Implicit wait for elements to load
        return driver
    except Exception as e:
        print(f"Error setting up WebDriver: {e}")
        return None

def wait_for_element(driver, by, value, timeout=20):
    """Waits for an element to be present and visible."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        return element
    except:
        print(f"Timeout waiting for element: {value}")
        return None

def wait_for_clickable(driver, by, value, timeout=20):
    """Waits for an element to be clickable."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        return element
    except:
        print(f"Timeout waiting for clickable element: {value}")
        return None

def rotate_ip_address():
    """
    Placeholder for IP rotation.
    On Replit, this is highly limited. A real solution would involve proxy services.
    """
    print("--- Simulating IP Rotation (No actual IP change on Replit without external services) ---")
    # In a more complex setup, you'd reconfigure proxies here.
    time.sleep(config.IP_ROTATION_DELAY) # Add a delay to simulate waiting for IP change
