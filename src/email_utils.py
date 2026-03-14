import smtplib
from email.mime.text import MIMEText
import config

def send_email_with_details(subject, body):
    """Sends an email with registration details."""
    if not all([config.EMAIL_SENDER_ADDRESS, config.EMAIL_SENDER_PASSWORD, config.NOTIFICATION_EMAIL]):
        print("Email sender details not configured. Skipping email notification.")
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config.EMAIL_SENDER_ADDRESS
    msg['To'] = config.NOTIFICATION_EMAIL

    try:
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(config.EMAIL_SENDER_ADDRESS, config.EMAIL_SENDER_PASSWORD)
            server.sendmail(config.EMAIL_SENDER_ADDRESS, config.NOTIFICATION_EMAIL, msg.as_string())
        print(f"Registration details sent to {config.NOTIFICATION_EMAIL}")
    except Exception as e:
        print(f"Failed to send email: {e}")
