import tkinter as tk

root = tk.Tk()
root.title("MEPIO - Login")
root.geometry("720x440")
root.configure(bg="#f0f4ff")
root.resizable(False, False)

left = tk.Canvas(root, width=280, height=440, highlightthickness=0, bg="#2d6cdf")
left.place(x=0, y=0)



left.create_oval(-60, -60, 240, 240, fill="#4a84e8", outline="")

left.create_text(110, 100, text="MEPIO", font=("Georgia", 55, "bold"),
                 fill="white", anchor="center")
 
# Welcome text
left.create_text(36, 330, text="Welcome", font=("Helvetica", 18, "bold"),
                 fill="white", anchor="w")
left.create_text(36, 358,
                 text="Micro-E-commerce Profit\n& Inventory Optimizer",
                 font=("Helvetica", 9), fill="#b8d4ff", anchor="w", justify="left")



right = tk.Frame(root, bg="#ffffff")
right.place(x=280, y=0, width=440, height=440)

shadow = tk.Frame(root, bg="#d0d8f0", width=4, height=440)
shadow.place(x=280, y=0)

title_label = tk.Label(right, text = "Welcome to MEPIO" , font=("Helvetica", 17, ), bg="#ffffff", fg="#1a1a1a"
         ).place(x=44, y=68)

register = tk.Label(right, text="Don't have an account? Create your account,\nit takes less than a minute.",
         font=("Helvetica", 8), bg="#ffffff", fg="#999999", justify="left"
         ).place(x=44, y=96)







def make_field(parent, y, icon, placeholder, show=None):
    # container for icon and entry box
    container = tk.Frame(parent, bg="#ffffff", highlightthickness=1, highlightbackground="#dcdde1")
    container.place(x=44, y=y, width=350, height=40)
    
    
    tk.Label(container, text=icon, bg="#ffffff", font=("Arial", 12)).pack(side="left", padx=5)
    
    # entry box
    entry = tk.Entry(container, relief="flat", font=("Helvetica", 10), bg = "white" , fg = "black" ,insertbackground="black" , show=show)
    entry.insert(0, placeholder) # 设置占位符
    entry.pack(side="left", fill="both", expand=True, padx=5)
    
    return entry

username_entry = make_field(right, y=148, icon="👤", placeholder="Username:  ")
password_entry = make_field(right, y=206, icon="🔒", placeholder="Password:  ")

remember_me = tk.Checkbutton(right, text="Remember me", bg="#ffffff", font=("Helvetica", 8), activebackground="#ffffff",relief="flat", bd=0)
remember_me.place(x=44, y= 250)

forgot_password = tk.Label(right, text = "Forgot Password? ", bg = "#ffffff" , relief = "flat" ,font=("Helvetica", 8), bd = 0 )
forgot_password.place(x=290, y= 253)

login_btn = tk.Button(right, text="LOGIN", font=("Arial", 12, "bold"), bg="#3498db",
                      fg="black", relief="flat",
                       activebackground= "#2980b9" , activeforeground="white",  width=30, height=2, cursor="hand2")
login_btn.place(x=44, y=300, width=350)



























root.mainloop()