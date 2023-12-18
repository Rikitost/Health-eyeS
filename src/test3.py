import tkinter as tk
import pygetwindow as gw
import pyautogui


class FullscreenTransparentWindow:
    def __init__(self):
        self.root = tk.Tk()

        # ウィンドウを最大化
        self.root.attributes('-zoomed', True)
        # ウィンドウの装飾を無効化
        self.root.overrideredirect(True)
        # ウィンドウの透明度を設定
        self.root.attributes("-alpha", 0.5)

        # クリックイベントが背後のウィンドウに渡るようにする
        self.root.bind("<Button-1>", self.pass_click_to_background)

        # 透明でないウィジェットを作成
        frame = tk.Frame(self.root, width=200, height=200, bg='white')
        frame.pack()

    def pass_click_to_background(self, event):
        # クリックイベントを背後のウィンドウに送る
        hwnd = gw.getWindowsWithTitle("Full Screen")[0]._hWnd
        pyautogui.click(button='left', x=event.x_root, y=event.y_root,
                        clicks=1, interval=0.0, buttonDown=None, buttonUp=None, duration=0)


if __name__ == "__main__":
    app = FullscreenTransparentWindow()
    app.root.mainloop()
