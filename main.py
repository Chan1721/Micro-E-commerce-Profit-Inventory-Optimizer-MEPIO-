import customtkinter as ctk #shortcut for customtkinter as ctk
import tkinter as tk 

#importing the login page
# from loginpage import root

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

        self.btn_inv = ctk.CTkButton(self.sidebar_frame, text="Analytics",
                                     command=lambda: self.show_page("Analytics"))

        self.btn_inv = ctk.CTkButton(self.sidebar_frame, text="Settings",
                                     command=lambda: self.show_page("Settings"))
        self.btn_inv.pack(pady=10)

        self.btn_inv = ctk.CTkButton(self.sidebar_frame, text="Help/Support",
                                     command=lambda: self.show_page("Help/Support"))
        self.btn_inv.pack(pady=10)

        # --- Page Manager Logic ---
        # Dictionary to hold page frames
        self.pages = {}

        # Initialize Dashboard page
        self.pages["dash"] = ctk.CTkFrame(self)
        ctk.CTkLabel(self.pages["dash"], text="Welcome to Dashboard", font=("Arial", 24)).pack()

        #   Initialize Inventory page
        self.pages["inv"] = ctk.CTkFrame(self)
        ctk.CTkLabel(self.pages["inv"], text="Stock Management System", font=("Arial", 24)).pack()

        #   Initialize Logistics page
        self.pages["Logistics"] = ctk.CTkFrame(self)
        ctk.CTkLabel(self.pages["Logistics"], text="Shipping and Logistics", font=("Arial", 24)).pack()

        #   Initialize Calculator page
        self.pages["Calculator"] = ctk.CTkFrame(self)
        ctk.CTkLabel(self.pages["Calculator"], text="Profit Calculator", font=("Arial", 24)).pack()

        #   Initialize Analytics page
        self.pages["Analytics"] = ctk.CTkFrame(self)
        ctk.CTkLabel(self.pages["Analytics"], text="Analytics", font=("Arial", 24)).pack()

        #   Initialize Settings page
        self.pages["Settings"] = ctk.CTkFrame(self)
        ctk.CTkLabel(self.pages["Settings"], text="Settings", font=("Arial", 24)).pack()

        self.pages["Help/Support"] = ctk.CTkFrame(self)
        ctk.CTkLabel(self.pages["Help/Support"], text="Help and Support", font=("Arial", 24)).pack()

        # Show the default page (Dashboard)
        self.show_page("dash")

    def show_page(self, page_name):
        # 1. Hide all pages (Forget all frames)
        for frame in self.pages.values():
            frame.grid_forget()
        
        # 2. Show the selected page
        self.pages[page_name].grid(row=0, column=1, padx=20, pady=20, sticky="nsew")


class BasePage(ctk.CTkFrame):
    """BasePage serves as a template for all pages, providing a consistent header and layout."""
    def __init__(self, parent, controller, title_text):
        super().__init__(parent, fg_color="#2b2b2b") 
        
        self.header = ctk.CTkLabel(self, text=title_text, font=("Helvetica", 24, "bold"))
        self.header.pack(pady=20, padx=20, anchor="w")

class DashboardPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Dashboard Overview")
        
        # Statistics card container
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=20)

        metrics = [("Total Revenue", "RM 12,450.00"), 
                   ("Net Profit", "RM 4,200.50"), 
                   ("Platform Fees", "RM 850.20"), 
                   ("Low Stock", "5 Items")]
        
        # loop through metrics to create cards
        for i, (name, value) in enumerate(metrics):
            card = ctk.CTkFrame(self.stats_container, corner_radius=12, fg_color="#2d2d2d", height=120)
            card.pack(side="left", padx=10, fill="both", expand=True)
            
            ctk.CTkLabel(card, text=name, font=("Helvetica", 13), text_color="#aaaaaa").pack(pady=(20, 5))
            ctk.CTkLabel(card, text=value, font=("Helvetica", 20, "bold"), text_color="#3498db").pack(pady=(0, 20))

        # platform fee information section
        self.fee_info = ctk.CTkFrame(self, corner_radius=12, fg_color="#2d2d2d")
        self.fee_info.pack(pady=30, padx=30, fill="both", expand=True)
        
        ctk.CTkLabel(self.fee_info, text="Active Platform Fee Settings", font=("Helvetica", 16, "bold")).pack(pady=15)
        
        fee_text = ("• Shopee MY: 4.0% Commission + 2.12% Transaction Fee\n"
                    "• TikTok Shop: 2.0% Marketplace Fee + Service Fee\n"
                    "• Lazada: Standard Category Commission Applied")
        ctk.CTkLabel(self.fee_info, text=fee_text, justify="left", font=("Helvetica", 13), text_color="#cccccc").pack(pady=10)
    
class CalculatorPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Profit Calculator")
        
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(self.input_frame, text="Cost Price (RM):").grid(row=0, column=0, padx=10, pady=10)
        self.cost_entry = ctk.CTkEntry(self.input_frame)
        self.cost_entry.grid(row=0, column=1, padx=10, pady=10)

# --- Settings Page ---
class SettingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "System Settings")
        
        self.switch_var = ctk.StringVar(value="on")
        self.dark_mode_switch = ctk.CTkSwitch(self, text="Dark Mode", variable=self.switch_var, onvalue="on", offvalue="off")
        self.dark_mode_switch.pack(pady=20, padx=20, anchor="w")

if __name__ == "__main__":
    app = MEPIOApp()
    app.mainloop()