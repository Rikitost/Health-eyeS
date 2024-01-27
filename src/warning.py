# 警告の画面
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

# ファイルをインポート
# グローバル変数
import end_flg_value as gend  # 終了フラグ 0:継続 1:終了(flg)
# 注意画面のフラグ(0:非表示,1:表示)
import warning_flg as warn
# 時間切れ(0;継続,1:終了)
import time_limit as limit


# 注意画面の設定等
def rootwin():
    # 注意画面の表示関数
    def toggle_visibility_on():
        # ウィンドウの透明度を設定 (0: 完全透明, 1: 完全不透明)
        root.attributes("-alpha", 0.97)
        # 時間切れだった場合
        if limit.flg == 1:
            warning_label.config(text="時間切れです!!")
        else:
            warning_label.config(text="近いです!!画面から離れてください!!")
# 非表示---------------------------------------------------------------------------------------------------------------------

    def toggle_visibility_off():
        warning_label.config(text="")
        # ウィンドウの透明度を設定 (0: 完全透明, 1: 完全不透明)
        root.attributes("-alpha", 0.0)
        # root.attributes("-transparent", "white")
    # ----------------------------------------------------------------------------------

    # global root
    # global warning_label
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
    root.state('zoomed')
    # root.attributes("-fullscreen", True)
    # タスクバー
    root.overrideredirect(True)
    # 最前面
    root.attributes("-topmost", True)
    # ウィンドウ移動、サイズ変更の無効
    root.bind("<B1-Motion>", lambda event: "break")
    root.bind("<Configure>", lambda event: "break")

    # # 喚起のラベル
    warning_label = tk.Label(root, text="", font=50)
    warning_label.pack()
    # warning_label.grid(row=5, column=5, padx=20, pady=10)  # 行0、列0に配置し、パディングを設定

    # 初期設定のためのoff
    toggle_visibility_off()

    def warning():
        # 終わりのフラグ
        if gend.flg == 1:
            toggle_visibility_off()
            root.quit()
            # root.destroy()
        else:
            # 注意画面の判定(近い時と時間切れ)
            if warn.flg == 1 or limit.flg == 1:
                # 注意画面のon
                toggle_visibility_on()
            else:
                # 注意画面のoff
                toggle_visibility_off()
            # 1秒ごとに監視いたします
            root.after(1000, warning)

    root.after(100, warning)

    root.mainloop()


if __name__ == '__main__':
    warn.flg = 0
    rootwin()
