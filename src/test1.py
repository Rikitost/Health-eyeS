from PIL import Image, ImageTk

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
import win32gui
import win32con
import win32ui
import win32api
import ctypes
import pygetwindow as gw
import pyautogui
import keyboard


class CameraViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Viewer")

        # OpenCVカメラキャプチャの初期化
        self.cap = cv2.VideoCapture(0)  # カメラの番号を指定

        # ウィンドウを全画面に設定
        self.root.attributes("-fullscreen", True)

        # タスクバーに表示させないように設定
        self.root.overrideredirect(True)

        # ウィンドウを常に最前面に表示する
        self.root.attributes("-topmost", True)

        # ウィンドウの移動とサイズ変更を無効にする
        self.root.bind("<B1-Motion>", lambda event: "break")
        self.root.bind("<Configure>", lambda event: "break")

        # 初期設定------------------------------
        # カメラの初期設定と準備
        self.init_camera()

        # 初期設定
        self.init_config()

        # 切り替えボタンを作成
        toggle_button = tk.Button(
            self.root, text="Toggle Visibility", command=self.toggle_visibility)
        toggle_button.pack(pady=20)

        # Canvasを作成してウィンドウに配置
        self.canvas = tk.Label(self.root)
        self.canvas.pack()

        # ウィンドウを閉じるときにカメラを解放
        self.root.protocol("WM_DELETE_WINDOW", self.release_camera)

        # カメラ表示を開始
        self.update_frame()

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

    def toggle_visibility(self):
        if self.root.state() == 'withdrawn':
            self.root.top()  # ウィンドウを最前面に設定
            self.root.deiconify()  # ウィンドウを表示
            self.update_frame()
        else:
            self.root.withdraw()  # ウィンドウを非表示
            self.release_camera()  # カメラを解放

    def update_frame(self):
        ret, frame = self.cap.read()

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
            disAns = distance(sampleLen, fwSample, ewSample,
                              statistics.mode(fwcount), statistics.mode(ewcount))
            if disAns == -1:
                # ぼかしの処理
                # コマンドライン
                print('10cm以下です!近すぎます!!\n')
            elif disAns == -2:
                # ぼかしの処理
                print('70cm以上離れています!!\n')
            else:
                if disAns < 30:
                    print('顔が近いので少し離れてください')
                elif disAns >= 30:
                    print(1)
                print('%.2fcm\n' % disAns)    # 小数第２位まで出力

    # カウントのリセット
            fwcount = []
            ewcount = []

        if ret:
            # カメラ画像をOpenCVのBGR形式からTkinter PhotoImage形式に変換
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)

            # Canvasに新しい画像を表示
            self.canvas.config(image=photo)
            self.canvas.image = photo

            # 10ミリ秒後にupdate_frame関数を再実行
            if self.root.state() == 'normal':
                self.root.after(10, self.update_frame)

    def release_camera(self):
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CameraViewerApp(root)
    root.mainloop()


# import tkinter as tk


# def toggle_visibility():
#     if root.state() == 'withdrawn':
#         root.deiconify()  # ウィンドウを表示
#     else:
#         root.withdraw()   # ウィンドウを非表示


# root = tk.Tk()

# # ウィンドウを全画面に設定
# root.attributes("-fullscreen", True)

# # タスクバーに表示させないように設定
# root.overrideredirect(True)

# # ウィンドウを常に最前面に表示する
# root.attributes("-topmost", True)

# # ウィンドウの移動とサイズ変更を無効にする
# root.bind("<B1-Motion>", lambda event: "break")
# root.bind("<Configure>", lambda event: "break")

# # 切り替えボタンを作成
# toggle_button = tk.Button(
#     root, text="Toggle Visibility", command=toggle_visibility)
# toggle_button.pack(pady=20)

# root.mainloop()


# from PIL import Image, ImageTk

# # import
# import cv2
# import sys
# import statistics   # 最頻値
# import tkinter as tk
# # 音
# # from plyer import notification
# import timeset
# # ぼかしの処理
# import numpy as np
# import win32gui
# import win32con
# import win32ui
# import win32api
# import ctypes
# import pygetwindow as gw
# import pyautogui
# import keyboard


# class CameraViewerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Camera Viewer")

#         # OpenCVカメラキャプチャの初期化
#         self.cap = cv2.VideoCapture(0)  # カメラの番号を指定

#         # ウィンドウを全画面に設定
#         self.root.attributes("-fullscreen", True)

#         # タスクバーに表示させないように設定
#         self.root.overrideredirect(True)

#         # ウィンドウを常に最前面に表示する
#         self.root.attributes("-topmost", True)

#         # ウィンドウの移動とサイズ変更を無効にする
#         self.root.bind("<B1-Motion>", lambda event: "break")
#         self.root.bind("<Configure>", lambda event: "break")

#         # 切り替えボタンを作成
#         toggle_button = tk.Button(
#             self.root, text="Toggle Visibility", command=self.toggle_visibility)
#         toggle_button.pack(pady=20)

#         # Canvasを作成してウィンドウに配置
#         self.canvas = tk.Label(self.root)
#         self.canvas.pack()

#         # ウィンドウを閉じるときにカメラを解放
#         self.root.protocol("WM_DELETE_WINDOW", self.release_camera)

#         # カメラ表示を開始
#         self.update_frame()

#     def toggle_visibility(self):
#         if self.root.state() == 'withdrawn':
#             self.root.top()  # ウィンドウを最前面に設定
#             self.root.deiconify()  # ウィンドウを表示
#             self.update_frame()
#         else:
#             self.root.withdraw()  # ウィンドウを非表示
#             self.release_camera()  # カメラを解放

#     def update_frame(self):
#         ret, frame = self.cap.read()
#         if ret:
#             # カメラ画像をOpenCVのBGR形式からTkinter PhotoImage形式に変換
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image = Image.fromarray(image)
#             photo = ImageTk.PhotoImage(image=image)

#             # Canvasに新しい画像を表示
#             self.canvas.config(image=photo)
#             self.canvas.image = photo

#             # 10ミリ秒後にupdate_frame関数を再実行
#             if self.root.state() == 'normal':
#                 self.root.after(10, self.update_frame)

#     def release_camera(self):
#         self.cap.release()
#         self.root.destroy()


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CameraViewerApp(root)
#     root.mainloop()


# # import tkinter as tk


# # def toggle_visibility():
# #     if root.state() == 'withdrawn':
# #         root.deiconify()  # ウィンドウを表示
# #     else:
# #         root.withdraw()   # ウィンドウを非表示


# # root = tk.Tk()

# # # ウィンドウを全画面に設定
# # root.attributes("-fullscreen", True)

# # # タスクバーに表示させないように設定
# # root.overrideredirect(True)

# # # ウィンドウを常に最前面に表示する
# # root.attributes("-topmost", True)

# # # ウィンドウの移動とサイズ変更を無効にする
# # root.bind("<B1-Motion>", lambda event: "break")
# # root.bind("<Configure>", lambda event: "break")

# # # 切り替えボタンを作成
# # toggle_button = tk.Button(
# #     root, text="Toggle Visibility", command=toggle_visibility)
# # toggle_button.pack(pady=20)

# # root.mainloop()
