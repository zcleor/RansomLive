import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

API_URL = "https://api-pro.ransomware.live/victims/recent?order=discovered"
API_KEY = os.getenv("API_KEY")

# Webland Email Settings
EMAIL_SENDER = os.getenv("EMAIL_SCRIPT")
EMAIL_PASSWORD = os.getenv("PW_SCRIPT")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("EMAIL_SERVER")
SMTP_PORT = 465  # SSL

def check_api():
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }

    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()

    swiss_victims = [
        v for v in data.get("victims", [])
        if v.get("country") in ["CH", "CHE", "US", "USA"]
    ]

    if not swiss_victims:
        print("No Swiss victims found.")
        return

    # Format email content
    body = "Swiss Victims Found:\n\n"
    for victim in swiss_victims:
        for key, value in victim.items():
            body += f"{key}: {value}\n"
        body += "\n" + "-"*40 + "\n"

    # Build email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "⚠️ Swiss Ransomware Victim Detected"

    msg.attach(MIMEText(body, "plain"))

    # Send email via Webland SMTP
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

    print("Email sent.")

if __name__ == "__main__":
    check_api()
