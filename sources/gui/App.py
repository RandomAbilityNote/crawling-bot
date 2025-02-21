import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from crawler import Crawler
from gspread import service_account
from shared import *
from model import *
from operator import attrgetter
from cloudinary import uploader
import concurrent.futures
import threading
import pyperclip

class App:
    def __init__(self, root):
        self._crawler = Crawler()
        self.root = root
        json_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "key.json")
        gc = service_account(json_file_path)
        self._doc = gc.open_by_url(spreadsheet_url)
        self._columns = ["name", "description", "tribes", "tip", "category", "image", "new"]
        self._dataSource = []
        self._getter = attrgetter(*self._columns)
        self.setup_ui()
        self._progress = 0
        self._image_files: list = []
        self._uploaded_image_urls: list = []
        self._lock = threading.Lock()  # 스레드 안전성을 위한 Lock

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, new_value):
        self._progress = new_value
        self._progressbar["value"] = new_value
        self.root.update_idletasks()  # UI 즉시 업데이트

    def setup_ui(self):
        width = self.root.winfo_screenwidth()
        height = 600
        self.root.title("이미지 업로더 툴")
        self.root.geometry(f"{width}x{height}")

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        table_frame = tk.Frame(main_frame)
        table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
       
        self.tree = ttk.Treeview(table_frame, columns=self._columns, show="headings")
        for col in self._columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

                # URL 표시 텍스트 필드 (읽기 전용)
        self._url_text = tk.Text(button_frame, height=1, width=30)
        self._url_text.pack(fill=tk.BOTH, pady=5, expand=True, side=tk.TOP)
        self._url_text.config(state=tk.DISABLED)

        btn_load_data = tk.Button(button_frame, text="최신 데이터 가져오기", command=self.start_loading)
        btn_load_data.pack(fill=tk.X, pady=5)

        btn_get_image = tk.Button(button_frame, text="이미지 가져오기", command=self.get_image)
        btn_get_image.pack(fill=tk.X, pady=5)

        btn_upload = tk.Button(button_frame, text="이미지를 URL로 변환", command=self.upload_images_concurrently)
        btn_upload.pack(fill=tk.X, pady=5)

        btn_save = tk.Button(button_frame, text="저장", command=self.save_data)
        btn_save.pack(fill=tk.X, pady=5)

        self._progressbar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self._progressbar.pack(pady=20)

    def start_loading(self):
        """스레드를 사용하여 데이터 로드 시작"""
        self.progress = 0
        thread = threading.Thread(target=self.load_sheet_data, daemon=True)
        thread.start()

    def load_sheet_data(self):
        """이전 데이터를 가져오는 함수 (Thread 사용)"""
        self.progress = 20
        self._dataSource = []
        self.tree.delete(*self.tree.get_children())

        url = "https://blog.naver.com/jhwon_00/222569309782"
        crawling_data = self._crawler.get_crawling_data(url)
        crawling_data.pop(0)

        try:
            prev_sheet = self._doc.worksheet(prev_version)
            records = prev_sheet.get_all_records()
            records_dict = {record["name"]: record for record in records}

            for i, data in enumerate(crawling_data):
                if data.name in records_dict:
                    prev = records_dict[data.name]
                    new_element = Ability(
                        data.name, data.desc, data.tribes,
                        prev["tip"], prev["category"], prev["image"]
                    )
                    self._dataSource.append(new_element)
                else:
                    self._dataSource.append(Ability(data.name, data.desc, data.tribes))

                self.progress = (i + 1) / len(crawling_data) * 100
        except Exception as e:
            print(f"Error: {e}")

        self.progress = 100
        self.update_tree_view()

    def update_tree_view(self):
        """UI 업데이트는 메인 스레드에서 실행"""
        self.tree.after(0, self._insert_tree_data)
        self._progressbar.stop()


    def _insert_tree_data(self):
        for data in self._dataSource:
            self.tree.insert("", tk.END, values=self._getter(data))

    def update_white_board(self, content):
        self._url_text.config(state=tk.NORMAL)
        self._url_text.delete(1.0, tk.END)
        self._url_text.insert(tk.END, content)
        self._url_text.config(state=tk.DISABLED)  # 다시 읽기 전용으로 설정

    def get_image(self):
        self._image_files = filedialog.askopenfilenames(title="이미지 가져오기", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        self.update_white_board("\n\n\n".join(self._image_files))

    def upload_image(self,image_path):
        print(f"image_path: {image_path}")
        try:
            result = uploader.upload(image_path)
            image_url = result.get("secure_url")

            if image_url:
                with self._lock:
                    self._uploaded_image_urls.append(image_url)
                print(f"✅ 업로드 성공: {image_url}")
            else:
                print(f"❌ 업로드 실패: {image_path}")

        except Exception as e:
            print(f"❌ 업로드 오류: {image_path}, 오류: {e}")

    def upload_images_concurrently(self):
        if not self._image_files:
            print("❌ 비어있습니다")
            return 
        
        self._uploaded_image_urls = ["1234","5678"]
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as worker:
            # future_to_image = {worker.submit(self.upload_image, img): img for img in self._image_files}
            
            # for i, future in enumerate(concurrent.futures.as_completed(future_to_image)):
            #     try:
            #         future.result()  # 오류 발생 시 예외 처리
            #     except Exception as e:
            #         self.progress = 0
            #         print(f"❌ Error Occured: {e}")
            #         self._progressbar.stop()
            #         self._uploaded_image_urls.clear()

            if self._uploaded_image_urls:
                self.update_white_board("\n\n\n".join(self._uploaded_image_urls))
                self.copy(",".join(self._uploaded_image_urls))
                print(f"🎉 모든 업로드 완료!")

    def copy(self, content):
        pyperclip.copy(content)        
        self.show_toast("URL이 클립보드에 복사되었습니다!")

    def save_data(self):
        print("저장 버튼 클릭됨!")

    def show_toast(self, message):
        """토스트 메시지"""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)  # 기본 윈도우 장식 없애기
        screen_width = self.root.winfo_screenwidth()  # 화면 너비
        toast_width = 200  # 토스트 메시지의 너비
        toast_height = 30  # 토스트 메시지의 높이

        # 중앙 위쪽에 배치
        x_pos = (screen_width - toast_width) // 2
        y_pos = 10  # 화면의 상단 10px 위치에 배치
        toast.geometry(f"{toast_width}x{toast_height}+{x_pos}+{y_pos}")

        label = tk.Label(toast, text=message, bg="black", fg="white", padx=10, pady=5)
        label.pack()
        toast.after(2000, toast.destroy)  # 2초 후에 토스트 메시지 닫기