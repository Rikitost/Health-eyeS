import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time
# ファイルをインポート
import password_input
# グローバル変数
# 時間計測スレッドの終了フラグ 0:継続 1:終了(flg)
import clock_thread_end_flg as gclock_thread_end
# 設定画面の終了フラグ 0:継続 1:終了(flg)
import setting_thread_end_flg as gsetting_thread_end
# 設定入力画面を操作している間設定選択画面を操作できなくするフラグ 0:解除 1:ロック (flg)
import form_lock_flg as gformlock
import end_flg_value as gend  # 終了フラグ 0:継続 1:終了(flg)
import time_count_value as gtime_cnt  # 時間計測のカウント(val)
import time_count_flg as gtime_flg  # 計測フラグ 0:時間計測中 1:時間計測終了(flg)
import pass_sec_value as gpass_sec  # パスワードが解かれたか 0:ロック 1:解除 (flg)
import restart_flg as grestart_flg  # 再起動フラグ 0:再起動待機 1:再起動 (flg)
# パスワード入力画面が閉じられたか 0:閉じられていない 1:閉じられた(flg)
import password_form_end_flg as gpass_form_end
import password_windowup_flg as gpass_windowup  # パスワード入力画面を起動する


def globalfile_reset():
    global gend
    global gformlock
    global gtime_cnt
    global gtime_flg
    global gpass_sec
    global grestart_flg
    gformlock.flg = 0
    gend.flg = 0
    gtime_cnt.val = 0
    gtime_flg.flg = 1
    gpass_sec.flg = 0
    grestart_flg.flg = 0    # 再起動フラグ 0:再起動待機 1:再起動 (flg)

# ファイル単体で実行する用初期化関数


def global_set():
    global gend
    global gformlock
    global gtime_cnt
    global gtime_flg
    global gpass_sec
    global grestart_flg
    gformlock.flg = 0
    gend.flg = 0
    gtime_cnt.val = 0
    gtime_flg.flg = 1
    gpass_sec.flg = 0
    grestart_flg.flg = 0    # 再起動フラグ 0:再起動待機 1:再起動 (flg)
    gpass_form_end.flg = 0
