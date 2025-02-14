import os
from dotenv import load_dotenv, find_dotenv

def init_env():
      load_dotenv(find_dotenv(filename="resources/.env"))

init_env()

spreadsheet_url = os.getenv("SHEET_URL")
lastest_version = os.getenv("VERSION")
