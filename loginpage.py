import customtkinter as CTk
import tkinter as tk
from registerpage import open_register_window
import tkinter.messagebox as messagebox
import sys
import json
import os
import sqlite3

CTk.set_appearance_mode("light")

# Basic Window Configuration
root = CTk.CTk()
root.title("MEPIO - Login")
root.geometry("720x440")
root.configure(fg_color="#f0f4ff")
root.resizable(True, True)

container = CTk.CTkFrame(root, fg_color="#ffffff", corner_radius=12, width=720, height=440)
container.place(relx=0.5, rely=0.5, anchor="center")
container.pack_propagate(False)

# Left Brand Area 
left = tk.Canvas(container, width=280, height=440, highlightthickness=0, bg="#2d6cdf")
left.place(x=0, y=0)
left.create_oval(-60, -60, 240, 240, fill="#4a84e8", outline="")
left.create_text(120, 100, text="MEPIO", font=("Georgia", 48, "bold"), fill="white", anchor="center")
left.create_text(36, 330, text="Welcome", font=("Helvetica", 18, "bold"), fill="white", anchor="w")
left.create_text(36, 358, text="Micro-E-commerce Profit\n& Inventory Optimizer", font=("Helvetica", 9), fill="#b8d4ff", anchor="w", justify="left")

# Right Login Form Area
right = CTk.CTkFrame(container, fg_color="#ffffff", width=440, height=440, corner_radius=0)
right.place(x=280, y=0)



def open_register():
    root.withdraw()
    open_register_window(root)

# Divider Shadow
shadow = CTk.CTkFrame(container, fg_color="#d0d8f0", width=4, height=440, corner_radius=0)
shadow.place(x=280, y=0)

# Titles and Headers
title_label = CTk.CTkLabel(right, text="Welcome to MEPIO", font=("Helvetica", 17, "bold"), fg_color="#ffffff", text_color="#1a1a1a")
title_label.place(x=44, y=95)

no_account_lbl = CTk.CTkLabel(right, text="Don't have an account?", font=("Helvetica", 12), text_color="#7a7a7a")
no_account_lbl.place(x=100, y=380) 

   
register_btn = CTk.CTkButton(right, text="Register Now", font=("Helvetica", 12, "bold", "underline"), 
                                 fg_color="transparent", hover_color="#f0f4ff", text_color="#3498db",
                                 width=80, height=20, cursor="hand2", anchor="w",
                                 command=open_register)
register_btn.place(x=245, y=384)



def make_field(parent, y, icon, title, show=None):
    
    title_label = CTk.CTkLabel(parent, text=f"{icon}  {title}", font=("Helvetica", 13, "bold"), text_color="#1a1a1a")
    title_label.place(x=44, y=y)
    
    
    entry = CTk.CTkEntry(parent, width=350, height=45, font=("Helvetica", 14), 
                         fg_color="#fcfcfc", border_color="#dcdde1", border_width=1,
                         text_color="black", show=show, corner_radius=8)
    entry.place(x=44, y=y + 25)
    
    return entry


username_entry = make_field(right, y=135, icon="👤", title="Username")
password_entry = make_field(right, y=210, icon="🔒", title="Password", show="*")


remember_me = CTk.CTkCheckBox(right, text="Remember me", bg_color="#ffffff", text_color="#1a1a1a", font=("Helvetica", 11), hover_color="#f0f4ff", border_width=2)
remember_me.place(x=44, y=290)

forgot_password = CTk.CTkLabel(right, text="Forgot Password?", fg_color="#ffffff", text_color="#3498db", font=("Helvetica", 11, "underline"), cursor="hand2")
forgot_password.place(x=290, y=290)


def save_remember_me(username):
    if remember_me.get() == 1:
        with open("remember_user.json", "w") as f:
            json.dump({"username": username}, f)
    else:
        if os.path.exists("remember_user.json"):
            os.remove("remember_user.json")

def load_remember_me():
    if os.path.exists("remember_user.json"):
        with open("remember_user.json", "r") as f:
            data = json.load(f)
            username_entry.insert(0, data.get("username", ""))
            remember_me.select()

load_remember_me()

def handle_login(): 
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showwarning("Warning", "Please fill in both username and password!")
        return

    try:
        conn = sqlite3.connect('mepio_system.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, password))
        user_record = cursor.fetchone()

        conn.close()

        if user_record:
            save_remember_me(username)
            root.after(200, root.quit)  # Close the login window after a short delay to allow the success message to show
        else:
            # 账号或密码对不上
            messagebox.showerror("Error", "Wrong username or password!")
            
    except Exception as e:
        messagebox.showerror("Database Error", f"Something went wrong: {e}")  
            


login_btn = CTk.CTkButton(right, text="LOGIN", font=("Arial", 14, "bold"), fg_color="#3498db", text_color="white", width=350, height=45, hover_color="#2980b9", cursor="hand2", command = handle_login)
login_btn.place(x=44, y=340)

def on_closing():
    root.destroy()  
    sys.exit()      #completely exit the program when the login window is closed, preventing the main app from opening


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

try:
    root.destroy()  
except:
    pass

import main         
app = main.MEPIOApp() 
app.mainloop()