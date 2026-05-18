import customtkinter as ctk #shortcut for customtkinter as ctk
import tkinter as tk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        super().__init__(parent, controller, "Advanced Profit Calculator")
        
        # --- Main Container for 2-Column Layout ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Left Column: Inputs (Scrollable to prevent overcrowding) ---
        self.input_frame = ctk.CTkScrollableFrame(self.main_container, corner_radius=15, fg_color="#252525", width=500)
        self.input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Section 1: Product & Platform Details
        ctk.CTkLabel(self.input_frame, text="1. Product & Platform Details", font=("Helvetica", 16, "bold"), text_color="#3498db").pack(pady=(10, 15), anchor="w", padx=20)
        
        self.entries = {}
        base_fields = [
            ("Cost Price (RM)", ""),
            ("Selling Price (RM)", ""),
            ("Platform Fee (%)", ""),
            ("Shipping Fee Paid by Seller (RM)", "")
        ]
        self.create_input_fields(base_fields)

        # Section 2: Smart Packaging Cost Breakdown
        ctk.CTkLabel(self.input_frame, text="2. Packaging Cost Breakdown", font=("Helvetica", 16, "bold"), text_color="#3498db").pack(pady=(20, 15), anchor="w", padx=20)
        
        # Preset Package Size Selection
        size_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        size_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(size_frame, text="Package Size Preset:", width=150, anchor="w").pack(side="left")
        
        self.size_option = ctk.CTkOptionMenu(
            size_frame, 
            values=["Small Flyer (RM 0.20)", "Medium Box (RM 0.80)", "Large Box (RM 1.50)", "Custom / Manual"],
            command=self.on_size_preset_change
        )
        self.size_option.pack(side="right", fill="x", expand=True)

        # Fine-grained Cost Breakdown Fields
        breakdown_fields = [
            ("Base Package Cost (RM)", ""),
            ("Labor Cost per Item (RM)", ""),
            ("Other Buffer Cost (RM)", "")
        ]
        self.create_input_fields(breakdown_fields)

        # Calculate Button
        self.calc_btn = ctk.CTkButton(self.input_frame, text="Calculate Net Profit", 
                                      fg_color="#27ae60", hover_color="#219150", 
                                      font=("Helvetica", 14, "bold"),
                                      command=self.perform_calculation)
        self.calc_btn.pack(pady=25, padx=40, fill="x")

        # --- Right Column: Financial Results ---
        self.result_frame = ctk.CTkFrame(self.main_container, corner_radius=15, fg_color="#1e1e1e")
        self.result_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(self.result_frame, text="Financial Summary", font=("Helvetica", 16, "bold"), text_color="#3498db").pack(pady=15)

        self.res_net_profit = self.create_result_row("Net Profit:", "RM 0.00", "#27ae60")
        self.res_roi = self.create_result_row("ROI (%):", "0.00%", "#3498db")
        self.res_total_packaging = self.create_result_row("Total Packaging Cost:", "RM 0.00", "#e67e22")
        self.res_fees = self.create_result_row("Platform Fees:", "RM 0.00", "#e74c3c")
        
        # Advisory insights based on calculations
        self.lbl_insight = ctk.CTkLabel(self.result_frame, text="Insight: Enter figures to run optimization analysis.", 
                                        font=("Helvetica", 12, "italic"), text_color="gray", wraplength=250)
        self.lbl_insight.pack(side="bottom", pady=30, padx=20)

    def create_input_fields(self, fields):
        """Helper to dynamically generate grouped input fields"""
        for label_text, default_val in fields:
            row = ctk.CTkFrame(self.input_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=5)
            
            lbl = ctk.CTkLabel(row, text=label_text, width=180, anchor="w")
            lbl.pack(side="left")
            
            entry = ctk.CTkEntry(row, placeholder_text=default_val)
            entry.insert(0, default_val)
            entry.pack(side="right", fill="x", expand=True)
            self.entries[label_text] = entry

    def create_result_row(self, label_text, value_text, color):
        row = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        row.pack(fill="x", padx=30, pady=12)
        
        lbl = ctk.CTkLabel(row, text=label_text, font=("Helvetica", 13))
        lbl.pack(side="left")
        
        val_lbl = ctk.CTkLabel(row, text=value_text, font=("Helvetica", 18, "bold"), text_color=color)
        val_lbl.pack(side="right")
        return val_lbl

    def on_size_preset_change(self, choice):
        """Triggered when the user selects a different packaging size option menu"""
        # Automatically adjust Base Package Cost input field based on preset choice
        if "Small Flyer" in choice:
            self.update_entry_value("Base Package Cost (RM)", "0.20")
        elif "Medium Box" in choice:
            self.update_entry_value("Base Package Cost (RM)", "0.80")
        elif "Large Box" in choice:
            self.update_entry_value("Base Package Cost (RM)", "1.50")
        elif "Custom / Manual" in choice:
            # Clear or allow user to completely type from scratch freely
            pass

    def update_entry_value(self, field_name, new_value):
        self.entries[field_name].delete(0, tk.END)
        self.entries[field_name].insert(0, new_value)

    def perform_calculation(self):
        try:
            # 1. Retrieve pricing data entries
            cost = float(self.entries["Cost Price (RM)"].get())
            selling = float(self.entries["Selling Price (RM)"].get())
            fee_p = float(self.entries["Platform Fee (%)"].get()) / 100
            shipping = float(self.entries["Shipping Fee Paid by Seller (RM)"].get())
            
            # 2. Retrieve fine-grained packaging inputs
            package_base = float(self.entries["Base Package Cost (RM)"].get())
            labor = float(self.entries["Labor Cost per Item (RM)"].get())
            buffer = float(self.entries["Other Buffer Cost (RM)"].get())

            # 3. Calculate breakdown formulas
            total_packaging = package_base + labor + buffer
            platform_fee_amount = selling * fee_p
            
            # Total expenditure calculations
            total_cost = cost + platform_fee_amount + shipping + total_packaging
            net_profit = selling - total_cost
            roi = (net_profit / cost * 100) if cost > 0 else 0

            # 4. Render output data strings back to UI elements
            self.res_net_profit.configure(text=f"RM {net_profit:.2f}")
            self.res_roi.configure(text=f"{roi:.2f}%")
            self.res_total_packaging.configure(text=f"RM {total_packaging:.2f}")
            self.res_fees.configure(text=f"RM {platform_fee_amount:.2f}")
            
            # 5. Dynamic Advisor Insights System
            if roi < 15:
                self.lbl_insight.configure(
                    text="⚠️ Warning: Low ROI! Consider reducing your labor/packaging cost or choosing a higher-margin platform strategy.",
                    text_color="#e74c3c"
                )
            else:
                self.lbl_insight.configure(
                    text="✅ Healthy Margin: This pricing setup efficiently covers fine packaging and provides strong commercial scale.",
                    text_color="#27ae60"
                )
            
        except ValueError:
            self.res_net_profit.configure(text="Invalid Input", text_color="#e74c3c")

