import os
import requests
import json
from datetime import datetime

API_URL = "https://api-pro.ransomware.live/victims/recent?order=discovered"
API_KEY = os.getenv("API_KEY")

def fetch_data():
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }

    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Create filename with timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"api_result_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved API result to {filename}")
    return filename

if __name__ == "__main__":
    fetch_data()
