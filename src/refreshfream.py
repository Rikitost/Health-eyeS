import win32gui
import ctypes
import cv2


def refresh_window():
    # # ウィンドウハンドルを取得
    hwnd = win32gui.GetDesktopWindow()
    # ctypes.windll.user32.InvalidateRect(hwnd, None, True)
    # ctypes.windll.user32.UpdateWindow(hwnd)

    # ウィンドウを閉じる
    cv2.destroyAllWindows()

    # # GUIリソースの解放
    # win32gui.ReleaseDC(hwnd, hwnd_dc)
    # win32gui.DeleteObject(save_bitmap.GetHandle())
