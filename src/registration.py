import random
import string
import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config
import browser
import email_utils

def generate_random_password(length=config.PASSWORD_LENGTH):
    """Generates a random password with a mix of characters."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def get_random_dob():
    """Generates a random date of birth within the configured range."""
    year = random.randint(config.MIN_BIRTH_YEAR, config.MAX_BIRTH_YEAR)
    month = random.randint(1, 12)
    # Ensure day is valid for the chosen month and year (simplified for common months)
    if month in [4, 6, 9, 11]:
        day = random.randint(1, 28) # Max 28 for these months
    elif month == 2:
        day = random.randint(1, 29) if year % 4 == 0 else random.randint(1, 28) # Leap year check
    else:
        day = random.randint(1, 31)
    return datetime.date(year, month, day)

def get_temporary_email():
    """
    Fetches a temporary email.
    NOTE: This is a critical and difficult part. Free temp email services often
    rate-limit or don't have stable APIs. This function needs to be replaced
    with a robust solution, possibly involving a paid service or a custom setup.
    For this example, we'll use a placeholder domain.
    """
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
    # Using a common temp email domain. This is highly likely to be blocked or unreliable.
    # Consider services like Mailinator (paid API), TempMail.io (check API status), or others.
    return f"{random_string}@temp-mail.org"

def register_account(driver):
    """Performs the account registration process for one account."""
    try:
        driver.get(config.TARGET_URL)
        print(f"Navigated to {config.TARGET_URL}")
        time.sleep(config.ACTION_DELAY)

        # --- Navigate to Register Tab ---
        # Find the 'Register' button within the sign-in modal.
        # The XPath might need adjustment if the website changes.
        register_tab = browser.wait_for_clickable(driver, By.XPATH, "//div[@role='dialog']//button[text()='Register']")
        if not register_tab:
            print("Could not find the 'Register' tab.")
            return None
        register_tab.click()
        print("Clicked 'Register' tab.")
        time.sleep(config.ACTION_DELAY)

        # --- Generate Data ---
        email = get_temporary_email()
        password = generate_random_password()
        dob = get_random_dob()

        # --- Fill Registration Form ---
        # Email Address
        email_input = browser.wait_for_element(driver, By.XPATH, "//input[@type='email' and @placeholder='Email Address *']")
        if email_input:
            email_input.send_keys(email)
            print(f"Entered email: {email}")
            time.sleep(config.ACTION_DELAY)
        else:
            print("Email input field not found.")
            return None

        # Password
        password_input = browser.wait_for_element(driver, By.XPATH, "//input[@type='password' and @placeholder='Password *']")
        if password_input:
            password_input.send_keys(password)
            print("Entered password.")
            time.sleep(config.ACTION_DELAY)
        else:
            print("Password input field not found.")
            return None

        # Confirm Password
        confirm_password_input = browser.wait_for_element(driver, By.XPATH, "//input[@type='password' and @placeholder='Confirm Password *']")
        if confirm_password_input:
            confirm_password_input.send_keys(password)
            print("Confirmed password.")
            time.sleep(config.ACTION_DELAY)
        else:
            print("Confirm password input field not found.")
            return None

        # Date of Birth
        # This involves interacting with a calendar widget, which is often complex.
        # We'll try to simulate clicks.
        dob_field = browser.wait_for_clickable(driver, By.XPATH, "//input[@placeholder='Date of Birth *']")
        if dob_field:
            dob_field.click()
            time.sleep(config.ACTION_DELAY)

            # Select Year
            year_select = browser.wait_for_clickable(driver, By.XPATH, "//div[@class='react-datepicker__year-select']")
            if year_select:
                year_select.click()
                year_option_xpath = f"//option[text()='{dob.year}']"
                year_option = browser.wait_for_clickable(driver, By.XPATH, year_option_xpath)
                if year_option:
                    year_option.click()
                    print(f"Selected year: {dob.year}")
                    time.sleep(config.ACTION_DELAY/2)
                else:
                    print(f"Could not find year option: {dob.year}")
                    return None
            else:
                print("Date of Birth year select not found.")
                return None

            # Select Month
            month_select = browser.wait_for_clickable(driver, By.XPATH, "//div[@class='react-datepicker__month-select']")
            if month_select:
                month_select.click()
                month_names = ["January", "February", "March", "April", "May", "June",
                               "July", "August", "September", "October", "November", "December"]
                month_option_xpath = f"//option[text()='{month_names[dob.month - 1]}']"
                month_option = browser.wait_for_clickable(driver, By.XPATH, month_option_xpath)
                if month_option:
                    month_option.click()
                    print(f"Selected month: {month_names[dob.month - 1]}")
                    time.sleep(config.ACTION_DELAY/2)
                else:
                    print(f"Could not find month option: {month_names[dob.month - 1]}")
                    return None
            else:
                print("Date of Birth month select not found.")
                return None

            # Select Day
            day_xpath = f"//div[contains(@class, 'react-datepicker__day') and not(contains(@class, 'outside')) and text()='{dob.day}']"
            day_element = browser.wait_for_clickable(driver, By.XPATH, day_xpath)
            if day_element:
                day_element.click()
                print(f"Selected day: {dob.day}")
                time.sleep(config.ACTION_DELAY)
            else:
                print(f"Could not find day element: {dob.day}")
                return None
        else:
            print("Date of Birth field not found or not clickable.")
            return None

        # Country - This often requires interacting with a dropdown or search input.
        # The XPath provided in the image is for a general div, which might not be correct.
        # We'll attempt to click and then find 'Denmark'.
        country_container = browser.wait_for_clickable(driver, By.XPATH, "//div[contains(@class, 'css-1hwfws3')]") # Guessing based on common select elements
        if country_container:
            country_container.click()
            time.sleep(config.ACTION_DELAY)
            # This XPath is specific and might break easily. Inspect the actual element.
            denmark_option_xpath = "//div[contains(@id, 'react-select') and contains(text(), 'Denmark')]"
            denmark_option = browser.wait_for_clickable(driver, By.XPATH, denmark_option_xpath)
            if denmark_option:
                denmark_option.click()
                print("Selected country: Denmark")
                time.sleep(config.ACTION_DELAY)
            else:
                print("Could not find 'Denmark' option in country selector.")
                # Attempt to send keys if it's a searchable input (less likely given screenshot)
                try:
                    country_input_search = driver.find_element(By.XPATH, "//input[starts-with(@id, 'react-select') and @type='text']")
                    country_input_search.send_keys("Denmark")
                    time.sleep(config.ACTION_DELAY/2)
                    country_input_search.send_keys(Keys.ENTER)
                    print("Attempted to search for Denmark.")
                    time.sleep(config.ACTION_DELAY)
                except:
                    print("Denmark option not found and search input not available.")
                    return None
        else:
            print("Country selection element not found.")
            return None

        # Affiliate Code (should be pre-filled if coming from a referral link)
        # If it needs to be manually entered:
        # affiliate_input = browser.wait_for_element(driver, By.XPATH, "//input[@name='affiliateCode']")
        # if affiliate_input and affiliate_input.get_attribute("value") != config.TARGET_AFFILIATE_CODE:
        #     affiliate_input.clear()
        #     affiliate_input.send_keys(config.TARGET_AFFILIATE_CODE)
        #     print(f"Entered affiliate code: {config.TARGET_AFFILIATE_CODE}")
        #     time.sleep(config.ACTION_DELAY)

        # Confirm Age Checkbox
        age_checkbox = browser.wait_for_clickable(driver, By.XPATH, "//input[@type='checkbox']")
        if age_checkbox:
            # Ensure it's checked. Sometimes it might be pre-checked or need clicking.
            if not age_checkbox.is_selected():
                age_checkbox.click()
                print("Checked 'I confirm that I am at least 18 years old'")
                time.sleep(config.ACTION_DELAY/2)
        else:
            print("Age confirmation checkbox not found.")
            return None

        # Complete Registration Button
        complete_button = browser.wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Complete Registration')]")
        if complete_button:
            complete_button.click()
            print("Clicked 'Complete Registration'")
            time.sleep(config.ACTION_DELAY + 5) # Give more time for the next step to load
        else:
            print("Complete Registration button not found.")
            return None

        # --- Claim Free $1.00 ---
        # This button appears after the initial registration.
        try:
            claim_button = browser.wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Claim Free $1.00')]")
            if claim_button:
                claim_button.click()
                print("Clicked 'Claim Free $1.00'")
                time.sleep(config.ACTION_DELAY + 3) # Wait for confirmation
            else:
                print("Could not find 'Claim Free $1.00' button. It might not be present or already claimed.")
        except Exception as e:
            print(f"Error clicking 'Claim Free $1.00': {e}. It might not be present.")

        # --- Collect and Return Details ---
        # In a real scenario, you'd need to fetch the verification link from the temp email.
        # For now, we'll return placeholder.
        verification_link = "N/A (Requires temp email integration)"
        print(f"Registration successful for: Email: {email}, Password: {password}")

        return {
            "email": email,
            "password": password,
            "verification_link": verification_link
        }

    except Exception as e:
        print(f"An error occurred during registration process: {e}")
        # Take a screenshot for debugging on Replit
        try:
            driver.save_screenshot("registration_error.png")
            print("Screenshot 'registration_error.png' saved for debugging.")
        except:
            print("Could not save screenshot.")
        return None
