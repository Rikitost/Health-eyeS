import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# ファイルをインポート
# グローバル変数
import end_flg_value as gend  # 終了フラグ 0:継続 1:終了(flg)


# formの表示関数
def toggle_visibility_on():
    global root
    # ウィンドウの透明度を設定 (0: 完全透明, 1: 完全不透明)
    root.attributes("-alpha", 0.97)
# 非表示---------------------------------------------------------------------------------------------------------------------


def toggle_visibility_off():
    global root
    # ウィンドウの透明度を設定 (0: 完全透明, 1: 完全不透明)
    root.attributes("-alpha", 0)
# ----------------------------------------------------------------------------------


# formの設定等
def rootwin():
    # form
    global root
    root = tk.Tk()
    root.title("注意画面")
    # ウィンドウの初期設定
    # ウィンドウの表示
    root.deiconify()
    # ウィンドウを透明クリック可能にする

    root.wm_attributes("-transparentcolor", "white")
    root.geometry("{0}x{1}+0+0".format(3000, 3000))
    # ウィンドウの初期設定
    # 画面全体
    # root.attributes("-zoomed", "1")
    # root.attributes("-fullscreen", True)
    # タスクバー
    root.overrideredirect(True)
    # 最前面
    # root.attributes("-topmost", True)
    # ウィンドウ移動、サイズ変更の無効
    root.bind("<B1-Motion>", lambda event: "break")
    root.bind("<Configure>", lambda event: "break")
    toggle_visibility_off()

    # この段階で root ウィンドウを終了
    if gend.flg == 1:
        root.quit()
        root.destroy()

    # root.after(100, HealtheyeS)
    root.mainloop()


if __name__ == '__main__':
    rootwin()
