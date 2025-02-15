import os
from dotenv import load_dotenv, find_dotenv

def init_env():
      load_dotenv(find_dotenv(filename="resources/.env"))

init_env()

spreadsheet_url = os.getenv("SHEET_URL")
prev_version = os.getenv("PREV_VERSION")
lastest_version = os.getenv("LASTEST_VERSION")
