import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from plyer import notification

# ファイルをインポート
import password_input
# グローバル変数
import end_flg_value as gend  # 終了フラグ 0:継続 1:終了(flg)
import pass_sec_value as gpass_sec  # パスワードが解かれたか 0:ロック 1:解除 (flg)
# 時間切れ(0;継続,1:終了)
import time_limit as limit


# 数値のみ入力を受け付ける処理
def on_validate(d, i, P, s, S, v, V, W):
    # Pが数字の場合はTrue、それ以外はFalse
    return (P.isdigit() and len(P) <= 4) or P == ""


# パスワード入力で閉じる
def setting_end():
    # passのフラグ
    global pass_form
    global setting_form
    print("終了")
    # パスワードを再取得
    fp = open('password.txt', 'r')
    f_password = fp.read()
    fp.close()
    # パスワードを設定していないなら
    if f_password == "":
        print("パスワード認証をスキップ")
        # print("パスワードフラグ：%d" % gpass_sec.flg)
        # formの削除
        setting_form.quit()
        # setting_form.destroy()
        gend.flg = 1  # 終了フラグを立てる
        print("設定なしのウインドウを閉じました")
    else:
        # pass入力のformがすでに開かれているかの判定
        if pass_form == 0:
            pass_form = 1
            # パスワード画面を開いた時に設定を操作できなくする
            for widget in setting_form.winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(state=tk.DISABLED)
            # パスワードのformを開く
            password_input.passbox_tk()
        # パスワードが解かれた
            if gpass_sec.flg == 1:
                setting_form.quit()
                # setting_form.destroy()
                gend.flg = 1  # 終了フラグを立てる
                print("設定ありのウインドウを閉じました")
                # gsetting_thread_end.flg = 1
            else:
                print("解除できていないようだ")

# 表示ラベル1秒ごとに更新されていく


def label_update():
    global limit_label
    global nokoritime
    global pass_form
    # 経過時間ラベルの更新
    # 経過時間ラベルの更新
    # limitlablがないときの例外処理
    if nokoritime <= 0:
        h = 0
        m = 0
        s = 0
        # 時間制限で注意画面の表示フラグを立てる
        limit.flg = 1
        # パスワードformの開いているか
        if pass_form == 0:
            # パスワードを入力させて終わる
            setting_end()
        # nokoritime = 0
    else:
        # 残り時間の通知
        if nokoritime == 300:
            # 通知の設定
            title = '時間の通知'
            message = '残り5分です'

            # 通知の表示
            notification.notify(
                title=title,
                message=message,
                app_icon='favicon.ico',  # アイコンのパス
                timeout=10,  # 通知が表示される時間（秒）
            )
        # カウントダウン
        nokoritime -= 1
        # 時間
        h = nokoritime // 3600
        m = (nokoritime % 3600) // 60
        s = nokoritime % 60
        limit_label.configure(text='残り時間:{:02}:{:02}:{:02}'.format(h, m, s))
        # afterで1秒ごとのカウントダウン
        setting_form.after(1000, label_update)


def setting():
    # form,ラベル時間,ファイルに入力された時間,パスワード,残り時間,フォームが複数開かないようするflg
    global setting_form
    global limit_label
    global label_realtime
    global f_limit
    global f_password
    global nokoritime
    global pass_form
    pass_form = 0
    # 注意のラベル
    global label_time_error
    global label_newpassword_error

    # ----------------------------------------------------------------------------------
    # パスワード設定ボタンを押したときの処理
# パスワード

    def pass_dicide_click():
        print("パスワード設定ボタンを押しました")
        # パスワードを取得
        password = password_entry.get()
        print(password)
        # パスワードをpassword.txtに保存
        f = open('password.txt', 'w')
        f.write(str(password))
        f.close()

        label_newpassword_error.configure(
            text="パスワードを設定しました", text_color='blue')
        # パスワード入力後に入力されてたものの削除(テキストボックス)
        password_entry.delete(0, ctk.END)

# 時間

    def limit_dicide_click():
        # 残り時間と現在の設定時間表示ラベルの更新部分
        global nokoritime
        global label_realtime
        global label_time_error
        # 入力した制限時間を取得
        limit = limit_entry.get()
        # 空白なら警告
        if limit == '' or int(limit) == 0:
            label_time_error.configure(text="設定してください", text_color='red')
            return
        else:
            # 分
            limit_minut = int(limit) * 60
            # 秒
            # limit_minut = int(limit)
            # 制限時間をlimit.txtに保存
            f = open('limit.txt', 'w')
            f.write(str(limit_minut))
            f.close()
            # ラベルの更新
            nokoritime = int(limit_minut)
            # 現在設定されている制限時間の更新
            label_realtime.configure(text='現在の制限時間:%d分' %
                                     (int(limit_minut) / 60))
            # メッセージを表示
            label_time_error.configure(text="設定完了", text_color='blue')
            # 時間入力後に入力されてたものの削除(テキストボックス)
            limit_entry.delete(0, ctk.END)
            # messagebox.showinfo('制限時間設定', '制限時間を設定しました')

    # ウインドウの×を押したときの処理（タイマーを止めてからウインドウを閉じる）

    def delete_window():
        # パスワードを入力させて終わる
        setting_end()


