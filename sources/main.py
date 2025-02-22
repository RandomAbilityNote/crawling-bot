from gui import App
import tkinter as tk
from tkinter import ttk, messagebox
from firebase_admin import credentials
import os
import json
import google.auth
from shared import *
import google.auth.transport.requests as gat
from google.oauth2 import service_account
from network import *

# 🔥 서비스 계정 JSON 파일 경로 (직접 다운로드한 파일로 변경)
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "..", "resources", "service-account.json")

# Firebase Remote Config API의 OAuth 범위
SCOPES = ["https://www.googleapis.com/auth/firebase.remoteconfig"]

# 🔥 Access Token 가져오는 함수
def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    
    credentials.refresh(gat.Request())  # ✅ 올바른 사용 방법
    
    return credentials.token

# 🔥 Remote Config 데이터 가져오는 함수
def get_remote_config():
    access_token = get_access_token()
    url = f"https://firebaseremoteconfig.googleapis.com/v1/projects/{project_id}/remoteConfig"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    request = (
        RequestBulder()
        .url(url)
        .method(Method.get)
        .headers(headers)
        .build()
    )

    session = Session()
    prepped = request.prepare()
    response = session.send(prepped)

    if response.status_code == 200:
        print("✅ Remote Config 데이터:")
        print(json.dumps(response.json(), indent=4))  # JSON 데이터 출력
    else:
        print("❌ 요청 실패:", response.text)

if __name__ == "__main__":
    get_remote_config()
