# 顔を認識し、カメラから顔(目)までの距離を出す
# 一定間隔おきに距離を出す
# キー入力「0」で即座に距離を出す（精度低）
# キー入力「1」でcmの表記位置変更
# キー入力「Esc」で終了
# 画面サイズ1280,720で計測

# import
import cv2
import sys
import statistics   # 最頻値
import tkinter as tk
import threading
import time
from tkinter import messagebox
import customtkinter as ctk

# import timeset
# import time_limit
import setting
# グローバル変数をセット
# 時間計測スレッドの終了フラグ 0:継続 1:終了(flg)
import clock_thread_end_flg as gclock_thread_end
# 設定画面スレッドの終了フラグ 0:継続 1:終了(flg)
import setting_thread_end_flg as gsetting_thread_end
# 設定入力画面を操作している間設定選択画面を操作できなくするフラグ 0:解除 1:ロック (flg)
import form_lock_flg as gformlock
import end_flg_value as gend  # 終了フラグ 0:継続 1:終了(flg)
import time_limit_value as glimit   # 制限時間 (val)
import time_count_value as gtime_cnt    # 時間計測のカウント (val)
import time_count_flg as gtime_flg  # 計測フラグ 0:時間計測中 1:時間計測終了 (flg)
import pass_sec_value as gpass_sec  # 入力されたパスワード (val)
import restart_flg as grestart_flg  # 再起動フラグ 0:再起動待機 1:再起動 (flg)
import password_windowup_flg as gpass_windowup  # パスワード入力画面を表示する

import password_input

# 初期値を None に設定
# thread_setting = None
# thread_passbox = None
# thread_setting = threading.Thread(target=setting.setting)
# thread_passbox = threading.Thread(target=password_input.passbox_tk)

# --------------------------------------------------------------------------------------------------------


def global_set():
    gsetting_thread_end.flg = 0  # 設定画面の終了フラグ 0:継続 1:終了(flg)
    gformlock.flg = 0  # 設定入力画面を操作している間設定選択画面を操作できなくするフラグ 0:解除 1:ロック (flg)
    gtime_cnt.val = 0   # 時間計測のカウント
    gend.flg = 0        # 終了フラグ 0:継続 1:終了
    gtime_flg.flg = 1   # 計測フラグ 0:時間計測中 1:時間計測終了
    gpass_sec.flg = 0   # パスワードが解かれたか 0:ロック 1:解除 (flg)
    grestart_flg.flg = 0    # 再起動フラグ 0:再起動待機 1:再起動 (flg)
    visibility_flg = 0  # 画面の表示フラグ 0:透過 1:表示


# 表示---------------------------------------------------------------------------------------------------------------------
def restart_after():
    global grestart_flg
    global root
    global newend_flg
    # if f_limit <= gtime_cnt.val and first == 0:
    #     # print("全画面")
    #     first = 1
    #     rootwin.root.focus_force()
    if gpass_windowup == 1:
        setting.setting_end()
    if gpass_sec.flg == 1 and gend.flg == 0:
        password_input.passbox_form.quit()

    if visibility_flg == 0:
        toggle_visibility_off()
    elif visibility_flg == 1:
        toggle_visibility_on()

    if grestart_flg.flg == 1:
        grestart_flg.flg = 0
        setting.setting_form.quit()
        setting.time_stop_click()
        print("タイマーを止めました")
        # setting.setting_form.quit()
        setting.setting_form.destroy()
        print("設定のウインドウを閉じました")
        time.sleep(3)
        setting()
        grestart_flg.flg = 0

    elif gend.flg == 1:
        if gsetting_thread_end.flg == 1:
            print("settingend通った")

            print("rootを終了します")
            # pass
            print("rootをquit")
            root.quit()
            print("thread_appを終了します")
            # thread_app.join()
            print("thread_appを終了しました")
            newend_flg = 1

        else:
            print("通った")
            # password_input.passbox_form.quit()
            setting.setting_form.quit()
            # setting.setting_form.destroy()
            print("設定のウインドウを閉じました")
            setting.time_stop_click()
            print("タイマーを止めました")
            # setting.setting_form.quit()
            # setting.setting_form.destroy()

            print("rootを終了します")
            # pass
            print("rootをquit")
            root.quit()
            print("thread_appを終了します")
            # thread_app.join()
            print("thread_appを終了しました")
            newend_flg = 1
            # root.destroy()

    else:
        root.after(1000, restart_after)


def toggle_visibility_on():
    # ウィンドウの透明度を設定 (0: 完全透明, 1: 完全不透明)
    root.attributes("-alpha", 0.97)
