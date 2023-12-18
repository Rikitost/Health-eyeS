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
        # 初手は非表示透明度0
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


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()


# # 顔を認識し、カメラから顔(目)までの距離を出す
# # 一定間隔おきに距離を出す
# # キー入力「0」で即座に距離を出す（精度低）
# # キー入力「1」でcmの表記位置変更
# # キー入力「Esc」で終了
# # 画面サイズ1280,720で計測

# # 追加行大体 importでファイルtimesetを追加
# # 148
# # 194から203ぐらい

# # import
# import cv2
# import sys
# import statistics   # 最頻値
# import tkinter as tk
# import threading
# import time
# from plyer import notification
# import timeset
# # ぼかしの処理
# import numpy as np
# import win32gui
# import win32con
# import win32ui
# import win32api
# import ctypes
# # import mosaic
# # import refreshfream

# # --------------------------------------------------------------------------------------------------------
# # グローバル変数: オリジナルのデスクトップ画像
# original_desktop_image = None
# screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) * 2
# screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) * 2

# # 初回のぼかし処理フラグ
# first_mosaic = True

# # ウィンドウを非表示にする関数


# def hide_window(hwnd):
#     win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

# # ウィンドウを表示にする関数


# def show_window(hwnd):
#     win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)

# # ぼかしをかける関数


# def mosaic():
#     global original_desktop_image, first_mosaic

#     # ウィンドウスクリーンのキャプチャ
#     hwnd = win32gui.GetDesktopWindow()
#     hide_window(hwnd)  # ウィンドウを非表示にする

#     hwnd_dc = win32gui.GetWindowDC(hwnd)
#     mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
#     save_dc = mfc_dc.CreateCompatibleDC()
#     save_bitmap = win32ui.CreateBitmap()
#     save_bitmap.CreateCompatibleBitmap(mfc_dc, screen_width, screen_height)
#     save_dc.SelectObject(save_bitmap)
#     save_dc.BitBlt((0, 0), (screen_width, screen_height),
#                    mfc_dc, (0, 0), win32con.SRCCOPY)

#     # ビットマップから画像データを取得
#     bmp_info = save_bitmap.GetInfo()
#     bmp_data = save_bitmap.GetBitmapBits(True)
#     image_np = np.frombuffer(bmp_data, dtype=np.uint8).reshape(
#         screen_height, screen_width, 4)

#     # 画像データを保存
#     if first_mosaic:
#         original_desktop_image = image_np.copy()
#         first_mosaic = False

#     # 画面全体にぼかしをかける
#     blur_kernel_size = (101, 101)
#     blurred_image = cv2.GaussianBlur(image_np, blur_kernel_size, 0)

#     # デスクトップにぼかしを適用
#     img_data = blurred_image.tobytes()
#     set_blur(img_data)

#     show_window(hwnd)  # ウィンドウを再表示

# # ぼかし解除の関数


# def unmosaic():
#     global original_desktop_image

#     if original_desktop_image is not None:
#         # 開いているウィンドウを閉じる
#         cv2.destroyAllWindows()

#         # オリジナルのデスクトップ画像に戻す
#         img_data = original_desktop_image.tobytes()
#         set_blur(img_data)

# # ぼかしをセットする関数


# def set_blur(img_data):
#     # BITMAPINFOHEADER構造体の作成
#     class BITMAPINFOHEADER(ctypes.Structure):
#         _fields_ = [
#             ("biSize", ctypes.c_uint32),
#             ("biWidth", ctypes.c_long),
#             ("biHeight", ctypes.c_long),
#             ("biPlanes", ctypes.c_short),
#             ("biBitCount", ctypes.c_short),
#             ("biCompression", ctypes.c_uint32),
#             ("biSizeImage", ctypes.c_uint32),
#             ("biXPelsPerMeter", ctypes.c_long),
#             ("biYPelsPerMeter", ctypes.c_long),
#             ("biClrUsed", ctypes.c_uint32),
#             ("biClrImportant", ctypes.c_uint32),
#         ]

#     bmi_header = BITMAPINFOHEADER()
#     bmi_header.biSize = ctypes.sizeof(BITMAPINFOHEADER)
#     bmi_header.biWidth = screen_width
#     bmi_header.biHeight = -screen_height
#     bmi_header.biPlanes = 1
#     bmi_header.biBitCount = 32
#     bmi_header.biCompression = win32con.BI_RGB

#     # BITMAPINFO構造体の作成
#     class BITMAPINFO(ctypes.Structure):
#         _fields_ = [("bmiHeader", BITMAPINFOHEADER),
#                     ("bmiColors", ctypes.c_ulong * 3)]

