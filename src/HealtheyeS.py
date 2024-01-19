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


import setting
import password_input
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


# アプリケーションの実行部分---------------------------------------------------------------------------------------------
# 時間の設定のフォーム
# global f_limit
# global f_password
# global_set()
# visibility_flg = 0
# newend_flg = 0
# # 現パスワードを読み込む
# fp = open("src/password.txt", "r")
# fp_password = fp.read()
# fp.close()
# print("初期設定のパスワード:%s" % fp_password)
# # 現制限時間を読み込む
# f = open("src/limit.txt", "r")
# f_limit = int(f.read())
# f.close()
# print("初期設定の制限時間:%d" % f_limit)

# thread_app = threading.Thread(target=rootwin)
# thread_app.start()


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

# 設定の画面を開くスレッド
thread_setting = threading.Thread(target=setting.setting)
thread_setting.start()

print("これから消えるよ")
thread_setting.join()
# thread_camera = threading.Thread(target=HealtheyeS, args=(mode_cnt, fw_count, ew_count, fw,
#                                  ew, dis_Ans, text_Change, fx, fy, ex, ey, SAMPLE_LEN, FW_SAMPLE, EW_SAMPLE, MODECOUNT))
# thread_camera.start()
# HealtheyeS(mode_cnt, fw_count, ew_count, fw, ew, dis_Ans, text_Change, fx, fy, ex, ey, SAMPLE_LEN, FW_SAMPLE, EW_SAMPLE, MODECOUNT)
# print("カメラを起動しました")


# 終了フラグまたは再起動フラグが立ったら終了
# if gend.flg == 1 or grestart_flg.flg == 1:
#     print("thread_cameraを終了します")
#     thread_camera.join()
#     print("thread_cameraを終了しました")

#     print("カメラを終了します")
#     # カメラのリソースを開放する
#     cap.release()
#     cv2.destroyAllWindows()
#     print("カメラが終了しました")

#     print("終了します")

# if gend.flg == 1 and newend_flg == 1:
#     print("thread_cameraを終了します")
#     thread_camera.join()
#     print("thread_cameraを終了待ち")

#     # print("カメラを終了します")
#     # # カメラのリソースを開放する
#     # cap.release()
#     # print("カメラが終了しました")

#     print("カメラを終了します")
#     # カメラのリソースを開放する
#     cap.release()
#     print("カメラが終了しました")
#     print("cv2.destroyAllWindows()を実行します")
#     cv2.destroyAllWindows()
#     print("cv2.destroyAllWindows()を実行しました")

#     # print("thread_appを終了します")
#     # thread_app.join()
#     # print("thread_appを終了しました")
#     # OpenCVのウィンドウをすべて閉じる
#     # print("rootを終了します")
#     # root.quit()
#     # print("rootを終了しました")

#     # password_input.passbox_end()
#     print("正常に終了しました")
#     sys.exit()
# # ------------------------------------------------------------------------------------------------------------------------