class AnalyticsPage(BasePage):
    def __init__(self, parent, controller):
        """
        Initializes the Advanced Analytics Page.
        This page focuses on 'Restock Capital Budget Forecasting' (Solution 3).
        It leverages stock velocity data to predict short-term and long-term cash flow
        requirements for inventory restocking, fully serving as a financial Optimizer.
        """
        super().__init__(parent, controller, "Capital Budget Forecasting")

        # --- Main Container Split into Two Columns ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # =========================================================================
        # LEFT COLUMN: PREDICTIVE KPI CARDS & STRATEGIC ADVICE
        # =========================================================================
        self.left_frame = ctk.CTkFrame(self.main_container, width=300, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))

        # KPI Card 1: Capital needed within the next 7 Days
        self.card_7d = ctk.CTkFrame(self.left_frame, fg_color="#e74c3c", corner_radius=10)
        self.card_7d.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(self.card_7d, text="7-Day Urgent Capital Needed", font=("Arial", 12, "bold"), text_color="white").pack(pady=(10, 2))
        ctk.CTkLabel(self.card_7d, text="RM 2,450.00", font=("Arial", 22, "bold"), text_color="white").pack(pady=(2, 10))

        # KPI Card 2: Capital needed within 30 Days
        self.card_30d = ctk.CTkFrame(self.left_frame, fg_color="#2e4053", corner_radius=10)
        self.card_30d.pack(fill="x", pady=10)
        ctk.CTkLabel(self.card_30d, text="30-Day Total Capital Projection", font=("Arial", 12), text_color="lightgray").pack(pady=(10, 2))
        ctk.CTkLabel(self.card_30d, text="RM 8,120.00", font=("Arial", 20, "bold"), text_color="#3498db").pack(pady=(2, 10))

        # Strategic Optimization Insight Box
        self.insight_box = ctk.CTkFrame(self.left_frame, fg_color="#1e1e1e", corner_radius=10)
        self.insight_box.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(self.insight_box, text="💡 Optimization Insights", font=("Arial", 14, "bold"), text_color="#27ae60").pack(pady=10, anchor="w", padx=15)
        
        insight_text = (
            "• Urgent Risk: 'COS-MY-LIP-001' breaches safety stock in 2 days. Allocating RM 1,200 immediately is highly recommended to secure cross-border shipment.\n\n"
            "• Cash Allocation Tip: Sourcing cost on Shopee items yields 4.5% higher ROI than TikTok counterparts this month. Redirect secondary capital back into Shopee listings."
        )
        lbl_insight = ctk.CTkLabel(self.insight_box, text=insight_text, justify="left", font=("Arial", 11), text_color="#bbbbbb", wraplength=260)
        lbl_insight.pack(pady=5, padx=15, fill="both")

        # =========================================================================
        # RIGHT COLUMN: VISUAL FORECASTING CHART CANVAS
        # =========================================================================
        self.right_frame = ctk.CTkFrame(self.main_container, fg_color="#252525", corner_radius=12)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Render the predictive chart onto this frame
        self.render_budget_chart()

    def render_budget_chart(self):
        """
        Generates and embeds a Matplotlib stacked line/bar chart representing
        the upcoming restocking capital demands tied to supplier lead times.
        """
        # Mock timeline: The next 4 weeks
        timeline_weeks = ['Week 1 (Urgent)', 'Week 2', 'Week 3', 'Week 4']
        
        # Sourcing expenses calculated by predicting stockout dates for different platform inventories
        shopee_restock_budget = [1500, 1200, 2000, 1000]
        tiktok_restock_budget = [950, 800, 1100, 500]

        # Initialize the Matplotlib figure plot frame matching the CustomTkinter dark UI
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#252525')
        ax.set_facecolor('#252525')

        # Generate stacked bar representation to clearly display total capital consolidation
        ax.bar(timeline_weeks, shopee_restock_budget, label='Shopee Inventory Needs', color='#ff4500', width=0.4)
        ax.bar(timeline_weeks, tiktok_restock_budget, bottom=shopee_restock_budget, label='TikTok Inventory Needs', color='#000000', width=0.4, edgecolor='gray')

        # Styling parameters to comply with dark mode styling rules
        ax.tick_params(colors='white', labelsize=10)
        ax.set_ylabel("Required Sourcing Capital (RM)", color='white', fontsize=11, labelpad=10)
        ax.set_title("30-Day Restock Capital Budget Forecast", color='white', fontsize=14, pad=15, fontweight='bold')
        ax.yaxis.grid(True, linestyle='--', alpha=0.2, color='gray')

        # Style the chart legends to identify distinct categories easily
        legend = ax.legend(facecolor='#1e1e1e', edgecolor='none', labelcolor='white')
        legend.get_frame().set_alpha(0.7)
        # Wipe out raw axis borders
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Inject the visualization canvas directly into the right frame layout
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)

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