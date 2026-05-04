import customtkinter as CTk
import tkinter as tk
import tkinter.messagebox as messagebox

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

    right = CTk.CTkFrame(reg_window, fg_color="#ffffff", width=440, height=440, corner_radius=0)
    right.place(x=280, y=0)

    def on_close():
        reg_window.destroy()      
        login_root.deiconify()

    back_btn = CTk.CTkButton(right, text="< Back", font=("Italic", 14), 
                             fg_color="transparent", text_color="#1a1a1a", 
                             hover_color="#eef2f9", width=60, height=30, cursor="hand2", 
                             command=on_close)
  
    back_btn.place(x=15, y=15)

    shadow = CTk.CTkFrame(reg_window, fg_color="#d0d8f0", width=4, height=440, corner_radius=0)
    shadow.place(x=280, y=0)

    register_label = CTk.CTkLabel(right, text="Register", font=("Helvetica", 17, "bold"), text_color="#1a1a1a")
    register_label.place(x=44, y=50)

    sub_label = CTk.CTkLabel(right, text="Create your MEPIO account.", font=("Helvetica", 10), text_color="#7a7a7a")
    sub_label.place(x=44, y=74)

    #username
    username_label = CTk.CTkLabel(right, text="👤 Username", font=("Helvetica", 14, "bold"), text_color="#1a1a1a")
    username_label.place(x=40, y=115) 
    
    
    reg_user_entry = CTk.CTkEntry(right, width=320, height=40, border_color="#d0d0d0", corner_radius=8)
    reg_user_entry.place(x=44, y=145)

    password_label = CTk.CTkLabel(right, text="🔒 Password", font=("Helvetica", 14, "bold"), text_color="#1a1a1a")
    password_label.place(x=40, y=195)

    reg_password_entry = CTk.CTkEntry(right, width=320, height=40, border_color="#d0d0d0", show="*", corner_radius=8)
    reg_password_entry.place(x=44, y=225)

    confirm_pass_lbl = CTk.CTkLabel(right, text="🔒 Confirm Password", font=("Helvetica", 14, "bold"), text_color="#1a1a1a")
    confirm_pass_lbl.place(x=40, y=275)
    
    reg_confirm_entry = CTk.CTkEntry(right, width=320, height=40, border_color="#d0d0d0", show="*", corner_radius=8)
    reg_confirm_entry.place(x=44, y=305)

    def handle_register():
        username = reg_user_entry.get()
        pwd = reg_password_entry.get()
        confirm_pwd = reg_confirm_entry.get()

        #check if users fill all fields
        if username == "" or pwd == "" or confirm_pwd == "":
            messagebox.showwarning("Warning", "Please fill in all fields!")
            return
        
        #check if the users fill the same as confirm pwd
        if pwd != confirm_pwd:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        sec_window = CTk.CTkToplevel(reg_window)
        sec_window.title("Step 2: Security")
        sec_window.geometry("400x350")
        sec_window.resizable(False, False)
        sec_window.grab_set() 

        CTk.CTkLabel(sec_window, text="Security Question", font=("Helvetica", 20, "bold")).place(x=40, y=30)
        CTk.CTkLabel(sec_window, text="Q: What is your favorite pet's name?", font=("Helvetica", 14, "bold"), text_color="#1a1a1a").place(x=40, y=85)

        answer_entry = CTk.CTkEntry(sec_window, width=320, height=40, placeholder_text="Enter your answer")
        answer_entry.place(x=40, y=120)

        def final_answer():
            answer = answer_entry.get()
            if answer == "":
                messagebox.showerror("Error", "Please provide an answer!")
                return
            messagebox.showinfo("Success", f"Account created for {username}!\nAnswer saved: {answer}")
            sec_window.destroy()
            on_close()

        complete_btn = CTk.CTkButton(sec_window, text="Complete Registration", fg_color="#0a192f", hover_color="#132b4f", width=320, height=40, command=final_answer)
        complete_btn.place(x=40, y=190)    


    #register button
    register_btn = CTk.CTkButton(right, text="Register", font=("Helvetica", 14, "bold"), 
                                 fg_color="#3498db", hover_color="#2980b9", text_color="white", 
                                 width=350, height=45, cursor="hand2", command = handle_register )
    register_btn.place(x=44, y=370)

    def on_close():
        reg_window.destroy()
        login_root.deiconify() 

    reg_window.protocol("WM_DELETE_WINDOW", on_close)