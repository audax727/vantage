import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv(override=True)

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")

print(f"Sending from: {EMAIL_ADDRESS}")
print(f"Password loaded: {'YES' if EMAIL_APP_PASSWORD else 'NO'}")

try:
    msg = MIMEText("This is a test email from Vantage to confirm your email reminders are working!", 'plain', 'utf-8')
    msg["Subject"] = "✅ Vantage Email Test — It Works!"
    msg["From"] = f"Vantage <{EMAIL_ADDRESS}>"
    msg["To"] = EMAIL_ADDRESS

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, [EMAIL_ADDRESS], msg.as_string())

    print("SUCCESS: Test email sent! Check your inbox at", EMAIL_ADDRESS)
except Exception as e:
    print(f"FAILED: {e}")
