import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time
# ファイルをインポート
import password_input
# グローバル変数
# 時間計測スレッドの終了フラグ 0:継続 1:終了(flg)
import clock_thread_end_flg as gclock_thread_end
# 設定画面の終了フラグ 0:継続 1:終了(flg)
import setting_thread_end_flg as gsetting_thread_end
# 設定入力画面を操作している間設定選択画面を操作できなくするフラグ 0:解除 1:ロック (flg)
import form_lock_flg as gformlock
import end_flg_value as gend  # 終了フラグ 0:継続 1:終了(flg)
import time_count_value as gtime_cnt  # 時間計測のカウント(val)
import time_count_flg as gtime_flg  # 計測フラグ 0:時間計測中 1:時間計測終了(flg)
import pass_sec_value as gpass_sec  # パスワードが解かれたか 0:ロック 1:解除 (flg)
import restart_flg as grestart_flg  # 再起動フラグ 0:再起動待機 1:再起動 (flg)
# パスワード入力画面が閉じられたか 0:閉じられていない 1:閉じられた(flg)
import password_form_end_flg as gpass_form_end
import password_windowup_flg as gpass_windowup  # パスワード入力画面を起動する


def globalfile_reset():
    global gend
    global gformlock
    global gtime_cnt
    global gtime_flg
    global gpass_sec
    global grestart_flg
    gformlock.flg = 0
    gend.flg = 0
    gtime_cnt.val = 0
    gtime_flg.flg = 1
    gpass_sec.flg = 0
    grestart_flg.flg = 0    # 再起動フラグ 0:再起動待機 1:再起動 (flg)

# ファイル単体で実行する用初期化関数


def global_set():
    global gend
    global gformlock
    global gtime_cnt
    global gtime_flg
    global gpass_sec
    global grestart_flg
    gformlock.flg = 0
    gend.flg = 0
    gtime_cnt.val = 0
    gtime_flg.flg = 1
    gpass_sec.flg = 0
    grestart_flg.flg = 0    # 再起動フラグ 0:再起動待機 1:再起動 (flg)
    gpass_form_end.flg = 0


def time_start_click():
    global thread_time_start
    if gformlock.flg == 0:
        f = open('limit.txt', 'r')
        f_limit = int(f.read())
        f.close()
        # 制限時間を過ぎたとき(設定した時間を過ぎているなら)
        if gtime_cnt.val >= f_limit:
            messagebox.showinfo('警告', '制限時間を過ぎています')
        else:
            if gtime_flg.flg == 1:
                gtime_flg.flg = 0  # 計測する
                # thread_time_start = threading.Thread(target=time_limit.clock)
                thread_time_start = threading.Thread(target=clock)
                thread_time_start.start()
                print("thread_time_startを開始しました")
                # time_limit.clock()
                print("計測開始")


def time_stop_click():
    if gformlock.flg == 0:
        if gtime_flg.flg == 0:
            gtime_flg.flg = 1  # 計測を止める
            # print("計測停止")


# 時間を計測する関数
def clock():

    # time_limit_count = 0
    while gtime_flg.flg == 0 and gend.flg == 0:
        # f = open('src/limit.txt', 'r')
        # f_limit = int(f.read())
        # f.close()

        # 制限時間を過ぎたとき
        if gtime_cnt.val >= f_limit:
            gtime_flg.flg = 1
            break
        # elif gend.flg == 1:
        #     gtime_flg.flg = 1
        #     print("thread_time_startを終了しました")
        #     break

        # time_limit_count += 1
        # gtime_cnt.val = time_limit_count
        gtime_cnt.val += 1
        # print(gtime_cnt.val)

        time.sleep(1)
    # 制限時間を過ぎたとき
    if gtime_cnt.val >= f_limit:
        # パスワードを再取得
        fp = open('password.txt', 'r')
        f_password = fp.read()
        fp.close()
        # 時間計測終了
        # time_limit_count = 0
        # gtime_cnt.val = 0
        # #メッセージを表示
        # messagebox.showinfo('時間制限','制限時間を超えました')

        print("時間計測を終了しました")
        if f_password == "":
            print("パスワード認証をスキップ")
        # else:
        #     password_input.passbox_end()
    else:

        print("計測停止")


