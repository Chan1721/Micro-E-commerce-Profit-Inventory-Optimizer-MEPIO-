import customtkinter as CTk
import tkinter as tk

# 1. Basic Window Configuration
root = CTk.CTk()
root.title("MEPIO - Login")
root.geometry("720x440")
root.configure(fg_color="#f0f4ff")
root.resizable(False, False)

# 2. Left Brand Area 
left = tk.Canvas(root, width=280, height=440, highlightthickness=0, bg="#2d6cdf")
left.place(x=0, y=0)
left.create_oval(-60, -60, 240, 240, fill="#4a84e8", outline="")
left.create_text(110, 100, text="MEPIO", font=("Georgia", 55, "bold"), fill="white", anchor="center")
left.create_text(36, 330, text="Welcome", font=("Helvetica", 18, "bold"), fill="white", anchor="w")
left.create_text(36, 358, text="Micro-E-commerce Profit\n& Inventory Optimizer", font=("Helvetica", 9), fill="#b8d4ff", anchor="w", justify="left")

# 3. Right Login Form Area
right = CTk.CTkFrame(root, fg_color="#ffffff", width=440, height=440, corner_radius=0)
right.place(x=280, y=0)

# Divider Shadow
shadow = CTk.CTkFrame(root, fg_color="#d0d8f0", width=4, height=440, corner_radius=0)
shadow.place(x=280, y=0)

# Titles and Headers
title_label = CTk.CTkLabel(right, text="Welcome to MEPIO", font=("Helvetica", 17, "bold"), fg_color="#ffffff", text_color="#1a1a1a")
title_label.place(x=44, y=68)

register = CTk.CTkLabel(right, text="Don't have an account? Create your account,\nit takes less than a minute.", font=("Helvetica", 8), fg_color="#ffffff", text_color="#999999", justify="left")
register.place(x=44, y=96)


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


login_btn = CTk.CTkButton(right, text="LOGIN", font=("Arial", 14, "bold"), fg_color="#3498db", text_color="white", width=350, height=45, hover_color="#2980b9", cursor="hand2")
login_btn.place(x=44, y=340)

root.mainloop()