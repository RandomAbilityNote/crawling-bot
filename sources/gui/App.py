import tkinter as tk
from tkinter import ttk, messagebox
from crawler import Crawler
from gspread import service_account
from shared import *
from model import *
from operator import attrgetter
import threading

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

        btn_load_data = tk.Button(button_frame, text="최신 데이터 가져오기", command=self.start_loading)
        btn_load_data.pack(fill=tk.X, pady=5)

        btn_get_image = tk.Button(button_frame, text="이미지 가져오기", command=self.get_image)
        btn_get_image.pack(fill=tk.X, pady=5)

        btn_upload = tk.Button(button_frame, text="이미지를 URL로 변환", command=self.upload_image)
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

    def get_image(self):
        print("이미지 가져오기 클릭됨!")

    def upload_image(self):
        url = "https://example.com/image.jpg"
        self.show_toast("URL이 클립보드에 복사되었습니다!")

    def save_data(self):
        print("저장 버튼 클릭됨!")

    def show_toast(self, message):
        """토스트 메시지"""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.geometry(f"+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")
        label = tk.Label(toast, text=message, bg="black", fg="white", padx=10, pady=5)
        label.pack()
        toast.after(2000, toast.destroy)