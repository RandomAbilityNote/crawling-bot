from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from model import Ablity


class Crawler:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")  # 브라우저 창 없이 실행

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)  # 최대 10초까지 대기
    
    def get_crawling_data(self, url: str) -> [Ablity]:
        print(f"🔍 크롤링 시작: {url}")
        self.driver.get(url)
        result: [Ablity] = []
        try:
            # 1️⃣ iframe이 로드될 때까지 대기
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))

            # 2️⃣ iframe 요소 가져오기
            iframe = self.driver.find_element(By.TAG_NAME, "iframe")

            # 3️⃣ iframe 내부로 전환
            self.driver.switch_to.frame(iframe)

            # 4️⃣ iframe 내 HTML 파싱
            # soup = BeautifulSoup(self.driver.page_source, "html.parser")
            rows = self.driver.find_elements(By.CLASS_NAME, "se-tr")
            rows.pop(0)

            print(f"📌 현재 URL: {self.driver.current_url}")
            print(f"📌 페이지 제목: {self.driver.title}")

            if rows:
                print("✅ 테이블 데이터 발견!")
                for row in rows:
                    columns = list(map(lambda r: r.text, row.find_elements(By.TAG_NAME, "td")))
                    result.append(Ablity(columns[1], columns[2], columns[0]))
            else:
                print("⚠️ 테이블 데이터가 없습니다!")

        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        finally:
            self.driver.quit()
        
        return result
        

    
   