#     bmi = BITMAPINFO()
#     bmi.bmiHeader = bmi_header

#     hdc = win32gui.GetDC(0)
#     ctypes.windll.gdi32.SetDIBitsToDevice(
#         hdc, 0, 0, screen_width, screen_height,
#         0, 0, 0, screen_height, img_data, ctypes.byref(
#             bmi), win32con.DIB_RGB_COLORS
#     )
#     win32gui.ReleaseDC(0, hdc)


# # 入力された値(fw,ew)から距離を求める関数--------------------------------------------------------------------


# def distance(sampleLen, fwSample, ewSample, fw, ew):
#     valuesAbs = []      # 入力された値xと事前に計測された値との絶対値を格納
#     cnt = 0             # カウントの役割をする変数
#     ans = 0             # 顔と画面との距離を格納
#     standard = 90       # ewとfwのどちらを距離算出に使うかの基準数値 (90は50cmのとき)

#     if ew >= standard:             # ewが基準値より小さければewを計算に使用
#         for i in ewSample:          # ewとの差の絶対値を格納
#             valuesAbs.insert(cnt, abs(i - ew))
#             cnt += 1

#         valuesAbs_sorted = sorted(valuesAbs)        # 絶対値の値たちを昇順にソートして格納

#         cnt = 0
#         for i in valuesAbs:         # ewに一番近い値（絶対値）の要素番号を見つける
#             if i == valuesAbs_sorted[0]:
#                 break
#             cnt += 1

#         if ew > ewSample[0]:        # 距離が恐らく10cm以下の場合
#             ans = -1
#         elif ew == ewSample[cnt]:       # ewとewに最も近い値が等しい場合
#             ans = sampleLen[cnt]
#         elif ew > ewSample[cnt]:        # ewに最も近い値がewよりも小さい場合
#             data1 = abs(ewSample[cnt] - ewSample[cnt-1])        # ewの大きさの差
#             data2 = abs(sampleLen[cnt] - sampleLen[cnt-1]
#                         ) / data1  # 1cmごとに変化するewの大きさ
#             # ewより小さくて最も近い値からどれだけの差があるか
#             data3 = abs(ew - ewSample[cnt-1])
#             data4 = data2 * data3                               # ewより小さくて最も近い値より何cm離れているか
#             # どれだけ画面から離れているか
#             ans = sampleLen[cnt-1] + data4
#         else:                       # ewに最も近い値がewよりも大きい場合
#             data1 = abs(ewSample[cnt] - ewSample[cnt+1])        # ewの大きさの差
#             data2 = abs(sampleLen[cnt] - sampleLen[cnt+1]
#                         ) / data1  # ewが1増えるごとに何cm増えるか
#             # ewより大きくて最も近い値からどれだけの差があるか
#             data3 = abs(ew - ewSample[cnt])
#             data4 = data2 * data3                               # ewより大きくて最も近い値より何cm離れているか
#             # どれだけ画面から離れているか
#             ans = sampleLen[cnt] + data4
#     else:       # ewが基準値より大きければfwを計算に使用

#         for i in fwSample:                      # fwとの差の絶対値を格納
#             valuesAbs.insert(cnt, abs(i - fw))
#             cnt += 1

#         valuesAbs_sorted = sorted(valuesAbs)    # 絶対値の値たちをソート（昇順）を格納

#         cnt = 0
#         for i in valuesAbs:                     # fwに一番近い値（絶対値）の要素番号を見つける
#             if i == valuesAbs_sorted[0]:
#                 break
#             cnt += 1

#         if fw < fwSample[len(fwSample)-1]:  # 距離が恐らく70cm以上の場合
#             ans = -2
#         elif fw == fwSample[cnt]:       # fwとfwに最も近い値が等しい場合
#             ans = sampleLen[cnt]
#         elif fw > fwSample[cnt]:        # fwに最も近い値がfwよりも小さい場合
#             data1 = abs(fwSample[cnt] - fwSample[cnt-1])        # fwの大きさの差
#             data2 = abs(sampleLen[cnt] - sampleLen[cnt-1]
#                         ) / data1  # 1cmごとに変化するfwの大きさ
#             # fwより小さくて最も近い値からどれだけの差があるか
#             data3 = abs(fw - fwSample[cnt-1])
#             data4 = data2 * data3                               # fwより小さくて最も近い値より何cm離れているか
#             # どれだけ画面から離れているか
#             ans = sampleLen[cnt-1] + data4
#         else:                           # fwに最も近い値がfwよりも大きい場合
#             data1 = abs(fwSample[cnt] - fwSample[cnt+1])        # fwの大きさの差
#             data2 = abs(sampleLen[cnt] - sampleLen[cnt+1]
#                         ) / data1  # fwが1増えるごとに何cm増えるか
#             # fwより大きくて最も近い値からどれだけの差があるか
#             data3 = abs(fw - fwSample[cnt])
#             data4 = data2 * data3                               # fwより大きくて最も近い値より何cm離れているか
#             # どれだけ画面から離れているか
#             ans = sampleLen[cnt] + data4
#     return ans


