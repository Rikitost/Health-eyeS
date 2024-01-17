# 470行ぐらい500行ぐらい
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
    # 経過時間ラベルの更新
    # 経過時間ラベルの更新
    # limitlablがないときの例外処理

    try:
        limit_label.configure(text='残り時間:%d' % gtime_cnt.val)
        # print("経過時間:%d" % gtime_cnt.val)
    except NameError:
        pass
    setting_form.after(1000, label_update)


def setting_end():
    global setting_form
    if gformlock.flg == 0:
        # パスワードを再取得
        fp = open('password.txt', 'r')
        f_password = fp.read()
        fp.close()
        # パスワードを設定していないなら
        if f_password == "":
            print("パスワード認証をスキップ")
            gend.flg = 1  # 終了フラグを立てる
            print("設定のウインドウを閉じました")
            # print("setting endflg:%d" % gend.flg)
            thread_time_start.join()
            print("thread_time_startを閉じました")
            setting_form.quit()
            setting_form.destroy()
        else:
            # print(gpass_sec.flg)
            password_input.passbox_tk()
        if gpass_sec.flg == 1:
            gend.flg = 1  # 終了フラグを立てる
            print("設定のウインドウを閉じました")
            thread_time_start.join()
            print("thread_time_startを閉じました")
            setting_form.quit()
            setting_form.destroy()


# 設定formを開く
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

    def password_set_click():
        def pass_dicide_click():
            # パスワードを取得
            password = pass_entry.get()
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
            # メッセージのOKボタンを押したらウインドウを閉じる
            if messagebox.OK:
                # # 現在のパスワードを表示
                # if password =="":
                #     password_now_label.configure(text='パスワードを設定していません',font=("",9))
                # else:
                #     password_now_label.configure(text='現在のパスワード:%s' % password,font=("",9))
                # gwinlock.flgを0にして設定画面を操作できるようにする
                formlock_off(pass_win)