def label_update():
    global limit_label
    global nokoritime
    # 経過時間ラベルの更新
    # 経過時間ラベルの更新
    # limitlablがないときの例外処理
    if nokoritime <= 0:
        nokoritime = 0
    else:
        nokoritime -= 1
    try:
        limit_label.configure(text='残り時間:%d' % nokoritime)
        # print("経過時間:%d" % gtime_cnt.val)
    except NameError:
        pass
    setting_form.after(1000, label_update)


def setting_end():
    global setting_form
    global gend
    global gpass_windowup
    if gformlock.flg == 0:
        # パスワードを再取得
        fp = open('password.txt', 'r')
        f_password = fp.read()
        fp.close()
        # パスワードを設定していないなら
        if f_password == "":
            print("パスワード認証をスキップ")
            gend.flg = 1  # 終了フラグを立てる
            print("パスワードフラグ：%d" % gpass_sec.flg)
            setting_form.quit()
            print("設定のウインドウを閉じました")
            # print("setting endflg:%d" % gend.flg)
            thread_time_start.join()
            print("thread_time_startを閉じました")

            # setting_form.destroy()
        else:
            # print(gpass_sec.flg)
            password_input.passbox_tk()
            print(gpass_sec.flg)
        if gpass_sec.flg == 1:
            gend.flg = 1  # 終了フラグを立てる
            thread_time_start.join()
            print("thread_time_startを閉じました")
            print("おわりフラグ：%d" % gend.flg)
            setting_form.quit()
            # setting_form.destroy()
            print("設定のウインドウを閉じました")
            gsetting_thread_end.flg = 1

            # setting_form.destroy()


def restart_after():
    global grestart_flg
    if grestart_flg.flg == 1:
        grestart_flg.flg = 0
        setting_form.quit()
        time_stop_click()
        print("タイマーを止めました")
        setting_form.quit()
        setting_form.destroy()
        print("設定のウインドウを閉じました")
        time.sleep(3)
        setting()
        grestart_flg.flg = 0
    elif gpass_sec.flg == 1:
        password_input.passbox_form.quit()
        setting_form.quit()
    else:
        setting_form.after(1000, restart_after)


def setting():
    global gend
    global setting_form

# 内容確認関連の関数-----------------------------------------------------------------
    # 入力内容確認の関数
    def value_check(entry_text, warning_label):
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

    # 数値のみ入力を受け付ける処理
    def on_validate(d, i, P, s, S, v, V, W):
        # Pが数字の場合はTrue、それ以外はFalse
        return (P.isdigit() and len(P) <= 4) or P == ""
# ----------------------------------------------------------------------------------

# ボタンクリック関連の関数------------------------------------------------------------
    # フォーム操作関連の関数------------------------------------------------------------
    # 別のフォームを開くときgwinlock.flg=1にして前のフォームの操作をできなくする関数
    def formlock_on():
        gformlock.flg = 1
    # ×で閉じたときgwinlock.flg=0にする関数(form=閉じるフォーム)

    def formlock_off(form):
        gformlock.flg = 0
        form.destroy()
    # ----------------------------------------------------------------------------------
    # パスワード設定ボタンを押したときの処理

    def pass_dicide_click():
        print("パスワード設定ボタンを押しました")
        # パスワードを取得
        password = password_entry.get()
        print(password)
        # パスワードをpassword.txtに保存
        f = open('password.txt', 'w')
        f.write(str(password))
        f.close()
        # 空白なら警告
        if password == '':
            # メッセージを表示
            messagebox.showinfo('パスワード設定', 'パスワードなしで設定しました')
        else:
            # メッセージを表示
            messagebox.showinfo('パスワード設定', 'パスワードを設定しました')

    def limit_dicide_click():
        global nokoritime
        # 入力した制限時間を取得
        limit = limit_entry.get()
        # 空白なら警告
        if limit == '':
            messagebox.showinfo('制限時間設定', '制限時間を設定してください(分)')
            # limit_winを最前面へ
            setting_form.lift()
            return
        else:
            # 分
            # limit_minut = int(limit) * 60
            # 秒
            limit_minut = int(limit)
            # 制限時間をlimit.txtに保存
            f = open('limit.txt', 'w')
            f.write(str(limit_minut))
            f.close()
            # ラベルの更新
            nokoritime = int(limit_minut)
            # メッセージを表示
            messagebox.showinfo('制限時間設定', '制限時間を設定しました')

    def app_restart_click():
        if gformlock.flg == 0:
            grestart_flg.flg = 1
            # # print("thread_time_startを終了しました")
            # time_stop_click()
            # print("タイマーを止めました")
            # setting_form.quit()
            # print("設定のウインドウを閉じました")

    # ウインドウの×を押したときの処理（タイマーを止めてからウインドウを閉じる）

    def delete_window():
        time_stop_click()
        gend.flg = 1
        setting_form.destroy()

