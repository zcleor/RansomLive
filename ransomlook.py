import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

API_URL = "https://api-pro.ransomware.live/victims/recent?order=discovered"
API_KEY = os.getenv("API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

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
        if v.get("country") in ["CH", "CHE"]
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

    # Send email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = "⚠️ Swiss Ransomware Victim Detected"

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())

    print("Email sent.")

if __name__ == "__main__":
    check_api()
