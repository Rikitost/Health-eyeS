# import
import cv2
import sys
import statistics   # 最頻値
import tkinter as tk


cnt = 0
# 距離


def calculate_distance(sampleLen, fwSample, ewSample, fw, ew):
    valuesAbs = []
    cnt = 0
    ans = 0
    standard = 90

    if ew >= standard:
        for i in ewSample:
            valuesAbs.insert(cnt, abs(i - ew))
            cnt += 1

        valuesAbs_sorted = sorted(valuesAbs)

        cnt = 0
        for i in valuesAbs:
            if i == valuesAbs_sorted[0]:
                break
            cnt += 1

        if ew > ewSample[0]:
            ans = -1
        elif ew == ewSample[cnt]:
            ans = sampleLen[cnt]
        elif ew > ewSample[cnt]:
            data1 = abs(ewSample[cnt] - ewSample[cnt-1])
            data2 = abs(sampleLen[cnt] - sampleLen[cnt-1]) / data1
            data3 = abs(ew - ewSample[cnt-1])
            data4 = data2 * data3
            ans = sampleLen[cnt-1] + data4
        else:
            data1 = abs(ewSample[cnt] - ewSample[cnt+1])
            data2 = abs(sampleLen[cnt] - sampleLen[cnt+1]) / data1
            data3 = abs(ew - ewSample[cnt])
            data4 = data2 * data3
            ans = sampleLen[cnt] + data4
    else:
        for i in fwSample:
            valuesAbs.insert(cnt, abs(i - fw))
            cnt += 1

        valuesAbs_sorted = sorted(valuesAbs)

        cnt = 0
        for i in valuesAbs:
            if i == valuesAbs_sorted[0]:
                break
            cnt += 1

        if fw < fwSample[len(fwSample)-1]:
            ans = -2
        elif fw == fwSample[cnt]:
            ans = sampleLen[cnt]
        elif fw > fwSample[cnt]:
            data1 = abs(fwSample[cnt] - fwSample[cnt-1])
            data2 = abs(sampleLen[cnt] - sampleLen[cnt-1]) / data1
            data3 = abs(fw - fwSample[cnt-1])
            data4 = data2 * data3
            ans = sampleLen[cnt-1] + data4
        else:
            data1 = abs(fwSample[cnt] - fwSample[cnt+1])
            data2 = abs(sampleLen[cnt] - sampleLen[cnt+1]) / data1
            data3 = abs(fw - fwSample[cnt])
            data4 = data2 * data3
            ans = sampleLen[cnt] + data4
    return ans


def check_face_and_toggle_visibility(cap, root):
    # ---------------------------------------------------------------------------------------------------------
    # カスケード分類器のパスを各変数に代入
    # pythonの実行
    fase_cascade_path = 'data\haarcascades\haarcascade_frontalface_default.xml'
    eye_cascade_path = 'data\haarcascades\haarcascade_eye.xml'
    # カスケード分類器の読み込み
    face_cascade = cv2.CascadeClassifier(fase_cascade_path)
    eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

    FRAME_LINESIZE = 2       # 顔に四角を描画する際の線の太さ
    FRAME_RGB_G = (0, 255, 0)  # 四角形を描画する際の色を格納(緑)
    FRAME_RGB_B = (255, 0, 0)  # 四角形を描画する際の色を格納(青)
    global cnt  # グローバル
    textChange = 0  # cmの表記を画面上部に固定にするか、顔に追従するかの切り替え
    fw = 100    # 顔の大きさの初期値（起動時エラー回避のため初期値設定）
    fx = 100    # 顔のx座標の初期値
    fy = 100    # 顔のy座標の初期値
    ew = 100    # 目の大きさの初期値
    ex = 100    # 目のx座標の初期値
    ey = 100    # 目のy座標の初期値
    disAns = 0  # 計測した距離を格納
    fwcount = []  # fwを一時的に格納（最頻値を出すために使用）
    ewcount = []  # ewを一時的に格納（最頻値を出すために使用）
    MODECOUNT = 50  # 最頻値を出すときの要素数（この値を変更することで計測値(cm)の正確性と計測にかかる時間が変化）
    # fwSample,ewSampleに対応した顔とカメラとの距離(cm)
    sampleLen = [10,   15,  20,  30,  40,  50,  60,  70]
    fwSample = [999, 999, 999, 999, 431, 348,
                292, 253]       # 事前に計測した距離に対応する顔の大きさ
    ewSample = [268, 214, 161, 118,  90,  62,
                59,  54]       # 事前に計測した距離に対応する目の大きさ

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラ画像の横幅を1280に設定
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # カメラ画像の縦幅を720に設定

    # -----------------------------------------------------------
    # もしカメラが起動していなかったら終了する
    if cap.isOpened() is False:
        print("カメラが起動していないため終了しました")
        sys.exit()

    # 時間の設定のフォーム
    # timeset.timeset_task()

    ret, frame = cap.read()

    # カラーをモノクロ化したキャプチャを代入(グレースケール化)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 顔の検出
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5)

    # 目の検出
    eyes = eye_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5)

    # 第1引数   効果を適応する画像
    # 第2引数   矩形の左上隅の座標
    # 第3引数   矩形の右下隅の座標
    # 第4引数   矩形の色
    # 第5引数   描画する線の太さ（-1以下だと塗りつぶし）
    # 顔に四角形(矩形)を描画する
    for (fx, fy, fw, fh) in faces:
        cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh),
                      FRAME_RGB_G, FRAME_LINESIZE)

    # 目に四角形(矩形)を描画する
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh),
                      FRAME_RGB_B, FRAME_LINESIZE)

    if cnt < MODECOUNT:
        fwcount.insert(cnt, fw)
        ewcount.insert(cnt, ew)
        cnt += 1
    else:
        cnt = 0
        disAns = calculate_distance(sampleLen, fwSample, ewSample,
                                    statistics.mode(fwcount), statistics.mode(ewcount))
        if disAns == -1:
            # コマンドライン
            print('10cm以下です!近すぎます!!\n')
        elif disAns == -2:
            print('70cm以上離れています!!\n')
        else:
            if disAns < 30:
                root.deiconify()  # 顔が遠いときは表示
                # コマンドライン
                print('顔が近いので少し離れてください')
            elif disAns >= 30:
                root.withdraw()  # 顔が近いときは非表示
            print('%.2fcm\n' % disAns)    # 小数第２位まで出力

        # カウントのリセット
        fwcount = []
        ewcount = []