# ----------------------------------------------------------------------------------
    global limit_label
    global f_limit
    global f_password
    global nokoritime
    # global setting_end_flg

    gsetting_thread_end.flg = 0

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
    limit_set_label = ctk.CTkLabel(setting_form, text='制限時間設定')
    limit_set_label.grid(row=6, column=0, pady=10, padx=10, sticky='w')
    # 線
    label_line = ctk.CTkLabel(
        setting_form, text='________________________________________________________________')
    label_line.grid(row=5, column=0, pady=12, padx=10, rowspan=4)
    # 新しい制限時間
    label_newtime = ctk.CTkLabel(setting_form, text='新しい制限時間')
    label_newtime.grid(row=8, column=0, pady=12, padx=10, sticky='w')
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
            setting_form, text='現在の制限時間:%s分' % f_limit)
    label_realtime.grid(row=9, column=0, pady=12, padx=10, sticky='e')
    # 再起動
    button_restart = ctk.CTkButton(
        setting_form, text='適用して再起動', command=lambda: app_restart_click())
    # button_restart.grid(row=11, column=0, pady=5,padx=5,sticky='e')
    # 経過時間
    limit_label = ctk.CTkLabel(setting_frame, text='残り時間')
    limit_label.grid(row=11, column=0, pady=12, padx=10, sticky='w')
    # 終了
    button_exit = ctk.CTkButton(
        setting_form, text='アプリを終了', command=lambda: setting_end(), fg_color='red')
    # button_exit = ctk.CTkButton(setting_form, text='アプリを終了', command=lambda:setting_end(),fg_color='red')
    button_exit.grid(row=12, column=0, pady=6, padx=5, sticky='e')

    setting_form.after(1000, restart_after)

    # 配置配置配置配置配置配置配置配置配置配置配置配置配置配置配置配置
    # パスワード設定ラベル
    # 再起動ボタン
    app_restart_btn = tk.Button(
        setting_frame, text='アプリを再起動', command=lambda: app_restart_click())
    # 終了ボタン
    app_end_btn = tk.Button(setting_frame, text='アプリを終了',
                            command=lambda: setting_end())

    setting_form.after(1000, label_update)
    time_start_click()

    setting_form.mainloop()


def clock_thread_end():
    thread_time_start.join()


if __name__ == '__main__':
    global_set()
    setting()
    # thread_time_start.join()
    # thread1 = threading.Thread(target=setting)
    # thread1.start()
    # 終了フラグが立つまでループ(再起動用のループ)
    # while gend.flg == 0:
    #     # 再起動ボタンを押したら
    #     if grestart_flg.flg == 1:
    #         # 設定画面のスレッドを終了
    #         thread_time_start.join()
    #         print("thread_time_startを終了しました")
    #         # thread1.join()
    #         grestart_flg.flg = 0
    #         print("再起動します")
    #         gsetting_thread_end.flg = 1
    #     # スレッドを終了してから再起動
    #     if gsetting_thread_end.flg == 1:
    #         globalfile_reset()
    #         # thread1 = threading.Thread(target=setting)
    #         # thread1.start()
    #         print("再起動しました")
