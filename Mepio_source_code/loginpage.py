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

def toggle_password():
    if show_password_cb.get() == 1:
        password_entry.configure(show="")  
    else:
        password_entry.configure(show="*")

show_password_cb = CTk.CTkCheckBox(
    right, text="Show", width=50, height=20, font=("Helvetica", 11), border_width=2,fg_color="#3498db",  bg_color="#fcfcfc",
    command=toggle_password
)
show_password_cb.place(x=320, y=247)        


remember_me = CTk.CTkCheckBox(right, text="Remember me", bg_color="#ffffff", text_color="#1a1a1a", font=("Helvetica", 11), hover_color="#f0f4ff", border_width=2)
remember_me.place(x=44, y=290)

forgot_password = CTk.CTkLabel(right, text="Forgot Password?", fg_color="#ffffff", text_color="#3498db", font=("Helvetica", 11, "underline"), cursor="hand2")
forgot_password.place(x=290, y=290)

def open_forgot_password(event=None):
    forgot_win = CTk.CTkToplevel(root)
    forgot_win.title("Password Recovery")
    forgot_win.geometry("400x420")
    forgot_win.resizable(False, False)
    forgot_win.grab_set() 

    CTk.CTkLabel(forgot_win, text="Recover Password", font=("Helvetica", 20, "bold")).place(x=40, y=25)

    # 1. Username
    CTk.CTkLabel(forgot_win, text="1. Enter your Username", font=("Helvetica", 12, "bold")).place(x=40, y=75)
    user_recovery_entry = CTk.CTkEntry(forgot_win, width=320, height=35, corner_radius=8)
    user_recovery_entry.place(x=40, y=100)

    # 2. Security Question
    CTk.CTkLabel(forgot_win, text="2. Security Question", font=("Helvetica", 12, "bold")).place(x=40, y=150)
    CTk.CTkLabel(forgot_win, text="Q: What is your favorite pet's name?", font=("Helvetica", 11), text_color="#7a7a7a").place(x=40, y=175)
    ans_recovery_entry = CTk.CTkEntry(forgot_win, width=320, height=35, corner_radius=8)
    ans_recovery_entry.place(x=40, y=200)

    # 3. New Password
    CTk.CTkLabel(forgot_win, text="3. Enter New Password", font=("Helvetica", 12, "bold")).place(x=40, y=250)
    new_pass_entry = CTk.CTkEntry(forgot_win, width=320, height=35, show="*", corner_radius=8)
    new_pass_entry.place(x=40, y=275)

    def process_reset():
        u = user_recovery_entry.get().strip()
        a = ans_recovery_entry.get().strip()
        np = new_pass_entry.get().strip()

        if not u or not a or not np:
            messagebox.showwarning("Warning", "Please fill in all fields!", parent=forgot_win)
            return

        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username=? AND security_answer=?", (u, a))
            match = cursor.fetchone()
            
            if not match:
                messagebox.showerror("Error", "Invalid Username or Security Answer!", parent=forgot_win)
                conn.close()
                return
                
            cursor.execute("UPDATE users SET password_hash=? WHERE username=?", (np, u))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Password reset successfully! You can now log in.", parent=forgot_win)
            forgot_win.destroy()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Something went wrong: {e}", parent=forgot_win)

    
    reset_btn = CTk.CTkButton(forgot_win, text="Update Password", font=("Helvetica", 13, "bold"), fg_color="#e67e22", hover_color="#d35400", width=320, height=40, command=process_reset)
    reset_btn.place(x=40, y=340)


forgot_password.bind("<Button-1>", open_forgot_password)


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