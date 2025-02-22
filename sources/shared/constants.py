import os
from dotenv import load_dotenv
from .utility import get_resource_path

def init_env():
      print(f"isExisted: {os.path.exists(get_resource_path(".env"))} ")
      print(f"isExisted: {os.path.exists(get_resource_path("key.json"))} ")
      print(f"isExisted: {os.path.exists(get_resource_path("service-account.json"))} ")
      load_dotenv(dotenv_path = get_resource_path(".env"))

init_env()

spreadsheet_url = os.getenv("SHEET_URL")
prev_version = os.getenv("PREV_VERSION")
lastest_version = os.getenv("LASTEST_VERSION")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
project_id = os.getenv("PROJECT_ID")
tool_version = os.getenv("TOOL_VERSION")

