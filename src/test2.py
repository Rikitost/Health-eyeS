# import
import cv2
import sys
import statistics   # 最頻値
import tkinter as tk
import threading
import time
# 音
# from plyer import notification
# ぼかしの処理
import numpy as np
import ctypes
import pygetwindow as gw
import pyautogui
# ファイルのimport
# import timeset


class MosaicForm:
    def __init__(self, root):
        self.root = root
        self.root.title("注意画面")

        # カメラの初期設定と準備
        self.init_camera()

        # 初期設定
        self.init_config()
        # GUI構築
        self.build_gui()
        # 初手は非表示(透明度0)
        self.toggle_visibility_off()

        # スレッドで定期的にUIを更新
        # self.update_thread = threading.Thread(
        #     target=self.update_gui_thread, daemon=True)
        # self.update_thread.start()
        # 1秒ごとに顔の判定距離計算等処理を開始
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
        self.mode_cnt = 0     # カウントの際に使用
        self.text_Change = 0  # cmの表記を画面上部に固定にするか、顔に追従するかの切り替え
        self.fw = 100    # 顔の大きさの初期値（起動時エラー回避のため初期値設定）
        self.fx = 100    # 顔のx座標の初期値
        self.fy = 100    # 顔のy座標の初期値
        self.ew = 100    # 目の大きさの初期値
        self.ex = 100    # 目のx座標の初期値
        self.ey = 100    # 目のy座標の初期値
        self.dis_Ans = 0  # 計測した距離を格納
        self.fw_count = []  # fwを一時的に格納（最頻値を出すために使用）
        self.ew_count = []  # ewを一時的に格納（最頻値を出すために使用）
        self.MODE = 50  # 最頻値を出すときの要素数（この値を変更することで計測値(cm)の正確性と計測にかかる時間が変化）
        # fwSample,ewSampleに対応した顔とカメラとの距離(cm)
        self.SAMPLE_LEN = [10,   15,  20,  30,  40,  50,  60,  70]
        self.FW_SAMPLE = [999, 999, 999, 999, 431, 348,
                          292, 253]       # 事前に計測した距離に対応する顔の大きさ
        self.EW_SAMPLE = [268, 214, 161, 118,  90,  62,
                          59,  54]       # 事前に計測した距離に対応する目の大きさ

        # ウィンドウの初期設定
        # ウィンドウの表示
        self.root.deiconify()

        # ウィンドウを透明クリック可能にする
        self.root.wm_attributes("-transparentcolor", "white")

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
        # labelの情報
        toggle_label = tk.Label(self.root, text="近いです離れてください")
        toggle_label.pack(pady=20)

    # ウィンドウにある終了

    def toggle_visibility(self):
        self.cap.release()
        self.root.destroy()

    # 表示
    def toggle_visibility_on(self):
        # ウィンドウの透明度を設定 (0: 完全透明, 1: 完全不透明)
        self.root.attributes("-alpha", 0.97)

    # 非表示
    def toggle_visibility_off(self):
        # ウィンドウの透明度を設定 (0: 完全透明, 1: 完全不透明)
        self.root.attributes("-alpha", 0)

    # 入力された値(fw,ew)から距離を求める関数--------------------------------------------------------------------

    def distance(self, sample_Len, fw_Sample, ew_Sample, fw, ew):
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
                # ewの大きさの差
                few_diff = abs(ew_Sample[value_abs_cnt] -
                               ew_Sample[value_abs_cnt-1])
                few_chg = abs(sample_Len[value_abs_cnt] - sample_Len[value_abs_cnt-1]
                              ) / few_diff  # 1cmごとに変化するewの大きさ
                # ewより小さくて最も近い値からどれだけの差があるか
                few_chg_diff = abs(ew - ew_Sample[value_abs_cnt-1])
                # ewより小さくて最も近い値より何cm離れているか
                few_add = few_chg * few_chg_diff
                # どれだけ画面から離れているか
                ans = sample_Len[value_abs_cnt-1] + few_add
            else:                       # ewに最も近い値がewよりも大きい場合
                # ewの大きさの差
                few_diff = abs(ew_Sample[value_abs_cnt] -
                               ew_Sample[value_abs_cnt+1])
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
                # fwの大きさの差
                few_diff = abs(fw_Sample[value_abs_cnt] -
                               fw_Sample[value_abs_cnt-1])
                few_chg = abs(sample_Len[value_abs_cnt] - sample_Len[value_abs_cnt-1]
                              ) / few_diff  # 1cmごとに変化するfwの大きさ
                # fwより小さくて最も近い値からどれだけの差があるか
                few_chg_diff = abs(fw - fw_Sample[value_abs_cnt-1])
                # fwより小さくて最も近い値より何cm離れているか
                few_add = few_chg * few_chg_diff
                # どれだけ画面から離れているか
                ans = sample_Len[value_abs_cnt-1] + few_add
            else:                           # fwに最も近い値がfwよりも大きい場合
                # fwの大きさの差
                few_diff = abs(fw_Sample[value_abs_cnt] -
                               fw_Sample[value_abs_cnt+1])
                few_chg = abs(sample_Len[value_abs_cnt] - sample_Len[value_abs_cnt+1]
                              ) / few_diff  # fwが1増えるごとに何cm増えるか
                # fwより大きくて最も近い値からどれだけの差があるか
                few_chg_diff = abs(fw - fw_Sample[value_abs_cnt])
                # fwより大きくて最も近い値より何cm離れているか
                few_add = few_chg * few_chg_diff
                # どれだけ画面から離れているか
                ans = sample_Len[value_abs_cnt] + few_add
        return ans

    # カメラで測定
    def switch_visibility_periodically(self):
        ret, frame = self.cap.read()

        # カラーをモノクロ化したキャプチャを代入(グレースケール化)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 顔の検出(minSizeによっては速度をあげれる)
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

        if self.mode_cnt < self.MODE:
            # テスト用
            print(self.mode_cnt)
            self.fw_count.insert(self.mode_cnt, self.fw)
            self.ew_count.insert(self.mode_cnt, self.ew)
            self.mode_cnt += 1
        else:
            # テスト用
            self.mode_cnt = 0
            print(self.mode_cnt)
            dis_Ans = self.distance(self.SAMPLE_LEN, self.FW_SAMPLE, self.EW_SAMPLE,
                                    statistics.mode(self.fw_count), statistics.mode(self.ew_count))
            if dis_Ans == -1:
                # 警告画面表示
                self.toggle_visibility_on()
                # コマンドライン
                print('10cm以下です!近すぎます!!\n')
            elif dis_Ans == -2:
                # ぼかしの処理
                self.toggle_visibility_off()
                print('70cm以上離れています!!\n')
            else:
                # 30以下
                if dis_Ans < 30:
                    # ぼかしの処理
                    self.toggle_visibility_on()
                    # コマンドライン
                    print('顔が近いので少し離れてください')
                # 30以上
                elif dis_Ans >= 30:
                    self.toggle_visibility_off()
                    # ぼかし
                print('%.2fcm\n' % dis_Ans)    # 小数第２位まで出力

            # カウントのリセット
            self.fw_count = []
            self.ew_count = []

        # self.toggle_visibility()  # 初回実行
        # 0.1秒後に再度切り替える
        self.root.after(100, self.switch_visibility_periodically)

# threadで
    # def update_gui_thread(self):
    #     while True:
    #         self.switch_visibility_periodically()
    #         time.sleep(0.1)


if __name__ == "__main__":
    root = tk.Tk()
    app = MosaicForm(root)
    root.mainloop()
