import os
import datetime

# --- Target Website ---
TARGET_URL = "https://acebet.co/welcome/r/bubu" # Example based on your link

# --- Registration Settings ---
NUM_ACCOUNTS_TO_CREATE = 5 # Start small for testing
COUNTRY = "Denmark" # As seen in the image

# --- Email Settings (use Replit Secrets) ---
NOTIFICATION_EMAIL = os.environ.get("NOTIFICATION_EMAIL", "your_default_notification_email@example.com")
EMAIL_SENDER_ADDRESS = os.environ.get("EMAIL_SENDER_ADDRESS", "your_default_sender_email@example.com")
EMAIL_SENDER_PASSWORD = os.environ.get("EMAIL_SENDER_PASSWORD", "your_default_password")
SMTP_SERVER = "smtp.gmail.com" # Example for Gmail
SMTP_PORT = 587

# --- Affiliate Code (use Replit Secrets) ---
TARGET_AFFILIATE_CODE = os.environ.get("TARGET_AFFILIATE_CODE", "BUBU")

# --- Random Data Generation Settings ---
PASSWORD_LENGTH = 12
MIN_BIRTH_YEAR = 1999
MAX_BIRTH_YEAR = 2005

# --- Delays ---
# Be respectful of the website's servers. Add delays between actions.
ACTION_DELAY = 2 # Seconds between clicks, typing, etc.
REGISTRATION_DELAY = 15 # Seconds between each full registration attempt
IP_ROTATION_DELAY = 30 # Seconds to wait after simulated IP rotation