# # ---------------------------------------------------------------------------------------------------------
# # カスケード分類器のパスを各変数に代入
# # pythonの実行
# fase_cascade_path = 'data\haarcascades\haarcascade_frontalface_default.xml'
# eye_cascade_path = 'data\haarcascades\haarcascade_eye.xml'
# # カスケード分類器の読み込み
# face_cascade = cv2.CascadeClassifier(fase_cascade_path)
# eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

# # Webカメラの準備（引数でカメラ指定、0は内臓カメラ）
# cap = cv2.VideoCapture(0)

# FRAME_LINESIZE = 2       # 顔に四角を描画する際の線の太さ
# FRAME_RGB_G = (0, 255, 0)  # 四角形を描画する際の色を格納(緑)
# FRAME_RGB_B = (255, 0, 0)  # 四角形を描画する際の色を格納(青)
# cnt = 0     # カウントの際に使用
# textChange = 0  # cmの表記を画面上部に固定にするか、顔に追従するかの切り替え
# fw = 100    # 顔の大きさの初期値（起動時エラー回避のため初期値設定）
# fx = 100    # 顔のx座標の初期値
# fy = 100    # 顔のy座標の初期値
# ew = 100    # 目の大きさの初期値
# ex = 100    # 目のx座標の初期値
# ey = 100    # 目のy座標の初期値
# disAns = 0  # 計測した距離を格納
# fwcount = []  # fwを一時的に格納（最頻値を出すために使用）
# ewcount = []  # ewを一時的に格納（最頻値を出すために使用）
# MODECOUNT = 50  # 最頻値を出すときの要素数（この値を変更することで計測値(cm)の正確性と計測にかかる時間が変化）
# # fwSample,ewSampleに対応した顔とカメラとの距離(cm)
# sampleLen = [10,   15,  20,  30,  40,  50,  60,  70]
# fwSample = [999, 999, 999, 999, 431, 348, 292, 253]       # 事前に計測した距離に対応する顔の大きさ
# ewSample = [268, 214, 161, 118,  90,  62,  59,  54]       # 事前に計測した距離に対応する目の大きさ

# # cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
# # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
# # cap.set(cv2.CAP_PROP_FPS, 10)           # カメラFPSを60FPSに設定
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラ画像の横幅を1280に設定
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # カメラ画像の縦幅を720に設定
# # print cap.get(cv2.CAP_PROP_FPS)
# # print cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# # print cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


# # -----------------------------------------------------------
# # もしカメラが起動していなかったら終了する
# if cap.isOpened() is False:
#     print("カメラが起動していないため終了しました")
#     sys.exit()


# # 時間の設定のフォーム
# timeset.timeset_task()


# # 無限ループで読み取った映像に変化を加える（1フレームごとに区切って変化）
# while True:
#     ret, frame = cap.read()

#     # カラーをモノクロ化したキャプチャを代入(グレースケール化)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # 顔の検出
#     faces = face_cascade.detectMultiScale(
#         gray, scaleFactor=1.3, minNeighbors=5)

#     # 目の検出
#     eyes = eye_cascade.detectMultiScale(
#         gray, scaleFactor=1.3, minNeighbors=5)

#     # 第1引数   効果を適応する画像
#     # 第2引数   矩形の左上隅の座標
#     # 第3引数   矩形の右下隅の座標
#     # 第4引数   矩形の色
#     # 第5引数   描画する線の太さ（-1以下だと塗りつぶし）
#     # 顔に四角形(矩形)を描画する
#     for (fx, fy, fw, fh) in faces:
#         cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh),
#                       FRAME_RGB_G, FRAME_LINESIZE)

#     # 目に四角形(矩形)を描画する
#     for (ex, ey, ew, eh) in eyes:
#         cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh),
#                       FRAME_RGB_B, FRAME_LINESIZE)

