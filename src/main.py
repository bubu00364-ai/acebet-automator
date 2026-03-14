import time
import config
import browser
import email_utils
import registration

def main():
    print("Starting Acebet Account Registration Script...")

    # Attempt to get sensitive info from environment variables (Replit Secrets)
    if not all([config.EMAIL_SENDER_ADDRESS, config.EMAIL_SENDER_PASSWORD, config.NOTIFICATION_EMAIL, config.TARGET_AFFILIATE_CODE]):
        print("\n--- WARNING ---")
        print("Sensitive email or affiliate code details are not configured.")
        print("Please set them using Replit Secrets:")
        print(" - EMAIL_SENDER_ADDRESS")
        print(" - EMAIL_SENDER_PASSWORD")
        print(" - NOTIFICATION_EMAIL")
        print(" - TARGET_AFFILIATE_CODE")
        print("The script may fail or send emails to default/placeholder addresses.")
        print("---------------\n")
        time.sleep(5) # Give user time to read

    successful_registrations = []
    failed_registrations = 0

    for i in range(config.NUM_ACCOUNTS_TO_CREATE):
        print(f"\n--- Attempting registration {i + 1}/{config.NUM_ACCOUNTS_TO_CREATE} ---")

        # Simulate IP rotation (conceptual on Replit)
        if i > 0: # No need to rotate before the first attempt
            browser.rotate_ip_address()

        driver = browser.setup_driver()
        if not driver:
            print("Failed to initialize WebDriver. Exiting.")
            break

        account_details = None
        try:
            account_details = registration.register_account(driver)
        except Exception as e:
            print(f"An unexpected error occurred in register_account: {e}")
        finally:
            if driver:
                driver.quit() # Close the browser after each attempt

        if account_details:
            successful_registrations.append(account_details)
            print(f"Successfully registered account {i + 1}: {account_details['email']}")

            # Send notification email
            subject = f"Acebet Account Registered - {account_details['email']}"
            body = (
                f"Email: {account_details['email']}\n"
                f"Password: {account_details['password']}\n"
                f"Affiliate Code Used: {config.TARGET_AFFILIATE_CODE}\n"
                f"Date of Birth: {account_details['dob'].strftime('%Y-%m-%d') if 'dob' in account_details else 'N/A'}\n" # Note: dob is not returned from register_account currently, needs modification if desired
                f"Verification Link: {account_details['verification_link']}\n\n"
                f"Note: Date of Birth and Verification Link are placeholders or may not be available without further integration."
            )
            email_utils.send_email_with_details(subject, body)
        else:
            failed_registrations += 1
            print(f"Failed to register account {i + 1}.")

        # Delay between registration attempts to avoid overwhelming the server
        print(f"Waiting for {config.REGISTRATION_DELAY} seconds before next attempt...")
        time.sleep(config.REGISTRATION_DELAY)

    print("\n--- Registration Process Complete ---")
    print(f"Successfully registered: {len(successful_registrations)} accounts.")
    print(f"Failed registrations: {failed_registrations} accounts.")

    if successful_registrations:
        print("\nSummary of registered accounts:")
        for acc in successful_registrations:
            print(f"- Email: {acc['email']}, Password: {acc['password']}")
    else:
        print("No accounts were successfully registered.")

if __name__ == "__main__":
    main()
