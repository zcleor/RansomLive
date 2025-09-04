import os
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

API_URL = "https://api-pro.ransomware.live/victims/recent?order=discovered"
API_KEY = os.getenv("API_KEY")
FILENAME = "api_results.json"

EMAIL_SENDER = os.getenv("EMAIL_SCRIPT")
EMAIL_PASSWORD = os.getenv("PW_SCRIPT")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("EMAIL_SERVER")
SMTP_PORT = 465  # SSL


def send_email(new_victims):
    """Send email with info about new victims"""
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
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("📧 Email mit neuen Einträgen verschickt.")
    except Exception as e:
        print(f"❌ Fehler beim Emailversand: {e}")


def fetch_data():
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY,
    }

    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()

    new_victims = data.get("victims", [])

    # Alte Daten laden
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            existing_victims = existing_data.get("victims", [])
    else:
        existing_data = {"victims": []}
        existing_victims = []

    existing_ids = {v.get("id") for v in existing_victims}

    # Neue Opfer herausfiltern
    unique_new_victims = [v for v in new_victims if v.get("id") not in existing_ids]

    if unique_new_victims:
        print(f"✅ {len(unique_new_victims)} neue Einträge gefunden")
        all_victims = existing_victims + unique_new_victims
        updated_data = {"victims": all_victims}

        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, indent=2, ensure_ascii=False)

        # Email nur senden, wenn neue Opfer gefunden wurden
        send_email(unique_new_victims)
    else:
        print("ℹ️ Keine neuen Einträge gefunden.")


if __name__ == "__main__":
    fetch_data()