# Tkinterウィンドウを作成
root = tk.Tk()

# ウィンドウのサイズ変更を無効化
root.resizable(width=False, height=False)

# ウィンドウの移動を無効化
root.overrideredirect(True)
root.title("Face Distance Measurement")
root.resizable(width=False, height=False)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
              root.winfo_screenheight()))
# root.withdraw()  # 顔が近いときは非表示

label = tk.Label(
    root, text="This window is initially hidden. It will be shown when a face is detected.")
label.pack(padx=20, pady=20)
close_button = tk.Button(root, text="Close", command=root.destroy)
close_button.pack(pady=10)
root.attributes('-topmost', True)
# カメラキャプチャを開始
cap = cv2.VideoCapture(0)

# イベントループ内で処理を実行
check_face_and_toggle_visibility(cap, root)

# Tkinterのイベントループを開始
root.mainloop()

# カメラキャプチャを停止
cap.release()

# import cv2
# import tkinter as tk
# from PIL import Image, ImageTk
# import sys
# import statistics   # 最頻値
# import tkinter as tk
# import threading
# import time


# class FaceDistanceWindow(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         self.title("Face Distance Measurement")
#         self.resizable(width=False, height=False)
#         self.overrideredirect(True)
#         self.geometry(
#             "{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
#         self.visible = False

#         label = tk.Label(
#             self, text="This window is initially hidden. It will be shown when a face is detected.")
#         label.pack(padx=20, pady=20)
#         close_button = tk.Button(self, text="Close", command=self.destroy)
#         close_button.pack(pady=10)
#         self.attributes('-topmost', True)
#         # カメラキャプチャを開始
#         self.cap = cv2.VideoCapture(0)
#         self.check_face_and_toggle_visibility()

#     def check_face_and_toggle_visibility(self):
#         # 顔の検出
#         # カスケード分類器のパスを各変数に代入
#         # pythonの実行
#         fase_cascade_path = 'data/haarcascades/haarcascade_frontalface_default.xml'
#         eye_cascade_path = 'data/haarcascades/haarcascade_eye.xml'
#         # カスケード分類器の読み込み
#         face_cascade = cv2.CascadeClassifier(fase_cascade_path)
#         eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

#         ret, frame = self.cap.read()

#         FRAME_LINESIZE = 2       # 顔に四角を描画する際の線の太さ
#         FRAME_RGB_G = (0, 255, 0)  # 四角形を描画する際の色を格納(緑)
#         FRAME_RGB_B = (255, 0, 0)  # 四角形を描画する際の色を格納(青)
#         cnt = 0     # カウントの際に使用
#         fw = 100    # 顔の大きさの初期値（起動時エラー回避のため初期値設定）
#         fx = 100    # 顔のx座標の初期値
#         fy = 100    # 顔のy座標の初期値
#         ew = 100    # 目の大きさの初期値
#         ex = 100    # 目のx座標の初期値
#         ey = 100    # 目のy座標の初期値
#         disAns = 0  # 計測した距離を格納
#         fwcount = []  # fwを一時的に格納（最頻値を出すために使用）
#         ewcount = []  # ewを一時的に格納（最頻値を出すために使用）
#         MODECOUNT = 50  # 最頻値を出すときの要素数（この値を変更することで計測値(cm)の正確性と計測にかかる時間が変化）
#         # fwSample,ewSampleに対応した顔とカメラとの距離(cm)
#         sampleLen = [10,   15,  20,  30,  40,  50,  60,  70]
#         fwSample = [999, 999, 999, 999, 431, 348,
#                     292, 253]       # 事前に計測した距離に対応する顔の大きさ
#         ewSample = [268, 214, 161, 118,  90,  62,
#                     59,  54]       # 事前に計測した距離に対応する目の大きさ

