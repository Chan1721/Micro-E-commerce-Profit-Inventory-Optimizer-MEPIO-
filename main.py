import customtkinter as ctk #shortcut for customtkinter as ctk
import tkinter as tk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
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
        ctk.CTkLabel(logo_box, text="M", font=("Helvetica", 18, "bold"),
             text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # Text next to the logo
        text_col = ctk.CTkFrame(brand_frame, fg_color="transparent")
        text_col.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(text_col, text="MEPIO", font=("Helvetica", 17, "bold"),
             text_color="#4F6EF7").pack(anchor="w")
        ctk.CTkLabel(text_col, text="Profit & Inventory", font=("Helvetica", 10),
             text_color="#94A3B8").pack(anchor="w")

        # Thin grey line below the brand
        ctk.CTkFrame(self.sidebar_frame, height=1, fg_color="#E2E8F0").pack(
            fill="x", padx=16, pady=(14, 12))

        # Navigation items mapping[cite: 1]
        nav_items = [
            (" Dashboard", "dash"),
            (" Inventory", "inv"),
            (" Logistics", "logistics"),
            (" Calculator", "calculator"),
            (" Analytics", "analytics"),
            (" Settings", "settings"),
            (" Help & Support", "help")
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
            ("Total Revenue", "RM 12,450.00", "+5.2% vs last month", "up"), 
            ("Net Profit", "RM 4,200.50", "-1.5% vs last month", "down"), 
            ("Platform Fees", "RM 850.20", "+12.0% vs last month", "up"), 
            ("Low Stock", "5 Items", "Requires Attention", "down")
        ]
        
        for name, value, trend, direction in metrics:
            card = ctk.CTkFrame(self.stats_frame, corner_radius=15, fg_color=("#FFFFFF", "#2B2B2B"))
            card.pack(side="left", padx=10, fill="both", expand=True)
            ctk.CTkLabel(card, text=name, font=("Helvetica", 12), text_color="gray").pack(pady=(15, 0))
            ctk.CTkLabel(card, text=value, font=("Helvetica", 18, "bold")).pack(pady=(5, 15))

            trend_color = "#2ecc71" if direction == "up" else "#e74c3c"
            ctk.CTkLabel(card, text=trend, font=("Helvetica", 11, "bold"), text_color=trend_color).pack(pady=(0, 15))

            # Bottom layout wrapper (Left and Right)
        self.bottom_wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_wrapper.pack(fill="both", expand=True, padx=20, pady=20)

    #platform benchmarking chart on the left
        self.chart_frame = ctk.CTkFrame(self.bottom_wrapper, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
        self.chart_frame.pack(side="left", fill="both", expand=True) 
        
        ctk.CTkLabel(self.chart_frame, text="Platform Benchmarking", font=("Helvetica", 16, "bold")).pack(pady=(15, 0), anchor="w", padx=20)
        ctk.CTkLabel(self.chart_frame, text="Revenue · Net profit · Platform fees", font=("Helvetica", 12), text_color="gray").pack(anchor="w", padx=20)


        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            text_clr = "#CCCCCC"  
            grid_clr = "#444444"  
            
        else:
            text_clr = "#555555"  
            grid_clr = "#E0E0E0"  

        fig, ax = plt.subplots(figsize=(4,2), dpi=100)
        fig.patch.set_facecolor("none") 
        ax.set_facecolor("none")

        platforms = ['Shopee MY', 'TikTok Shop', 'Lazada'] 
        x = [0, 1, 2] 
        
    
        width = 0.15 


        revenue = [5800, 4100, 2600]
        net_profit = [1800, 1500, 900]
        platform_fees = [300, 200, 100]

        color_rev = '#637AFA'   
        color_prof = '#5DC66A'  
        color_fee = '#EAA844'   

        ax.bar([i - width for i in x], revenue, width=width, label='Revenue', color=color_rev)
        ax.bar(x, net_profit, width=width, label='Net profit', color=color_prof)
        ax.bar([i + width for i in x], platform_fees, width=width, label='Platform fees', color=color_fee)

        
        ax.set_xticks(x)
        ax.set_xticklabels(platforms, color=text_clr, fontsize=4, fontweight ='bold',fontname='Helvetica')
        ax.tick_params(axis='y', colors=text_clr, labelsize=5)

        for label in ax.get_yticklabels(): #params cant change fontname in tick_params, have to loop through labels
            label.set_fontname("Helvetica")
            label.set_fontsize(8)
            label.set_fontweight("bold")

        ax.yaxis.grid(True, color=grid_clr, linestyle='-', linewidth=0.5, alpha=0.5)
        ax.set_axisbelow(True) 
        for spine in ax.spines.values():
            spine.set_visible(False) 
        ax.spines['bottom'].set_visible(True) 
        ax.spines['bottom'].set_color(grid_clr)

    
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, frameon=False, labelcolor=text_clr, prop={'family': 'Helvetica', 'size': 8, 'weight': 'bold'})

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # --- Right Side: Vertical Quick Actions ---
        self.action_card = ctk.CTkFrame(self.bottom_wrapper, width=220, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
        self.action_card.pack(side="right", fill="y")
        self.action_card.pack_propagate(False) 
        
        ctk.CTkLabel(self.action_card, text="Quick Actions", font=("Helvetica", 16, "bold")).pack(pady=(20, 15))
        
        # Action Buttons
        ctk.CTkButton(self.action_card, text="➕ Calculate Profit", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                      border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                      command=lambda: controller.show_page("calculator")).pack(pady=8, padx=20, fill="x")
                      
        ctk.CTkButton(self.action_card, text="🔄 Sync Inventory", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                      border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                      command=lambda: controller.show_page("inv")).pack(pady=8, padx=20, fill="x")
                      
        ctk.CTkButton(self.action_card, text="📦 Restock Low Items", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                      border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                      command=lambda: controller.show_page("logistics")).pack(pady=8, padx=20, fill="x")
        
        ctk.CTkButton(self.action_card, text="📊 View Profit Trends", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                      border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                      command=lambda: controller.show_page("analytics")).pack(pady=8, padx=20, fill="x")


###### open style accordion for fee update
        self.fee_btn = ctk.CTkButton(self.action_card, text="⚙️ Update Fee Rates", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                      border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                      command=self.toggle_fee_accordion)
        self.fee_btn.pack(pady=8, padx=20, fill="x")

        self.accordion_frame = ctk.CTkFrame(self.action_card, fg_color=("#F8F9FA", "#1E1E1E"), corner_radius=8)
    
        ctk.CTkLabel(self.accordion_frame, text="Set current commission % :", font=("Helvetica", 11, "italic"), text_color="gray").pack(pady=(8, 0), padx=15, anchor="w")

        self.shopee_entry = ctk.CTkEntry(self.accordion_frame, placeholder_text="Shopee (e.g. 5.5)", height=28, font=("Helvetica", 11))
        self.shopee_entry.pack(pady=(10, 5), padx=15, fill="x")
        
        self.tiktok_entry = ctk.CTkEntry(self.accordion_frame, placeholder_text="TikTok (e.g. 3.2)", height=28, font=("Helvetica", 11))
        self.tiktok_entry.pack(pady=5, padx=15, fill="x")
        
        self.lazada_entry = ctk.CTkEntry(self.accordion_frame, placeholder_text="Lazada (e.g. 4.0)", height=28, font=("Helvetica", 11))
        self.lazada_entry.pack(pady=5, padx=15, fill="x")
        
        self.save_fee_btn = ctk.CTkButton(self.accordion_frame, text="Save & Apply", fg_color="#27ae60", hover_color="#219150", height=28, font=("Helvetica", 11, "bold"), command=self.save_fees_inline)
        self.save_fee_btn.pack(pady=(5, 10), padx=15, fill="x")

        self.is_accordion_open = False
    
    def toggle_fee_accordion(self):
        if self.is_accordion_open:
            self.accordion_frame.pack_forget()  
            self.is_accordion_open = False
        else:
            self.accordion_frame.pack(pady=5, padx=20, fill="x")  
            self.is_accordion_open = True

    def save_fees_inline(self):       
        s_fee = self.shopee_entry.get()
        t_fee = self.tiktok_entry.get()
        l_fee = self.lazada_entry.get()

        if not s_fee or not t_fee or not l_fee:
            import tkinter.messagebox as messagebox
            messagebox.showwarning("Incomplete", "Please fill in all rates!")
            return
        
        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE system_settings 
                SET shopee_fee=?, tiktok_fee=?, lazada_fee=? 
                WHERE setting_id=1
            ''', (float(s_fee), float(t_fee), float(l_fee)))
            
            conn.commit()
            conn.close()

            import tkinter.messagebox as messagebox
            messagebox.showinfo("Success", f"Fee rates updated successfully!\nShopee: {s_fee}%\nTikTok: {t_fee}%\nLazada: {l_fee}%") 
            
            self.toggle_fee_accordion()

        except ValueError:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", "Please enter valid numbers (e.g., 5.5)!")
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Database Error", f"Something went wrong: {e}")

######accordion style         

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
        self.input_frame = ctk.CTkScrollableFrame(self.main_container, corner_radius=15, fg_color=("#FFFFFF", "#252525"), width=500)
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
        ctk.CTkLabel(size_frame, text="Package Size Preset:", width=150, anchor="w", text_color=("#333333", "#E0E0E0")).pack(side="left")
        
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
        self.result_frame = ctk.CTkFrame(self.main_container, corner_radius=15, fg_color=("#FFFFFF", "#1e1e1e"))
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
            
            lbl = ctk.CTkLabel(row, text=label_text, width=180, anchor="w", text_color=("#333333", "#E0E0E0"))
            lbl.pack(side="left")
            
            entry = ctk.CTkEntry(row, placeholder_text=default_val)
            entry.insert(0, default_val)
            entry.pack(side="right", fill="x", expand=True)
            self.entries[label_text] = entry

    def create_result_row(self, label_text, value_text, color):
        row = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        row.pack(fill="x", padx=30, pady=12)
        
        lbl = ctk.CTkLabel(row, text=label_text, font=("Helvetica", 13), text_color=("#1A1A1A", "white"))
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
        Initializes the Advanced Restock Optimization Analytics Page.
        This framework addresses the Supervisor's feedback by calculating:
        1. Exact Recommended Reorder Quantity (Buy How Many)
        2. Expected Sourcing Capital Demands (Total Procurement Cost)
        3. Inventory Expiry Risk Matrix (Factoring in Expiration Dates)
        """
        super().__init__(parent, controller, "Restock & Expiry Optimizer")

        # --- Main Layout Framework (Two-Column Split Grid) ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # =========================================================================
        # LEFT COLUMN: CRITICAL ACTION ALERTS & STRATEGIC PROCUREMENT ADVISORY
        # =========================================================================
        self.left_frame = ctk.CTkFrame(self.main_container, width=320, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))

        # KPI Card 1: Total Sourcing Capital Required Immediately
        self.card_total_cost = ctk.CTkFrame(self.left_frame, fg_color="#e74c3c", corner_radius=10)
        self.card_total_cost.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(self.card_total_cost, text="Total Procurement Budget Needed", font=("Arial", 11, "bold"), text_color="white").pack(pady=(10, 2))
        ctk.CTkLabel(self.card_total_cost, text="RM 5,150.00", font=("Arial", 22, "bold"), text_color="white").pack(pady=(2, 10))

        # KPI Card 2: Impending Expiry Risk Warning
        self.card_expiry_alert = ctk.CTkFrame(self.left_frame, fg_color="#e67e22", corner_radius=10)
        self.card_expiry_alert.pack(fill="x", pady=10)
        ctk.CTkLabel(self.card_expiry_alert, text="🚨 Inventory Batches Near Expiry", font=("Arial", 11), text_color="white").pack(pady=(10, 2))
        ctk.CTkLabel(self.card_expiry_alert, text="85 Units At Risk", font=("Arial", 18, "bold"), text_color="white").pack(pady=(2, 10))

        # Supervisor Compliance Optimization Insight Console
        self.insight_box = ctk.CTkFrame(self.left_frame, fg_color="#1e1e1e", corner_radius=10)
        self.insight_box.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(self.insight_box, text="📋 Smart Sourcing Recommendations", font=("Arial", 13, "bold"), text_color="#27ae60").pack(pady=10, anchor="w", padx=15)
        
        # Advisory strings displaying precise 'Buy How Many' and 'Cost' metrics
        recommendation_text = (
            "• SKU: COS-MY-LIP-001\n"
            "  - Dynamic Order Qty: Buy 150 units\n"
            "  - Estimated Supplier Cost: RM 1,500.00\n"
            "  - Reason: Stock depletion imminent combined with 35 units batch expiring on June 15.\n\n"
            "• SKU: COS-MY-MAS-002\n"
            "  - Dynamic Order Qty: Buy 200 units\n"
            "  - Estimated Supplier Cost: RM 3,650.00\n"
            "  - Reason: Standard 7-day velocity depletion check; current batch expiry profile remains stable."
        )
        lbl_insight = ctk.CTkLabel(self.insight_box, text=recommendation_text, justify="left", font=("Arial", 11), text_color="#bbbbbb", wraplength=280)
        lbl_insight.pack(pady=5, padx=15, fill="both")

        # =========================================================================
        # RIGHT COLUMN: VISUAL REORDER QUANTITY & COST COMPARISON CHART
        # =========================================================================
        
        self.right_frame = ctk.CTkFrame(self.main_container, fg_color=("#FFFFFF", "#252525"), corner_radius=12)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Render the enhanced visual chart matching the supervisor's metrics
        self.render_optimization_chart()

    def render_optimization_chart(self):
        """
        Generates a dual-axis Matplotlib chart showcasing:
        1. Bars representing the exact reorder volume (Buy How Many) per product.
        2. A line plotting the corresponding financial procurement cost.
        """
        products_sku = ['Lipstick\n[LIP-001]', 'Mascara\n[MAS-002]', 'EyeLiner\n[EYE-003]']
        buy_quantities = [150, 200, 50]         # Exact volume to purchase (Buy How Many)
        procurement_costs = [1500, 3650, 500]   # Dynamic Cost calculations (RM)

        # Initialize the figure canvas frame
        fig, ax1 = plt.subplots(figsize=(6, 4), facecolor='#252525')
        ax1.set_facecolor('#252525')

        # Primary Axis (Left): Bar chart plotting Reorder Volumes
        color_bars = '#3498db'
        ax1.set_ylabel('Recommended Reorder Qty (Units)', color=color_bars, fontsize=11, fontweight='bold', labelpad=10)
        bars = ax1.bar(products_sku, buy_quantities, color=color_bars, width=0.35, alpha=0.8, label='Order Quantity')
        ax1.tick_params(axis='y', labelcolor=color_bars, colors='white')
        
        # Secondary Axis (Right): Twin line chart mapping the matching Cost Prices
        ax2 = ax1.twinx()
        color_line = '#2ecc71'
        ax2.set_ylabel('Total Sourcing Cost (RM)', color=color_line, fontsize=11, fontweight='bold', labelpad=10)
        line = ax2.plot(products_sku, procurement_costs, color=color_line, marker='o', linewidth=2, label='Procurement Cost (RM)')
        ax2.tick_params(axis='y', labelcolor=color_line, colors='white')

        # Format layout elements to match dark UI styles
        ax1.tick_params(axis='x', colors='white', labelsize=10)
        ax1.set_title("Restock Optimizer: Required Volumes & Supplier Costs", color='white', fontsize=12, pad=15, fontweight='bold')
        ax1.yaxis.grid(True, linestyle='--', alpha=0.1, color='gray')

        # Remove structural spine boarders
        for spine in list(ax1.spines.values()) + list(ax2.spines.values()):
            spine.set_visible(False)

        # Embed the Matplotlib canvas securely into CustomTkinter container layout
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)



    def calculate_all_roi(self):
        def get_roi(cost_entry, profit_entry, res_label):
            try:
                cost = float(cost_entry.get())
                profit = float(profit_entry.get())
                
                if cost == 0:
                    res_label.configure(text="Error", text_color="red")
                    return
                
                roi = (profit / cost) * 100
                
                res_label.configure(text=f"{roi:.1f}%", text_color="#27ae60" if roi > 0 else "red")
            except ValueError:
                res_label.configure(text="-- %", text_color="gray")

        get_roi(self.sp_cost, self.sp_profit, self.sp_res)
        get_roi(self.tk_cost, self.tk_profit, self.tk_res)
        get_roi(self.lz_cost, self.lz_profit, self.lz_res)

class SettingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "System Settings")  

        # --- Main Layout: Two-Column Container ---
        self.content_wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self.content_wrapper.pack(fill="both", expand=True, padx=40, pady=10)

        
        # Left Column: General System Preferences
        self.sys_card = ctk.CTkFrame(self.content_wrapper, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
        self.sys_card.pack(side="left", fill="both", expand=True, padx=(0, 15))

        ctk.CTkLabel(self.sys_card, text="General Preferences", font=("Helvetica", 16, "bold")).pack(pady=(25, 20), padx=25, anchor="w")

        self.dark_mode_switch = ctk.CTkSwitch(self.sys_card, text="Enable Dark Mode Visualization", command=self.toggle_dark_mode)
        self.dark_mode_switch.pack(pady=15, padx=25, anchor="w")

        self.sync_btn = ctk.CTkButton(self.sys_card, text="Sync Database", width=200, fg_color="#3498db")
        self.sync_btn.pack(pady=(20, 10), padx=25, anchor="w")

        self.export_btn = ctk.CTkButton(self.sys_card, text="Export Settings", width=200, fg_color="#3498db")
        self.export_btn.pack(pady=10, padx=25, anchor="w")



    # Backend Integration Placeholder 
    def save_fees_mock(self):
        shopee_fee = self.shopee_entry.get()
        tiktok_fee = self.tiktok_entry.get()
        lazada_fee = self.lazada_entry.get()
        
        print(f"[DEBUG] Fees Updated - Shopee: {shopee_fee} | TikTok: {tiktok_fee} | Lazada: {lazada_fee}")
        
        # TODO: Connect to database function once backend is ready
        # e.g., db.update_platform_fees(shopee_fee, tiktok_fee, lazada_fee)

    def toggle_dark_mode(self):
        if self.dark_mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

class HelpPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Help & Support Center")
        
        # User manual textbox
        help_text = ctk.CTkTextbox(self, width=600, height=300, font=("Helvetica", 12))
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