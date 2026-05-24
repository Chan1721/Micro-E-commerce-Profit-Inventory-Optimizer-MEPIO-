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
        
        ctk.CTkButton(self.action_card, text="⚙️ Update Fee Rates", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                      border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                      command=lambda: controller.show_page("settings")).pack(pady=8, padx=20, fill="x")

        ctk.CTkButton(self.action_card, text="📊 View Profit Trends", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                      border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                      command=lambda: controller.show_page("analytics")).pack(pady=8, padx=20, fill="x")

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
        input_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#2B2B2B"))
        input_frame.pack(pady=10, padx=20, fill="x")
        
        labels = ["Cost Price (RM):", "Selling Price (RM):", "Platform Fee Rate (%):", "Packaging Cost (RM):"]
        for i, text in enumerate(labels):
            ctk.CTkLabel(input_frame, text=text, text_color=("#333333", "#FFFFFF"), font=("Helvetica", 14, "bold")).grid(row=i, column=0, padx=20, pady=10, sticky="w")
            ctk.CTkEntry(input_frame, width=250, border_color="#E0E0E0", fg_color="#F8F9FA", text_color="#333333").grid(row=i, column=1, padx=20, pady=10)

        ctk.CTkButton(self, text="Calculate Net Profit", fg_color="#27ae60", hover_color="#219150").pack(pady=20)

class AnalyticsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Data Analytics")
        ctk.CTkLabel(self, text="Profit Trends & Performance Analysis", font=("Helvetica", 14), text_color="#333333").pack(pady=10)
        
        # Visual placeholder for charts
        chart_box = ctk.CTkFrame(self, height=300, fg_color=("#FFFFFF", "#2B2B2B"))
        chart_box.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(chart_box, text="[ Chart Visualization Module Loading... ]", font=("Helvetica", 14, "italic"), text_color="#888888").place(relx=0.5, rely=0.5, anchor="center")



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


        # Right Column: Platform Fee Configurations
        # dont know where to put first so,if want can just copy to other pages
        self.fee_card = ctk.CTkFrame(self.content_wrapper, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
        self.fee_card.pack(side="right", fill="both", expand=True, padx=(15, 0))

        ctk.CTkLabel(self.fee_card, text="Platform Fee Rates", font=("Helvetica", 16, "bold")).pack(pady=(25, 10), padx=25, anchor="w")
        ctk.CTkLabel(self.fee_card, text="Update the current commission rates for accurate profit calculation.", font=("Helvetica", 12), text_color="gray").pack(padx=25, anchor="w", pady=(0, 20))

        self.shopee_entry = ctk.CTkEntry(self.fee_card, placeholder_text="Shopee Fee (e.g. 5.5%)", width=250)
        self.shopee_entry.pack(pady=10, padx=25, anchor="w")

        self.tiktok_entry = ctk.CTkEntry(self.fee_card, placeholder_text="TikTok Shop Fee (e.g. 3.2%)", width=250)
        self.tiktok_entry.pack(pady=10, padx=25, anchor="w")

        self.lazada_entry = ctk.CTkEntry(self.fee_card, placeholder_text="Lazada Fee (e.g. 4.0%)", width=250)
        self.lazada_entry.pack(pady=10, padx=25, anchor="w")

        self.update_fee_btn = ctk.CTkButton(self.fee_card, text="Save Fee Updates", fg_color="#5DC66A", hover_color="#4CAF50", width=250, command=self.save_fees_mock)
        self.update_fee_btn.pack(pady=(25, 10), padx=25, anchor="w")

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