# ----------------------------------------------------------------------------------
    f = open('limit.txt', 'r')
    f_limit = int(f.read())
    f.close()

    fp = open('password.txt', 'r')
    f_password = fp.read()
    fp.close()

    nokoritime = int(f_limit)

    # Selecting GUI theme - dark, light , system (for system default)
    ctk.set_appearance_mode("white")

    # Selecting color theme - blue, green, dark-blue
    ctk.set_default_color_theme("blue")

    # メインウィンドウ
    setting_form = ctk.CTk()
    form_x = 400
    form_y = 500
    setting_form.geometry('%dx%d' % (form_x, form_y))
    setting_form.title('設定画面')

    # # スタイルの作成
    # style = ttk.Style()
    # style.configure("Red.TButton", background='red')

    # ×を押したときの処理
    setting_form.protocol("WM_DELETE_WINDOW", lambda: delete_window())
    # フレームの作成
    setting_frame = ctk.CTkFrame(setting_form)
    setting_frame.configure(width=200, height=50)
    setting_frame.grid(row=12, column=0, pady=12, padx=10, sticky="w")
    # タイトル
    # custom_font = ctk.CTkFont(size=20)
    label_title = ctk.CTkLabel(setting_form, text="Health-eyeS", font=("", 20))
    label_title.grid(row=0, column=0, pady=20)
    # 線
    label_line = ctk.CTkLabel(
        setting_form, text='________________________________________________________________')
    label_line.grid(row=0, column=0, pady=12, padx=10, rowspan=3)
    # パスワード設定
    password_set_label = ctk.CTkLabel(setting_form, text='パスワード設定')
    password_set_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    # 線
    label_line = ctk.CTkLabel(
        setting_form, text='________________________________________________________________')
    label_line.grid(row=1, column=0, pady=12, padx=10, rowspan=3)
    # 新しいパスワード
    label_newpassword = ctk.CTkLabel(setting_form, text='新しいパスワード')
    label_newpassword.grid(row=3, column=0, padx=10, pady=10, sticky='w')
    validation = setting_form.register(on_validate)

    # パスワードの注意
    label_newpassword_error = ctk.CTkLabel(
        setting_form, text='', text_color='red')
    label_newpassword_error.grid(row=4, column=0, padx=10, pady=10, sticky='w')

    # パスワードテキストボックス
    password_entry = ctk.CTkEntry(setting_form, placeholder_text="半角数字4桁", validate="key", validatecommand=(
        validation, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
    password_entry.grid(row=3, column=0, pady=12, padx=10)
    # パスワード決定ボタン
    password_btn = ctk.CTkButton(
        setting_form, text='決定', command=lambda: pass_dicide_click(), width=50, height=5)
    password_btn.grid(row=4, column=0, pady=12, padx=10)

    # 線
    label_line = ctk.CTkLabel(
        setting_form, text='________________________________________________________________')
    label_line.grid(row=4, column=0, pady=12, padx=10, rowspan=3)

    # 制限時間の設定
    limit_set_label = ctk.CTkLabel(setting_form, text='制限時間設定(半角数字で入力)')
    limit_set_label.grid(row=6, column=0, pady=10, padx=10, sticky='w')
    # 線
    label_line = ctk.CTkLabel(
        setting_form, text='________________________________________________________________')
    label_line.grid(row=5, column=0, pady=12, padx=10, rowspan=4)
    # 新しい制限時間
    label_newtime = ctk.CTkLabel(setting_form, text='新しい制限時間')
    label_newtime.grid(row=8, column=0, pady=12, padx=10, sticky='w')

    # 設定の注意
    label_time_error = ctk.CTkLabel(setting_form, text='', text_color='red')
    label_time_error.grid(row=9, column=0, pady=12, padx=10, sticky='w')

    # 制限時間テキストボックス
    limit_entry = ctk.CTkEntry(setting_form, placeholder_text="半角数字(分)", validate="key", validatecommand=(
        validation, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
    limit_entry.grid(row=8, column=0, pady=12, padx=10)
    # 制限時間決定ボタン
    limit_btn = ctk.CTkButton(
        setting_form, text='決定', command=lambda: limit_dicide_click(), width=50, height=5)
    limit_btn.grid(row=9, column=0, pady=12, padx=10,)
    # 現在の制限時間
    if f_limit == "":
        label_realtime = ctk.CTkLabel(setting_form, text='制限時間を設定していません')
    else:
        label_realtime = ctk.CTkLabel(
            setting_form, text='現在の制限時間:%s分' % (f_limit / 60))
    label_realtime.grid(row=9, column=0, pady=12, padx=10, sticky='e')

    # 経過時間
    limit_label = ctk.CTkLabel(setting_frame, text='残り時間')
    limit_label.grid(row=11, column=0, pady=12, padx=10, sticky='w')
    # 終了
    button_exit = ctk.CTkButton(
        setting_form, text='アプリを終了', command=lambda: setting_end(), fg_color='red', text_color='black')
    # button_exit = ctk.CTkButton(setting_form, text='アプリを終了', command=lambda:setting_end(),fg_color='red')
    button_exit.grid(row=12, column=0, pady=6, padx=5, sticky='e')

# ----------------------------------------------------------------
# ラベルに飛ばす
    label_update()

    setting_form.mainloop()


if __name__ == '__main__':
    # global_set()
    setting()
