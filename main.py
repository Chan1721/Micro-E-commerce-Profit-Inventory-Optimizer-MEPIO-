import customtkinter as ctk #shortcut for customtkinter as ctk
import tkinter as tk 

#importing the login page
# from loginpage import root
from loginpage import root
from inventorypage import InventoryPage

class MEPIOApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MEPIO - Profit & Inventory Optimizer")
        self.geometry("1100x650")

        # Configure main window grid layout[cite: 1]
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar Configuration ---[cite: 1]
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="MEPIO MENU", font=("Helvetica", 20, "bold"))
        self.logo_label.pack(pady=30)

        # Navigation items mapping[cite: 1]
        nav_items = [
            ("Dashboard", "dash"),
            ("Inventory", "inv"),
            ("Logistics", "logistics"),
            ("Calculator", "calculator"),
            ("Analytics", "analytics"),
            ("Settings", "settings"),
            ("Help & Support", "help")
        ]

        # Generate sidebar buttons dynamically to avoid variable conflicts[cite: 1]
        for text, page_key in nav_items:
            btn = ctk.CTkButton(self.sidebar_frame, text=text, 
                                command=lambda k=page_key: self.show_page(k))
            btn.pack(pady=5, padx=10, fill="x")

        # --- Page Manager Initialization ---[cite: 1]
        self.pages = {}

        # Initialize all page classes[cite: 1]
        self.pages["dash"] = DashboardPage(self, self)
        self.pages["inv"] = InventoryPage(self, self)
        self.pages["logistics"] = LogisticsPage(self, self)
        self.pages["calculator"] = CalculatorPage(self, self)
        self.pages["analytics"] = AnalyticsPage(self, self)
        self.pages["settings"] = SettingsPage(self, self)
        self.pages["help"] = HelpPage(self, self)

        # Display default page[cite: 1]
        self.show_page("dash")

    def show_page(self, page_name):
        # Hide all pages using grid_forget[cite: 1]
        for frame in self.pages.values():
            frame.grid_forget()
        
        # Display selected page in the main container area[cite: 1]
        self.pages[page_name].grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        #   Initialize Inventory page
        self.pages["inv"] = InventoryPage(self)
        ctk.CTkLabel(self.pages["inv"], text="Stock Management System", font=("Arial", 24)).pack()

# --- UI Templates ---[cite: 1]

class BasePage(ctk.CTkFrame):
    """Template class for all pages to ensure UI consistency."""
    def __init__(self, parent, controller, title_text):
        super().__init__(parent, fg_color="#2b2b2b") 
        self.header = ctk.CTkLabel(self, text=title_text, font=("Helvetica", 24, "bold"), text_color="#3498db")
        self.header.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Decorative separator line
        line = ctk.CTkFrame(self, height=2, fg_color="#3d3d3d")
        line.pack(fill="x", padx=20, pady=(0, 20))

class DashboardPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Dashboard Overview")
        
        # Statistical summary cards
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=20)
        
        metrics = [
            ("Total Revenue", "RM 12,450.00"), 
            ("Net Profit", "RM 4,200.50"), 
            ("Platform Fees", "RM 850.20"), 
            ("Low Stock", "5 Items")
        ]
        
        for name, value in metrics:
            card = ctk.CTkFrame(self.stats_frame, corner_radius=10, fg_color="#333333")
            card.pack(side="left", padx=10, fill="both", expand=True)
            ctk.CTkLabel(card, text=name, font=("Arial", 12), text_color="gray").pack(pady=(15, 0))
            ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold")).pack(pady=(5, 15))

        # Platform Fee Section (Result of Market Research)
        self.fee_info = ctk.CTkFrame(self, corner_radius=12, fg_color="#252525")
        self.fee_info.pack(pady=30, padx=30, fill="both", expand=True)
        ctk.CTkLabel(self.fee_info, text="Active Platform Fee Settings", font=("Arial", 16, "bold")).pack(pady=15)
        
        fee_text = (
            "• Shopee MY: 4.0% Commission + 2.12% Transaction Fee\n"
            "• TikTok Shop: 2.0% Marketplace Fee + Service Fee\n"
            "• Lazada: Standard Category-based Commission"
        )
        ctk.CTkLabel(self.fee_info, text=fee_text, justify="left", font=("Arial", 13), text_color="#bbbbbb").pack(pady=10)

class InventoryPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Stock Management System")
        # Placeholder for teammate's work
        ctk.CTkLabel(self, text="Inventory modules are currently being integrated by the Database Lead.", 
                     text_color="gray", font=("Arial", 14, "italic")).pack(expand=True)

class LogisticsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Shipping & Logistics")
        
        # Tracking simulation section
        self.track_frame = ctk.CTkFrame(self)
        self.track_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(self.track_frame, text="Quick Track (J&T / Poslaju):").pack(side="left", padx=10)
        self.track_entry = ctk.CTkEntry(self.track_frame, placeholder_text="Enter Tracking Number", width=300)
        self.track_entry.pack(side="left", padx=10, fill="x", expand=True)
        ctk.CTkButton(self.track_frame, text="Track Order", width=100).pack(side="left", padx=10)

class CalculatorPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Profit Calculator")
        
        # Calculation input area
        input_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#252525")
        input_frame.pack(pady=10, padx=20, fill="x")
        
        labels = ["Cost Price (RM):", "Selling Price (RM):", "Platform Fee Rate (%):", "Packaging Cost (RM):"]
        for i, text in enumerate(labels):
            ctk.CTkLabel(input_frame, text=text).grid(row=i, column=0, padx=20, pady=10, sticky="w")
            ctk.CTkEntry(input_frame, width=250).grid(row=i, column=1, padx=20, pady=10)

        ctk.CTkButton(self, text="Calculate Net Profit", fg_color="#27ae60", hover_color="#219150").pack(pady=20)

class AnalyticsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Data Analytics")
        ctk.CTkLabel(self, text="Profit Trends & Performance Analysis", font=("Arial", 14)).pack(pady=10)
        
        # Visual placeholder for charts
        chart_box = ctk.CTkFrame(self, height=300, fg_color="#1a1a1a")
        chart_box.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(chart_box, text="[ Chart Visualization Module Loading... ]", text_color="gray").place(relx=0.5, rely=0.5, anchor="center")

class SettingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "System Settings")
        
        self.dark_mode_switch = ctk.CTkSwitch(self, text="Enable Dark Mode Visualization")
        self.dark_mode_switch.select()
        self.dark_mode_switch.pack(pady=20, padx=30, anchor="w")
        
        ctk.CTkButton(self, text="Sync Database", width=150).pack(pady=10, padx=30, anchor="w")
        ctk.CTkButton(self, text="Export Settings", width=150, fg_color="transparent", border_width=1).pack(pady=10, padx=30, anchor="w")

class HelpPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Help & Support Center")
        
        # User manual textbox
        help_text = ctk.CTkTextbox(self, width=600, height=300, font=("Arial", 12))
        help_text.pack(pady=10, padx=20, fill="both", expand=True)
        help_text.insert("0.0", "MEPIO SYSTEM DOCUMENTATION\n\n"
                               "1. DASHBOARD: View real-time profit and revenue metrics.\n"
                               "2. CALCULATOR: Pre-calculate profit margins before product listing.\n"
                               "3. LOGISTICS: Manage shipping fees and track local orders.\n"
                               "4. SETTINGS: Adjust platform commission rates for Shopee/TikTok.")
        help_text.configure(state="disabled") # Read-only

if __name__ == "__main__":
    app = MEPIOApp()
    app.mainloop()