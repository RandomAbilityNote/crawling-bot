import tkinter as tk
from tkinter import ttk, messagebox
# import pyperclip

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("이미지 업로더 툴")
        self.root.geometry("900x600")

        # 메인 프레임 (왼쪽: 테이블, 오른쪽: 버튼)
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 왼쪽: 테이블 (Treeview)
        table_frame = tk.Frame(main_frame)
        table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("name", "description", "tribes", "tip", "category", "image", "new")  # 마지막 열은 체크박스
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # 각 열 제목 추가
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # 마지막 열(체크박스) 크기 조정
        self.tree.column("new", width=50, anchor="center")

        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # 테이블 배치
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 더미 데이터 추가
        sample_data = [("홍길동", 25, "개발자"), ("김철수", 30, "디자이너"), ("이영희", 28, "기획자")]
        for name, age, job in sample_data:
            self.tree.insert("", tk.END, values=(name, age, job, False))

        # 오른쪽: 버튼 UI
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # 이미지 가져오기 버튼
        self.btn_get_image = tk.Button(button_frame, text="이미지 가져오기", command=self.get_image)
        self.btn_get_image.pack(fill=tk.X, pady=5)

        # URL 표시 텍스트 필드 (읽기 전용)
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(button_frame, textvariable=self.url_var, state="readonly", width=30)
        self.url_entry.pack(fill=tk.X, pady=5)

        # URL 변환 버튼
        self.btn_upload = tk.Button(button_frame, text="이미지를 URL로 변환", command=self.upload_image)
        self.btn_upload.pack(fill=tk.X, pady=5)

        # 저장 버튼
        self.btn_save = tk.Button(button_frame, text="저장", command=self.save_data)
        self.btn_save.pack(fill=tk.X, pady=5)

    def get_image(self):
        print("이미지 가져오기 클릭됨!")

    def upload_image(self):
        # URL 변환 기능 (더미 데이터)
        url = "https://example.com/image.jpg"
        self.url_var.set(url)

        # URL 클립보드 복사
        # pyperclip.copy(url)

        # 토스트 메시지 (UX 방해 없이 자동 사라짐)
        self.show_toast("URL이 클립보드에 복사되었습니다!")

    def save_data(self):
        print("저장 버튼 클릭됨!")

    def show_toast(self, message):
        """토스트 메시지 창 띄우기"""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)  # 창의 제목 표시줄 제거
        toast.geometry(f"+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")  # 부모 창 기준 위치 조정
        label = tk.Label(toast, text=message, bg="black", fg="white", padx=10, pady=5)
        label.pack()
        
        # 일정 시간 후 자동 제거
        toast.after(2000, toast.destroy)

# 앱 실행
root = tk.Tk()
app = App(root)
root.mainloop()