# 非表示---------------------------------------------------------------------------------------------------------------------


def toggle_visibility_off():
    # ウィンドウの透明度を設定 (0: 完全透明, 1: 完全不透明)
    root.attributes("-alpha", 0)
# def endroot():
#     if gend.flg == 1:
#         # root.quit()
#         pass
#     root.after(100,endroot)


def on_root_click(event):
    print("rootをクリックしました")
    root.attributes("-topmost", False)
    password_input.passbox_form.attributes("-topmost", True)
    # アクティブに
    password_input.passbox_form.focus_force()


def rootwin():
    global root
    global visibility_flg
    global first
    first = 0
    root = tk.Tk()
    root.title("注意")
    # ウィンドウの初期設定
    # ウィンドウの表示
    root.deiconify()
    # ウィンドウを透明クリック可能にする
    # タイトルバーを非表示にする
    root.overrideredirect(True)

    root.wm_attributes("-transparentcolor", "white")
    root.geometry("{0}x{1}+0+0".format(3000, 3000))
    # ウィンドウの初期設定
    # 画面全体
    # root.attributes("-zoomed", "1")
    # root.attributes("-fullscreen", True)
    # タスクバー
    # root.overrideredirect(True)
    # 最前面
    root.attributes("-topmost", True)
    # ウィンドウ移動、サイズ変更の無効
    # root.bind("<B1-Motion>", lambda event: "break")
    # root.bind("<Configure>", lambda event: "break")
    root.bind("<Button-1>", on_root_click)
    toggle_visibility_off()
    visibility_flg = 0
    # root.after(100,endroot)
    root.after(1000, restart_after)
    root.mainloop()
    # del root

# 再起動する関数


def restart_app():
    # pass
    global f_limit
    global thread_setting
    global thread_passbox
    while gend.flg == 0:
        #     # 再起動ボタンを押したら
        if grestart_flg.flg == 1:
            # タイマーのスレッドを終了
            setting.clock_thread_end()
            print("clock_threadを終了しました")
            # 設定画面のスレッドを終了
            thread_setting.join()
            print("thread_settingを終了しました")
            grestart_flg.flg = 0
            print("再起動します")
            gsetting_thread_end.flg = 1
        # スレッドの終了を確認してから再起動
        if gsetting_thread_end.flg == 1:
            setting.globalfile_reset()
            thread_setting = threading.Thread(target=setting.setting)
            thread_setting.start()
            print("再起動しました")

            # 制限時間を更新
            f = open("limit.txt", "r")
            f_limit = int(f.read())
            f.close()
            print("制限時間:%d" % f_limit)
            grestart_flg.flg = 0
            print("カメラを再起動しています…")

            # 時間計測開始
            # setting.time_start_click()

            HealtheyeS(mode_cnt, fw_count, ew_count, fw, ew, dis_Ans, text_Change,
                       fx, fy, ex, ey, SAMPLE_LEN, FW_SAMPLE, EW_SAMPLE, MODECOUNT)
        # elif gend.flg == 1:
        #     break


# 入力された値(fw,ew)から距離を求める関数--------------------------------------------------------------------


