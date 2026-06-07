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
            (" Orders", "orders"),
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
        self.pages["orders"] = OrderPage(self, self)
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
        self.bind("<Map>", self.on_page_show)

    def on_page_show(self, event):
        """Override this method in child classes to trigger actions when the page is shown."""
        if event.widget == self:
            pass

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
        self.chart_canvas_widget = None
     
        
        ctk.CTkLabel(self.chart_frame, text="Platform Benchmarking", font=("Helvetica", 16, "bold")).pack(pady=(15, 0), anchor="w", padx=20)
        ctk.CTkLabel(self.chart_frame, text="Revenue · Net profit · Platform fees", font=("Helvetica", 12), text_color="gray").pack(anchor="w", padx=20)

        self.load_benchmark_data() # 启动动态读取！


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
    
    def on_page_show(self, event):
        if event.widget == self:
            self.load_benchmark_data()

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
        super().__init__(parent, controller, "Shipping & Logistics Tracking")

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

            self.update_idletasks()

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
        super().__init__(parent, controller, "Advanced Profit Calculator")
        
        # --- Main Container for 2-Column Layout ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Left Column: Inputs (Scrollable to prevent overcrowding) ---
        self.input_frame = ctk.CTkScrollableFrame(self.main_container, corner_radius=15, fg_color=("#FFFFFF", "#252525"), width=500)
        self.input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

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
        """Initializes the Advanced Restock Optimization Analytics Page with proper tuple bindings."""
        super().__init__(parent, controller, "Restock & Expiry Optimizer")

        # --- Standard Dual-Color Theme Configuration ---
        self.bg_side_panel = ("#F8FAFC", "#1E1E1E")
        self.bg_card_inner = ("#FFFFFF", "#252525")
        self.text_main_color = ("#1E293B", "#F1F5F9")
        self.text_sub_color = ("#64748B", "#94A3B8")

        # --- Main Layout Framework ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # LEFT COLUMN
        self.left_frame = ctk.CTkScrollableFrame(self.main_container, width=340, corner_radius=15, fg_color=self.bg_side_panel)
        self.left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))

        # KPI 1
        self.card_total_cost = ctk.CTkFrame(self.left_frame, fg_color=("#FF4D4D", "#E74C3C"), corner_radius=10)
        self.card_total_cost.pack(fill="x", pady=(0, 10), padx=5)
        ctk.CTkLabel(self.card_total_cost, text="Total Procurement Budget Needed", font=("Arial", 11, "bold"), text_color="white").pack(pady=(10, 2))
        self.lbl_total_cost_val = ctk.CTkLabel(self.card_total_cost, text="RM 0.00", font=("Arial", 22, "bold"), text_color="white")
        self.lbl_total_cost_val.pack(pady=(2, 10))

        # KPI 2
        self.card_expiry_alert = ctk.CTkFrame(self.left_frame, fg_color=("#FFA502", "#E67E22"), corner_radius=10)
        self.card_expiry_alert.pack(fill="x", pady=10, padx=5)
        ctk.CTkLabel(self.card_expiry_alert, text="🚨 Inventory Batches Near Expiry", font=("Arial", 11), text_color="white").pack(pady=(10, 2))
        self.lbl_expiry_val = ctk.CTkLabel(self.card_expiry_alert, text="0 Units At Risk", font=("Arial", 18, "bold"), text_color="white")
        self.lbl_expiry_val.pack(pady=(2, 10))

        # Inputs
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

        self.btn_calculate = ctk.CTkButton(
            self.left_frame, text="Run Restock Optimization", 
            fg_color="#27ae60", hover_color="#219150", 
            font=("Arial", 12, "bold"), command=self.execute_restock_analysis
        )
        self.btn_calculate.pack(pady=15, padx=10, fill="x")

        # Insight Box
        self.insight_box = ctk.CTkFrame(self.left_frame, fg_color=self.bg_card_inner, corner_radius=10)
        self.insight_box.pack(fill="both", expand=True, pady=10, padx=5)
        ctk.CTkLabel(self.insight_box, text="📋 Smart Sourcing Recommendations", font=("Arial", 13, "bold"), text_color="#27ae60").pack(pady=10, anchor="w", padx=15)
        
        self.lbl_insight = ctk.CTkLabel(self.insight_box, text="", justify="left", font=("Arial", 11), text_color=self.text_sub_color, wraplength=280)
        self.lbl_insight.pack(pady=(0, 15), padx=15, fill="both")

        # RIGHT COLUMN — FIXED: Correctly referenced variable to stop tuple nested errors
        self.right_frame = ctk.CTkFrame(self.main_container, fg_color=self.bg_card_inner, corner_radius=12)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.canvas_widget = None
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

class OrderPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Multi-Platform Orders Stream")
        
        # --- Theme Adaptive Colors ---
        self.bg_card_inner = ("#FFFFFF", "#252525")
        self.bg_row_even = ("#F1F5F9", "#1D1E1F")
        self.text_main = ("#1E293B", "#F1F5F9")
        self.text_sub = ("#64748B", "#94A3B8")

        # --- Mock Database Template ---
        self.all_orders_mock = [
            ("Shopee MY", "SHP-20260525-091", "Matte Lipstick [LIP-001] x2", "RM 30.00", "To Ship", "#e67e22"),
            ("TikTok Shop", "TT-992314-MX", "Waterproof Mascara [MAS-002] x1", "RM 18.25", "To Ship", "#e67e22"),
            ("Lazada MY", "LZD-77621-PL", "EyeLiner [EYE-003] x1", "RM 10.00", "Completed", "#27ae60"),
            ("Shopee MY", "SHP-20260525-099", "Matte Lipstick [LIP-001] x1", "RM 15.00", "Unpaid", "#7f8c8d"),
            ("TikTok Shop", "TT-992315-LK", "Matte Lipstick [LIP-001] x3", "RM 45.00", "Completed", "#27ae60"),
            ("Lazada MY", "LZD-77625-AS", "Waterproof Mascara [MAS-002] x2", "RM 36.50", "To Ship", "#e67e22")
        ]

        # Currently selected platform filter condition (Defaults to "All")
        self.current_platform_filter = "All"

        # --- Main Layout Framework ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # =========================================================================
        # 1. TOP FILTER BAR (Platform Categories & Sub-navigation)
        # =========================================================================
        self.filter_bar = ctk.CTkFrame(self.main_container, fg_color=self.bg_card_inner, corner_radius=12)
        self.filter_bar.pack(fill="x", pady=(0, 10))

        # Platform Navigation Label
        lbl_filter_title = ctk.CTkLabel(self.filter_bar, text="Platform Channel:", font=("Arial", 12, "bold"), text_color=self.text_main)
        lbl_filter_title.pack(side="left", padx=(20, 10), pady=15)

        platforms = ["All", "Shopee", "TikTok", "Lazada"]
        self.tab_buttons = {}
        for p in platforms:
            # Using custom button styles to simulate tab switching behaviors
            btn = ctk.CTkButton(
                self.filter_bar, text=p, width=80, height=28,
                fg_color="#3498db" if p == "All" else "transparent", # Highlight "All" by default
                text_color="white" if p == "All" else self.text_main,
                border_width=1 if p != "All" else 0,
                border_color="#3498db",
                command=lambda choice=p: self.filter_by_platform(choice)
            )
            btn.pack(side="left", padx=5)
            self.tab_buttons[p] = btn

        # =========================================================================
        # 2. LIST METADATA & ANNOTATION (System Notices & Metrics Units)
        # =========================================================================
        self.meta_info_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.meta_info_frame.pack(fill="x", pady=(5, 0))

        # Left Side: System/Sync Annotations
        lbl_notice = ctk.CTkLabel(
            self.meta_info_frame, 
            text="* Annotation: Order stream auto-syncs every 5 mins via API handshake protocol. Statuses aligned to standard ERP nodes.", 
            font=("Arial", 11, "italic"), 
            text_color="#e67e22"
        )
        lbl_notice.pack(side="left", padx=5)

        # Right Side: Financial & Quantity Units
        lbl_unit = ctk.CTkLabel(
            self.meta_info_frame, 
            text="Unit: Gross Revenue (RM) | Quantity (Pcs)", 
            font=("Arial", 11, "bold"), 
            text_color=self.text_sub
        )
        lbl_unit.pack(side="right", padx=5)

        # =========================================================================
        # 3. CENTRAL DATAGRID (Centralized Order Stream Table Frame)
        # =========================================================================
        # Table Header Row
        self.table_header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.table_header.pack(fill="x", pady=(15, 0), padx=25)

        ctk.CTkLabel(self.table_header, text="Platform", font=("Arial", 11, "bold"), text_color=self.text_sub, width=100, anchor="w").pack(side="left")
        ctk.CTkLabel(self.table_header, text="Order Credentials & Items", font=("Arial", 11, "bold"), text_color=self.text_sub, anchor="w").pack(side="left", padx=15)
        ctk.CTkLabel(self.table_header, text="Status", font=("Arial", 11, "bold"), text_color=self.text_sub, width=80, anchor="center").pack(side="right", padx=15)
        ctk.CTkLabel(self.table_header, text="Order Value", font=("Arial", 11, "bold"), text_color=self.text_sub, width=80, anchor="e").pack(side="right", padx=15)

        # Scrollable Data Container
        self.order_table_frame = ctk.CTkScrollableFrame(self.main_container, corner_radius=12, fg_color=self.bg_card_inner)
        self.order_table_frame.pack(fill="both", expand=True, pady=(5, 10), padx=5)

        # First-time list data rendering
        self.render_filtered_list()

    def filter_by_platform(self, selected_platform):
        """Click handler for platform filter buttons, updates the current filter condition and triggers list re-rendering with proper button state management."""
        self.current_platform_filter = selected_platform
        
        # Dynamically switch the button active styling states
        for p, btn in self.tab_buttons.items():
            if p == selected_platform:
                btn.configure(fg_color="#3498db", text_color="white", border_width=0)
            else:
                btn.configure(fg_color="transparent", text_color=self.text_main, border_width=1)
        self.render_filtered_list()

    def render_filtered_list(self):
        """Dynamically renders the order list based on the current platform filter condition, with proper clearing and re-rendering logic."""
        # 1. Clear existing row widgets before re-rendering to prevent UI duplication anomalies
        for widget in self.order_table_frame.winfo_children():
            # Keep the centralized title intact and only clear row entries
            if isinstance(widget, ctk.CTkLabel) and "Centralized" in widget.cget("text"):
                continue
            widget.destroy()

        # 2. Dynamically process and render dataset records matching the active filter criteria
        for platform, order_id, items, value, status, status_color in self.all_orders_mock:
            
            # If selected platform filter is not "All" and the current order's platform does not match the filter, skip rendering this order row
            if self.current_platform_filter != "All" and self.current_platform_filter not in platform:
                continue

            row = ctk.CTkFrame(self.order_table_frame, fg_color=self.bg_row_even, corner_radius=8)
            row.pack(fill="x", padx=20, pady=5)

            # Platform display segment
            p_color = "#ff4500" if "Shopee" in platform else ("#111111", "#ffffff") if "TikTok" in platform else "#000080"
            lbl_platform = ctk.CTkLabel(row, text=f"[{platform}]", font=("Arial", 11, "bold"), text_color=p_color, width=100, anchor="w")
            lbl_platform.pack(side="left", padx=(15, 5), pady=8)

            # Order information detail credentials segment
            lbl_details = ctk.CTkLabel(row, text=f"ID: {order_id}   |   {items}", font=("Arial", 12), text_color=self.text_main, anchor="w")
            lbl_details.pack(side="left", padx=15)

            # Execution status badge pill capsule segment
            lbl_status = ctk.CTkLabel(row, text=status, font=("Arial", 10, "bold"), text_color="white", fg_color=status_color, corner_radius=5, width=80)
            lbl_status.pack(side="right", padx=15)

            # Transaction numeric amount value segment
            lbl_value = ctk.CTkLabel(row, text=value, font=("Arial", 12, "bold"), text_color=self.text_main, width=80, anchor="e")
            lbl_value.pack(side="right", padx=15)

if __name__ == "__main__":
    app = MEPIOApp()
    app.mainloop()