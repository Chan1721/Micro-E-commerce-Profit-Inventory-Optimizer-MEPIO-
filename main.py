import customtkinter as ctk #shortcut for customtkinter as ctk
import tkinter as tk 

#importing the login page
#from loginpage import root

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
        
        # --- Main Container for 2-Column Layout ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Left Column: Inputs ---
        self.input_frame = ctk.CTkFrame(self.main_container, corner_radius=15, fg_color="#252525")
        self.input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(self.input_frame, text="Transaction Details", font=("Helvetica", 16, "bold"), text_color="#3498db").pack(pady=15)

        self.entries = {}
        fields = [
            ("Cost Price (RM)", ""),
            ("Selling Price (RM)", ""),
            ("Platform Fee (%)", ""),  # Default combined fee for Shopee/TikTok
            ("Shipping Fee (RM)", ""),
            ("Packaging Cost (RM)", "")
        ]

        for label_text, default_val in fields:
            row = ctk.CTkFrame(self.input_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=5)
            
            lbl = ctk.CTkLabel(row, text=label_text, width=150, anchor="w")
            lbl.pack(side="left")
            
            entry = ctk.CTkEntry(row, placeholder_text=default_val)
            entry.insert(0, default_val)
            entry.pack(side="right", fill="x", expand=True)
            self.entries[label_text] = entry

        self.calc_btn = ctk.CTkButton(self.input_frame, text="Calculate Profit", 
                                      fg_color="#27ae60", hover_color="#219150", 
                                      font=("Helvetica", 14, "bold"),
                                      command=self.perform_calculation)
        self.calc_btn.pack(pady=20, padx=40, fill="x")

        # --- Right Column: Results Visualization ---
        self.result_frame = ctk.CTkFrame(self.main_container, corner_radius=15, fg_color="#1e1e1e")
        self.result_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(self.result_frame, text="Financial Summary", font=("Helvetica", 16, "bold"), text_color="#3498db").pack(pady=15)

        self.res_net_profit = self.create_result_row("Net Profit:", "RM 0.00", "#27ae60")
        self.res_roi = self.create_result_row("ROI (%):", "0.00%", "#3498db")
        self.res_fees = self.create_result_row("Total Fees:", "RM 0.00", "#e74c3c")
        
        # Disclaimer or Tip
        tip_text = "Tip: High ROI (>20%) is recommended for long-term sustainability."
        ctk.CTkLabel(self.result_frame, text=tip_text, font=("Helvetica", 11, "italic"), text_color="gray").pack(side="bottom", pady=20)

    def create_result_row(self, label_text, value_text, color):
        row = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        row.pack(fill="x", padx=30, pady=15)
        
        lbl = ctk.CTkLabel(row, text=label_text, font=("Helvetica", 13))
        lbl.pack(side="left")
        
        val_lbl = ctk.CTkLabel(row, text=value_text, font=("Helvetica", 18, "bold"), text_color=color)
        val_lbl.pack(side="right")
        return val_lbl

    def perform_calculation(self):
        try:
            # 1. Get input values
            cost = float(self.entries["Cost Price (RM)"].get())
            selling = float(self.entries["Selling Price (RM)"].get())
            fee_p = float(self.entries["Platform Fee (%)"].get()) / 100
            shipping = float(self.entries["Shipping Fee (RM)"].get())
            packaging = float(self.entries["Packaging Cost (RM)"].get())

            # 2. Calculation logic
            platform_fee_amount = selling * fee_p
            total_cost = cost + platform_fee_amount + shipping + packaging
            net_profit = selling - total_cost
            roi = (net_profit / cost * 100) if cost > 0 else 0

            # 3. Update UI
            self.res_net_profit.configure(text=f"RM {net_profit:.2f}")
            self.res_roi.configure(text=f"{roi:.2f}%")
            self.res_fees.configure(text=f"RM {(platform_fee_amount + shipping + packaging):.2f}")
            
        except ValueError:
            # Simple error feedback if user enters non-numbers
            self.res_net_profit.configure(text="Invalid Input", text_color="#e74c3c")
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