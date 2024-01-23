import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

# ファイルをインポート
# グローバル変数
import end_flg_value as gend  # 終了フラグ 0:継続 1:終了(flg)
# 注意画面のフラグ(0:非表示,1:表示)
import warning_flg as warn


# formの設定等
def rootwin():
    # formの表示関数
    def toggle_visibility_on():
        # ウィンドウの透明度を設定 (0: 完全透明, 1: 完全不透明)
        root.attributes("-alpha", 0.97)
# 非表示---------------------------------------------------------------------------------------------------------------------

    def toggle_visibility_off():
        # ウィンドウの透明度を設定 (0: 完全透明, 1: 完全不透明)
        root.attributes("-alpha", 0)
    # ----------------------------------------------------------------------------------

    # form
    root = tk.Tk()
    root.title("注意画面")
    # ウィンドウの初期設定
    # ウィンドウの表示
    root.deiconify()
    # ウィンドウを透明クリック可能にする

    root.wm_attributes("-transparentcolor", "white")
    # root.geometry("{0}x{1}+0+0".format(3000, 3000))
    # ウィンドウの初期設定
    # 画面全体
    # root.attributes("-zoomed", "1")
    root.attributes("-fullscreen", True)
    # タスクバー
    root.overrideredirect(True)
    # 最前面
    root.attributes("-topmost", True)
    # ウィンドウ移動、サイズ変更の無効
    root.bind("<B1-Motion>", lambda event: "break")
    root.bind("<Configure>", lambda event: "break")

    # 注意画面の判定
    if warn.flg == 1:
        toggle_visibility_on()
    else:
        toggle_visibility_off()

    # 終わりのフラグ
    if gend.flg == 1:
        toggle_visibility_off()
        root.quit()
    else:
        # 1秒ごとに監視
        root.after(1000, rootwin)

    root.mainloop()


if __name__ == '__main__':
    rootwin()
