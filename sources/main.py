from gui import App
import tkinter as tk
from tkinter import messagebox
from firebase_admin import credentials
import os
from shared import *
import google.auth.transport.requests as gat
from google.oauth2 import service_account
from network import *

# 🔥 서비스 계정 JSON 파일 경로 (직접 다운로드한 파일로 변경)
SERVICE_ACCOUNT_FILE = get_resource_path("service-account.json")

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
def get_remote_version() -> str :
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
        data = response.json()
        return data["parameters"]["python_tool_version"]["defaultValue"]["value"].strip('"')
    else:
        MAX = "10000.10000.10000"
        print("❌ 요청 실패:", response.text)
        return MAX
    
def compare_version(local: str, remote: str) -> bool :
    def convert(versions: str) -> int:
        version_list =  list(map(int, versions.split(".")))
        version_value = 0 
        for i, number in enumerate(version_list):
            version_value += pow(10, 2-i) * number
    
        return version_value
    
    return convert(local) == convert(remote)

if __name__ == "__main__":
    root = tk.Tk()
    print(tool_version)
    remote_version = get_remote_version()
 
    if compare_version(tool_version, remote_version):
        app = App(root)
        root.mainloop()
    else:
        # 🔥 시스템 경고 메시지 띄우기
        messagebox.showerror("업데이트 필요", "다음 버전을 설치해주세요.")
        # 🔥 프로그램 강제 종료
        os._exit(1)
       