#     if cnt < MODECOUNT:
#         fwcount.insert(cnt, fw)
#         ewcount.insert(cnt, ew)
#         cnt += 1
#     else:
#         cnt = 0
#         disAns = distance(sampleLen, fwSample, ewSample,
#                           statistics.mode(fwcount), statistics.mode(ewcount))
#         if disAns == -1:
#             # ぼかしの処理
#             mosaic()
#             # コマンドライン
#             print('10cm以下です!近すぎます!!\n')
#         elif disAns == -2:
#             # ぼかしの処理
#             unmosaic()
#             print('70cm以上離れています!!\n')
#         else:
#             if disAns < 30:
#                 # ぼかしの処理
#                 mosaic()
#                 # # 通知の設定
#                 # notification_title = 'ちかい'
#                 # notification_message = 'ちかづきすぎですはなれて！'
#                 # notification_timeout = 10  # 表示時間（秒）

#                 # # 通知を送る
#                 # notification.notify(
#                 #     title=notification_title,
#                 #     message=notification_message,
#                 #     timeout=notification_timeout
#                 # )
#                 # コマンドライン
#                 print('顔が近いので少し離れてください')
#             elif disAns >= 30:
#                 unmosaic()
#             print('%.2fcm\n' % disAns)    # 小数第２位まで出力

# # カウントのリセット
#         fwcount = []
#         ewcount = []

#     # 画面に距離を表示
#     if disAns == -1:
#         # imshowで表示させている
#         cv2.putText(frame,
#                     # テキスト(英数字のみ)
#                     text="Less than 10 cm! Please stay away!!",
#                     org=(0, 30),       # 座標
#                     # フォント(デフォルト cv2.FONT_HERSHEY_SIMPLEX)
#                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                     # 文字の縮尺(本来は1.0を設定すればいいが顔の大きさに連動して文字も縮尺を変えるためfwを掛け、微調整で255で割っている)
#                     fontScale=(1.0),
#                     color=(0, 0, 255),  # 文字の色(顔枠と別の色)
#                     thickness=2,        # 文字の太さ
#                     lineType=cv2.LINE_AA)    # アルゴリズムの種類（文字を滑らかにするかどうか,デフォルトはcv2.LINE_8）
#     elif disAns == -2:
#         # 元データ
#         cv2.putText(frame,
#                     text="Over 70 cm! Please come closer!!",
#                     org=(0, 30),
#                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                     fontScale=(1.0),
#                     color=(0, 0, 255),
#                     thickness=2,
#                     lineType=cv2.LINE_AA)
#     else:
#         if disAns < 30 and disAns != 0:     # 30cm未満の場合、警告を出す
#             cv2.putText(frame,
#                         text="Less than 30 cm! Please stay away!!",
#                         org=(370, 60),
#                         fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                         fontScale=(1.0),
#                         color=(0, 0, 255),
#                         thickness=2,
#                         lineType=cv2.LINE_AA)
#         if textChange == 0:     # 現在cmのテキストを頭上に表示する
#             cv2.putText(frame,
#                         text=str(round(disAns, 2))+"cm",
#                         org=(fx, fy-6),
#                         fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                         fontScale=(1.0),
#                         color=(0, 255, 0),
#                         thickness=2,
#                         lineType=cv2.LINE_AA)
#         else:                   # 現在cmのテキストを画面上部に固定で表示する
#             cv2.putText(frame,
#                         text=str(round(disAns, 2))+"cm",
#                         org=(600, 30),
#                         fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                         fontScale=(1.0),
#                         color=(0, 255, 0),
#                         thickness=2,
#                         lineType=cv2.LINE_AA)

#     # 結果を表示
#     # cv2.imshow('gray', gray)
#     # 画像の表示
#     # cv2.imshow('YourFace', frame)

#     # キー入力を10ms待つ
#     # 「Esc」を押すと無限ループから抜けて終了処理に移る
#     key = cv2.waitKey(10)
#     if key == 27:
#         break
#     elif key == ord('0'):       # 「0」を押すと距離が即座に出る
#         disAns = distance(sampleLen, fwSample, ewSample, fw, ew)
#         print('%.2fcm\n' % disAns)
#     elif key == ord('1'):
#         if textChange == 0:     # 現在cmのテキストを頭上に表示している場合、画面上部に固定化する
#             textChange = 1
#         else:                  # 現在cmのテキストを画面上部に固定化している場合、頭上に表示する
#             textChange = 0

# # 終了処理
# unmosaic()
# # カメラのリソースを開放する
# cap.release()
# # OpenCVのウィンドウをすべて閉じる
# cv2.destroyAllWindows()
