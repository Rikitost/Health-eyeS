# form1.py
import tkinter as tk
import threading
import time
# ファイルとformの名前
from test2 import MosaicForm


class Form1(tk.Tk):
    def __init__(self):
        super().__init__()
        # ウィンドウのサイズ
        self.time_form.geometry('250x200')
        # ウィンドウの大きさ固定
        self.time_form.resizable(width=False, height=False)

        # 画面のタイトル
        self.time_form.title('時間を設定')

        # ×で閉じられないようにする
        self.time_form.protocol("WM_DELETE_WINDOW", click_close)

        # フォームの制限時間入力ラベル
        self.timeset_label = tk.Label(text='時間を入力してください(分)')
        self.timeset_label.pack()

        # 入力の制限
        validation_time = self.time_form.register(on_validate_time)
        validation_pass = self.time_form.register(on_validate_pass)

        # 制限時間入力のテキストボックス
        self.timeset_text = tk.Entry(self.time_form, validate="key", validatecommand=(
            validation_time, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.timeset_text.pack()

        # フォームのパスワード設定ラベル
        self.timeset_label = tk.Label(text='パスワードを設定してください(半角数字4桁)')
        self.timeset_label.pack()

        # # パスワード入力のテキストボックス
        self.passset_text = tk.Entry(self.time_form, validate="key", validatecommand=(
            validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.passset_text.pack()

        # 警告ラベル
        self.warning_time_label = tk.Label(text='')
        self.warning_time_label.pack()

        self.warning_pass_label = tk.Label(text='')
        self.warning_pass_label.pack()

        # # 入力決定のボタン
        self.timeset_button = tk.Button(
            self.time_form,
            text='設定',
            command=lambda: settimebutton_push(
                warning_time_label, warning_pass_label)
        ).pack()

        # 時間表示
    # ×で閉じられないようにする関数

    def click_close(self):
        pass

    # 入力内容確認の関数

    def value_check(self, entry_text, warning_label):
        # 数字の判定
        if entry_text.get().isdigit():
            return True
        else:
            warning_label.config(text='数字を入力してください')
            return
        # 桁数の判定
        if len(entry_text.get()) > 4:
            warning_label.config(text='%sは4桁以内で入力してください' % entry_text.get())
            return

    # ボタンを押したときの判定

    def settimebutton_push(self, warning_time_label, warning_pass_label):
        # 数値の入力方式が正しいか判定
        if self.value_check(self.timeset_text, warning_time_label) == True and value_check(passset_text, warning_pass_label) == True:
            # if int(timeset_text.get()) > 0:
            self.glimit.val = int(self.timeset_text.get())
            gpass = int(self.passset_text.get())
            print("timeset:%d" % self.glimit.val)
            print("passset:%d" % gpass)
            # フォームを閉じる
            self.time_form.destroy()

            f = open('password.txt', 'w')
            f.write(str(gpass))
            f.close()
        else:
            return

    # 数値のみ
    def on_validate_time(d, i, P, s, S, v, V, W):
        # Pが数字の場合はTrue、それ以外はFalse
        return (P.isdigit() and len(P) <= 4) or P == ""

    def on_validate_pass(d, i, P, s, S, v, V, W):
        # Pが数字の場合はTrue、それ以外はFalse
        return (P.isdigit() and len(P) <= 4) or P == ""

    def open_form2(self):
        # フォーム1で入力された値を取得
        value_from_form1 = self.entry.get()

        # 新しいトップレベルウィンドウ(Form2)を作成
        form2 = Form2(self, value_from_form1)
        form2.show()


if __name__ == "__main__":
    form1 = Form1()
    form1.mainloop()


# import tkinter as tk


# class TransparentCanvasWithLabel:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Transparent Canvas with Label")
#         self.root.geometry("800x600")

#         # 透明なウィンドウ
#         self.transparent_window = tk.Toplevel(self.root)
#         self.transparent_window.attributes("-alpha", 0.0)
#         self.transparent_window.overrideredirect(True)
#         self.transparent_window.geometry("800x600")

#         # キャンバスを配置
#         self.canvas = tk.Canvas(self.transparent_window, width=800, height=600)
#         self.canvas.pack()

#         # キャンバス上にラベルを表示
#         label_text = "Hello, Transparent Canvas!"
#         label_x, label_y = 400, 300  # ラベルの座標（中央に配置）
#         self.label = self.canvas.create_text(
#             label_x, label_y, text=label_text, font=("Helvetica", 16), fill="white")


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = TransparentCanvasWithLabel(root)
#     root.mainloop()