def distance(sample_Len, fw_Sample, ew_Sample, fw, ew):
    value_Abs = []      # 入力された値xと事前に計測された値との絶対値を格納
    value_abs_cnt = 0             # カウントの役割をする変数
    ans = 0             # 顔と画面との距離を格納
    standard = 90       # ewとfwのどちらを距離算出に使うかの基準数値 (90は50cmのとき)

    if ew >= standard:             # ewが基準値より小さければewを計算に使用
        for i in ew_Sample:          # ewとの差の絶対値を格納
            value_Abs.insert(value_abs_cnt, abs(i - ew))
            value_abs_cnt += 1

        valuesAbs_sorted = sorted(value_Abs)        # 絶対値の値たちを昇順にソートして格納

        value_abs_cnt = 0
        for i in value_Abs:         # ewに一番近い値（絶対値）の要素番号を見つける
            if i == valuesAbs_sorted[0]:
                break
            value_abs_cnt += 1

        if ew > ew_Sample[0]:        # 距離が恐らく10cm以下の場合
            ans = -1
        elif ew == ew_Sample[value_abs_cnt]:       # ewとewに最も近い値が等しい場合
            ans = sample_Len[value_abs_cnt]
        elif ew > ew_Sample[value_abs_cnt]:        # ewに最も近い値がewよりも小さい場合
            few_diff = abs(ew_Sample[value_abs_cnt] -
                           ew_Sample[value_abs_cnt-1])        # ewの大きさの差
            few_chg = abs(sample_Len[value_abs_cnt] - sample_Len[value_abs_cnt-1]
                          ) / few_diff  # 1cmごとに変化するewの大きさ
            # ewより小さくて最も近い値からどれだけの差があるか
            few_chg_diff = abs(ew - ew_Sample[value_abs_cnt-1])
            # ewより小さくて最も近い値より何cm離れているか
            few_add = few_chg * few_chg_diff
            # どれだけ画面から離れているか
            ans = sample_Len[value_abs_cnt-1] + few_add
        else:                       # ewに最も近い値がewよりも大きい場合
            few_diff = abs(ew_Sample[value_abs_cnt] -
                           ew_Sample[value_abs_cnt+1])        # ewの大きさの差
            few_chg = abs(sample_Len[value_abs_cnt] - sample_Len[value_abs_cnt+1]
                          ) / few_diff  # ewが1増えるごとに何cm増えるか
            # ewより大きくて最も近い値からどれだけの差があるか
            few_chg_diff = abs(ew - ew_Sample[value_abs_cnt])
            # ewより大きくて最も近い値より何cm離れているか
            few_add = few_chg * few_chg_diff
            # どれだけ画面から離れているか
            ans = sample_Len[value_abs_cnt] + few_add
    else:       # ewが基準値より大きければfwを計算に使用

        for i in fw_Sample:                      # fwとの差の絶対値を格納
            value_Abs.insert(value_abs_cnt, abs(i - fw))
            value_abs_cnt += 1

        valuesAbs_sorted = sorted(value_Abs)    # 絶対値の値たちをソート（昇順）を格納

        value_abs_cnt = 0
        for i in value_Abs:                     # fwに一番近い値（絶対値）の要素番号を見つける
            if i == valuesAbs_sorted[0]:
                break
            value_abs_cnt += 1

        if fw < fw_Sample[len(fw_Sample)-1]:  # 距離が恐らく70cm以上の場合
            ans = -2
        elif fw == fw_Sample[value_abs_cnt]:       # fwとfwに最も近い値が等しい場合
            ans = sample_Len[value_abs_cnt]
        elif fw > fw_Sample[value_abs_cnt]:        # fwに最も近い値がfwよりも小さい場合
            few_diff = abs(fw_Sample[value_abs_cnt] -
                           fw_Sample[value_abs_cnt-1])        # fwの大きさの差
            few_chg = abs(sample_Len[value_abs_cnt] - sample_Len[value_abs_cnt-1]
                          ) / few_diff  # 1cmごとに変化するfwの大きさ
            # fwより小さくて最も近い値からどれだけの差があるか
            few_chg_diff = abs(fw - fw_Sample[value_abs_cnt-1])
            # fwより小さくて最も近い値より何cm離れているか
            few_add = few_chg * few_chg_diff
            # どれだけ画面から離れているか
            ans = sample_Len[value_abs_cnt-1] + few_add
        else:                           # fwに最も近い値がfwよりも大きい場合
            few_diff = abs(fw_Sample[value_abs_cnt] -
                           fw_Sample[value_abs_cnt+1])        # fwの大きさの差
            few_chg = abs(sample_Len[value_abs_cnt] - sample_Len[value_abs_cnt+1]
                          ) / few_diff  # fwが1増えるごとに何cm増えるか
            # fwより大きくて最も近い値からどれだけの差があるか
            few_chg_diff = abs(fw - fw_Sample[value_abs_cnt])
            # fwより大きくて最も近い値より何cm離れているか
            few_add = few_chg * few_chg_diff
            # どれだけ画面から離れているか
            ans = sample_Len[value_abs_cnt] + few_add
    return ans

# 無限ループで読み取った映像に変化を加える（1フレームごとに区切って変化）
# count = 0


