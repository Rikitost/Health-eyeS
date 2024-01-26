# 顔を認識し、カメラから顔(目)までの距離を出す
# 一定間隔おきに距離を出し近いかどうかの判定、近ければ画面を表示させ遠ければ画面を透明化
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

# 使用ファイル
import warning
import setting
import password_input
# グローバル変数のファイル
import end_flg_value as gend  # 終了フラグ 0:継続 1:終了(flg)
import warning_flg as warn  # 注意画面のフラグ(0:非表示,1:表示)
import time_limit as limit  # 時間切れ(0;継続,1:終了)


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


def HealtheyeS(mode_cnt, fw_count, ew_count, fw, ew, dis_Ans, textChange, fx, fy, ex, ey, sampleLen, fwSample, ewSample, MODE):
    # 0.1秒間ごとに処理をする
    time.sleep(0.1)
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
# フレームごとに配列に代入回数に満たすと距離を測る
    if mode_cnt < MODE:
        fw_count.insert(mode_cnt, fw)
        ew_count.insert(mode_cnt, ew)
        mode_cnt += 1
    else:
        mode_cnt = 0
        dis_Ans = distance(sampleLen, fwSample, ewSample,
                           statistics.mode(fw_count), statistics.mode(ew_count))
        # 距離によって表示を変える
        if dis_Ans == -1:
            # ぼかしの処理
            warn.flg = 1
            MODE = 20
        elif dis_Ans == -2:
            # ぼかしの処理
            warn.flg = 0
            MODE = 50
        else:
            if dis_Ans < 30:
                # ぼかしの処理
                warn.flg = 1
                MODE = 20
            elif dis_Ans >= 30:
                warn.flg = 0
                MODE = 50
            print('%.2fcm\n' % dis_Ans)    # 小数第２位まで出力

    # カウントのリセット
        fw_count = []
        ew_count = []

    # 終了フラグ
    if gend.flg != 1:
        HealtheyeS(mode_cnt, fw_count, ew_count, fw, ew, dis_Ans,
                   textChange, fx, fy, ex, ey, sampleLen, fwSample, ewSample, MODE)


# アプリケーションの実行部分---------------------------------------------------------------------------------------------
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

# 時間の設定のフォーム
# 終わりフラグ初期値
# グローバル変数の初期値
gend.flg = 0
warn.flg = 0
limit.flg = 0

# 注意画面のスレッド
thread_warning = threading.Thread(target=warning.rootwin)
thread_warning.start()

# ラムダ式を使用して HealtheyeS 関数を呼び出す
# thread_camera = threading.Thread(target=HealtheyeS, args=(mode_cnt, fw_count, ew_count, fw,
#                                                           ew, dis_Ans, text_Change, fx, fy, ex, ey, SAMPLE_LEN, FW_SAMPLE, EW_SAMPLE, MODECOUNT))
# thread_camera.start()

# 設定画面のスレッド
thread_setting = threading.Thread(target=setting.setting)
thread_setting.start()


print("カメラを起動中…")


while True:
    time.sleep(1)
    # 全ての終了処理
    if gend.flg == 1:
        # カメラの開放
        cap.release()
        # cvのデストロイ
        cv2.destroyAllWindows()
        print("カメラが終了しました")
        # カメラスレッド
        # thread_camera.join()
        print("カメラのスレッド終了")
        # 注意画面のスレッド
        thread_warning.join()
        print("画面のスレッド終了")
        # 設定のスレッド
        thread_setting.join()
        print("設定のスレッド")
        # 全てを終わらせるのだ

        print("終了します")
        break

sys.exit()
