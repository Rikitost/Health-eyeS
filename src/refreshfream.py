import cv2
import numpy as np
import win32gui
import win32con
import win32ui
import win32api
import ctypes
import keyboard


def refresh_window():
    global original_desktop_image

    if original_desktop_image is not None:
        # 開いているウィンドウを閉じる
        cv2.destroyAllWindows()

        # オリジナルのデスクトップ画像に戻す
        img_data = original_desktop_image.tobytes()
        set_blur(img_data)

    # # ウィンドウハンドルを取得
    # hwnd = win32gui.GetDesktopWindow()
    # ctypes.windll.user32.InvalidateRect(hwnd, None, True)
    # ctypes.windll.user32.UpdateWindow(hwnd)

    # ウィンドウを閉じる
    # cv2.destroyAllWindows()

    # # GUIリソースの解放
    # win32gui.ReleaseDC(hwnd, hwnd_dc)
    # win32gui.DeleteObject(save_bitmap.GetHandle())
