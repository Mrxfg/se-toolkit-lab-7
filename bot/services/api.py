import requests
from config import LMS_API_URL, LMS_API_KEY

headers = {
    "Authorization": f"Bearer {LMS_API_KEY}"
}

def get_items():
    try:
        res = requests.get(f"{LMS_API_URL}/items/", headers=headers)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return str(e)

def get_scores(lab):
    try:
        res = requests.get(f"{LMS_API_URL}/analytics/pass-rates?lab={lab}", headers=headers)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return str(e)