def HealtheyeS(mode_cnt, fw_count, ew_count, fw, ew, dis_Ans, textChange, fx, fy, ex, ey, sampleLen, fwSample, ewSample, MODE):

    global thread_passbox
    global visibility_flg
    global gpass_windowup
    printcnt = 0
    f = open('limit.txt', 'r')
    f_limit = int(f.read())
    f.close()
    print("制限時間:%d" % f_limit)

    # 終了ボタンや再起動ボタンが押されたら処理を終了する
    while gend.flg == 0 and grestart_flg.flg == 0:

        time.sleep(0.1)

        if gend.flg == 1:
            return  # 終了フラグが立っていたら処理を終了する
        # if gend.flg == 1:
        #     print("カメラを終了します")
        #     # カメラのリソースを開放する
        #     cap.release()
        #     print("カメラが終了しました")
        #     break
        # print("camera endflg:%d" % gend.flg)

        # count += 1
        ret, frame = cap.read()

        # カラーをモノクロ化したキャプチャを代入(グレースケール化)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 顔の検出
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

        # 目の検出
        eyes = eye_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

    # デバック-------------------------------------------------
        # # 第1引数   効果を適応する画像
        # # 第2引数   矩形の左上隅の座標
        # # 第3引数   矩形の右下隅の座標
        # # 第4引数   矩形の色
        # # 第5引数   描画する線の太さ（-1以下だと塗りつぶし）
        # 顔に四角形(矩形)を描画する
        for (fx, fy, fw, fh) in faces:
            cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh),
                          FRAME_RGB_G, FRAME_LINESIZE)

        # 目に四角形(矩形)を描画する
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh),
                          FRAME_RGB_B, FRAME_LINESIZE)
    # -----------------------------------------------------------
        if mode_cnt < MODE:
            fw_count.insert(mode_cnt, fw)
            ew_count.insert(mode_cnt, ew)
            mode_cnt += 1
        else:
            mode_cnt = 0
            dis_Ans = distance(sampleLen, fwSample, ewSample,
                               statistics.mode(fw_count), statistics.mode(ew_count))
            # 制限時間が過ぎているならパス
            if f_limit <= gtime_cnt.val:
                pass
            # 距離によって表示を変える
            else:
                if dis_Ans == -1:
                    # ぼかしの処理
                    visibility_flg = 1
                    # toggle_visibility_on()
                    # コマンドライン
                    print('10cm以下です!近すぎます!!\n')
                    MODE = 20
                elif dis_Ans == -2:
                    # ぼかしの処理
                    visibility_flg = 0
                    # toggle_visibility_off()
                    # if f_limit > gtime_cnt.val:
                    print('70cm以上離れています!!\n')
                    MODE = 50
                else:
                    if dis_Ans < 30:
                        # ぼかしの処理
                        visibility_flg = 1
                        # toggle_visibility_on()
                        # コマンドライン
                        print('顔が近いので少し離れてください')
                        MODE = 20
                    elif dis_Ans >= 30:
                        visibility_flg = 0
                        # toggle_visibility_off()
                        # if f_limit > gtime_cnt.val:
                        print('%.2fcm\n' % dis_Ans)    # 小数第２位まで出力
                        MODE = 50

    # カウントのリセット
            fw_count = []
            ew_count = []

        # 10秒後に1度顔の判定
        # root.after(100, HealtheyeS(mode_cnt, fw_count, ew_count, fw, ew, dis_Ans, textChange, fx, fy, ex, ey, sampleLen, fwSample, ewSample, MODECOUNT))
        # root.after(100,HealtheyeS(mode_cnt, fw_count, ew_count, fw, ew, dis_Ans, textChange, fx, fy, ex, ey, sampleLen, fwSample, ewSample, MODECOUNT))
        # cv2.imshow('gray', gray)
        # 画像の表示
        # cv2.imshow('YourFace', frame)
    # time_limitの変更箇所-----------------------------------------

        # 制限時間を超えたらパスワード入力画面を表示
        # if f_limit <= gtime_cnt.val:
        if gtime_flg.flg == 0:
            # f = open('src/limit.txt', 'r')
            # f_limit = int(f.read())
            # f.close()
            if f_limit <= gtime_cnt.val:
                gtime_flg.flg = 1
                visibility_flg = 1
                # toggle_visibility_on()
                root.focus_force()
                print("画面を覆う")
                break
                # メッセージを表示
                # messagebox.showinfo('時間制限','制限時間を超えました')

                # thread_passbox = threading.Thread(target=password_input.passbox_tk)
                # thread_passbox.start()
                # gpass_windowup = 1
                # password_input.passbox_tk()

                print("モザイクとパスワードを出す")

                if gpass_sec.flg == 1 and gend.flg == 0:
                    # thread_passbox.join()
                    print("thread_passboxを終了しました")
                    visibility_flg = 1
                    # toggle_visibility_off()
                    # grestart_flg.flg = 1
                    gpass_sec.flg = 0
        if gend.flg == 1:
            break
        # if gpass_sec.flg == 1:
        #     pass
        # print("end:%d" % gend.flg)
    if f_limit <= gtime_cnt.val:

        root.focus_force()
        password_input.passbox_tk()
        visibility_flg = 0
        gend.flg = 1


