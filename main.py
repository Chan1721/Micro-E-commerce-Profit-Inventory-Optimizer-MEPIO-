import customtkinter as ctk #shortcut for customtkinter as ctk
import tkinter as tk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
ctk.set_appearance_mode("light")

#importing the login page
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
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=("#FFFFFF", "#1D1E1F"))
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Brand section at top of sidebar
        brand_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        brand_frame.pack(fill="x", padx=16, pady=(24, 4))

        # Small blue square with "M" inside — acts as a logo
        logo_box = ctk.CTkFrame(brand_frame, width=36, height=36,
                         corner_radius=8, fg_color="#4F6EF7")
        logo_box.pack(side="left")
        logo_box.pack_propagate(False)  # keeps the box at 36x36
        ctk.CTkLabel(logo_box, text="M", font=("SF Pro Display", 18, "bold"),
             text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # Text next to the logo
        text_col = ctk.CTkFrame(brand_frame, fg_color="transparent")
        text_col.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(text_col, text="MEPIO", font=("SF Pro Display", 17, "bold"),
             text_color="#4F6EF7").pack(anchor="w")
        ctk.CTkLabel(text_col, text="Profit & Inventory", font=("SF Pro Display", 10),
             text_color="#94A3B8").pack(anchor="w")

        # Thin grey line below the brand
        ctk.CTkFrame(self.sidebar_frame, height=1, fg_color="#E2E8F0").pack(
            fill="x", padx=16, pady=(14, 12))

        # Navigation items mapping[cite: 1]
        nav_items = [
            ("🏠  Dashboard", "dash"),
            ("📦  Inventory", "inv"),
            ("🚚  Logistics", "logistics"),
            ("🧮  Calculator", "calculator"),
            ("📊  Analytics", "analytics"),
            ("⚙️  Settings", "settings"),
            ("❓  Help & Support", "help")
        ]

        # Generate sidebar buttons dynamically to avoid variable conflicts[cite: 1]
        for text, page_key in nav_items:
            btn = ctk.CTkButton(self.sidebar_frame, text=f"  {text}", 
                                fg_color="transparent", text_color=("#475569","#F8FAFC"), hover_color="#e2e8f0",
                                font=("Helvetica", 14, "bold"), anchor="w",
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
        super().__init__(parent, fg_color="transparent") 
        self.header = ctk.CTkLabel(self, text=title_text, font=("Helvetica", 24, "bold"), text_color="#3498db")
        self.header.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Decorative separator line
        line = ctk.CTkFrame(self, height=2, fg_color="#E0E0E0")
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
            card = ctk.CTkFrame(self.stats_frame, corner_radius=15, fg_color=("#FFFFFF", "#2B2B2B"))
            card.pack(side="left", padx=10, fill="both", expand=True)
            ctk.CTkLabel(card, text=name, font=("SF Pro Display", 12), text_color="gray").pack(pady=(15, 0))
            ctk.CTkLabel(card, text=value, font=("SF Pro Display", 18, "bold")).pack(pady=(5, 15))

        # Platform Fee Section (Result of Market Research)
        self.fee_info = ctk.CTkFrame(self, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
        self.fee_info.pack(pady=30, padx=30, fill="both", expand=True)
        ctk.CTkLabel(self.fee_info, text="Active Platform Fee Settings", font=("SF Pro Display", 16, "bold")).pack(pady=15)
        
        fee_text = (
            "• Shopee MY: 4.0% Commission + 2.12% Transaction Fee\n"
            "• TikTok Shop: 2.0% Marketplace Fee + Service Fee\n"
            "• Lazada: Standard Category-based Commission"
        )
        ctk.CTkLabel(self.fee_info, text=fee_text, justify="left", font=("SF Pro Display", 13), text_color="#bbbbbb").pack(pady=10)

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
        Initializes the Advanced Restock Optimization Analytics Page with Manual Key-in entries.
        Upgraded with adaptive Light/Dark mode dynamic tuples to fully support appearance synchronization.
        """
        super().__init__(parent, controller, "Restock & Expiry Optimizer")

        # --- Adaptive Color Palette Configuration ---
        # Format: (Light Mode Color, Dark Mode Color)
        self.bg_side_panel = ("#F8FAFC", "#1E1E1E")
        self.bg_card_inner = ("#FFFFFF", "#252525")
        self.text_main_color = ("#1E293B", "#F1F5F9")
        self.text_sub_color = ("#64748B", "#94A3B8")

        # --- Main Layout Framework (Two-Column Split Grid) ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # =========================================================================
        # LEFT COLUMN: CRITICAL ACTION ALERTS, MANUAL INPUTS & ADVISORY
        # =========================================================================
        # Scrollable frame now dynamically alters its background during theme shifts
        self.left_frame = ctk.CTkScrollableFrame(self.main_container, width=340, corner_radius=15, fg_color=self.bg_side_panel)
        self.left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))

        # KPI Card 1: Total Sourcing Capital Required Immediately (Red Alert Accent)
        self.card_total_cost = ctk.CTkFrame(self.left_frame, fg_color=("#FF4D4D", "#E74C3C"), corner_radius=10)
        self.card_total_cost.pack(fill="x", pady=(0, 10), padx=5)
        ctk.CTkLabel(self.card_total_cost, text="Total Procurement Budget Needed", font=("Arial", 11, "bold"), text_color="white").pack(pady=(10, 2))
        self.lbl_total_cost_val = ctk.CTkLabel(self.card_total_cost, text="RM 0.00", font=("Arial", 22, "bold"), text_color="white")
        self.lbl_total_cost_val.pack(pady=(2, 10))

        # KPI Card 2: Impending Expiry Risk Warning (Orange Warning Accent)
        self.card_expiry_alert = ctk.CTkFrame(self.left_frame, fg_color=("#FFA502", "#E67E22"), corner_radius=10)
        self.card_expiry_alert.pack(fill="x", pady=10, padx=5)
        ctk.CTkLabel(self.card_expiry_alert, text="🚨 Inventory Batches Near Expiry", font=("Arial", 11), text_color="white").pack(pady=(10, 2))
        self.lbl_expiry_val = ctk.CTkLabel(self.card_expiry_alert, text="0 Units At Risk", font=("Arial", 18, "bold"), text_color="white")
        self.lbl_expiry_val.pack(pady=(2, 10))

        # --- Manual Key-in Setup Group ---
        ctk.CTkLabel(self.left_frame, text="📊 Manual Optimization Inputs", font=("Arial", 13, "bold"), text_color="#3498db").pack(pady=(15, 10), anchor="w", padx=10)
        
        self.entries = {}
        input_fields = [
            ("Current Local Stock (Units)", "50"),
            ("Average Daily Sales (Units)", "10"),
            ("Stock Near Expiry (Units)", "35"),
            ("Supplier Cost per Unit (RM)", "10.00")
        ]
        
        for label_text, default_val in input_fields:
            row = ctk.CTkFrame(self.left_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=5)
            
            lbl = ctk.CTkLabel(row, text=label_text, anchor="w", font=("Arial", 11), text_color=self.text_main_color)
            lbl.pack(side="left")
            
            entry = ctk.CTkEntry(row, placeholder_text=default_val, width=80)
            entry.insert(0, default_val)
            entry.pack(side="right")
            self.entries[label_text] = entry

        # Interactive Calculation Execution Trigger Button
        self.btn_calculate = ctk.CTkButton(
            self.left_frame, text="Run Restock Optimization", 
            fg_color="#27ae60", hover_color="#219150", 
            font=("Arial", 12, "bold"), command=self.execute_restock_analysis
        )
        self.btn_calculate.pack(pady=15, padx=10, fill="x")

        # Supervisor Compliance Optimization Insight Console Box
        self.insight_box = ctk.CTkFrame(self.left_frame, fg_color=self.bg_card_inner, corner_radius=10)
        self.insight_box.pack(fill="both", expand=True, pady=10, padx=5)
        ctk.CTkLabel(self.insight_box, text="📋 Smart Sourcing Recommendations", font=("Arial", 13, "bold"), text_color="#27ae60").pack(pady=10, anchor="w", padx=15)
        
        self.lbl_insight = ctk.CTkLabel(self.insight_box, text="", justify="left", font=("Arial", 11), text_color=self.text_sub_color, wraplength=280)
        self.lbl_insight.pack(pady=(0, 15), padx=15, fill="both")

        # =========================================================================
        # RIGHT COLUMN: VISUAL REORDER QUANTITY & COST COMPARISON CHART
        # =========================================================================
        self.right_frame = ctk.CTkFrame(self.main_container, fg_color=self.bg_card_inner, corner_radius=12)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Safe tracking pipeline placeholder to manage the Matplotlib widget container element
        self.canvas_widget = None
        
        # Stream initial calculations automatically during interface layout mounting
        self.execute_restock_analysis()

    def execute_restock_analysis(self):
        """Extracts values from the manual entries, executes calculation math and refreshes the layout."""
        try:
            current_stock = int(self.entries["Current Local Stock (Units)"].get())
            daily_sales = int(self.entries["Average Daily Sales (Units)"].get())
            expiry_stock = int(self.entries["Stock Near Expiry (Units)"].get())
            unit_cost = float(self.entries["Supplier Cost per Unit (RM)"].get())

            # Core Optimization Algorithm
            target_30d_demand = daily_sales * 30
            usable_safe_stock = current_stock - expiry_stock
            if usable_safe_stock < 0:
                usable_safe_stock = 0

            recommended_buy_qty = target_30d_demand - usable_safe_stock
            if recommended_buy_qty < 0:
                recommended_buy_qty = 0

            total_procurement_cost = recommended_buy_qty * unit_cost

            # Update Text Outputs
            self.lbl_total_cost_val.configure(text=f"RM {total_procurement_cost:,.2f}")
            self.lbl_expiry_val.configure(text=f"{expiry_stock} Units At Risk")

            recommendation_text = (
                f"• Target 30-Day Demand: {target_30d_demand} units\n"
                f"• Adjusted Usable Stock: {usable_safe_stock} units\n"
                f"  (Deducted {expiry_stock} units near expiry risk)\n\n"
                f"➔ Recommended Buy: {recommended_buy_qty} units\n"
                f"➔ Sourcing Cost: RM {total_procurement_cost:,.2f}"
            )
            self.lbl_insight.configure(text=recommendation_text, text_color=self.text_sub_color)

            # Re-render adaptive chart plot parameters
            self.render_optimization_chart(recommended_buy_qty, total_procurement_cost)

        except ValueError:
            self.lbl_insight.configure(text="⚠️ Error: Please check inputs. Use digits only.", text_color="#e74c3c")

    def render_optimization_chart(self, buy_qty, total_cost):
        """Generates a dynamic multi-axis chart reacting to app configuration changes."""
        if self.canvas_widget is not None:
            self.canvas_widget.destroy()

        # Fetch current background state from system runtime settings to style Matplotlib canvas
        current_mode = ctk.get_appearance_mode()
        fig_face_color = "#FFFFFF" if current_mode == "Light" else "#252525"
        label_axis_color = "#1E293B" if current_mode == "Light" else "#FFFFFF"
        grid_line_color = "#E2E8F0" if current_mode == "Light" else "#404040"

        products_sku = ['Manual Item\n[Simulated]', 'Mascara\n[MAS-002]', 'EyeLiner\n[EYE-003]']
        buy_quantities = [buy_qty, 200, 50] 
        procurement_costs = [total_cost, 3650, 500] 

        fig, ax1 = plt.subplots(figsize=(6, 4), facecolor=fig_face_color)
        ax1.set_facecolor(fig_face_color)

        # Primary Axis (Left Side Volume Chart Bars)
        color_bars = '#3498db'
        ax1.set_ylabel('Recommended Reorder Qty (Units)', color=color_bars, fontsize=11, fontweight='bold', labelpad=10)
        bars = ax1.bar(products_sku, buy_quantities, color=color_bars, width=0.35, alpha=0.8)
        ax1.tick_params(axis='y', labelcolor=color_bars)
        
        # Secondary Axis (Right Side Line Cost Overlay)
        ax2 = ax1.twinx()
        color_line = '#2ecc71'
        ax2.set_ylabel('Total Sourcing Cost (RM)', color=color_line, fontsize=11, fontweight='bold', labelpad=10)
        line = ax2.plot(products_sku, procurement_costs, color=color_line, marker='o', linewidth=2)
        ax2.tick_params(axis='y', labelcolor=color_line)

        # Custom Axis Tick Aesthetics syncing with theme
        ax1.tick_params(axis='x', colors=label_axis_color, labelsize=10)
        ax1.set_title("Restock Optimizer: Required Volumes & Supplier Costs", color=label_axis_color, fontsize=12, pad=15, fontweight='bold')
        ax1.yaxis.grid(True, linestyle='--', alpha=0.3, color=grid_line_color)

        for spine in list(ax1.spines.values()) + list(ax2.spines.values()):
            spine.set_visible(False)

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=15, pady=15)

class SettingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "System Settings")  

        self.dark_mode_switch = ctk.CTkSwitch(self, text="Enable Dark Mode Visualization" , command=self.toggle_dark_mode)
        self.dark_mode_switch.select()
        self.dark_mode_switch.pack(pady=20, padx=30, anchor="w")
        
        ctk.CTkButton(self, text="Sync Database", width=150).pack(pady=10, padx=30, anchor="w")
        ctk.CTkButton(self, text="Export Settings", width=150, border_width=1).pack(pady=10, padx=30, anchor="w")

    def toggle_dark_mode(self):
        if self.dark_mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

class HelpPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Help & Support Center")
        
        # User manual textbox
        help_text = ctk.CTkTextbox(self, width=600, height=300, font=("SF Pro Display", 12))
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