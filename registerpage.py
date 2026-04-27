import customtkinter as CTk
import tkinter as tk

def open_register_window(login_root):
    reg_window = CTk.CTkToplevel()
    reg_window.title = "Register Mepio"
    reg_window.geometry("720x440")
    reg_window.resizable(True, True)


# Left Brand Area 
    left = tk.Canvas(reg_window, width=280, height=440, highlightthickness=0, bg="#2d6cdf")
    left.place(x=0, y=0)
    left.create_oval(-60, -60, 240, 240, fill="#4a84e8", outline="")
    left.create_text(120, 100, text="MEPIO", font=("Georgia", 48, "bold"), fill="white", anchor="center")
    left.create_text(36, 330, text="Welcome", font=("Helvetica", 18, "bold"), fill="white", anchor="w")
    left.create_text(36, 358, text="Micro-E-commerce Profit\n& Inventory Optimizer", font=("Helvetica", 9), fill="#b8d4ff", anchor="w", justify="left")

    def on_close():
        reg_window.destroy()
        login_root.deiconify() 
    
    reg_window.protocol("WM_DELETE_WINDOW", on_close)