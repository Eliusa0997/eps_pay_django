import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

SERVICE_ACCOUNT_FILE = "serviceAccountKey.json"

PROJECT_ID = "epspay-bcd1f"

SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

def send_fcm_notification(token, title, body):
    credentials.refresh(Request())
    access_token = credentials.token

    url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body,
            }
        }
    }

    response = requests.post(url, json=data, headers=headers)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    return response.json()