import os
import sys

def get_resource_path(relative_path: str) -> str:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..", "resources"))
    
    if getattr(sys, 'frozen', False):  # PyInstaller 실행 파일인 경우
        base_path = os.path.join(sys._MEIPASS, "resources")

    return os.path.join(base_path, relative_path)