#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラ画像の横幅を1280に設定
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # カメラ画像の縦幅を720に設定

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(
#             gray, scaleFactor=1.3, minNeighbors=5)
#         # 目の検出
#         eyes = eye_cascade.detectMultiScale(
#             gray, scaleFactor=1.3, minNeighbors=5)

#         # 第1引数   効果を適応する画像
#         # 第2引数   矩形の左上隅の座標
#         # 第3引数   矩形の右下隅の座標
#         # 第4引数   矩形の色
#         # 第5引数   描画する線の太さ（-1以下だと塗りつぶし）
#         # 顔に四角形(矩形)を描画する
#         for (fx, fy, fw, fh) in faces:
#             cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh),
#                           FRAME_RGB_G, FRAME_LINESIZE)

#         # 目に四角形(矩形)を描画する
#         for (ex, ey, ew, eh) in eyes:
#             cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh),
#                           FRAME_RGB_B, FRAME_LINESIZE)

#         if cnt < MODECOUNT:
#             fwcount.insert(cnt, fw)
#             ewcount.insert(cnt, ew)
#             cnt += 1
#         else:
#             cnt = 0
#             disAns = self.calculate_distance(sampleLen, fwSample, ewSample,
#                                              statistics.mode(fwcount), statistics.mode(ewcount))
#             if disAns == -1:
#                 self.withdraw()
#                 self.visible = False
#                 # コマンドライン
#                 print('10cm以下です!近すぎます!!\n')
#             elif disAns == -2:
#                 # ぼかしの処理
#                 self.withdraw()
#                 self.visible = True
#                 print('70cm以上離れています!!\n')
#             else:
#                 if disAns < 30:
#                     # ぼかしの処理
#                     self.withdraw()
#                     self.visible = False
#                     # コマンドライン
#                     print('顔が近いので少し離れてください')
#                 elif disAns >= 30:
#                     self.withdraw()
#                     self.visible = True
#                 print('%.2fcm\n' % disAns)    # 小数第２位まで出力

#             # カウントのリセット
#             fwcount = []
#             ewcount = []

#         # 再帰的に呼び出す
#         self.after(1000, self.check_face_and_toggle_visibility)

# # 距離の計算
#     def calculate_distance(self, sampleLen, fwSample, ewSample, fw, ew):
#         valuesAbs = []      # 入力された値xと事前に計測された値との絶対値を格納
#         cnt = 0             # カウントの役割をする変数
#         ans = 0             # 顔と画面との距離を格納
#         standard = 90       # ewとfwのどちらを距離算出に使うかの基準数値 (90は50cmのとき)

#         if ew >= standard:             # ewが基準値より小さければewを計算に使用
#             for i in ewSample:          # ewとの差の絶対値を格納
#                 valuesAbs.insert(cnt, abs(i - ew))
#                 cnt += 1

#             valuesAbs_sorted = sorted(valuesAbs)        # 絶対値の値たちを昇順にソートして格納

#             cnt = 0
#             for i in valuesAbs:         # ewに一番近い値（絶対値）の要素番号を見つける
#                 if i == valuesAbs_sorted[0]:
#                     break
#                 cnt += 1

#             if ew > ewSample[0]:        # 距離が恐らく10cm以下の場合
#                 ans = -1
#             elif ew == ewSample[cnt]:       # ewとewに最も近い値が等しい場合
#                 ans = sampleLen[cnt]
#             elif ew > ewSample[cnt]:        # ewに最も近い値がewよりも小さい場合
#                 data1 = abs(ewSample[cnt] - ewSample[cnt-1])        # ewの大きさの差
#                 data2 = abs(sampleLen[cnt] - sampleLen[cnt-1]
#                             ) / data1  # 1cmごとに変化するewの大きさ
#                 # ewより小さくて最も近い値からどれだけの差があるか
#                 data3 = abs(ew - ewSample[cnt-1])
#                 data4 = data2 * data3                               # ewより小さくて最も近い値より何cm離れているか
#                 # どれだけ画面から離れているか
#                 ans = sampleLen[cnt-1] + data4
#             else:                       # ewに最も近い値がewよりも大きい場合
#                 data1 = abs(ewSample[cnt] - ewSample[cnt+1])        # ewの大きさの差
#                 data2 = abs(sampleLen[cnt] - sampleLen[cnt+1]
#                             ) / data1  # ewが1増えるごとに何cm増えるか
#                 # ewより大きくて最も近い値からどれだけの差があるか
#                 data3 = abs(ew - ewSample[cnt])
#                 data4 = data2 * data3                               # ewより大きくて最も近い値より何cm離れているか
#                 # どれだけ画面から離れているか
#                 ans = sampleLen[cnt] + data4
#         else:       # ewが基準値より大きければfwを計算に使用

#             for i in fwSample:                      # fwとの差の絶対値を格納
#                 valuesAbs.insert(cnt, abs(i - fw))
#                 cnt += 1

#             valuesAbs_sorted = sorted(valuesAbs)    # 絶対値の値たちをソート（昇順）を格納

#             cnt = 0
#             for i in valuesAbs:                     # fwに一番近い値（絶対値）の要素番号を見つける
#                 if i == valuesAbs_sorted[0]:
#                     break
#                 cnt += 1

#             if fw < fwSample[len(fwSample)-1]:  # 距離が恐らく70cm以上の場合
#                 ans = -2
#             elif fw == fwSample[cnt]:       # fwとfwに最も近い値が等しい場合
#                 ans = sampleLen[cnt]
#             elif fw > fwSample[cnt]:        # fwに最も近い値がfwよりも小さい場合
#                 data1 = abs(fwSample[cnt] - fwSample[cnt-1])        # fwの大きさの差
#                 data2 = abs(sampleLen[cnt] - sampleLen[cnt-1]
#                             ) / data1  # 1cmごとに変化するfwの大きさ
#                 # fwより小さくて最も近い値からどれだけの差があるか
#                 data3 = abs(fw - fwSample[cnt-1])
#                 data4 = data2 * data3                               # fwより小さくて最も近い値より何cm離れているか
#                 # どれだけ画面から離れているか
#                 ans = sampleLen[cnt-1] + data4
#             else:                           # fwに最も近い値がfwよりも大きい場合
#                 data1 = abs(fwSample[cnt] - fwSample[cnt+1])        # fwの大きさの差
#                 data2 = abs(sampleLen[cnt] - sampleLen[cnt+1]
#                             ) / data1  # fwが1増えるごとに何cm増えるか
#                 # fwより大きくて最も近い値からどれだけの差があるか
#                 data3 = abs(fw - fwSample[cnt])
#                 data4 = data2 * data3                               # fwより大きくて最も近い値より何cm離れているか
#                 # どれだけ画面から離れているか
#                 ans = sampleLen[cnt] + data4
#         return ans

# # 終了処理
#     def destroy(self):
#         # ウィンドウが閉じられたときにカメラキャプチャを停止する
#         if self.cap.isOpened():
#             self.cap.release()
#         tk.Tk.destroy(self)


# # ウィンドウのインスタンスを作成
# window = FaceDistanceWindow()
# # Tkinterのイベントループを開始
# window.mainloop()


# import tkinter as tk


# def check_condition_and_toggle_visibility(window, visible):
#     # ここに条件を追加
#     # 例: 特定の条件が満たされた場合、ウィンドウを表示
#     if True:  # ここに実際の条件を追加
#         if not visible:
#             window.deiconify()  # ウィンドウを表示
#             visible = True
#     else:
#         if visible:
#             window.withdraw()  # ウィンドウを非表示
#             visible = False

#     # 条件を確認し、再帰的に呼び出す（例: 一定の間隔で条件を確認する）
#     window.after(
#         1000, lambda: check_condition_and_toggle_visibility(window, visible))


# if __name__ == "__main__":
#     root = tk.Tk()

#     # ウィンドウのサイズ変更を無効化
#     root.resizable(width=False, height=False)

#     # ウィンドウの移動を無効化
#     root.overrideredirect(True)

#     label = tk.Label(
#         root, text="This window is initially hidden. It will be shown when a condition is met.")
#     label.pack(padx=20, pady=20)

#     # ウィンドウを閉じるボタン
#     close_button = tk.Button(root, text="Close", command=root.destroy)
#     close_button.pack(pady=10)

#     # ウィンドウを最前面に表示
#     root.attributes('-topmost', True)

#     # ウィンドウを画面全体に広げる
#     root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
#                   root.winfo_screenheight()))

#     # 画面表示状態を格納する変数
#     visible = False

#     # 条件を確認し、ウィンドウを表示または非表示にする
#     check_condition_and_toggle_visibility(root, visible)

#     # Tkinterのイベントループを開始
#     root.mainloop()
