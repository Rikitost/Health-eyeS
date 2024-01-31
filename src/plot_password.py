import customtkinter as ctk 
import tkinter.messagebox as tkmb 

# Selecting GUI theme - dark, light , system (for system default) 
ctk.set_appearance_mode("White") 

# Selecting color theme - blue, green, dark-blue 
ctk.set_default_color_theme("blue") 

app = ctk.CTk() 
app.geometry("350x250") 
app.title("パスワード入力") 


def login(): 

    password = ""
    new_window = ctk.CTkToplevel(app) 

    new_window.title("あああ") 

    new_window.geometry("350x150") 

    



  
frame = ctk.CTkFrame(master=app) 
frame.pack(pady=20,padx=40,fill='both',expand=True) 
  
label = ctk.CTkLabel(master=frame,text='パスワードを入力してください') 
label.pack(pady=12,padx=10) 
  
  

  
user_pass= ctk.CTkEntry(master=frame,placeholder_text="半角数字4桁",show="*") 
user_pass.pack(pady=12,padx=10) 
  
  
button = ctk.CTkButton(master=frame,text='決定',command=login) 
button.pack(pady=12,padx=10) 
  

  
  
app.mainloop()