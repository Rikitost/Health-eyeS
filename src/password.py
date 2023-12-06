# tkinterのimport
import tkinter as tk
# 間違えたときのメッセージボックス
from tkinter import messagebox
# 解除パスワード入力の表示

# ボタンを押したときの判定


def setpassbutton_push():
    # パスワードの判定
    if int(pass_text.get()) > 0:
        # フォームを閉じる
        pass_form.destroy()
    else:
        return


# フォームの生成
def pass_task():
    # グローバル変数で宣言
    global pass_form
    global pass_text
    # 時間入力のform
    pass_form = tk.Tk()

    # ウィンドウのサイズ
    pass_form.geometry('250x200')
    # ウィンドウの大きさ固定
    pass_form.resizable(width=False, height=False)

    # 画面のタイトル
    pass_form.title('時間を設定')

    # フォームのラベル
    pass_label = tk.Label(text='時間を入力してください(分)')
    pass_label.place(x=30, y=50)

    # 入力のテキストボックス
    pass_text = tk.Entry(width=30)
    pass_text.place(x=30, y=70)

    # 入力決定のボタン
    timeset_button = tk.Button(
        pass_form,
        text='設定',
        command=setpassbutton_push
    ).place(x=100, y=150)

    # フォームのループ
    pass_form.mainloop()
