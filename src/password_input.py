import tkinter as tk
import timeset
import threading

# import HealtheyeS

#グローバル変数をセット
import form_lock_flg as gformlock # 設定入力画面を操作している間設定選択画面を操作できなくするフラグ 0:解除 1:ロック (flg)
import pass_sec_value as gpass_sec  # パスワードが解かれたか 0:ロック 1:解除 (flg)
import end_flg_value as gend        # 終了フラグ 0:継続 1:終了(flg)


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

def pass_open():
    timeset.value_check(passset_text,warning_pass_label)
    #数値の入力方式が正しいか判定
    if timeset.value_check(passset_text,warning_pass_label) == True:
        # 入力されたパスワードを取得(int変換)
        input_pass = passset_text.get()
        
        # password.txtを読み込んでパスワードを取得
        f = open('src/password.txt', 'r')
        password = f.read()
        # print(password)
        # print(input_pass)
        # パスワードが設定されていない場合スキップする
        if password == "":
            f.close()
            gpass_sec.flg = 1
            formlock_off()
            passbox_form.quit()
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
                    # passbox_form.quit()
                    passbox_form.destroy()
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
    
    #パスワード入力画面を操作している間設定画面を操作できなくする
    formlock_on()
    passbox_form = tk.Tk()
    passbox_form.geometry('250x200')
    passbox_form.title('パスワードを入力してください')
    # 常に最前面に表示
    passbox_form.attributes("-topmost", True)
    
    
    # #×で閉じられないようにする
    passbox_form.protocol("WM_DELETE_WINDOW", click_close)
    
    # フォームのパスワード設定ラベル
    pass_label = tk.Label(passbox_form,text='パスワードを設定してください(半角数字4桁)')
    pass_label.pack()
    # 入力の制限
    validation_pass = passbox_form.register(timeset.on_validate_pass)

    # パスワード入力のテキストボックス
    passset_text = tk.Entry(passbox_form, validate="key", validatecommand=(
        validation_pass, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
    passset_text.pack()
    
    warning_pass_label = tk.Label(passbox_form,text='')
    warning_pass_label.pack()

    # 入力決定のボタン
    timeset_button = tk.Button(
        passbox_form,
        text='決定',
        command=lambda: pass_open()
    ).pack()
    
    
    passbox_form.mainloop()


def passbox():


    passbox_tk()

    # フォームの生成
    thread_passbox = threading.Thread(target=passbox_tk)
    thread_passbox.start()

if __name__ == '__main__':
    global_set()
    f = open('src/password.txt', 'r')
    password = f.read()
    f.close()
    passbox()