# 時間切れとかで出てくるform
        if gformlock.flg == 0:
            # gwinlock.flgを1にして設定画面を操作できないようにする
            formlock_on()
            pass_win = ctk.CTk()
            pass_win.title('パスワード設定')
            pass_win.geometry('400x300')
            # モーダルダイアログにする
            # pass_win.grab_set()
            # ウインドウの×を押したときの処理
            pass_win.protocol("WM_DELETE_WINDOW",
                              lambda: formlock_off(pass_win))
            # パスワード設定ラベル
            dic_label = ctk.CTkLabel(pass_win, text='パスワードを設定してください(半角数字4桁)')
            dic_label.place(x=0, y=0)

            validation_pass = pass_win.register(on_validate)
            # パスワード入力のテキストボックス
            # pass_entry = ctk.CTkEntry(pass_win, validate="key", validatecommand=(
            #     validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'), placeholder_text="半角数字4桁", show="*")
            pass_entry = ctk.CTkEntry(pass_win, validate="key", validatecommand=(
                validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
            pass_entry.pack()
            # 警告ラベル
            warning_label = tk.Label(pass_win, text='')
            warning_label.place(x=0, y=40)
            # 決定ボタン
            pass_decide_btn = tk.Button(
                pass_win, text='決定', command=lambda: pass_dicide_click())
            pass_decide_btn.place(x=0, y=60)
        else:
            pass

    def limit_set_click():
        # 決定ボタンを押したときの処理
        def limit_dicide_click():
            # 入力した制限時間を取得
            limit = limit_entry.get()
            # 空白なら警告
            if limit == '':
                messagebox.showinfo('制限時間設定', '制限時間を設定してください(分)')
                # limit_winを最前面へ
                limit_win.lift()
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
                # メッセージを表示
                messagebox.showinfo('制限時間設定', '制限時間を設定しました')
                # メッセージのOKボタンを押したらウインドウを閉じる
                # if messagebox.OK:
                #     if limit =="":
                #         limit_now_label.configure(text='制限時間を設定していません',font=("",9))
                #     else:
                #         limit_now_label.configure(text='現在の制限時間:%s分' % limit,font=("",9))

                #     # 設定画面を操作できるようにする
                #     formlock_off(limit_win)

        if gformlock.flg == 0:
            # gwinlock.flgを1にして設定画面を操作できないようにする
            formlock_on()
            # フォームの生成
            limit_win = tk.Tk()
            limit_win.title('制限時間設定')
            limit_win.geometry('400x300')
            # モーダルダイアログにする
            # limit_win.grab_set()
            # ウインドウの×を押したときの処理
            limit_win.protocol("WM_DELETE_WINDOW",
                               lambda: formlock_off(limit_win))
            limit_win.focus_set()
            # 制限時間設定ラベル
            dic_label = tk.Label(limit_win, text='制限時間を設定してください(半角数字4桁)')
            dic_label.place(x=0, y=0)

            validation_pass = limit_win.register(on_validate)
            # 制限時間入力のテキストボックス
            limit_entry = tk.Entry(limit_win, validate="key", validatecommand=(
                validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
            limit_entry.pack()
            # 警告ラベル
            warning_label = tk.Label(limit_win, text='')
            warning_label.place(x=0, y=40)
            # 決定ボタン
            limit_decide_btn = tk.Button(
                limit_win, text='決定', command=lambda: limit_dicide_click())
            limit_decide_btn.place(x=0, y=60)

    def app_restart_click():
        if gformlock.flg == 0:
            grestart_flg.flg = 1
            # print("thread_time_startを終了しました")
            time_stop_click()
            print("タイマーを止めました")
            setting_form.quit()
            print("設定のウインドウを閉じました")

    # ウインドウの×を押したときの処理（タイマーを止めてからウインドウを閉じる）

    def delete_window():
        time_stop_click()
        setting_form.destroy()

# ----------------------------------------------------------------------------------
    global limit_label
    global f_limit
    global f_password
    # global setting_end_flg

    gsetting_thread_end.flg = 0

    f = open('limit.txt', 'r')
    f_limit = int(f.read())
    f.close()

    fp = open('password.txt', 'r')
    f_password = fp.read()
    fp.close()

    ctk.set_appearance_mode("white")

    # Selecting color theme - blue, green, dark-blue
    ctk.set_default_color_theme("blue")

    # メインウィンドウ
    setting_form = ctk.CTk()
    form_x = 400
    form_y = 500
    setting_form.geometry('%dx%d' % (form_x, form_y))
    setting_form.title('設定画面')

    # ×を押したときの処理
    setting_form.protocol("WM_DELETE_WINDOW", lambda: delete_window())
    # フレームの作成
    setting_frame = ctk.CTkFrame(setting_form)
    setting_frame.configure(width=150, height=50)
    setting_frame.grid(row=12, column=0, pady=12, padx=10, sticky="w")
    # タイトル
    custom_font = ctk.CTkFont(size=20)
    label_title = ctk.CTkLabel(
        setting_form, text="Health-eyeS", font=custom_font)
    label_title.grid(row=0, column=0, pady=20)
    # 線
    label_line = ctk.CTkLabel(
        setting_form, text='________________________________________________________________')
    label_line.grid(row=0, column=0, pady=12, padx=10, rowspan=3)
    # パスワード設定
    password_set_label = ctk.CTkLabel(setting_form, text='パスワード設定(半角数字4桁)')
    password_set_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    # 線
    label_line = ctk.CTkLabel(
        setting_form, text='________________________________________________________________')
    label_line.grid(row=1, column=0, pady=12, padx=10, rowspan=3)
    # 新しいパスワード+
    label_newpassword = ctk.CTkLabel(setting_form, text='新しいパスワード')
    label_newpassword.grid(row=3, column=0, padx=10, pady=10, sticky='w')

    # パスワード入力のテキストボックス
    validation_pass = setting_form.register(on_validate)
    user_pass = ctk.CTkEntry(setting_form, validate="key", validatecommand=(
        validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'), show="*")
    user_pass.grid(row=3, column=0, pady=12, padx=10)

    # 決定ボタン
    button_decision = ctk.CTkButton(
        setting_form, text='決定', command=setting, width=50, height=5)
    button_decision.grid(row=4, column=0, pady=12, padx=10)
    # # 新しいパスワード-
    # password_set_btn = tk.Button(setting_frame,text='パスワード設定',command=lambda:password_set_click())
    # 線
    label_line = ctk.CTkLabel(
        setting_form, text='________________________________________________________________')
    label_line.grid(row=4, column=0, pady=12, padx=10, rowspan=3)

    # # 現在のパスワード
    # if f_password =="":
    #     password_now_label = tk.Label(setting_frame,text='パスワードを設定していません',font=("",9))
    # else:
    #     password_now_label = tk.Label(setting_frame,text='現在のパスワード:%s' % f_password,font=("",9))
    # 制限時間の設定
    limit_set_label = ctk.CTkLabel(setting_form, text='制限時間設定(分)')
    limit_set_label.grid(row=6, column=0, pady=10, padx=10, sticky='w')
    # 線
    label_line = ctk.CTkLabel(
        setting_form, text='________________________________________________________________')
    label_line.grid(row=5, column=0, pady=12, padx=10, rowspan=4)
    # 新しい制限時間+
    label_newtime = ctk.CTkLabel(setting_form, text='新しい制限時間')
    label_newtime.grid(row=8, column=0, pady=12, padx=10, sticky='w')

    # テキストボックス
    validation_pass = setting_form.register(on_validate)
    user_entry = ctk.CTkEntry(setting_form, validate="key", validatecommand=(
        validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'), show="*")
    # user_entry = ctk.CTkEntry(setting_form, placeholder_text="半角数字(分)")
    user_entry.grid(row=8, column=0, pady=12, padx=10)

    # 決定ボタン
    button_decision = ctk.CTkButton(
        setting_form, text='決定', command=setting, width=50, height=5)
    button_decision.grid(row=9, column=0, pady=12, padx=10,)
    # # 新しい制限時間-
    # limit_set_btn = tk.Button(setting_frame,text='制限時間設定',command=lambda:limit_set_click())

    # if f_limit =="":
    #     limit_now_label = tk.Label(setting_frame,text='制限時間を設定していません',font=("",9))
    # else:
    #     limit_now_label = tk.Label(setting_frame,text='現在の制限時間:%s分' % f_limit,font=("",9))
    # 現在の制限時間
    label_realtime = ctk.CTkLabel(setting_form, text='現在の制限時間')
    label_realtime.grid(row=9, column=0, pady=12, padx=10, sticky='e')
    # 再起動
    button_restart = ctk.CTkButton(
        setting_form, text='適用して再起動', command=lambda: app_restart_click())
    button_restart.grid(row=11, column=0, pady=5, padx=5, sticky='e')
    # 経過時間
    limit_label = ctk.CTkLabel(setting_form, text='残り時間')
    limit_label.grid(row=11, column=0, pady=12, padx=10, sticky='w')
    # 終了
    button_exit = ctk.CTkButton(
        setting_form, text='アプリを終了', command=lambda: setting_end(), fg_color='red')
    # button_exit = ctk.CTkButton(setting_form, text='アプリを終了', command=lambda:setting_end(),fg_color='red')
    button_exit.grid(row=12, column=0, pady=6, padx=5, sticky='e')

    # 配置配置配置配置配置配置配置配置配置配置配置配置配置配置配置配置
    # パスワード設定ラベル

    # #計測開始ボタン
    # time_start_btn = tk.Button(setting_frame,text='計測開始',command=lambda:time_start_click())
    # #計測停止ボタン
    # time_stop_btn = tk.Button(setting_frame,text='計測停止',command=lambda:time_stop_click())
    # 再起動ボタン
    app_restart_btn = tk.Button(
        setting_frame, text='アプリを再起動', command=lambda: app_restart_click())
    # 終了ボタン
    app_end_btn = tk.Button(setting_frame, text='アプリを終了',
                            command=lambda: setting_end())

    # # テキストの位置
    # label_place = 0
    # # ボタンの位置
    # btn_place = form_x*(3/5)
    # # パスワード設定の配置(y=0)
    # password_set_label.place(x=label_place,y=0)
    # password_now_label.place(x=label_place,y=20)# form_xの3/5の位置に配置
    # password_set_btn.place(x=btn_place,y=0,width=100,height=30)  # form_xの2/5の位置に配置
    # # 制限時間設定の配置
    # limit_set_label.place(x=label_place,y=50)
    # limit_now_label.place(x=label_place,y=70)
    # limit_set_btn.place(x=btn_place,y=50,width=100,height=30)
    # # 経過時間ラベルの配置
    # limit_label.place(x=form_x*(7/10),y=form_x*(9/10))
    # # # 計測開始ボタンの配置
    # # time_start_btn.place(x=120,y=60)
    # # # 計測停止ボタンの配置
    # # time_stop_btn.place(x=120,y=100)
    # # 再起動ボタンの配置
    # app_restart_btn.place(x=0,y=form_y*9/10)
    # # 終了ボタンの配置
    # app_end_btn.place(x=form_x/2-40,y=form_y-150)

    # setting_frame.pack()
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
    while gend.flg == 0:
        # 再起動ボタンを押したら
        if grestart_flg.flg == 1:
            # 設定画面のスレッドを終了
            thread_time_start.join()
            print("thread_time_startを終了しました")
            # thread1.join()
            grestart_flg.flg = 0
            print("再起動します")
            gsetting_thread_end.flg = 1
        # スレッドを終了してから再起動
        if gsetting_thread_end.flg == 1:
            globalfile_reset()
            # thread1 = threading.Thread(target=setting)
            # thread1.start()
            print("再起動しました")
