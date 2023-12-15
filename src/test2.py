# import
import cv2
import sys
import statistics   # 最頻値
import tkinter as tk
# 音
# from plyer import notification
import timeset
# ぼかしの処理
import numpy as np
import ctypes
import pygetwindow as gw
import pyautogui


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("注意画面")

        # カメラの初期設定と準備
        self.init_camera()

        # 初期設定
        self.init_config()
        # GUI構築
        self.build_gui()

        self.toggle_visibility_off()

        # 10秒ごとに最前面と最背面に切り替える処理を開始
        self.switch_visibility_periodically()

# カメラ設定
    def init_camera(self):
        # カスケード分類器のパスを各変数に代入
        fase_cascade_path = 'data\haarcascades\haarcascade_frontalface_default.xml'
        eye_cascade_path = 'data\haarcascades\haarcascade_eye.xml'

        # カスケード分類器の読み込み
        self.face_cascade = cv2.CascadeClassifier(fase_cascade_path)
        self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

        # Webカメラの準備
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラ画像の横幅を1280に設定
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # カメラ画像の縦幅を720に設定

        # カメラが起動していなかった場合は終了
        if self.cap.isOpened() is False:
            print("カメラが起動していないため終了しました")
            sys.exit()

# 値の初期値
    def init_config(self):
        # 値の初期設定をここに記述

        self.FRAME_LINESIZE = 2       # 顔に四角を描画する際の線の太さ
        self.FRAME_RGB_G = (0, 255, 0)  # 四角形を描画する際の色を格納(緑)
        self.FRAME_RGB_B = (255, 0, 0)  # 四角形を描画する際の色を格納(青)
        self.cnt = 0     # カウントの際に使用
        self.textChange = 0  # cmの表記を画面上部に固定にするか、顔に追従するかの切り替え
        self.fw = 100    # 顔の大きさの初期値（起動時エラー回避のため初期値設定）
        self.fx = 100    # 顔のx座標の初期値
        self.fy = 100    # 顔のy座標の初期値
        self.ew = 100    # 目の大きさの初期値
        self.ex = 100    # 目のx座標の初期値
        self.ey = 100    # 目のy座標の初期値
        self.disAns = 0  # 計測した距離を格納
        self.fwcount = []  # fwを一時的に格納（最頻値を出すために使用）
        self.ewcount = []  # ewを一時的に格納（最頻値を出すために使用）
        self.MODECOUNT = 50  # 最頻値を出すときの要素数（この値を変更することで計測値(cm)の正確性と計測にかかる時間が変化）
        # fwSample,ewSampleに対応した顔とカメラとの距離(cm)
        self.sampleLen = [10,   15,  20,  30,  40,  50,  60,  70]
        self.fwSample = [999, 999, 999, 999, 431, 348,
                         292, 253]       # 事前に計測した距離に対応する顔の大きさ
        self.ewSample = [268, 214, 161, 118,  90,  62,
                         59,  54]       # 事前に計測した距離に対応する目の大きさ

        # ウィンドウの初期設定
        # 画面全体
        self.root.attributes("-fullscreen", True)
        # タスクバー
        self.root.overrideredirect(True)
        # 最前面
        self.root.attributes("-topmost", True)
        # ウィンドウ移動、サイズ変更の無効
        self.root.bind("<B1-Motion>", lambda event: "break")
        self.root.bind("<Configure>", lambda event: "break")
