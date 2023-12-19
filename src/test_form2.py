# form2.py
import tkinter as tk


class Form2(tk.Toplevel):
    def __init__(self, master, value_from_form1):
        super().__init__(master)
        self.title("Form 2")

        # ラベルで値を表示
        self.label = tk.Label(
            self, text=f"Value from Form 1: {value_from_form1}")
        self.label.pack(pady=10)

    def show(self):
        self.grab_set()  # フォーム2が閉じるまで他のウィンドウとのやりとりを制限
        self.wait_window()
