from gspread import service_account, WorksheetNotFound, Worksheet
from shared import *
from crawler import Crawler
from model import *

json_file_path = os.path.join(os.path.dirname(__file__),".." ,"resources", "key.json")
gc = service_account(json_file_path)
doc = gc.open_by_url(spreadsheet_url)

crawler = Crawler()
crawling_data = crawler.get_crawling_data("https://blog.naver.com/jhwon_00/222569309782")
crawling_data.pop(0)

header = ["name", "description", "tribes", "tip", "category", "imgae"]

def update(prev_sheet: Worksheet, sheet: Worksheet):
    records = prev_sheet.get_all_records()
    records_dict = {}

    for record in records:
        records_dict[record["name"]] = record

    new_list: [Ability] = []

    for data in crawling_data:
        if records_dict[data.name]:
            prev = records_dict[data.name]
            tip, category, image = (prev["tip"], prev["category"], prev["image"])
            new_element = Ability(data.name, data.desc, data.tribes, tip, category, image)
            new_list.append(new_element)
        else:
            new_list.append(Ability(data.name, data.desc, data.tribes))

    sheet.update(range_name=f"A1:F1", values= [header])
    sheet.update(range_name=f"A2:F{2+len(crawling_data)-1}", values= [[ability.name, ability.desc, ability.tribes, ability.tip, ability.category, ability.image] for ability in new_list])

try:
    prev_sheet = doc.worksheet(prev_version)
    new_sheet = doc.worksheet(lastest_version)
    update(prev_sheet, new_sheet)
    print("✅ 업데이트 종료")
except WorksheetNotFound as e :
    doc.add_worksheet(title=lastest_version, rows= len(crawling_data)+1, cols=len(header))
    print(f"🎉 {lastest_version} 시트 생성")
    prev_sheet = doc.worksheet(prev_version)
    new_sheet = doc.worksheet(lastest_version)
    update(prev_sheet, new_sheet)
    print("✅ 업데이트 종료")

except Exception as e:
    print(f"Error: {e}")