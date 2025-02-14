import gspread
from shared import *
from crawler import Crawler

crawler = Crawler()

print(lastest_version)
result = crawler.get_crawling_data("https://blog.naver.com/jhwon_00/222569309782")

print(result)

# gc = gspread.service_account(json_file_path)
# doc = gc.open_by_url(spreadsheet_url)

# worksheet = doc.worksheet("메인")
# print(worksheet.row_values(1))
# worksheet.update([["1234"]], "B3")