import customtkinter as ctk 
import tkinter.messagebox as tkmb 
from tkinter import ttk
import os
# Selecting GUI theme - dark, light , system (for system default) 
ctk.set_appearance_mode("white") 

# Selecting color theme - blue, green, dark-blue 
ctk.set_default_color_theme("blue") 

app = ctk.CTk() 
app.geometry("400x500") 
app.title("設定画面") 

class App(ctk.CTk):
    def __init__():
        super().__init__()

    def setting(): 
        Timelimit = ""
        password = ""
        new_window = ctk.CTkToplevel(app) 
        new_window.title("") 
        new_window.geometry("350x350") 

    def close_app():
        app.destroy()

    
    # スタイルの作成
    style = ttk.Style()
    style.configure("Red.TButton", background='red')

    custom_font = ctk.CTkFont(family="fantasy", size=14, weight="bold")

    #フレームの作成
    frame = ctk.CTkFrame(app)
    frame.configure(width=150, height=50)
    frame.grid(row=12, column=0, pady=12, padx=10,sticky="w")

    custom_font = ctk.CTkFont(size=20)
    label_title = ctk.CTkLabel(app, text="Health-eyeS", font=custom_font) 
    label_title.grid(row=0, column=0, pady=20) 

    label_line = ctk.CTkLabel(app, text='________________________________________________________________')
    label_line.grid(row=0, column=0, pady=12, padx=10,rowspan=3) 

    label_password = ctk.CTkLabel(app, text='パスワード設定') 
    label_password.grid(row=2, column=0,padx=10, pady=10, sticky='w') 

    label_line = ctk.CTkLabel(app, text='________________________________________________________________')
    label_line.grid(row=1, column=0, pady=12, padx=10,rowspan=3) 

    label_newpassword = ctk.CTkLabel(app, text='新しいパスワード') 
    label_newpassword.grid(row=3, column=0,padx=10, pady=10, sticky='w') 

    user_pass = ctk.CTkEntry(app, placeholder_text="半角数字4桁", show="*") 
    user_pass.grid(row=3, column=0, pady=12, padx=10) 

    button_decision = ctk.CTkButton(app, text='決定', command=setting,width=50, height=5) 
    button_decision.grid(row=4, column=0,pady=12, padx=10) 

    label_line = ctk.CTkLabel(app, text='________________________________________________________________')
    label_line.grid(row=4, column=0, pady=12,padx=10,rowspan=3) 

    label_time = ctk.CTkLabel(app, text='制限時間設定') 
    label_time.grid(row=6, column=0, pady=10, padx=10,sticky='w') 

    label_line = ctk.CTkLabel(app, text='________________________________________________________________')
    label_line.grid(row=5, column=0, pady=12, padx=10,rowspan=4)

    label_newtime = ctk.CTkLabel(app, text='新しい制限時間') 
    label_newtime.grid(row=8, column=0, pady=12, padx=10,sticky='w')

    user_entry = ctk.CTkEntry(app, placeholder_text="半角数字(分)") 
    user_entry.grid(row=8, column=0, pady=12, padx=10) 

    button_decision = ctk.CTkButton(app, text='決定', command=setting,width=50, height=5) 
    button_decision.grid(row=9, column=0, pady=12, padx=10,) 

    label_realtime = ctk.CTkLabel(app, text='現在の制限時間') 
    label_realtime.grid(row=9, column=0, pady=12, padx=10,sticky='e')

    button_restart = ctk.CTkButton(app, text='適用して再起動', command=setting) 
    button_restart.grid(row=11, column=0, pady=5,padx=5,sticky='e') 

    label_rtime = ctk.CTkLabel(app, text='残り時間') 
    label_rtime.grid(row=11, column=0, pady=12, padx=10,sticky='w')

    #label_rtime = ctk.CTkLabel(frame, text='残り時間') 
    #label_rtime.grid(row=12, column=0, pady=12, padx=10,sticky='w')

    button_exit = ctk.CTkButton(app, text='アプリを終了', command=close_app,fg_color='red') 
    button_exit.grid(row=12, column=0, pady=6, padx=5,sticky='e')


    app.mainloop()
