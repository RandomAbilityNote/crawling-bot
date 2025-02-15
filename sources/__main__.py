from gspread import service_account, WorksheetNotFound, Worksheet
from shared import *
from crawler import Crawler
from model import *

json_file_path = os.path.join(os.path.dirname(__file__),".." ,"resources", "key.json")
gc = service_account(json_file_path)
doc = gc.open_by_url(spreadsheet_url)

crawler = Crawler()
ablities = crawler.get_crawling_data("https://blog.naver.com/jhwon_00/222569309782")
ablities.pop(0)

header = ["name", "description", "tribes", "tip", "category", "imgae"]

def update(prev_sheet: Worksheet, sheet: Worksheet):
    records = prev_sheet.get_all_records()
    records_dict = {}

    for record in records:
        records_dict[record["name"]] = record

    update_values: [Ablity] = []

    for ablity in ablities:
        if records_dict[ablity.name]:
            prev = records_dict[ablity.name]
            tip, category, image = (prev["tip"], prev["category"], prev["image"])
            new = Ablity(ablity.name, ablity.desc, ablity.tribes, tip, category, image)
            update_values.append(new)
        else:
            update_values.append(Ablity(ablity.name, ablity.desc, ablity.tribes))

    sheet.update(range_name=f"A1:F1", values= [header])
    sheet.update(range_name=f"A2:F{2+len(ablities)-1}", values= [[ability.name, ability.desc, ablity.tribes, ability.tip, ability.category, ability.image] for ability in update_values])

try:
    prev_sheet = doc.worksheet("메인")
    new_sheet = doc.worksheet(lastest_version)
    update(prev_sheet, new_sheet)

            
    print("✅ 업데이트 종료")
except WorksheetNotFound as e :
    doc.add_worksheet(title=lastest_version, rows= len(ablities)+1, cols=len(header))
    prev_sheet = doc.worksheet("메인")
    new_sheet = doc.worksheet(lastest_version)
    update(prev_sheet, new_sheet)
    print("✅ 업데이트 종료")

except Exception as e:
    print(f"Error: {e}")