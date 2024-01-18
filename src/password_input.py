import tkinter as tk
import customtkinter as ctk 
import timeset
import threading

# import HealtheyeS

#グローバル変数をセット
import form_lock_flg as gformlock # 設定入力画面を操作している間設定選択画面を操作できなくするフラグ 0:解除 1:ロック (flg)
import pass_sec_value as gpass_sec  # パスワードが解かれたか 0:ロック 1:解除 (flg)
import end_flg_value as gend        # 終了フラグ 0:継続 1:終了(flg)
import password_form_end_flg as gpass_form_end # パスワード入力画面が閉じられたか 0:閉じられていない 1:閉じられた(flg)


def global_set():
    gpass_sec.flg = 0
#×で閉じられないようにする関数
def click_close():
    pass
def formlock_on():
    gformlock.flg = 1
def formlock_off():
    gformlock.flg = 0

def passbox_end():
    print("パスワードのウインドウを閉じました")
    passbox_form.quit()
    gpass_form_end.flg = 1

def pass_open():
    global gpass_sec
    
    timeset.value_check(passset_text,warning_pass_label)
    #数値の入力方式が正しいか判定
    if timeset.value_check(passset_text,warning_pass_label) == True:
        # 入力されたパスワードを取得(int変換)
        input_pass = passset_text.get()
        
        # password.txtを読み込んでパスワードを取得
        f = open('src/password.txt', 'r')
        password = f.read()
        # パスワードが設定されていない場合スキップする
        if password == "":
            f.close()
            gpass_sec.flg = 1
            formlock_off()
            print("パスワードを設定していないためスキップしやした")
            passbox_form.quit()
            # passbox_form.destroy()
        else:
            # パスワードが設定されている場合
            if input_pass != "":
                password = int(password)
                f.close()
                # パスワードが一致したら終了
                if int(input_pass) == password:
                    gpass_sec.flg = 1
                    formlock_off()
                    # HealtheyeS.toggle_visibility_off()
                    
                    # passbox_form.destroy()
                    print("パスワードが一致しました")
                    passbox_form.quit()
                    
                    # passbox_form.destroy()
                else:
                    warning_pass_label.config(text='パスワードが違います')

            else:
                warning_pass_label.config(text='パスワードが違います')
    else:
        return

def passbox_tk():
    global passbox_form
    global passset_text
    global warning_pass_label
    
    gpass_form_end.flg = 0
    # Selecting GUI theme - dark, light , system (for system default) 
    ctk.set_appearance_mode("White") 

    # Selecting color theme - blue, green, dark-blue 
    ctk.set_default_color_theme("blue") 

    #パスワード入力画面を操作している間設定画面を操作できなくする
    formlock_on()
    passbox_form = ctk.CTk() 
    passbox_form.geometry("350x250")
    passbox_form.title("パスワード入力")
    # 常に最前面に表示
    # passbox_form.attributes("-topmost", True)
    
    
    # #×で閉じられないようにする
    passbox_form.protocol("WM_DELETE_WINDOW", click_close)
    # フレームの生成
    passbox_frame = ctk.CTkFrame(master=passbox_form) 
    passbox_frame.pack(pady=20,padx=40,fill='both',expand=True)
    # フォームのパスワード設定ラベル
    pass_label = ctk.CTkLabel(master=passbox_frame,text='パスワードを入力してください')
    pass_label.pack(pady=12,padx=10)
    # 入力の制限
    validation_pass = passbox_form.register(timeset.on_validate_pass)
    # パスワード入力のテキストボックス
    passset_text= ctk.CTkEntry(master=passbox_frame, validate="key", validatecommand=(
        validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'),placeholder_text="半角数字4桁",show="*") 
    passset_text.pack(pady=12,padx=10) 
    # パスワード入力のテキストボックス
    # passset_text = tk.Entry(passbox_form, validate="key", validatecommand=(
    #     validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
    # passset_text.pack()
    
    warning_pass_label = tk.Label(passbox_form,text='')
    warning_pass_label.pack()

    # 入力決定のボタン
    # timeset_button = ctk.CTkButton(master=passbox_frame,text='決定',command=lambda: pass_open())
    # timeset_button.pack(pady=12,padx=10)
    timeset_button = ctk.CTkButton(
        passbox_frame,
        text='決定',
        command=lambda: pass_open()
    )
    timeset_button.pack(pady=12,padx=10)
    
    
    passbox_form.mainloop()
    # del passbox_form


# def passbox():


#     passbox_tk()

#     # フォームの生成
#     thread_passbox = threading.Thread(target=passbox_tk)
#     thread_passbox.start()

if __name__ == '__main__':
    global_set()
    f = open('src/password.txt', 'r')
    password = f.read()
    f.close()
    passbox_tk()