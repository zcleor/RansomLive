import os
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -------------------- Config --------------------
API_URL = "https://api-pro.ransomware.live/victims/recent?order=discovered"
API_KEY = os.getenv("API_KEY")
FILENAME = "api_results.json"

EMAIL_SENDER = os.getenv("EMAIL_SCRIPT")
EMAIL_PASSWORD = os.getenv("PW_SCRIPT")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("EMAIL_SERVER")
SMTP_PORT = 465  # SSL

ALLOWED_COUNTRIES = {"CH", "CHE"}  # Länder-Filter

# -------------------- Email Funktion --------------------
def send_email(new_victims):
    subject = f"⚠️ {len(new_victims)} neue Ransomware-Einträge entdeckt"
    body = "Neue Opfer wurden entdeckt:\n\n"

    for victim in new_victims:
        for key, value in victim.items():
            body += f"{key}: {value}\n"
        body += "\n" + "-" * 40 + "\n"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)  # ✅ sicherer als sendmail
        print("📧 Email mit neuen Einträgen verschickt.")
    except Exception as e:
        print(f"❌ Fehler beim Emailversand: {e}")

# -------------------- API Fetch Funktion --------------------
def fetch_data():
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY,
    }

    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Filter nur auf erlaubte Länder
    all_victims = [
        v for v in data.get("victims", [])
        if v.get("country") in ALLOWED_COUNTRIES
    ]

    # Alte Daten laden (robust gegen leere/kaputte Datei)
    existing_victims = []
    if os.path.exists(FILEN
