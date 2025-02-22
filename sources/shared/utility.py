import os
import sys

def get_resource_path(relative_path: str) -> str:
    if getattr(sys, 'frozen', False):  # PyInstaller 실행 파일인 경우
        base_path = sys._MEIPASS
    else:  # 개발 환경
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..", "resources"))
    
    return os.path.join(base_path, relative_path)