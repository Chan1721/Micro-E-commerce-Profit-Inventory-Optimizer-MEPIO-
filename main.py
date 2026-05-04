import customtkinter as ctk #shortcut for customtkinter as ctk
import tkinter as tk 

#importing the login page
from loginpage import root
from inventorypage import InventoryPage

app = ctk.CTk() # intializes the app, this is the main window of the program 
class MEPIOApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MEPIO")
        self.geometry("1100x600")

        # Configure grid layout for the main window
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        # Bind buttons to Page Manager
        self.btn_dash = ctk.CTkButton(self.sidebar_frame, text="Dashboard", 
                                      command=lambda: self.show_page("dash"))
        self.btn_dash.pack(pady=10)

        self.btn_inv = ctk.CTkButton(self.sidebar_frame, text="Inventory", 
                                     command=lambda: self.show_page("inv"))
        self.btn_inv.pack(pady=10)

        self.btn_inv = ctk.CTkButton(self.sidebar_frame, text="Logistics",
                                     command=lambda: self.show_page("Logistics"))
        self.btn_inv.pack(pady=10)

        self.btn_inv = ctk.CTkButton(self.sidebar_frame, text="Calculator",
                                     command=lambda: self.show_page("Calculator"))
        self.btn_inv.pack(pady=10)

        self.btn_inv = ctk.CTkButton(self.sidebar_frame, text="Settings",
                                     command=lambda: self.show_page("Settings"))
        self.btn_inv.pack(pady=10)

        # --- Page Manager Logic ---
        # Dictionary to hold page frames
        self.pages = {}

        # Initialize Dashboard page
        self.pages["dash"] = ctk.CTkFrame(self)
        ctk.CTkLabel(self.pages["dash"], text="Welcome to Dashboard", font=("Arial", 24)).pack()

        #   Initialize Inventory page
        self.pages["inv"] = InventoryPage(self)
        ctk.CTkLabel(self.pages["inv"], text="Stock Management System", font=("Arial", 24)).pack()

        #   Initialize Logistics page
        self.pages["Logistics"] = ctk.CTkFrame(self)
        ctk.CTkLabel(self.pages["Logistics"], text="Shipping and Logistics", font=("Arial", 24)).pack()

        #   Initialize Calculator page
        self.pages["Calculator"] = ctk.CTkFrame(self)
        ctk.CTkLabel(self.pages["Calculator"], text="Profit Calculator", font=("Arial", 24)).pack()

        self.profit_label = ctk.CTkLabel(self, text="RM 0.00", font=("Arial", 24, "bold"))
        self.profit_label.place(x=50, y=100)

        #   Initialize Settings page
        self.pages["Settings"] = ctk.CTkFrame(self)
        ctk.CTkLabel(self.pages["Settings"], text="Settings", font=("Arial", 24)).pack()

        # Show the default page (Dashboard)
        self.show_page("dash")

    def show_page(self, page_name):
        # 1. Hide all pages (Forget all frames)
        for page in self.pages.values():
            page.grid_forget()
        
        # 2. Show the selected page
        self.pages[page_name].grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

if __name__ == "__main__":
    app = MEPIOApp()
    app.mainloop()