def build_gui():
    # GUIの構築をここに記述
    # labelの情報
    toggle_label = tk.Label(root, text="近いです離れてください")
    toggle_label.pack(pady=20)


# ---------------------------------------------------------------------------------------------------------

# アプリケーションの実行部分---------------------------------------------------------------------------------------------
# 時間の設定のフォーム
global f_limit
global f_password
global_set()
visibility_flg = 0
newend_flg = 0
# 現パスワードを読み込む
fp = open("password.txt", "r")
fp_password = fp.read()
fp.close()
print("初期設定のパスワード:%s" % fp_password)
# 現制限時間を読み込む
f = open("limit.txt", "r")
f_limit = int(f.read())
f.close()
print("初期設定の制限時間:%d" % f_limit)

thread_app = threading.Thread(target=rootwin)
thread_app.start()

thread_setting = threading.Thread(target=setting.setting)
thread_setting.start()

print("カメラを起動中…")


# カスケード分類器のパスを各変数に代入
# pythonの実行
fase_cascade_path = 'data\haarcascades\haarcascade_frontalface_default.xml'
eye_cascade_path = 'data\haarcascades\haarcascade_eye.xml'
# カスケード分類器の読み込み
face_cascade = cv2.CascadeClassifier(fase_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

# Webカメラの準備（引数でカメラ指定、0は内臓カメラ）
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラ画像の横幅を1280に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # カメラ画像の縦幅を720に設定

# もしカメラが起動していなかったら終了する
if cap.isOpened() is False:
    print("カメラが起動していないため終了しました")
    sys.exit()

# Webカメラの初期設定-----------------------------------------------------------
FRAME_LINESIZE = 2       # 顔に四角を描画する際の線の太さ
FRAME_RGB_G = (0, 255, 0)  # 四角形を描画する際の色を格納(緑)
FRAME_RGB_B = (255, 0, 0)  # 四角形を描画する際の色を格納(青)
mode_cnt = 0     # カウントの際に使用
text_Change = 0  # cmの表記を画面上部に固定にするか、顔に追従するかの切り替え
fw = 100    # 顔の大きさの初期値（起動時エラー回避のため初期値設定）
fx = 100    # 顔のx座標の初期値
fy = 100    # 顔のy座標の初期値
ew = 100    # 目の大きさの初期値
ex = 100    # 目のx座標の初期値
ey = 100    # 目のy座標の初期値
dis_Ans = 0  # 計測した距離を格納
fw_count = []  # fwを一時的に格納（最頻値を出すために使用）
ew_count = []  # ewを一時的に格納（最頻値を出すために使用）
MODECOUNT = 50  # 最頻値を出すときの要素数（この値を変更することで計測値(cm)の正確性と計測にかかる時間が変化）
# fwSample,ewSampleに対応した顔とカメラとの距離(cm)
SAMPLE_LEN = [10,   15,  20,  30,  40,  50,  60,  70]
FW_SAMPLE = [999, 999, 999, 999, 431, 348,
             292, 253]       # 事前に計測した距離に対応する顔の大きさ
EW_SAMPLE = [268, 214, 161, 118,  90,  62,
             59,  54]       # 事前に計測した距離に対応する目の大きさ
# -------------------------------------------------------------------------------


# 時間計測開始
setting.time_start_click()

print("カメラを起動")
thread_camera = threading.Thread(target=HealtheyeS, args=(mode_cnt, fw_count, ew_count, fw,
                                 ew, dis_Ans, text_Change, fx, fy, ex, ey, SAMPLE_LEN, FW_SAMPLE, EW_SAMPLE, MODECOUNT))
thread_camera.start()
# HealtheyeS(mode_cnt, fw_count, ew_count, fw, ew, dis_Ans, text_Change, fx, fy, ex, ey, SAMPLE_LEN, FW_SAMPLE, EW_SAMPLE, MODECOUNT)
print("カメラを起動しました")

restart_app()
if newend_flg == 1:
    print("thread_cameraを終了します")
    thread_camera.join()
    print("thread_cameraを終了待ち")

    # print("カメラを終了します")
    # # カメラのリソースを開放する
    # cap.release()
    # print("カメラが終了しました")

    print("カメラを終了します")
    # カメラのリソースを開放する
    cap.release()
    print("カメラが終了しました")
    print("cv2.destroyAllWindows()を実行します")
    cv2.destroyAllWindows()
    print("cv2.destroyAllWindows()を実行しました")

    print("正常に終了しました")
    sys.exit()
