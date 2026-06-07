import customtkinter as ctk #shortcut for customtkinter as ctk
import tkinter as tk 
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import datetime
import random
from tkinter import messagebox
ctk.set_appearance_mode("light")

#importing the login page
from inventorypage import InventoryPage

class MEPIOApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("MEPIO - Profit & Inventory Optimizer")
        self.geometry("1100x650")

        # Configure main window grid layout to auto-expand in both dimensions
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar Configuration ---
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
        ctk.CTkLabel(logo_box, text="M", font=("Arial", 18, "bold"),
             text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # Text next to the logo
        text_col = ctk.CTkFrame(brand_frame, fg_color="transparent")
        text_col.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(text_col, text="MEPIO", font=("Arial", 17, "bold"),
             text_color="#4F6EF7").pack(anchor="w")
        ctk.CTkLabel(text_col, text="Profit & Inventory", font=("Arial", 10),
             text_color="#94A3B8").pack(anchor="w")

        # Thin grey line below the brand
        ctk.CTkFrame(self.sidebar_frame, height=1, fg_color="#E2E8F0").pack(
            fill="x", padx=16, pady=(14, 12))

        # Navigation items mapping
        nav_items = [
            (" Dashboard", "dash"),
            (" Orders", "orders"),
            (" Inventory", "inv"),
            (" Logistics", "logistics"),
            (" Calculator", "calculator"),
            (" Analytics", "analytics"),
            (" Settings", "settings"),
            (" Accounts", "accounts"),
            (" Help & Support", "help")
        ]

        # Generate sidebar buttons dynamically to avoid variable conflicts
        for text, page_key in nav_items:
            btn = ctk.CTkButton(self.sidebar_frame, text=f"  {text}", 
                                fg_color="transparent", text_color=("#475569","#F8FAFC"), hover_color="#e2e8f0",
                                font=("Arial", 14, "bold"), anchor="w",
                                command=lambda k=page_key: self.show_page(k))
            btn.pack(pady=5, padx=10, fill="x")

        # --- Page Manager Initialization ---
        self.pages = {}

        # Initialize all page classes
        self.pages["dash"] = DashboardPage(self, self)
        self.pages["orders"] = OrderPage(self, self)
        self.pages["inv"] = InventoryPage(self, self)
        self.pages["logistics"] = LogisticsPage(self, self)
        self.pages["calculator"] = CalculatorPage(self, self)
        self.pages["analytics"] = AnalyticsPage(self, self)
        self.pages["settings"] = SettingsPage(self, self)
        self.pages["accounts"] = AccountsPage(self, self)
        self.pages["help"] = HelpPage(self, self)

        # FIXED: Moved show_page down here so the self.pages dictionary exists before execution
        self.show_page("dash")
        
    def on_closing(self):
        self.quit()     
        self.destroy()

    def show_page(self, page_name):
        # Hide all pages using grid_forget
        for frame in self.pages.values():
            frame.grid_forget()
        
        # Display selected page in the main container area
        self.pages[page_name].grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

class BasePage(ctk.CTkFrame):
    """Template class for all pages to ensure UI consistency."""
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent") 
        self.header = ctk.CTkLabel(self, text="", font=("Arial", 24, "bold"), text_color="#3498db")
        
        # Decorative separator line
        line = ctk.CTkFrame(self, height=2, fg_color="#E0E0E0")
        self.bind("<Map>", self.on_page_show)

    def on_page_show(self, event):
        """Override this method in child classes to trigger actions when the page is shown."""
        if event.widget == self:
            pass

class DashboardPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
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
            ctk.CTkLabel(card, text=name, font=("Arial", 12), text_color="gray").pack(pady=(15, 0))
            ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold")).pack(pady=(5, 15))

            trend_color = "#2ecc71" if direction == "up" else "#e74c3c"
            ctk.CTkLabel(card, text=trend, font=("Arial", 11, "bold"), text_color=trend_color).pack(pady=(0, 15))

        # Bottom layout wrapper (Left and Right)
        self.bottom_wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_wrapper.pack(fill="both", expand=True, padx=20, pady=20)

        # platform benchmarking chart on the left
        self.chart_frame = ctk.CTkFrame(self.bottom_wrapper, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
        self.chart_frame.pack(side="left", fill="both", expand=True) 
        self.chart_canvas_widget = None
     
        
        ctk.CTkLabel(self.chart_frame, text="Platform Benchmarking", font=("Arial", 16, "bold")).pack(pady=(15, 0), anchor="w", padx=20)
        ctk.CTkLabel(self.chart_frame, text="Revenue · Net profit · Platform fees", font=("Arial", 12), text_color="gray").pack(anchor="w", padx=20)

        self.load_benchmark_data() # 启动动态读取！


        # --- Right Side: Vertical Quick Actions ---
        if not hasattr(self, "action_card"):
            self.action_card = ctk.CTkFrame(self.bottom_wrapper, width=220, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
            self.action_card.pack(side="right", fill="y", padx=(10, 0))
            self.action_card.pack_propagate(False) 
            
            ctk.CTkLabel(self.action_card, text="Quick Actions", font=("Arial", 16, "bold")).pack(pady=(20, 15))
            
            # Action Buttons
            ctk.CTkButton(self.action_card, text="➕ Calculate Profit", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                          border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                          command=lambda: self.master.show_page("calculator")).pack(pady=8, padx=20, fill="x")
                          
            ctk.CTkButton(self.action_card, text="🔄 Sync Inventory", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                          border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                          command=lambda: self.master.show_page("inv")).pack(pady=8, padx=20, fill="x")
                          
            ctk.CTkButton(self.action_card, text="📦 Restock Low Items", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                          border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                          command=lambda: self.master.show_page("logistics")).pack(pady=8, padx=20, fill="x")
            
            ctk.CTkButton(self.action_card, text="📊 View Profit Trends", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                          border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                          command=lambda: self.master.show_page("analytics")).pack(pady=8, padx=20, fill="x")

            self.fee_btn = ctk.CTkButton(self.action_card, text="⚙️ Update Fee Rates", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                          border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                          command=self.toggle_fee_accordion)
            self.fee_btn.pack(pady=8, padx=20, fill="x")

            self.accordion_frame = ctk.CTkFrame(self.action_card, fg_color=("#F8F9FA", "#1E1E1E"), corner_radius=8)
        
            ctk.CTkLabel(self.accordion_frame, text="Set current commission % :", font=("Arial", 11, "italic"), text_color="gray").pack(pady=(8, 0), padx=15, anchor="w")

            self.shopee_entry = ctk.CTkEntry(self.accordion_frame, placeholder_text="Shopee (e.g. 5.5)", height=28, font=("Arial", 11))
            self.shopee_entry.pack(pady=(10, 5), padx=15, fill="x")
            
            self.tiktok_entry = ctk.CTkEntry(self.accordion_frame, placeholder_text="TikTok (e.g. 3.2)", height=28, font=("Arial", 11))
            self.tiktok_entry.pack(pady=5, padx=15, fill="x")
            
            self.lazada_entry = ctk.CTkEntry(self.accordion_frame, placeholder_text="Lazada (e.g. 4.0)", height=28, font=("Arial", 11))
            self.lazada_entry.pack(pady=5, padx=15, fill="x")
            
            self.save_fee_btn = ctk.CTkButton(self.accordion_frame, text="Save & Apply", fg_color="#27ae60", hover_color="#219150", height=28, font=("Arial", 11, "bold"), command=self.save_fees_inline)
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

    def load_benchmark_data(self): 
        import sqlite3

        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()   

            cursor.execute("SELECT COUNT(*) FROM profit_records")
            record_count = cursor.fetchone()[0]

            if record_count == 0:
                # 🚨 数据库是空的！触发 Empty State
                conn.close()
                self.render_empty_state()
                return  

            cursor.execute("SELECT platform, SUM(selling_price), SUM(net_profit), SUM(platform_fee) FROM profit_records GROUP BY platform")
            data = cursor.fetchall()
            conn.close() 

            self.render_chart(data)

        except Exception as e:
            print(f"DB Error: {e}")
            self.render_empty_state()

    def render_chart(self, db_data):
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import customtkinter as ctk

        for widget in self.chart_frame.winfo_children():
            if not isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        platforms = ['Shopee', 'TikTok', 'Lazada']
        revenue = [0.0, 0.0, 0.0]
        net_profit = [0.0, 0.0, 0.0]
        platform_fees = [0.0, 0.0, 0.0]

        for row in db_data:
            db_plat = row[0]
            if db_plat in platforms:
                idx = platforms.index(db_plat)
                revenue[idx] = row[1] or 0.0
                net_profit[idx] = row[2] or 0.0
                platform_fees[idx] = row[3] or 0.0

        current_mode = ctk.get_appearance_mode()
        fig_face_color = "#FFFFFF" if current_mode == "Light" else "#2B2B2B"
        text_clr = "#CCCCCC" if current_mode == "Dark" else "#555555"
        grid_clr = "#444444" if current_mode == "Dark" else "#E0E0E0"

        fig, ax = plt.subplots(figsize=(4,2), dpi=100)
        fig.patch.set_facecolor(fig_face_color)
        ax.set_facecolor(fig_face_color)

        x = range(len(platforms))
        width = 0.15

        ax.bar([i - width for i in x], revenue, width=width, label='Revenue', color='#637AFA')
        ax.bar(x, net_profit, width=width, label='Net profit', color='#5DC66A')
        ax.bar([i + width for i in x], platform_fees, width=width, label='Platform fees', color='#EAA844')

        ax.set_xticks(x)
        ax.set_xticklabels(platforms, color=text_clr, fontsize=6, fontweight='bold', fontname='Helvetica')
        ax.tick_params(axis='y', colors=text_clr, labelsize=5)
        
        for label in ax.get_yticklabels():
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
        self.chart_canvas_widget = canvas.get_tk_widget()
        self.chart_canvas_widget.pack(fill="both", expand=True, padx=10, pady=(5, 10))        

    def render_empty_state(self):
        for widget in self.chart_frame.winfo_children():
            if not isinstance(widget, ctk.CTkLabel): # 保留 Title
                widget.destroy()

            empty_frame = ctk.CTkFrame(self.chart_frame, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True, pady=30)  

            ctk.CTkLabel(empty_frame, text="📊", font=("Helvetica", 40)).pack(pady=(10, 5))
            ctk.CTkLabel(empty_frame, text="No Benchmark Data Yet", font=("Helvetica", 14, "bold"), text_color="#94A3B8").pack() 

            ctk.CTkLabel(empty_frame, text="Run your first profit calculation in the\nCalculator to generate live insights.", font=("Helvetica", 11), text_color="#64748B").pack(pady=5) 

            ctk.CTkButton(empty_frame, text="Go to Calculator", width=120, height=28, fg_color="#3498db", font=("Helvetica", 11, "bold"),command=lambda: self.master.show_page("calculator") ).pack(pady=15)        

######accordion style         

class LogisticsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.header.configure(text="Shipping & Logistics Tracking")

        self.tabs = ctk.CTkTabview(self, width=800, height=400, fg_color=("#FFFFFF", "#2B2B2B"))
        self.tabs.pack(pady=(30, 10), padx=20, fill="both", expand=True)

        self.tab_in = self.tabs.add(" Inbound (Supplier Restock)")
        self.tab_out = self.tabs.add(" Outbound (Customer Orders)")

        self.recent_frames = {}

        self.build_tracking_ui(self.tab_in, "Inbound", "e.g., YT123456789 (China)")
        self.build_tracking_ui(self.tab_out, "Outbound", "e.g., 620000000000 (J&T)")

    def init_recent_db(self):
        import sqlite3
        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recent_tracking (
                    tracking_no TEXT PRIMARY KEY,
                    courier TEXT,
                    track_type TEXT,
                    last_tracked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Recent DB Init Error: {e}")    

    def build_tracking_ui(self, parent_tab, track_type, placeholder):
        search_frame = ctk.CTkFrame(parent_tab, fg_color="transparent")
        search_frame.pack(fill="x", pady=40, padx=20)
        
        ctk.CTkLabel(search_frame, text=f"{track_type} Track Number:", font=("Helvetica", 14, "bold")).pack(side="left", padx=(0, 10))
        
        entry = ctk.CTkEntry(search_frame, placeholder_text=placeholder, width=250, height=35)
        entry.pack(side="left", padx=10)
        
        if track_type == "Inbound":
            self.courier_var = ctk.StringVar(value="17TRACK (Universal)")
            couriers = ["17TRACK (Universal)", "Cainiao (淘宝集运)", "MyPoz (大马海运)"]
            dropdown = ctk.CTkOptionMenu(search_frame, variable=self.courier_var, values=couriers, width=160, height=35)
            dropdown.pack(side="left", padx=5)
            
            btn = ctk.CTkButton(search_frame, text="Track Parcel", fg_color="#3498db", font=("Helvetica", 13, "bold"), height=35,
                                command=lambda: self.execute_tracking(entry.get(), self.courier_var.get(),track_type))
            desc = "Select your specific China freight forwarder or universal tracker."
        else:
            btn = ctk.CTkButton(search_frame, text="Track via Tracking.my", fg_color="#3498db", font=("Helvetica", 13, "bold"), height=35,
                                command=lambda: self.execute_tracking(entry.get(), "tracking.my", track_type))
            desc = "Uses Tracking.my for Local Malaysia Couriers (J&T, Shopee Express, etc)."
            
        btn.pack(side="left", padx=10)

        recent_container = ctk.CTkFrame(parent_tab, fg_color="transparent")
        recent_container.pack(fill="x", padx=20, pady=(0, 20))
        
        self.recent_frames[track_type] = recent_container
        
        self.load_recents(track_type)
        
        ctk.CTkLabel(parent_tab, text=f"💡 Note: {desc}\nSystem will securely redirect to official tracking portal.", text_color="gray", font=("Helvetica", 12)).pack(pady=20)

    def load_recents(self, track_type):
        frame = self.recent_frames[track_type]
        
        for widget in list(frame.winfo_children()):
            widget.destroy()

        ctk.CTkLabel(frame, text="🕒 Recent:", font=("Helvetica", 12, "bold"), text_color="gray").pack(side="left", padx=(0, 10))

        import sqlite3
        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("SELECT tracking_no, courier FROM recent_tracking WHERE track_type=? ORDER BY last_tracked DESC LIMIT 4", (track_type,))
            recents = cursor.fetchall()
            conn.close()

            if not recents:
                ctk.CTkLabel(frame, text="No recent records yet.", font=("Helvetica", 11, "italic"), text_color="#A0A0A0").pack(side="left")
            else:
                for no, courier in recents:
                    short_courier = courier.split()[0]
                    btn_text = f"{no} ({short_courier})" 
                    
                    btn = ctk.CTkButton(
                        frame, text=btn_text, fg_color="#F1F5F9", text_color="#3498db", hover_color="#E2E8F0", 
                        font=("Helvetica", 11, "bold"), height=24, border_width=1, border_color="#D1D5DB",
                        command=lambda q=no, s=courier: self.execute_tracking(q, s, track_type) 
                    )
                    btn.pack(side="left", padx=5)


        except Exception as e:
            print(f" UI Refresh Error: {e}")

    def execute_tracking(self, query, service, track_type):
        import webbrowser
        import tkinter.messagebox as messagebox
        import sqlite3
        
        query = query.strip()
        if not query:
            messagebox.showwarning("Empty Field", "Please enter a tracking number first!")
            return
        
        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("REPLACE INTO recent_tracking (tracking_no, courier, track_type, last_tracked) VALUES (?, ?, ?, CURRENT_TIMESTAMP)", (query, service, track_type))
            conn.commit()
            conn.close()
            
            self.load_recents(track_type)
        except Exception as e:
            print(f"DB Save Error: {e}")
            
        if service == "17TRACK (Universal)":
            url = f"https://t.17track.net/en#nums={query}"
            
        elif service == "Cainiao (Taobao)":
            url = f"https://global.cainiao.com/detail.htm?mailNoList={query}"
            
        elif service == "MyPoz (Malaysia Sea Freight)":
            url = f"https://mypoz.com/tracking?no={query}"
            
        else: 
            url = f"https://tracking.my/track/{query}"
            
        webbrowser.open(url)

class CalculatorPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # 内部采用左右弹性分栏
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

        # --- Left Column: Inputs ---
        self.input_frame = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color=("#FFFFFF", "#252525"))
        self.input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5)

        # Section 1: Product & Platform Details
        ctk.CTkLabel(self.input_frame, text="1. Product & Platform Details", font=("Helvetica", 16, "bold"), text_color="#3498db").pack(pady=(10, 15), anchor="w", padx=20)

        #cwl加的
        self.platform_var = ctk.StringVar(value="Shopee")
        p_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        p_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(p_frame, text="Target Platform:", width=180, anchor="w", text_color=("#333333", "#E0E0E0")).pack(side="left")
        ctk.CTkOptionMenu(p_frame, variable=self.platform_var, values=["Shopee", "TikTok", "Lazada"]).pack(side="right", fill="x", expand=True)
        #cwl加的

        self.entries = {}
        base_fields = [
            ("Cost Price (RM)", ""),
            ("Selling Price (RM)", ""),
            ("Platform Fee (%)", ""),
            ("Shipping Fee Paid by Seller (RM)", "")
        ]
        self.create_input_fields(base_fields)

        ctk.CTkLabel(self.input_frame, text="2. Packaging Cost Breakdown", font=("Arial", 16, "bold"), text_color="#3498db").pack(pady=(20, 15), anchor="w", padx=20)
        
        size_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        size_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(size_frame, text="Package Size Preset:", width=150, anchor="w", text_color=("#333333", "#E0E0E0")).pack(side="left")
        
        self.size_option = ctk.CTkOptionMenu(
            size_frame, 
            values=["Small Flyer (RM 0.20)", "Medium Box (RM 0.80)", "Large Box (RM 1.50)", "Custom / Manual"],
            command=self.on_size_preset_change
        )
        self.size_option.pack(side="right", fill="x", expand=True)

        breakdown_fields = [
            ("Base Package Cost (RM)", ""),
            ("Labor Cost per Item (RM)", ""),
            ("Other Buffer Cost (RM)", "")
        ]
        self.create_input_fields(breakdown_fields)

        self.calc_btn = ctk.CTkButton(self.input_frame, text="Calculate Net Profit", 
                                      fg_color="#27ae60", hover_color="#219150", 
                                      font=("Arial", 14, "bold"),
                                      command=self.perform_calculation)
        self.calc_btn.pack(pady=25, padx=40, fill="x")

        # --- Right Column: Financial Results ---
        self.result_frame = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color=("#FFFFFF", "#1e1e1e"), width=300)
        self.result_frame.pack(side="right", fill="both", expand=False, padx=(10, 0), pady=5)

        ctk.CTkLabel(self.result_frame, text="Financial Summary", font=("Arial", 16, "bold"), text_color="#3498db").pack(pady=15)

        self.res_net_profit = self.create_result_row("Net Profit:", "RM 0.00", "#27ae60")
        self.res_roi = self.create_result_row("ROI (%):", "0.00%", "#3498db")
        self.res_total_packaging = self.create_result_row("Total Packaging Cost:", "RM 0.00", "#e67e22")
        self.res_fees = self.create_result_row("Platform Fees:", "RM 0.00", "#e74c3c")
        
        self.lbl_insight = ctk.CTkLabel(self.result_frame, text="Insight: Enter figures to run optimization analysis.", 
                                        font=("Arial", 12, "italic"), text_color="gray", wraplength=250)
        self.lbl_insight.pack(side="bottom", pady=30, padx=20)

    def create_input_fields(self, fields):
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
        lbl = ctk.CTkLabel(row, text=label_text, font=("Arial", 13), text_color=("#1A1A1A", "white"))
        lbl.pack(side="left")
        val_lbl = ctk.CTkLabel(row, text=value_text, font=("Arial", 18, "bold"), text_color=color)
        val_lbl.pack(side="right")
        return val_lbl

    def on_size_preset_change(self, choice):
        if "Small Flyer" in choice:
            self.update_entry_value("Base Package Cost (RM)", "0.20")
        elif "Medium Box" in choice:
            self.update_entry_value("Base Package Cost (RM)", "0.80")
        elif "Large Box" in choice:
            self.update_entry_value("Base Package Cost (RM)", "1.50")

    def update_entry_value(self, field_name, new_value):
        self.entries[field_name].delete(0, tk.END)
        self.entries[field_name].insert(0, new_value)

    def perform_calculation(self):
        try:
            cost = float(self.entries["Cost Price (RM)"].get())
            selling = float(self.entries["Selling Price (RM)"].get())
            fee_p = float(self.entries["Platform Fee (%)"].get()) / 100
            shipping = float(self.entries["Shipping Fee Paid by Seller (RM)"].get())
            package_base = float(self.entries["Base Package Cost (RM)"].get())
            labor = float(self.entries["Labor Cost per Item (RM)"].get())
            buffer = float(self.entries["Other Buffer Cost (RM)"].get())

            total_packaging = package_base + labor + buffer
            platform_fee_amount = selling * fee_p
            total_cost = cost + platform_fee_amount + shipping + total_packaging
            net_profit = selling - total_cost
            roi = (net_profit / cost * 100) if cost > 0 else 0

            #cwladd
            selected_platform = self.platform_var.get()
            import sqlite3
            try:
                conn = sqlite3.connect('mepio_system.db')
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO profit_records 
                    (sku, platform, selling_price, cost_price, platform_fee, net_profit) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, ("SIMULATION", selected_platform, selling, cost, platform_fee_amount, net_profit))
                
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Sync DB Error: {e}")
            #cwladd    

            # 4. Render output data strings back to UI elements
            self.res_net_profit.configure(text=f"RM {net_profit:.2f}")
            self.res_roi.configure(text=f"{roi:.2f}%")
            self.res_total_packaging.configure(text=f"RM {total_packaging:.2f}")
            self.res_fees.configure(text=f"RM {platform_fee_amount:.2f}")
            
            if roi < 15:
                self.lbl_insight.configure(text="⚠️ Warning: Low ROI!", text_color="#e74c3c")
            else:
                self.lbl_insight.configure(
                    text="✅ Healthy Margin: This pricing setup efficiently covers fine packaging and provides strong commercial scale.",
                    text_color="#27ae60"
                )

            self.run_roi_benchmarking()    
            
        except ValueError:
            self.res_net_profit.configure(text="Invalid Input", text_color="#e74c3c")

    def run_roi_benchmarking(self):
        import sqlite3
        import tkinter.messagebox as messagebox

        try:
            cost_str = self.entries["Cost Price (RM)"].get()
            selling_str = self.entries["Selling Price (RM)"].get()

            if not cost_str or not selling_str:
                return
            
            cost = float(cost_str)
            selling = float(selling_str)
            if cost <= 0 or selling <= 0:
                return
            
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT COUNT(*) FROM inventory")
                item_count = cursor.fetchone()[0]
            except sqlite3.OperationalError:
                item_count = 0  
            
            if item_count == 0:
                conn.close() 
                self.lbl_insight.configure(
                    text="⚠️ Benchmarking Unavailable! Please add initial items in Inventory first.",
                    text_color="#C0392B"
                )
                return

            cursor.execute("SELECT shopee_fee, tiktok_fee, lazada_fee FROM system_settings WHERE setting_id=1")
            row = cursor.fetchone()
            if row:
                shopee_fee_pct, tiktok_fee_pct, lazada_fee_pct = row
            else:
                shopee_fee_pct, tiktok_fee_pct, lazada_fee_pct = 5.5, 3.2, 4.0    

            conn.close()

            shopee_fee_amt = selling * (shopee_fee_pct / 100)
            tiktok_fee_amt = selling * (tiktok_fee_pct / 100)
            lazada_fee_amt = selling * (lazada_fee_pct / 100)

            try:
                shipping = float(self.entries["Shipping Fee Paid by Seller (RM)"].get())
            except:
                shipping = 0.0
                
            try:
                pkg_base = float(self.entries["Base Package Cost (RM)"].get())
                labor = float(self.entries["Labor Cost per Item (RM)"].get())
                buffer_cost = float(self.entries["Other Buffer Cost (RM)"].get())
                total_pkg = pkg_base + labor + buffer_cost
            except:
                total_pkg = 0.20
                
            shopee_net = selling - cost - shipping - total_pkg - shopee_fee_amt
            tiktok_net = selling - cost - shipping - total_pkg - tiktok_fee_amt
            lazada_net = selling - cost - shipping - total_pkg - lazada_fee_amt

            shopee_roi = (shopee_net / cost) * 100
            tiktok_roi = (tiktok_net / cost) * 100
            lazada_roi = (lazada_net / cost) * 100

            rois = {"Shopee": shopee_roi, "TikTok Shop": tiktok_roi, "Lazada": lazada_roi}
            best_platform = max(rois, key=rois.get)


            first_insight = self.lbl_insight.cget("text")
            
            second_insight = (
                f"📊 Live Benchmarking (DB Rates):\n"
                f"• Shopee: {shopee_roi:.0f}% | TikTok: {tiktok_roi:.0f}% | Lazada: {lazada_roi:.0f}%\n"
                f"💡 ADVICE: [{best_platform}] is the optimal platform."
            )
            
            combined_insight = f"{first_insight}\n\n{second_insight}"
            
            self.lbl_insight.configure(
                text=combined_insight, 
                text_color="#1B4F72" #3498db for main text, #C0392B for warnings
            )

        except ValueError:
            pass 
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"System Error: {e}")   


class AnalyticsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.bg_side_panel = ("#F8FAFC", "#1E1E1E")
        self.bg_card_inner = ("#FFFFFF", "#252525")
        self.text_main_color = ("#1E293B", "#F1F5F9")
        self.text_sub_color = ("#64748B", "#94A3B8")

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

        # LEFT COLUMN
        self.left_frame = ctk.CTkFrame(self.content_frame, width=340, corner_radius=15, fg_color=self.bg_side_panel)
        self.left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))

        # KPI 1
        self.card_total_cost = ctk.CTkFrame(self.left_frame, fg_color=("#FF4D4D", "#E74C3C"), corner_radius=10)
        self.card_total_cost.pack(fill="x", pady=10, padx=15)
        ctk.CTkLabel(self.card_total_cost, text="Total Procurement Budget Needed", font=("Arial", 11, "bold"), text_color="white").pack(pady=(10, 2))
        self.lbl_total_cost_val = ctk.CTkLabel(self.card_total_cost, text="RM 0.00", font=("Arial", 22, "bold"), text_color="white")
        self.lbl_total_cost_val.pack(pady=(2, 10))

        # KPI 2
        self.card_expiry_alert = ctk.CTkFrame(self.left_frame, fg_color=("#FFA502", "#E67E22"), corner_radius=10)
        self.card_expiry_alert.pack(fill="x", pady=10, padx=15)
        ctk.CTkLabel(self.card_expiry_alert, text="🚨 Inventory Batches Near Expiry", font=("Arial", 11), text_color="white").pack(pady=(10, 2))
        self.lbl_expiry_val = ctk.CTkLabel(self.card_expiry_alert, text="0 Units At Risk", font=("Arial", 18, "bold"), text_color="white")
        self.lbl_expiry_val.pack(pady=(2, 10))

        # Inputs
        ctk.CTkLabel(self.left_frame, text="📊 Manual Optimization Inputs", font=("Arial", 13, "bold"), text_color="#3498db").pack(pady=(15, 10), anchor="w", padx=15)
        
        self.entries = {}
        input_fields = [
            ("Current Local Stock (Units)", "50"),
            ("Average Daily Sales (Units)", "10"),
            ("Stock Near Expiry (Units)", "35"),
            ("Supplier Cost per Unit (RM)", "10.00")
        ]
        
        for label_text, default_val in input_fields:
            row = ctk.CTkFrame(self.left_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=5)
            lbl = ctk.CTkLabel(row, text=label_text, anchor="w", font=("Arial", 11), text_color=self.text_main_color)
            lbl.pack(side="left")
            entry = ctk.CTkEntry(row, placeholder_text=default_val, width=80)
            entry.insert(0, default_val)
            entry.pack(side="right")
            self.entries[label_text] = entry

        self.btn_calculate = ctk.CTkButton(
            self.left_frame, text="Run Restock Optimization", 
            fg_color="#27ae60", hover_color="#219150", 
            font=("Arial", 12, "bold"), command=self.execute_restock_analysis
        )
        self.btn_calculate.pack(pady=15, padx=15, fill="x")

        # Insight Box
        self.insight_box = ctk.CTkFrame(self.left_frame, fg_color=self.bg_card_inner, corner_radius=10)
        self.insight_box.pack(fill="both", expand=True, pady=10, padx=15)
        ctk.CTkLabel(self.insight_box, text="📋 Smart Sourcing Recommendations", font=("Arial", 13, "bold"), text_color="#27ae60").pack(pady=10, anchor="w", padx=15)
        self.lbl_insight = ctk.CTkLabel(self.insight_box, text="", justify="left", font=("Arial", 11), text_color=self.text_sub_color, wraplength=280)
        self.lbl_insight.pack(pady=(0, 15), padx=15, fill="both")

        # RIGHT COLUMN
        self.right_frame = ctk.CTkFrame(self.content_frame, fg_color=self.bg_card_inner, corner_radius=12)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.canvas_widget = None
        self.execute_restock_analysis()

    def on_page_show(self, event):
        """when the Analytics page is shown, re-run the analysis to refresh insights and charts with current input values"""
        if event.widget == self:
            self.execute_restock_analysis()

    def execute_restock_analysis(self):
        try:
            current_stock = int(self.entries["Current Local Stock (Units)"].get())
            daily_sales = int(self.entries["Average Daily Sales (Units)"].get())
            expiry_stock = int(self.entries["Stock Near Expiry (Units)"].get())
            unit_cost = float(self.entries["Supplier Cost per Unit (RM)"].get())

            target_30d_demand = daily_sales * 30
            usable_safe_stock = max(0, current_stock - expiry_stock)
            recommended_buy_qty = max(0, target_30d_demand - usable_safe_stock)
            total_procurement_cost = recommended_buy_qty * unit_cost

            self.lbl_total_cost_val.configure(text=f"RM {total_procurement_cost:,.2f}")
            self.lbl_expiry_val.configure(text=f"{expiry_stock} Units At Risk")

            recommendation_text = (
                f"• Target 30-Day Demand: {target_30d_demand} units\n"
                f"• Adjusted Usable Stock: {usable_safe_stock} units\n"
                f"  (Deducted {expiry_stock} units near expiry risk)\n\n"
                f"➔ Recommended Buy: {recommended_buy_qty} units\n"
                f"➔ Sourcing Cost: RM {total_procurement_cost:,.2f}"
            )
            self.lbl_insight.configure(text=recommendation_text)

            self.render_optimization_chart(recommended_buy_qty, total_procurement_cost)
        except ValueError:
            if hasattr(self, 'lbl_insight'):
                self.lbl_insight.configure(text="⚠️ Error: Please check inputs. Use digits only.", text_color="#e74c3c")

    def render_optimization_chart(self, buy_qty, total_cost):
        # FIXED: Clear previous active figures to completely resolve the Matplotlib cache color lock
        plt.close('all')

        if self.canvas_widget is not None:
            self.canvas_widget.destroy()

        current_mode = ctk.get_appearance_mode()
        fig_face_color = "#FFFFFF" if current_mode == "Light" else "#252525"
        label_axis_color = "#1E293B" if current_mode == "Light" else "#FFFFFF"
        grid_line_color = "#E2E8F0" if current_mode == "Light" else "#404040"

        products_sku = ['Manual Item\n[Simulated]', 'Mascara\n[MAS-002]', 'EyeLiner\n[EYE-003]']
        buy_quantities = [buy_qty, 200, 50] 
        procurement_costs = [total_cost, 3650, 500]

        # FIXED: Reduced base canvas figure sizes to scale perfectly without cutoff on non-fullscreen resolutions
        fig, ax1 = plt.subplots(figsize=(4.2, 3.2), facecolor=fig_face_color)
        ax1.set_facecolor(fig_face_color)

        color_bars = '#3498db'
        ax1.set_ylabel('Recommended Reorder Qty (Units)', color=color_bars, fontsize=10, fontweight='bold', labelpad=10)
        bars = ax1.bar(products_sku, buy_quantities, color=color_bars, width=0.3, alpha=0.8)
        ax1.tick_params(axis='y', labelcolor=color_bars, labelsize=9)
        
        ax2 = ax1.twinx()
        color_line = '#2ecc71'
        ax2.set_ylabel('Total Sourcing Cost (RM)', color=color_line, fontsize=10, fontweight='bold', labelpad=10)
        line = ax2.plot(products_sku, procurement_costs, color=color_line, marker='o', linewidth=2)
        ax2.tick_params(axis='y', labelcolor=color_line, labelsize=9)

        ax1.tick_params(axis='x', colors=label_axis_color, labelsize=9)
        ax1.set_title("Restock Optimizer: Required Volumes & Supplier Costs", color=label_axis_color, fontsize=11, pad=15, fontweight='bold')
        ax1.yaxis.grid(True, linestyle='--', alpha=0.3, color=grid_line_color)

        for spine in list(ax1.spines.values()) + list(ax2.spines.values()):
            spine.set_visible(False)

        # FIXED: Enforce clear padding layout logic inside smaller window bounds
        fig.tight_layout(pad=1.5)

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=5, pady=5)

class SettingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)  
        self.content_wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self.content_wrapper.pack(fill="both", expand=True, padx=40, pady=10)
        
        self.sys_card = ctk.CTkFrame(self.content_wrapper, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
        self.sys_card.pack(side="left", fill="both", expand=True, padx=(0, 15))

        ctk.CTkLabel(self.sys_card, text="General Preferences", font=("Arial", 16, "bold")).pack(pady=(25, 20), padx=25, anchor="w")

        self.dark_mode_switch = ctk.CTkSwitch(self.sys_card, text="Enable Dark Mode Visualization", command=self.toggle_dark_mode)
        self.dark_mode_switch.pack(pady=15, padx=25, anchor="w")

        self.sync_btn = ctk.CTkButton(self.sys_card, text="Sync Database", width=200, fg_color="#3498db")
        self.sync_btn.pack(pady=(20, 10), padx=25, anchor="w")

        self.export_btn = ctk.CTkButton(self.sys_card, text="Export Settings", width=200, fg_color="#3498db")
        self.export_btn.pack(pady=10, padx=25, anchor="w")

    def toggle_dark_mode(self):
        if self.dark_mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

class HelpPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        help_text = ctk.CTkTextbox(self, width=600, height=300, font=("Arial", 12))
        help_text.pack(pady=10, padx=20, fill="both", expand=True)
        help_text.insert("0.0", "MEPIO SYSTEM DOCUMENTATION\n\n"
                               "1. DASHBOARD: View real-time profit and revenue metrics.\n"
                               "2. CALCULATOR: Pre-calculate profit margins before product listing.\n"
                               "3. LOGISTICS: Manage shipping fees and track local orders.\n"
                               "4. SETTINGS: Adjust platform commission rates for Shopee/TikTok.")
        help_text.configure(state="disabled")

class OrderPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.bg_card_inner = ("#FFFFFF", "#252525")
        self.bg_row_even = ("#F1F5F9", "#1D1E1F")
        self.text_main = ("#1E293B", "#F1F5F9")
        self.text_sub = ("#64748B", "#94A3B8")

        self.current_platform_filter = "All"
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Filter and Control Bar
        self.filter_bar = ctk.CTkFrame(self.main_container, fg_color=self.bg_card_inner, corner_radius=12)
        self.filter_bar.pack(fill="x", pady=(0, 10))

        lbl_filter_title = ctk.CTkLabel(self.filter_bar, text="Platform Channel:", font=("Arial", 12, "bold"), text_color=self.text_main)
        lbl_filter_title.pack(side="left", padx=(20, 10), pady=15)

        platforms = ["All", "Shopee", "TikTok", "Lazada"]
        self.tab_buttons = {}
        for p in platforms:
            btn = ctk.CTkButton(
                self.filter_bar, text=p, width=80, height=28,
                fg_color="#3498db" if p == "All" else "transparent",
                text_color="white" if p == "All" else self.text_main,
                border_width=1 if p != "All" else 0,
                border_color="#3498db",
                command=lambda choice=p: self.filter_by_platform(choice)
            )
            btn.pack(side="left", padx=5)
            self.tab_buttons[p] = btn

        # NEW ACTION: Dynamic API Sync Trigger Button on the right
        self.btn_sync_orders = ctk.CTkButton(
            self.filter_bar,
            text="🔄 Sync Orders",
            fg_color="#3498db",
            hover_color="#2980b9",
            height=28,
            font=("Arial", 11, "bold"),
            command=self.trigger_api_order_pull
        )
        self.btn_sync_orders.pack(side="right", padx=20, pady=10)

        # Meta Information Banner
        self.meta_info_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.meta_info_frame.pack(fill="x", pady=(5, 0))

        lbl_notice = ctk.CTkLabel(
            self.meta_info_frame, 
            text="* Live Data Node: Connected via local secure token gateway handshake.", 
            font=("Arial", 11, "italic"), 
            text_color="#e67e22"
        )
        lbl_notice.pack(side="left", padx=5)

        lbl_unit = ctk.CTkLabel(
            self.meta_info_frame, 
            text="Unit: Gross Revenue (RM) | Quantity (Pcs)", 
            font=("Arial", 11, "bold"), 
            text_color=self.text_sub
        )
        lbl_unit.pack(side="right", padx=5)

        # Table Header Framework Layout
        self.table_header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.table_header.pack(fill="x", pady=(15, 0), padx=25)

        ctk.CTkLabel(self.table_header, text="Platform", font=("Arial", 11, "bold"), text_color=self.text_sub, width=100, anchor="w").pack(side="left")
        ctk.CTkLabel(self.table_header, text="Order Credentials & Items [Mapped via ShopID]", font=("Arial", 11, "bold"), text_color=self.text_sub, anchor="w").pack(side="left", padx=15)
        ctk.CTkLabel(self.table_header, text="Status", font=("Arial", 11, "bold"), text_color=self.text_sub, width=80, anchor="center").pack(side="right", padx=15)
        ctk.CTkLabel(self.table_header, text="Order Value", font=("Arial", 11, "bold"), text_color=self.text_sub, width=80, anchor="e").pack(side="right", padx=15)

        # Scrollable grid canvas area
        self.order_table_frame = ctk.CTkScrollableFrame(self.main_container, corner_radius=12, fg_color=self.bg_card_inner)
        self.order_table_frame.pack(fill="both", expand=True, pady=(5, 10), padx=5)

        # Initial fetch to render data from SQLite
        self.render_filtered_list()

    def on_page_show(self, event):
        """Triggers dynamic database refetch whenever the user navigates into this view tab viewpoint."""
        if event.widget == self:
            self.render_filtered_list()

    def filter_by_platform(self, selected_platform):
        self.current_platform_filter = selected_platform
        for p, btn in self.tab_buttons.items():
            if p == selected_platform:
                btn.configure(fg_color="#3498db", text_color="white", border_width=0)
            else:
                btn.configure(fg_color="transparent", text_color=self.text_main, border_width=1)
        self.render_filtered_list()

    def trigger_api_order_pull(self):
        """Fetches and synchronizes live order items exclusively for marketplace accounts linked by the user."""
        # 1. Query the database to find real shops connected by the user
        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("SELECT platform, shop_id FROM linked_accounts")
            active_shops = cursor.fetchall()
        except sqlite3.OperationalError:
            active_shops = []

        # 2. Guard clause: If the user hasn't linked any real shop yet, block synchronization
        if not active_shops:
            messagebox.showwarning(
                "Sync Warning", 
                "No connected channels found!\n\nPlease link a real Shopee, TikTok, or Lazada account first via the Accounts panel."
            )
            if 'conn' in locals():
                conn.close()
            return

        # 3. Simulate getting real order payload matching the user's specific linked shops
        synced_count = 0
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        for platform, shop_id in active_shops:
            # Generate a realistic mock order item bound strictly to this specific shop_id
            order_id = f"ORD-{platform[:3].upper()}-{random.randint(100000, 999999)}"
            product_name = f" [{shop_id}] Premium Cosmetic Package SKU-{random.randint(10,99)}"
            order_value = f"RM {round(random.uniform(25.0, 150.0), 2)}"
            
            # Insert the customized order entry straight into database
            cursor.execute('''
                INSERT OR REPLACE INTO marketplace_orders 
                (order_id, product_name, platform, shop_id, order_value, order_status, synced_at)
                VALUES (?, ?, ?, ?, ?, 'Unfulfilled', ?)
            ''', (order_id, product_name, platform, shop_id, order_value, current_time))
            
            # Update the last_synced timestamp on the user's account row to show progress
            cursor.execute(
                "UPDATE linked_accounts SET last_synced = ? WHERE shop_id = ?",
                (current_time, shop_id)
            )
            synced_count += 1

        conn.commit()
        conn.close()

        # 4. Notify user and trigger local UI refreshing if applicable
        messagebox.showinfo(
            "Sync Complete", 
            f"🎉 Order stream refreshed successfully!\nSynchronized {synced_count} real multi-channel orders into data matrix."
        )
        
        # If your order page has a list drawing function, invoke it here to show new data
        if hasattr(self, 'refresh_orders_table'):
            self.refresh_orders_table()
        elif hasattr(self, 'load_orders'):
            self.load_orders()

        conn.commit()
        conn.close()

        messagebox.showinfo("Sync Success", f"API synchronization execution complete!\nDownloaded {synced_count} fresh streaming orders across all linked store credentials.")
        self.render_filtered_list()

    def render_filtered_list(self):
        """Reads synced streaming data fields straight from the SQLite engine cache matrix."""
        for widget in self.order_table_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('mepio_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT platform, order_id, items, order_value, status, status_color FROM marketplace_orders")
        db_orders = cursor.fetchall()
        conn.close()

        if not db_orders:
            lbl_empty = ctk.CTkLabel(
                self.order_table_frame, 
                text="[ No synchronized live orders cached. Click '🔄 Sync Orders via API' to pull streaming streams. ]", 
                text_color=self.text_sub, 
                font=("Arial", 12, "italic")
            )
            lbl_empty.pack(pady=50, expand=True)
            return

        for platform, order_id, items, value, status, status_color in db_orders:
            # Apply upper-tier UI channel navigation view filter
            if self.current_platform_filter != "All" and self.current_platform_filter not in platform:
                continue

            row = ctk.CTkFrame(self.order_table_frame, fg_color=self.bg_row_even, corner_radius=8)
            row.pack(fill="x", padx=20, pady=5)

            p_color = "#ff4500" if "Shopee" in platform else ("#111111", "#ffffff") if "TikTok" in platform else "#000080"
            lbl_platform = ctk.CTkLabel(row, text=f"[{platform}]", font=("Arial", 11, "bold"), text_color=p_color, width=100, anchor="w")
            lbl_platform.pack(side="left", padx=(15, 5), pady=8)

            lbl_details = ctk.CTkLabel(row, text=f"ID: {order_id}   |   {items}", font=("Arial", 12), text_color=self.text_main, anchor="w")
            lbl_details.pack(side="left", padx=15)

            lbl_status = ctk.CTkLabel(row, text=status, font=("Arial", 10, "bold"), text_color="white", fg_color=status_color, corner_radius=5, width=80)
            lbl_status.pack(side="right", padx=15)

            lbl_value = ctk.CTkLabel(row, text=value, font=("Arial", 12, "bold"), text_color=self.text_main, width=80, anchor="e")
            lbl_value.pack(side="right", padx=15)

class AccountsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.bg_card = ("#FFFFFF", "#252525")
        self.text_main = ("#1E293B", "#F1F5F9")
        self.text_sub = ("#64748B", "#94A3B8")

        # Main layout structure
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- UPPER SECTION: Modern One-Click Connect Card ---
        self.link_panel = ctk.CTkFrame(self.main_container, fg_color=self.bg_card, corner_radius=12)
        self.link_panel.pack(fill="x", pady=(0, 15), padx=5)

        ctk.CTkLabel(self.link_panel, text="🔌 Connect Marketplace Channel", font=("Arial", 15, "bold"), text_color="#2ecc71").pack(anchor="w", padx=20, pady=(15, 2))
        ctk.CTkLabel(self.link_panel, text="Link your merchant account automatically via secure official OAuth 2.0 handshake.", font=("Arial", 11), text_color=self.text_sub).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Action Row for One-Click OAuth
        oauth_row = ctk.CTkFrame(self.link_panel, fg_color="transparent")
        oauth_row.pack(fill="x", padx=20, pady=(0, 15))

        self.opt_platform = ctk.CTkOptionMenu(oauth_row, values=["Shopee MY", "TikTok Shop", "Lazada MY"], width=150)
        self.opt_platform.pack(side="left", padx=(0, 15))

        self.btn_oauth = ctk.CTkButton(
            oauth_row, 
            text="🚀 Instant Login & Link Account", 
            fg_color="#2ecc71", 
            hover_color="#27ae60", 
            font=("Arial", 12, "bold"), 
            width=220,
            command=self.open_mock_oauth_browser
        )
        self.btn_oauth.pack(side="left")

        # --- PROGRESSIVE DISCLOSURE: Hidden Developer Corner ---
        self.advanced_btn = ctk.CTkButton(
            self.link_panel, 
            text="⚙️ Advanced: Manual API Token Entry", 
            fg_color="transparent", 
            text_color=self.text_sub,
            hover=False,
            font=("Arial", 11, "underline"),
            width=180,
            anchor="w"
        )
        self.advanced_btn.pack(anchor="w", padx=20, pady=(0, 10))
        self.advanced_btn.bind("<Button-1>", lambda e: self.toggle_manual_accordion())

        # Collapsible frame for manual tokens (Hidden by default)
        self.manual_accordion = ctk.CTkFrame(self.link_panel, fg_color=("#F8FAFC", "#1E1E1E"), corner_radius=8)
        self.is_accordion_open = False

        self.ent_shop_id = ctk.CTkEntry(self.manual_accordion, placeholder_text="Developer Shop ID", width=150)
        self.ent_shop_id.pack(side="left", padx=10, pady=10)

        self.ent_token = ctk.CTkEntry(self.manual_accordion, placeholder_text="API Access Token/Key", width=250, show="*")
        self.ent_token.pack(side="left", padx=10, pady=10)

        self.btn_manual_bind = ctk.CTkButton(self.manual_accordion, text="Bind", fg_color="#3498db", width=80, command=self.db_bind_account_manual)
        self.btn_manual_bind.pack(side="left", padx=10, pady=10)

        # --- LOWER SECTION: Connected Channels Network Nodes ---
        ctk.CTkLabel(self.main_container, text="📜 Active Connected Stores & Nodes", font=("Arial", 13, "bold"), text_color=self.text_main).pack(anchor="w", padx=5, pady=(5, 5))

        self.scroll_table = ctk.CTkScrollableFrame(self.main_container, corner_radius=12, fg_color=self.bg_card)
        self.scroll_table.pack(fill="both", expand=True, padx=5, pady=5)

        # Initial fetch
        self.refresh_account_grid()

    def toggle_manual_accordion(self):
        """Toggles the visibility of the advanced developer manual input corner."""
        if self.is_accordion_open:
            self.manual_accordion.pack_forget()
            self.is_accordion_open = False
        else:
            self.manual_accordion.pack(fill="x", padx=20, pady=(0, 15), before=self.advanced_btn)
            self.is_accordion_open = True

    def open_mock_oauth_browser(self):
        """Spawns an interactive high-fidelity pop-up mimicking the marketplace official login authorization screen."""
        target_p = self.opt_platform.get()
        
        # Create a stylized independent top-level window acting as a "Secure Web Browser"
        self.browser_win = ctk.CTkToplevel(self)
        self.browser_win.title(f"🔒 Secure Authorization Server - Connecting {target_p}")
        self.browser_win.geometry("460x400")
        self.browser_win.grab_set()
        self.browser_win.resizable(False, False)

        # Web browser simulator frame layout
        browser_bar = ctk.CTkFrame(self.browser_win, height=30, fg_color=("#E2E8F0", "#1D1E1F"), corner_radius=0)
        browser_bar.pack(fill="x")
        browser_bar.pack_propagate(False)
        ctk.CTkLabel(browser_bar, text=f"🌐 https://partner.{target_p.lower().replace(' ', '')}.com/oauth2/authorize", text_color="gray", font=("Arial", 10)).pack(side="left", padx=15)

        web_content = ctk.CTkFrame(self.browser_win, fg_color=("#F8FAFC", "#121212"))
        web_content.pack(fill="both", expand=True, padx=20, pady=20)

        # Brand header mimicking official channels
        p_color = "#ff4500" if "Shopee" in target_p else ("#111111", "#ffffff") if "TikTok" in target_p else "#000080"
        ctk.CTkLabel(web_content, text=target_p, font=("Arial", 22, "bold"), text_color=p_color).pack(pady=(15, 2))
        ctk.CTkLabel(web_content, text="Seller Partner Network Center", font=("Arial", 11), text_color="gray").pack(pady=(0, 20))

        # Login inputs
        ctk.CTkLabel(web_content, text="Registered Seller Email / Phone:", font=("Arial", 11, "bold")).pack(anchor="w", padx=30, pady=2)
        self.ent_web_user = ctk.CTkEntry(web_content, placeholder_text="seller_account@gmail.com", width=340, height=32)
        self.ent_web_user.pack(pady=(0, 12))

        ctk.CTkLabel(web_content, text="Password:", font=("Arial", 11, "bold")).pack(anchor="w", padx=30, pady=2)
        self.ent_web_pass = ctk.CTkEntry(web_content, placeholder_text="••••••••••••", width=340, height=32, show="*")
        self.ent_web_pass.pack(pady=(0, 25))

        # Call-To-Action buttons
        btn_login = ctk.CTkButton(
            web_content, 
            text="Verify Credentials & Agree Authorization", 
            fg_color=p_color,
            text_color="white" if "TikTok" not in target_p else ("black" if ctk.get_appearance_mode()=="Light" else "white"),
            font=("Arial", 12, "bold"), 
            height=36, 
            width=340,
            command=self.process_oauth_success
        )
        btn_login.pack()

    def process_oauth_success(self):
        """Processes the web handshake response, auto-generates credentials tokens, and inserts them straight to SQLite."""
        username = self.ent_web_user.get().strip()
        password = self.ent_web_pass.get().strip()
        plat = self.opt_platform.get()

        import tkinter.messagebox as messagebox
        import datetime
        import random

        if not username or not password:
            messagebox.showerror("Auth Failure", "Please enter your seller login credentials to continue authorization flow.", parent=self.browser_win)
            return

        # Extract shop name from email or text to create an automated shop identification token reference
        extracted_shop_id = username.split('@')[0] + "_store"
        # Auto generate a fake encrypted Access Token securely behind the scenes
        generated_token = f"auto_oauth_token_{random.randint(100000, 999999)}"
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO linked_accounts (platform, shop_id, auth_token, sync_status, last_synced) VALUES (?, ?, ?, 'Active', ?)",
                (plat, extracted_shop_id, generated_token, current_time)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("OAuth Success", f"🎉 Secure connection mesh established!\n\nMEPIO has successfully linked into '{plat}' channel via Shop ID: {extracted_shop_id}.", parent=self.browser_win)
            self.browser_win.destroy()
            self.refresh_account_grid()
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplication Notice", f"This store identity ({extracted_shop_id}) is already verified inside the database matrix.", parent=self.browser_win)
        except Exception as e:
            messagebox.showerror("System Error", f"Failed to commit database sequence: {e}", parent=self.browser_win)

    def db_bind_account_manual(self):
        """Fallback method for advanced developers inserting parameters manually from the hidden corner."""
        plat = self.opt_platform.get()
        shop = self.ent_shop_id.get().strip()
        tok = self.ent_token.get().strip()

        import tkinter.messagebox as messagebox
        import datetime

        if not shop or not tok:
            messagebox.showerror("Validation Error", "Advanced fields cannot be empty.")
            return

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO linked_accounts (platform, shop_id, auth_token, sync_status, last_synced) VALUES (?, ?, ?, 'Active', ?)",
                (plat, shop, tok, current_time)
            )
            conn.commit()
            conn.close()

            self.ent_shop_id.delete(0, tk.END)
            self.ent_token.delete(0, tk.END)
            self.toggle_manual_accordion() # close back down panel

            messagebox.showinfo("Manual Bind Success", f"Developer node active for {shop}.")
            self.refresh_account_grid()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def db_unlink_account(self, account_id):
        import tkinter.messagebox as messagebox
        if messagebox.askyesno("Confirm Disconnect", "Sever this active synchronization node connection link?"):
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM linked_accounts WHERE account_id = ?", (account_id,))
            conn.commit()
            conn.close()
            self.refresh_account_grid()

    def refresh_account_grid(self):
        for child in self.scroll_table.winfo_children():
            child.destroy()
        conn = sqlite3.connect('mepio_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT account_id, platform, shop_id, sync_status, last_synced FROM linked_accounts")
        records = cursor.fetchall()
        conn.close()

        if not records:
            lbl_empty = ctk.CTkLabel(self.scroll_table, text="[ No active marketplace connections found. Use the panel above to pair your first channel. ]", text_color=self.text_sub, font=("Arial", 12, "italic"))
            lbl_empty.pack(pady=40, expand=True)
            return

        for account_id, platform, shop_id, status, last_sync in records:
            row_frame = ctk.CTkFrame(self.scroll_table, fg_color=("#F1F5F9", "#1D1E1F"), corner_radius=8)
            row_frame.pack(fill="x", padx=15, pady=6)
            p_color = "#ff4500" if "Shopee" in platform else ("#111111", "#ffffff") if "TikTok" in platform else "#000080"
            lbl_plat = ctk.CTkLabel(row_frame, text=f"[{platform}]", font=("Arial", 12, "bold"), text_color=p_color, width=120, anchor="w")
            lbl_plat.pack(side="left", padx=(15, 10), pady=12)
            lbl_details = ctk.CTkLabel(row_frame, text=f"Shop ID: {shop_id}  |  Last Sync: {last_sync}", font=("Arial", 12), text_color=self.text_main)
            lbl_details.pack(side="left", padx=10)
            btn_unlink = ctk.CTkButton(row_frame, text="⛔ Unlink Account", fg_color="#e74c3c", hover_color="#c0392b", font=("Arial", 11, "bold"), width=120, command=lambda aid=account_id: self.db_unlink_account(aid))
            btn_unlink.pack(side="right", padx=15)
            lbl_status = ctk.CTkLabel(row_frame, text=status, font=("Arial", 10, "bold"), text_color="white", fg_color="#27ae60", corner_radius=4, width=70)
            lbl_status.pack(side="right", padx=10)

    def on_page_show(self, event):
        if event.widget == self:
            self.refresh_account_grid()

if __name__ == "__main__":
    app = MEPIOApp()
    app.mainloop()