# ウィンドウの設定

    def build_gui(self):
        # GUIの構築をここに記述
        toggle_button = tk.Button(
            self.root, text="Toggle Visibility", command=self.toggle_visibility)
        toggle_button.pack(pady=20)

    # ウィンドウにある終了
    def toggle_visibility(self):
        self.cap.release()
        self.root.destroy()

    # 表示
    def toggle_visibility_on(self):
        self.root.deiconify()

    # 非表示
    def toggle_visibility_off(self):
        self.root.withdraw()

    # 入力された値(fw,ew)から距離を求める関数--------------------------------------------------------------------

    def distance(self, sampleLen, fwSample, ewSample, fw, ew):
        valuesAbs = []      # 入力された値xと事前に計測された値との絶対値を格納
        cnt = 0             # カウントの役割をする変数
        ans = 0             # 顔と画面との距離を格納
        standard = 90       # ewとfwのどちらを距離算出に使うかの基準数値 (90は50cmのとき)

        if ew >= standard:             # ewが基準値より小さければewを計算に使用
            for i in ewSample:          # ewとの差の絶対値を格納
                valuesAbs.insert(cnt, abs(i - ew))
                cnt += 1

            valuesAbs_sorted = sorted(valuesAbs)        # 絶対値の値たちを昇順にソートして格納

            cnt = 0
            for i in valuesAbs:         # ewに一番近い値（絶対値）の要素番号を見つける
                if i == valuesAbs_sorted[0]:
                    break
                cnt += 1

            if ew > ewSample[0]:        # 距離が恐らく10cm以下の場合
                ans = -1
            elif ew == ewSample[cnt]:       # ewとewに最も近い値が等しい場合
                ans = sampleLen[cnt]
            elif ew > ewSample[cnt]:        # ewに最も近い値がewよりも小さい場合
                data1 = abs(ewSample[cnt] - ewSample[cnt-1])        # ewの大きさの差
                data2 = abs(sampleLen[cnt] - sampleLen[cnt-1]
                            ) / data1  # 1cmごとに変化するewの大きさ
                # ewより小さくて最も近い値からどれだけの差があるか
                data3 = abs(ew - ewSample[cnt-1])
                data4 = data2 * data3                               # ewより小さくて最も近い値より何cm離れているか
                # どれだけ画面から離れているか
                ans = sampleLen[cnt-1] + data4
            else:                       # ewに最も近い値がewよりも大きい場合
                data1 = abs(ewSample[cnt] - ewSample[cnt+1])        # ewの大きさの差
                data2 = abs(sampleLen[cnt] - sampleLen[cnt+1]
                            ) / data1  # ewが1増えるごとに何cm増えるか
                # ewより大きくて最も近い値からどれだけの差があるか
                data3 = abs(ew - ewSample[cnt])
                data4 = data2 * data3                               # ewより大きくて最も近い値より何cm離れているか
                # どれだけ画面から離れているか
                ans = sampleLen[cnt] + data4
        else:       # ewが基準値より大きければfwを計算に使用

            for i in fwSample:                      # fwとの差の絶対値を格納
                valuesAbs.insert(cnt, abs(i - fw))
                cnt += 1

            valuesAbs_sorted = sorted(valuesAbs)    # 絶対値の値たちをソート（昇順）を格納

            cnt = 0
            for i in valuesAbs:                     # fwに一番近い値（絶対値）の要素番号を見つける
                if i == valuesAbs_sorted[0]:
                    break
                cnt += 1

            if fw < fwSample[len(fwSample)-1]:  # 距離が恐らく70cm以上の場合
                ans = -2
            elif fw == fwSample[cnt]:       # fwとfwに最も近い値が等しい場合
                ans = sampleLen[cnt]
            elif fw > fwSample[cnt]:        # fwに最も近い値がfwよりも小さい場合
                data1 = abs(fwSample[cnt] - fwSample[cnt-1])        # fwの大きさの差
                data2 = abs(sampleLen[cnt] - sampleLen[cnt-1]
                            ) / data1  # 1cmごとに変化するfwの大きさ
                # fwより小さくて最も近い値からどれだけの差があるか
                data3 = abs(fw - fwSample[cnt-1])
                data4 = data2 * data3                               # fwより小さくて最も近い値より何cm離れているか
                # どれだけ画面から離れているか
                ans = sampleLen[cnt-1] + data4
            else:                           # fwに最も近い値がfwよりも大きい場合
                data1 = abs(fwSample[cnt] - fwSample[cnt+1])        # fwの大きさの差
                data2 = abs(sampleLen[cnt] - sampleLen[cnt+1]
                            ) / data1  # fwが1増えるごとに何cm増えるか
                # fwより大きくて最も近い値からどれだけの差があるか
                data3 = abs(fw - fwSample[cnt])
                data4 = data2 * data3                               # fwより大きくて最も近い値より何cm離れているか
                # どれだけ画面から離れているか
                ans = sampleLen[cnt] + data4
        return ans

    # カメラで測定
    def switch_visibility_periodically(self):
        ret, frame = self.cap.read()

        # カラーをモノクロ化したキャプチャを代入(グレースケール化)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 顔の検出
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

        # 目の検出
        eyes = self.eye_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

        # 第1引数   効果を適応する画像
        # 第2引数   矩形の左上隅の座標
        # 第3引数   矩形の右下隅の座標
        # 第4引数   矩形の色
        # 第5引数   描画する線の太さ（-1以下だと塗りつぶし）
        # 顔に四角形(矩形)を描画する
        for (self.fx, self.fy, self.fw, self.fh) in faces:
            cv2.rectangle(frame, (self.fx, self.fy), (self.fx + self.fw, self.fy + self.fh),
                          self.FRAME_RGB_G, self.FRAME_LINESIZE)

        # 目に四角形(矩形)を描画する
        for (self.ex, self.ey, self.ew, self.eh) in eyes:
            cv2.rectangle(frame, (self.ex, self.ey), (self.ex + self.ew, self.ey + self.eh),
                          self.FRAME_RGB_B, self.FRAME_LINESIZE)

        if self.cnt < self.MODECOUNT:
            # テスト用
            print(self.cnt)
            self.fwcount.insert(self.cnt, self.fw)
            self.ewcount.insert(self.cnt, self.ew)
            self.cnt += 1
        else:
            # テスト用
            self.cnt = 0
            print(self.cnt)
            disAns = self.distance(self.sampleLen, self.fwSample, self.ewSample,
                                   statistics.mode(self.fwcount), statistics.mode(self.ewcount))
            if disAns == -1:
                # ぼかしの処理
                self.toggle_visibility_on()
                # コマンドライン
                print('10cm以下です!近すぎます!!\n')
            elif disAns == -2:
                # ぼかしの処理
                self.toggle_visibility_off()
                print('70cm以上離れています!!\n')
            else:
                # 30以下
                if disAns < 30:
                    # ぼかしの処理
                    self.toggle_visibility_on()
                    # コマンドライン
                    print('顔が近いので少し離れてください')
                # 30以上
                elif disAns >= 30:
                    self.toggle_visibility_off()
                    # ぼかし
                print('%.2fcm\n' % disAns)    # 小数第２位まで出力

            # カウントのリセット
            self.fwcount = []
            self.ewcount = []
        # self.toggle_visibility()  # 初回実行
        # 1秒後に再度切り替える 7秒で1
        self.root.after(100, self.switch_visibility_periodically)


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
