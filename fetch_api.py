import os
import requests
import json

API_URL = "https://api-pro.ransomware.live/victims/recent?order=discovered"
API_KEY = os.getenv("API_KEY")
FILENAME = "api_results.json"   # immer gleiche Datei

def fetch_data():
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }

    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()

    new_victims = data.get("victims", [])

    # Alte Daten laden, falls Datei existiert
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            existing_victims = existing_data.get("victims", [])
    else:
        existing_data = {"victims": []}
        existing_victims = []

    # IDs der bereits bekannten Opfer
    existing_ids = {v.get("id") for v in existing_victims}

    # Nur neue Opfer herausfiltern
    unique_new_victims = [v for v in new_victims if v.get("id") not in existing_ids]

    if unique_new_victims:
        print(f"✅ {len(unique_new_victims)} neue Einträge gefunden")
        all_victims = existing_victims + unique_new_victims
        updated_data = {"victims": all_victims}

        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, indent=2, ensure_ascii=False)
    else:
        print("ℹ️ Keine neuen Einträge gefunden.")

if __name__ == "__main__":
    fetch_data()
