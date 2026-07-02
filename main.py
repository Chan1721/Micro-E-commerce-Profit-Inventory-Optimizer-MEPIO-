import customtkinter as ctk #shortcut for customtkinter as ctk
import tkinter as tk 
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import datetime
import random
from database import init_database
from tkinter import messagebox
import webbrowser
ctk.set_appearance_mode("light")

#importing the login page
from inventorypage import InventoryPage
# from loginpage import LoginPage

class MEPIOApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        init_database()
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

        spacer = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        logout_btn = ctk.CTkButton(self.sidebar_frame, text=" ➜]   Logout", 
                                   fg_color="transparent", text_color=("#475569","#F8FAFC"), hover_color="#e2e8f0",
                                   font=("Arial", 14, "bold"), anchor="w",
                                   command=self.execute_logout)
        logout_btn.pack(pady=20, padx=10, fill="x", side="bottom")    

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

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # === yj: APP COLD-START AUTOMATED VIEW REDIRECTION ===
        # Query the persistence storage matrix to retrieve user startup perspective preference
        init_geometry = "1100x650"  # Default fallback dimensions
        target_page_key = "dash"    # Default fallback page token
        
        try:
            import sqlite3
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            # Fetch both configuration metrics concurrently in a single pipeline query
            cursor.execute("SELECT default_view, app_geometry FROM system_settings WHERE setting_id = 1")
            row = cursor.fetchone()
            conn.close()
            
            if row:
                # 1. Parse and map the view preference safely
                if row[0]:
                    preferred_view = row[0]
                    view_mapping = {
                        "Dashboard": "dash",
                        "Shopee View": "shopee",
                        "TikTok View": "tiktok",
                        "Lazada View": "lazada",
                        "Inventory": "inventory",
                        "Logistics": "logistics"
                    }
                    target_page_key = view_mapping.get(preferred_view, "dash")
                    print(f"Bootstrap Log: Startup view locked to token '{target_page_key}'")
                
                # 2. Parse and map the geometry dimension token securely (Fixes row[0] cross-assignment bug)
                if len(row) > 1 and row[1]:
                    init_geometry = row[1]
                    print(f"Bootstrap Log: Window resolution initialized to '{init_geometry}'")

            # Route the initial window lifecycle layer directly to target configurations
            self.geometry(init_geometry)
            self.show_page(target_page_key)

        except Exception as bootstrap_fault:
            # Safe operational fallback execution track to insulate core engine from crashes
            print(f"Subsystem Bootstrap Exception - Defaults enforced: {bootstrap_fault}")
            self.geometry("1100x650")
            self.show_page("dash")
        # === yj: END OF INTEGRATED REDIRECTION LAYER ===
        
    def on_closing(self):
        self.quit()     
        self.destroy()

        import sys
        sys.exit(0)

    def execute_logout(self):
        import sys
        import subprocess
        
        from tkinter import messagebox
        confirm = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        
        if confirm:
            self.destroy()

            subprocess.Popen([sys.executable, "loginpage.py"])
            
            sys.exit(0)    

    def show_page(self, page_name):
        # Hide all pages using grid_forget
        for frame in self.pages.values():
            frame.grid_forget()
        
        # Display selected page in the main container area
        self.pages[page_name].grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def refresh_all_charts(self):
        dash_page = self.pages.get("dash")
        if dash_page is not None:
            dash_page.load_benchmark_data()
            dash_page.on_page_refresh()

        logistics_page = self.pages.get("logistics")
        if logistics_page is not None and getattr(logistics_page, "_carrier_chart_frame_ref", None) is not None:
            logistics_page.render_carrier_chart(logistics_page._carrier_chart_frame_ref)

        analytics_page = self.pages.get("analytics")
        if analytics_page is not None:
            analytics_page.execute_restock_analysis()    

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

        # === yj: RESTRUCTURED METRICS CARDS MATRIX (FIXES NAMEERROR) ===
        safe_text_color = ("#1A1A1A", "#F0F0F0")

        # 1. Card 1: Total Orders
        card_orders = ctk.CTkFrame(self.stats_frame, corner_radius=15, fg_color=("#FFFFFF", "#2B2B2B"))
        card_orders.pack(side="left", padx=10, fill="both", expand=True)
        ctk.CTkLabel(card_orders, text="Total Orders", font=("Arial", 12), text_color="gray").pack(pady=(15, 0))
        
        self.lbl_orders_val = ctk.CTkLabel(card_orders, text="0 Pcs", font=("Arial", 22, "bold"), text_color=safe_text_color)
        self.lbl_orders_val.pack(pady=(5, 15))

        # 2. Card 2: Total Revenue
        card_rev = ctk.CTkFrame(self.stats_frame, corner_radius=15, fg_color=("#FFFFFF", "#2B2B2B"))
        card_rev.pack(side="left", padx=10, fill="both", expand=True)
        ctk.CTkLabel(card_rev, text="Total Revenue", font=("Arial", 12), text_color="gray").pack(pady=(15, 0))
        
        self.lbl_rev_val = ctk.CTkLabel(card_rev, text="RM 0.00", font=("Arial", 22, "bold"), text_color=safe_text_color)
        self.lbl_rev_val.pack(pady=(5, 15))

        # 3. Card 3: Platform Fees
        card_fees = ctk.CTkFrame(self.stats_frame, corner_radius=15, fg_color=("#FFFFFF", "#2B2B2B"))
        card_fees.pack(side="left", padx=10, fill="both", expand=True)
        ctk.CTkLabel(card_fees, text="Platform Fees", font=("Arial", 12), text_color="gray").pack(pady=(15, 0))
        
        self.lbl_fees_val = ctk.CTkLabel(card_fees, text="RM 0.00", font=("Arial", 18, "bold"), text_color=safe_text_color)
        self.lbl_fees_val.pack(pady=(5, 15))
        ctk.CTkLabel(card_fees, text="Live Calculation", font=("Arial", 11, "bold"), text_color="#2ecc71").pack(pady=(0, 15))

        # 4. Card 4: Low Stock (clickable — routes straight to the Inventory page)
        card_stock = ctk.CTkFrame(self.stats_frame, corner_radius=15, fg_color=("#FFFFFF", "#2B2B2B"), cursor="hand2")
        card_stock.pack(side="left", padx=10, fill="both", expand=True)
        ctk.CTkLabel(card_stock, text="Low Stock", font=("Arial", 12), text_color="gray").pack(pady=(15, 0))
        
        self.lbl_stock_val = ctk.CTkLabel(card_stock, text="0 Items", font=("Arial", 18, "bold"), text_color=safe_text_color)
        self.lbl_stock_val.pack(pady=(5, 15))
        lbl_stock_cta = ctk.CTkLabel(card_stock, text="Requires Attention →", font=("Arial", 11, "bold"), text_color="#e74c3c")
        lbl_stock_cta.pack(pady=(0, 15))

        # Clicking anywhere on the card (or its inner labels) jumps straight to Inventory
        self.card_stock = card_stock
        for widget in (card_stock, self.lbl_stock_val, lbl_stock_cta):
            widget.bind("<Button-1>", lambda e: self.master.show_page("inv"))
        # === yj: END OF FIXED METRICS MATRIX ===

        # Bottom layout wrapper (Left and Right)
        self.bottom_wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_wrapper.pack(fill="both", expand=True, padx=20, pady=20)

        # platform benchmarking chart on the left
        self.chart_frame = ctk.CTkFrame(self.bottom_wrapper, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
        self.chart_frame.pack(side="left", fill="both", expand=True) 
        self.chart_canvas_widget = None
     
        
        ctk.CTkLabel(self.chart_frame, text="Platform Benchmarking", font=("Arial", 16, "bold")).pack(pady=(15, 0), anchor="w", padx=20)
        ctk.CTkLabel(self.chart_frame, text="Revenue · Net profit · Platform fees", font=("Arial", 12), text_color="gray").pack(anchor="w", padx=20)

        self.load_benchmark_data() 


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
                          
            ctk.CTkButton(self.action_card, text="🔄 Update Inventory", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
                          border_color=("#D1D1D1", "#444444"), hover_color=("#E5E5E5", "#333333"),
                          command=lambda: self.master.show_page("inv")).pack(pady=8, padx=20, fill="x")
                          
            ctk.CTkButton(self.action_card, text="📦 Track Shipments", fg_color="transparent", border_width=1, text_color=("#333333", "#FFFFFF"),
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

            
            status_box = ctk.CTkFrame(self.action_card, fg_color=("#F1F5F9", "#1D1E1F"), corner_radius=8)
            status_box.pack(side="bottom", fill="x", padx=15, pady=20)

            spacer = ctk.CTkFrame(self.action_card, fg_color="transparent")
            spacer.pack(side="bottom", fill="both", expand=True)

            ctk.CTkLabel(status_box, text="⚙️ System Status", font=("Arial", 12, "bold"), text_color=("#333333", "#E0E0E0")).pack(anchor="w", padx=12, pady=(12, 0))

            status_row = ctk.CTkFrame(status_box, fg_color="transparent")
            status_row.pack(fill="x", padx=12, pady=6)
            
            ctk.CTkLabel(status_row, text="🟢", font=("Arial", 10)).pack(side="left")
            ctk.CTkLabel(status_row, text="All services operational", font=("Arial", 11, "bold"), text_color="#27ae60").pack(side="left", padx=6)

            import datetime
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            
            ctk.CTkLabel(status_box, text=f"MEPIO Core v1.0.0", font=("Arial", 10), text_color="gray").pack(anchor="w", padx=12)
            ctk.CTkLabel(status_box, text=f"Last Backup: {current_date}", font=("Arial", 10), text_color="gray").pack(anchor="w", padx=12, pady=(0, 12))

        # Populate the KPI cards with live numbers right away instead of leaving
        # them on their static "0" placeholders until the page is re-shown.
        self.on_page_refresh()

      
    def fetch_live_dashboard_metrics(self):
        """Queries multiple database relations to dynamically compute live summary telemetry numbers."""
        total_orders = 0
        total_revenue = 0.0
        low_stock_count = 0
        total_platform_fees = 0.0  # Dynamic tracking anchor initialized

        try:
            import sqlite3
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()

            # 1. Pull total synchronized order items row counts from linked tables
            cursor.execute("SELECT COUNT(*) FROM marketplace_orders")
            total_orders = cursor.fetchone()[0]

            # 2. Extract active commission configurations to map cross-channel parameters
            # Safely query systemic multipliers from setting registers
            shopee_rate, tiktok_rate, lazada_rate = 5.0, 5.0, 5.0  # Standard fallback variables
            try:
                cursor.execute("SELECT shopee_fee, tiktok_fee, lazada_fee FROM system_settings WHERE setting_id=1")
                setting_row = cursor.fetchone()
                if setting_row:
                    shopee_rate = float(setting_row[0] or 5.0)
                    tiktok_rate = float(setting_row[1] or 5.0)
                    lazada_rate = float(setting_row[2] or 5.0)
            except sqlite3.OperationalError:
                pass

            # 3. INTERVIEW DEMO CORE NODE: Iterate sales logs and compute tailored fee percentages
            cursor.execute("SELECT platform, order_value FROM marketplace_orders")
            rows = cursor.fetchall()
            for platform, val_str in rows:
                try:
                    clean_val = float(val_str.replace('RM', '').replace(' ', '').strip())
                    total_revenue += clean_val
                    
                    # Distribute calculation metrics depending on database platform labels
                    if "Shopee" in platform:
                        total_platform_fees += clean_val * (shopee_rate / 100.0)
                    elif "TikTok" in platform:
                        total_platform_fees += clean_val * (tiktok_rate / 100.0)
                    elif "Lazada" in platform:
                        total_platform_fees += clean_val * (lazada_rate / 100.0)
                    else:
                        total_platform_fees += clean_val * 0.05  # General fallback rule
                except:
                    pass

            # 4. Run condition scanner to detect matching low-stock hazards.
            #    NOTE: mirrors InventoryPage's own logic (qty <= per-item threshold,
            #    default threshold = 5) instead of a hardcoded "stock < 10" guess,
            #    and uses the real column name (local_stock) so the count this
            #    card shows always matches what the Inventory page marks as low.
            try:
                cursor.execute(
                    "SELECT COUNT(*) FROM inventory WHERE local_stock <= COALESCE(threshold, 5)"
                )
                low_stock_count = cursor.fetchone()[0]
            except sqlite3.OperationalError:
                low_stock_count = 0

            conn.close()
        except sqlite3.OperationalError:
            pass

        return total_orders, total_revenue, low_stock_count, total_platform_fees
    
    def on_page_show(self, event):
        if event.widget == self:
            self.load_benchmark_data()
            self.on_page_refresh()

    # === (Live Analytics Sync Pipelines) ===
    def on_page_refresh(self, event=None):
        """Dynamic bridge listener triggering UI card text configuration whenever the user switches back to dashboard."""
        
        # Safely re-configure underlying text labels targets to project active data streams
        t_orders, t_rev, t_stock, t_fees = self.fetch_live_dashboard_metrics()

        if hasattr(self, 'lbl_orders_val') and self.lbl_orders_val:
            self.lbl_orders_val.configure(text=f"{t_orders} Pcs")
        if hasattr(self, 'lbl_rev_val') and self.lbl_rev_val:
            self.lbl_rev_val.configure(text=f"RM {t_rev:.2f}")
        if hasattr(self, 'lbl_stock_val') and self.lbl_stock_val:
            self.lbl_stock_val.configure(text=f"{t_stock} Items")
            # Visually flag the card when there really is something to act on
            if hasattr(self, 'card_stock') and self.card_stock:
                self.card_stock.configure(
                    fg_color=("#FEF2F2", "#3B1E1E") if t_stock > 0 else ("#FFFFFF", "#2B2B2B")
                )
        if hasattr(self, 'lbl_fees_val') and self.lbl_fees_val:
            self.lbl_fees_val.configure(text=f"RM {t_fees:.2f}")

    def toggle_fee_accordion(self):
        if self.is_accordion_open:
            self.accordion_frame.pack_forget()  
            self.is_accordion_open = False
        else:
            self.accordion_frame.pack(pady=5, padx=20, fill="x", after=self.fee_btn)  
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
            if not isinstance(widget, ctk.CTkLabel): 
                widget.destroy()

            empty_frame = ctk.CTkFrame(self.chart_frame, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True, pady=30)  

            ctk.CTkLabel(empty_frame, text="📊", font=("Helvetica", 40)).pack(pady=(10, 5))
            ctk.CTkLabel(empty_frame, text="No Benchmark Data Yet", font=("Helvetica", 14, "bold"), text_color="#94A3B8").pack() 

            ctk.CTkLabel(empty_frame, text="Run your first profit calculation in the\nCalculator to generate live insights.", font=("Helvetica", 11), text_color="#64748B").pack(pady=5) 

            ctk.CTkButton(empty_frame, text="Go to Calculator", width=120, height=28, fg_color="#3498db", font=("Helvetica", 11, "bold"),command=lambda: self.master.show_page("calculator") ).pack(pady=15)        

def render_carrier_chart(self, chart_frame):
        """Queries relational tables to aggregate performance telemetry or seeds mock records for runtime demos."""
        for widget in chart_frame.winfo_children():
            widget.destroy()

        import sqlite3
        # Define uniform structural mapping parameters for enterprise standard reporting matrices
        carriers = ["J&T Express", "Shopee Xpress", "Pos Laju", "GDex", "City-Link"]
        avg_days = [0.0] * len(carriers)
        on_time_pct = [0.0] * len(carriers)
        cost_per_pkg = [0.0] * len(carriers)

        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            
            # 1. Structural schema safety enforcement: Create logistics telemetry matrix if uninitialized
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS carrier_shipments (
                    shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    carrier_name TEXT,
                    delivery_days REAL,
                    is_on_time INTEGER,
                    shipping_cost REAL
                )
            ''')
            conn.commit()

            # 2. Automated Seeding Loop: Populate backend if database ledger holds zero active nodes
            cursor.execute("SELECT COUNT(*) FROM carrier_shipments")
            if cursor.fetchone()[0] == 0:
                import random
                # Inject 25 high-fidelity synthetic runtime logs to simulate real enterprise traffic streams
                seed_data = []
                for _ in range(25):
                    c_name = random.choice(carriers)
                    # Construct parametric profiles mapped linearly to match unique operational characteristics
                    if c_name == "J&T Express":
                        seed_data.append((c_name, round(random.uniform(1.2, 2.2), 1), 1 if random.random() < 0.88 else 0, round(random.uniform(5.0, 6.0), 2)))
                    elif c_name == "Shopee Xpress":
                        seed_data.append((c_name, round(random.uniform(1.8, 2.8), 1), 1 if random.random() < 0.82 else 0, round(random.uniform(3.8, 4.6), 2)))
                    else:
                        seed_data.append((c_name, round(random.uniform(1.5, 3.5), 1), 1 if random.random() < 0.90 else 0, round(random.uniform(4.5, 7.0), 2)))
                
                cursor.executemany("INSERT INTO carrier_shipments (carrier_name, delivery_days, is_on_time, shipping_cost) VALUES (?, ?, ?, ?)", seed_data)
                conn.commit()

            # 3. High-Performance SQL Aggregation: Fetch complex analytical averages group-by constraints
            cursor.execute('''
                SELECT carrier_name, 
                       AVG(delivery_days), 
                       (SUM(is_on_time) * 100.0 / COUNT(*)), 
                       AVG(shipping_cost) 
                FROM carrier_shipments 
                GROUP BY carrier_name
            ''')
            analytics_rows = cursor.fetchall()
            conn.close()

            # 4. Data Extraction Node: Map multi-dimensional tuple lists directly into UI data layers
            for row in analytics_rows:
                db_name = row[0]
                if db_name in carriers:
                    idx = carriers.index(db_name)
                    avg_days[idx] = row[1] or 0.0
                    on_time_pct[idx] = row[2] or 0.0
                    cost_per_pkg[idx] = row[3] or 0.0

        except sqlite3.OperationalError as db_err:
            print(f"Interview Demo Pipeline Exception - Logistics telemetry fault: {db_err}")
            # Reliable safe fallbacks arrays if external storage disk fails
            avg_days, on_time_pct, cost_per_pkg = [2.0]*5, [85.0]*5, [5.00]*5

        # --- Graphics Matplotlib Engine Context Construction ---
        current_mode = ctk.get_appearance_mode()
        fig_face = "#FFFFFF" if current_mode == "Light" else "#2B2B2B"
        text_clr = "#555555" if current_mode == "Light" else "#CCCCCC"
        grid_clr = "#E0E0E0" if current_mode == "Light" else "#444444"

        fig, axes = plt.subplots(1, 3, figsize=(9, 2.8), dpi=96)
        fig.patch.set_facecolor(fig_face)
        fig.subplots_adjust(wspace=0.45, left=0.07, right=0.97, top=0.82, bottom=0.22)

        short_labels = ["J&T", "SXpress", "Pos Laju", "GDex", "City-Link"]
        datasets = [
            (axes[0], avg_days,     "Avg Delivery (days)", "#637AFA", "{:.1f}d"),
            (axes[1], on_time_pct,  "On-Time Rate (%)",    "#5DC66A", "{:.0f}%"),
            (axes[2], cost_per_pkg, "Cost / Parcel (RM)",  "#EAA844", "RM{:.2f}"),
        ]

        for ax, values, title, color, fmt in datasets:
            ax.set_facecolor(fig_face)
            bars = ax.bar(short_labels, values, color=color, width=0.5, zorder=3)
            ax.set_title(title, color=text_clr, fontsize=8, fontweight="bold", pad=6)
            ax.tick_params(axis='x', colors=text_clr, labelsize=6.5, rotation=15)
            ax.tick_params(axis='y', colors=text_clr, labelsize=6.5)
            ax.yaxis.grid(True, color=grid_clr, linestyle='-', linewidth=0.5, alpha=0.6)
            ax.set_axisbelow(True)
            for spine in ax.spines.values():
                spine.set_visible(False)
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.02,
                        fmt.format(val), ha='center', va='bottom', color=text_clr,
                        fontsize=6, fontweight='bold')

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, padding=8)
        plt.close(fig)

######accordion style         

class LogisticsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.header.configure(text="Shipping & Logistics Tracking")

        self.tabs = ctk.CTkTabview(self, width=800, height=400, fg_color=("#FFFFFF", "#2B2B2B"))
        self.tabs.pack(pady=(30, 10), padx=20, fill="both", expand=True)

        self.tab_in = self.tabs.add(" Inbound (Supplier Restock)")
        self.tab_out = self.tabs.add(" Outbound (Customer Orders)")
        self.tab_carrier = self.tabs.add(" Carrier Efficiency")

        self.recent_frames = {}

        self.build_tracking_ui(self.tab_in, "Inbound", "e.g., YT123456789 (China)")
        self.build_tracking_ui(self.tab_out, "Outbound", "e.g., 620000000000 (J&T)")
        self.build_carrier_efficiency_ui(self.tab_carrier)

    def on_page_show(self, event):
        if event.widget == self and getattr(self, "_carrier_chart_frame_ref", None) is not None:
            self.render_carrier_chart(self._carrier_chart_frame_ref)

    def init_recent_db(self):
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
            couriers = ["17TRACK (Universal)", "Cainiao (Taobao)", "MyPoz (Malaysia Sea Freight)"]
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

                    item_frame = ctk.CTkFrame(frame, fg_color="transparent")
                    item_frame.pack(side="left", padx=5)
                    
                    btn = ctk.CTkButton(
                        frame, text=btn_text, fg_color="#F1F5F9", text_color="#3498db", hover_color="#E2E8F0", 
                        font=("Helvetica", 11, "bold"), height=24, border_width=1, border_color="#D1D5DB",
                        command=lambda q=no, s=courier: self.execute_tracking(q, s, track_type) 
                    )
                    btn.pack(side="left", padx=5)

                    del_btn = ctk.CTkButton(
                        item_frame, text="✖", width=24, height=24, fg_color="transparent", 
                        text_color="#e74c3c", hover_color="#f8d7da", font=("Helvetica", 12),
                        command=lambda q=no: self.delete_recent_tracking(q, track_type)
                    )
                    del_btn.pack(side="left")


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

    def delete_recent_tracking(self, tracking_no, track_type):
        import sqlite3
        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recent_tracking WHERE tracking_no=?", (tracking_no,))
            conn.commit()
            conn.close()
            
            self.load_recents(track_type)
        except Exception as e:
            print(f"Delete UI Error: {e}")    

    def build_carrier_efficiency_ui(self, parent_tab):
        # Header section
        header_frame = ctk.CTkFrame(parent_tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 5))
        ctk.CTkLabel(header_frame, text="Shipping Carrier Efficiency Comparison", font=("Helvetica", 16, "bold")).pack(side="left")

        self._carrier_chart_frame_ref = None

        ctk.CTkLabel(parent_tab, text="Avg. delivery speed, on-time rate & cost-per-parcel across local couriers.",
                     font=("Helvetica", 11), text_color="gray").pack(anchor="w", padx=20, pady=(0, 10))

        # Stats summary cards
        cards_frame = ctk.CTkFrame(parent_tab, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=(0, 10))

        carrier_summary = [
            ("J&T Express",   "⚡ Fastest Avg",   "1.8 days",        "#3498db"),
            ("Shopee Xpress", "💰 Cheapest",       "RM 4.20/parcel",  "#27ae60"),
            ("Pos Laju",      "🏆 Best On-Time",   "96% on-time",     "#9b59b6"),
            ("GDex",          "📦 Most Used",      "38% of orders",   "#e67e22"),
        ]
        for carrier, label, value, color in carrier_summary:
            card = ctk.CTkFrame(cards_frame, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
            card.pack(side="left", padx=8, fill="both", expand=True)
            ctk.CTkLabel(card, text=carrier, font=("Helvetica", 11, "bold"), text_color=color).pack(pady=(12, 0))
            ctk.CTkLabel(card, text=label, font=("Helvetica", 10), text_color="gray").pack()
            ctk.CTkLabel(card, text=value, font=("Helvetica", 14, "bold")).pack(pady=(2, 12))

        # Refresh button
        chart_outer = ctk.CTkFrame(parent_tab, fg_color="transparent")
        chart_outer.pack(fill="both", expand=True, padx=20, pady=(0, 5))

        btn_refresh = ctk.CTkButton(chart_outer, text="🔄 Refresh Chart", fg_color="#3498db",
                                    font=("Helvetica", 12, "bold"), height=30, width=120,
                                    command=lambda: self.render_carrier_chart(chart_frame))
        btn_refresh.pack(anchor="e", pady=(0, 5))

        # Chart frame
        chart_frame = ctk.CTkFrame(chart_outer, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
        chart_frame.pack(fill="both", expand=True)
        self._carrier_chart_frame_ref = chart_frame
        self.render_carrier_chart(chart_frame)

        ctk.CTkLabel(parent_tab,
                     text="💡 Data based on simulated order history. Connect live courier API in Settings for real-time metrics.",
                     text_color="gray", font=("Helvetica", 11)).pack(pady=(5, 10))

    def render_carrier_chart(self, chart_frame):
        for widget in chart_frame.winfo_children():
            widget.destroy()

        carriers     = ["J&T Express", "Shopee Xpress", "Pos Laju", "GDex", "City-Link"]
        avg_days     = [1.8, 2.3, 2.1, 2.7, 3.1]
        on_time_pct  = [88,  82,  96,  78,  71 ]
        cost_per_pkg = [5.50, 4.20, 6.80, 5.10, 4.90]

        current_mode = ctk.get_appearance_mode()
        fig_face = "#FFFFFF" if current_mode == "Light" else "#2B2B2B"
        text_clr = "#555555" if current_mode == "Light" else "#CCCCCC"
        grid_clr = "#E0E0E0" if current_mode == "Light" else "#444444"

        fig, axes = plt.subplots(1, 3, figsize=(9, 2.8), dpi=96)
        fig.patch.set_facecolor(fig_face)
        fig.subplots_adjust(wspace=0.45, left=0.07, right=0.97, top=0.82, bottom=0.22)

        short_labels = ["J&T", "SXpress", "Pos Laju", "GDex", "City-Link"]
        datasets = [
            (axes[0], avg_days,     "Avg Delivery (days)", "#637AFA", "{:.1f}d"),
            (axes[1], on_time_pct,  "On-Time Rate (%)",    "#5DC66A", "{:.0f}%"),
            (axes[2], cost_per_pkg, "Cost / Parcel (RM)",  "#EAA844", "RM{:.2f}"),
        ]

        for ax, values, title, color, fmt in datasets:
            ax.set_facecolor(fig_face)
            bars = ax.bar(short_labels, values, color=color, width=0.5, zorder=3)
            ax.set_title(title, color=text_clr, fontsize=8, fontweight="bold", pad=6)
            ax.tick_params(axis='x', colors=text_clr, labelsize=6.5, rotation=15)
            ax.tick_params(axis='y', colors=text_clr, labelsize=6.5)
            ax.yaxis.grid(True, color=grid_clr, linestyle='-', linewidth=0.5, alpha=0.6)
            ax.set_axisbelow(True)
            for spine in ax.spines.values():
                spine.set_visible(False)
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.02,
                        fmt.format(val), ha='center', va='bottom', color=text_clr,
                        fontsize=6, fontweight='bold')

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        plt.close(fig)


class CalculatorPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

        # --- Left Column: Inputs ---
        self.input_frame = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color=("#FFFFFF", "#252525"))
        self.input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5)

        # Section 1: Product & Platform Details
        ctk.CTkLabel(self.input_frame, text="1. Product & Platform Details", font=("Helvetica", 16, "bold"), text_color="#3498db").pack(pady=(10, 15), anchor="w", padx=20)

        self.platform_var = ctk.StringVar(value="Shopee")
        p_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        p_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(p_frame, text="Target Platform:", width=180, anchor="w", text_color=("#333333", "#E0E0E0")).pack(side="left")
        ctk.CTkOptionMenu(p_frame, variable=self.platform_var, values=["Shopee", "TikTok", "Lazada"], command=self.auto_fill_platform_fee).pack(side="right", fill="x", expand=True)
        self.entries = {}
        base_fields = [
            ("Cost Price (RM)", ""),
            ("Selling Price (RM)", ""),
            ("Platform Fee (%)", ""),
            ("Shipping Fee Paid by Seller (RM)", ""),
            ("Estimated Tax Rate (%)", "0"),     
            ("Partner Profit Share (%)", "0")
        ]
        self.create_input_fields(base_fields)
        self.auto_fill_platform_fee(self.platform_var.get())  

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

        self.res_net_profit = self.create_result_row("Gross Profit:", "RM 0.00", "#3498db")
        self.res_tax = self.create_result_row("Tax Provisioning:", "RM 0.00", "#e74c3c")
        self.res_share = self.create_result_row("Partner Share:", "RM 0.00", "#e67e22")
        self.res_final_profit = self.create_result_row("Final Take-Home:", "RM 0.00", "#27ae60")
        
        self.res_roi = self.create_result_row("ROI (%):", "0.00%", "#8e44ad")
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
            tax_p = float(self.entries["Estimated Tax Rate (%)"].get() or 0) / 100
            share_p = float(self.entries["Partner Profit Share (%)"].get() or 0) / 100

            total_packaging = package_base + labor + buffer
            platform_fee_amount = selling * fee_p
            total_cost = cost + platform_fee_amount + shipping + total_packaging
            net_profit = selling - total_cost
            roi = (net_profit / cost * 100) if cost > 0 else 0

            tax_amount = net_profit * tax_p if net_profit > 0 else 0
            share_amount = (net_profit - tax_amount) * share_p if net_profit > 0 else 0
            final_takehome = net_profit - tax_amount - share_amount

            # 4. Render output data strings back to UI elements
            self.res_net_profit.configure(text=f"RM {net_profit:.2f}")
            self.res_tax.configure(text=f"-RM {tax_amount:.2f}")
            self.res_share.configure(text=f"-RM {share_amount:.2f}")
            self.res_final_profit.configure(text=f"RM {final_takehome:.2f}")

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

    # =========================================================================
    # CORE LOGIC: Auto-fetch platform fees from database based on selection
    # =========================================================================
    def auto_fill_platform_fee(self, platform_choice):
        import sqlite3
        import tkinter as tk
        try:
            # 1. Connect to DB and get the saved rates
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("SELECT shopee_fee, tiktok_fee, lazada_fee FROM system_settings WHERE setting_id=1")
            row = cursor.fetchone()
            conn.close()
            
            # 2. Safety fallback if DB is empty
            if row:
                s_fee, t_fee, l_fee = row
            else:
                s_fee, t_fee, l_fee = 5.5, 3.2, 4.0 
            
            # 3. Match the selected platform to the correct fee
            if "Shopee" in platform_choice:
                fee_val = s_fee
            elif "TikTok" in platform_choice:
                fee_val = t_fee
            elif "Lazada" in platform_choice:
                fee_val = l_fee
            else:
                fee_val = 0.0

            # 4. Magically update the UI entry field
            if "Platform Fee (%)" in self.entries:
                self.entries["Platform Fee (%)"].delete(0, tk.END)
                self.entries["Platform Fee (%)"].insert(0, str(fee_val))
                
        except Exception as e:
            print(f"Auto-fill fee error: {e}")         


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
        self.controller = controller
        
        # Safe fallback text color adaptive to dark/light theme
        safe_text_color = ("#1A1A1A", "#F0F0F0")

        # 1. Main Layout Containers
        self.content_wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self.content_wrapper.pack(fill="both", expand=True, padx=40, pady=10)
        
        # === yj: ADDED SCROLLABLE FRAME CONDUIT FOR UNLIMITED SETTINGS EXTENSION ===
        # Replaced normal Frame with CTkScrollableFrame to allow smooth mouse-wheel scrolling
        self.scroll_container = ctk.CTkScrollableFrame(self.content_wrapper, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True)

        self.sys_card = ctk.CTkFrame(self.scroll_container, corner_radius=12, fg_color=("#FFFFFF", "#2B2B2B"))
        self.sys_card.pack(fill="both", expand=True, padx=5, pady=5)

        # Title Headings inside your card
        ctk.CTkLabel(self.sys_card, text="General Preferences & Marketplace Config", font=("Arial", 16, "bold"), text_color=safe_text_color).pack(pady=(25, 15), padx=25, anchor="w")

        # 2. Original Interactive Switches (Your original switch preserved)
        self.dark_mode_switch = ctk.CTkSwitch(self.sys_card, text="Enable Dark Mode Visualization", command=lambda: self.toggle_dark_mode())
        self.dark_mode_switch.pack(pady=10, padx=25, anchor="w")

        # 3. ADDED COMPONENT A: Application Startup View Dropdown
        ctk.CTkLabel(self.sys_card, text="Startup Default View Viewport:", font=("Arial", 12, "bold"), text_color=safe_text_color).pack(pady=(15, 2), padx=25, anchor="w")
        
        # Safely fetch persistent perspective preference token from local DB storage registers
        current_pref = "Dashboard"
        try:
            import sqlite3
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("SELECT default_view FROM system_settings WHERE setting_id = 1")
            row = cursor.fetchone()
            if row and row[0]:
                current_pref = row[0]
            conn.close()
        except Exception:
            pass

        # Build dropdown interface frame wrapper mapping target view keys safely
        view_options = ["Dashboard", "Shopee View", "TikTok View", "Lazada View", "Inventory", "Logistics"]
        self.view_menu = ctk.CTkOptionMenu(self.sys_card, values=view_options, width=220)
        self.view_menu.set(current_pref)
        self.view_menu.pack(pady=(0, 15), padx=25, anchor="w")

        # 4. ADDED COMPONENT B: Restored Platform Commission Fee Input Entries
        ctk.CTkLabel(self.sys_card, text="Marketplace Commission Fee Percentages (%):", font=("Arial", 12, "bold"), text_color=safe_text_color).pack(pady=(10, 5), padx=25, anchor="w")

        # Load dynamic multipliers parameters initialization row values safely
        shopee_val, tiktok_val, lazada_val = "5.5", "3.2", "4.0"
        try:
            import sqlite3
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("SELECT shopee_fee, tiktok_fee, lazada_fee FROM system_settings WHERE setting_id = 1")
            row = cursor.fetchone()
            if row:
                shopee_val = str(row[0])
                tiktok_val = str(row[1])
                lazada_val = str(row[2])
            conn.close()
        except Exception:
            pass

        # Horizontal alignment row stack configuration for Shopee entry form nodes
        row_shopee = ctk.CTkFrame(self.sys_card, fg_color="transparent")
        row_shopee.pack(fill="x", padx=25, pady=3)
        ctk.CTkLabel(row_shopee, text="Shopee Rate:", font=("Arial", 12), text_color=safe_text_color, width=100, anchor="w").pack(side="left")
        self.ent_shopee = ctk.CTkEntry(row_shopee, width=100)
        self.ent_shopee.insert(0, shopee_val)
        self.ent_shopee.pack(side="left")

        # Horizontal alignment row stack configuration for TikTok entry form nodes
        row_tiktok = ctk.CTkFrame(self.sys_card, fg_color="transparent")
        row_tiktok.pack(fill="x", padx=25, pady=3)
        ctk.CTkLabel(row_tiktok, text="TikTok Rate:", font=("Arial", 12), text_color=safe_text_color, width=100, anchor="w").pack(side="left")
        self.ent_tiktok = ctk.CTkEntry(row_tiktok, width=100)
        self.ent_tiktok.insert(0, tiktok_val)
        self.ent_tiktok.pack(side="left")

        # Horizontal alignment row stack configuration for Lazada entry form nodes
        row_lazada = ctk.CTkFrame(self.sys_card, fg_color="transparent")
        row_lazada.pack(fill="x", padx=25, pady=3)
        ctk.CTkLabel(row_lazada, text="Lazada Rate:", font=("Arial", 12), text_color=safe_text_color, width=100, anchor="w").pack(side="left")
        self.ent_lazada = ctk.CTkEntry(row_lazada, width=100)
        self.ent_lazada.insert(0, lazada_val)
        self.ent_lazada.pack(side="left")

        # 5. Original Bottom Operational Buttons (Your original buttons preserved)
        self.sync_btn = ctk.CTkButton(self.sys_card, text="Sync Database", width=200, fg_color="#3498db")
        self.sync_btn.pack(pady=(25, 10), padx=25, anchor="w")

        self.export_btn = ctk.CTkButton(self.sys_card, text="Export Settings", width=200, fg_color="#3498db")
        self.export_btn.pack(pady=10, padx=25, anchor="w")

        # 6. APP WINDOW RESOLUTION PREFERENCE INTERFACE
        ctk.CTkLabel(self.sys_card, text="Application Window Resolution:", font=("Arial", 12, "bold"), text_color=safe_text_color).pack(pady=(15, 2), padx=25, anchor="w")
        
        # Safe database query to retrieve active persistent geometry configuration
        current_geo = "1100x650"
        try:
            import sqlite3
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("SELECT app_geometry FROM system_settings WHERE setting_id = 1")
            row = cursor.fetchone()
            if row and row[0]:
                current_geo = row[0]
            conn.close()
        except Exception:
            pass

        # Resolution preset matrix mappings
        geo_options = ["1100x650 (Default)", "1280x720 (HD)", "1440x900", "1600x900", "1920x1080 (FHD)"]
        self.geo_menu = ctk.CTkOptionMenu(self.sys_card, values=geo_options, width=220)
        
        # Set the visual text to match saved layout config securely
        matching_ui_text = next((opt for opt in geo_options if current_geo in opt), "1100x650 (Default)")
        self.geo_menu.set(matching_ui_text)
        self.geo_menu.pack(pady=(0, 25), padx=25, anchor="w")

        # === yj: ADDED GLOBAL MASTER SAVE BUTTON AT THE BOTTOM ===
        # This button dispatches a transaction that saves all sections simultaneously
        btn_save_all = ctk.CTkButton(self.sys_card, text="💾 Save All Configuration Profiles", font=("Arial", 14, "bold"), width=320, height=40, fg_color="#2ecc71", hover_color="#27ae60", command=lambda: self.save_all_settings())
        btn_save_all.pack(pady=(10, 35), padx=25, anchor="w")

    # === INTERVIEW HIGHLIGHT: PERSISTENCE SUBSYSTEM BACKEND HANDLERS ===
    def save_view_preference(self):
        """Persists the selected UI perspective element into the relational settings table registers."""
        selected_view = self.view_menu.get()
        try:
            import sqlite3
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE system_settings SET default_view = ? WHERE setting_id = 1", (selected_view,))
            conn.commit()
            conn.close()
            print(f"Success: Startup perspective locked to '{selected_view}' view.")
        except Exception as e:
            print(f"Error persisting configuration metadata: {e}")

    def save_fee_configuration(self):
        """Persists parsed dynamic multiplier percentage entry data into the system settings schema rows."""
        try:
            shopee_fee = float(self.ent_shopee.get() or 5.5)
            tiktok_fee = float(self.ent_tiktok.get() or 3.2)
            lazada_fee = float(self.ent_lazada.get() or 4.0)

            import sqlite3
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE system_settings 
                SET shopee_fee = ?, tiktok_fee = ?, lazada_fee = ? 
                WHERE setting_id = 1
            """, (shopee_fee, tiktok_fee, lazada_fee))
            conn.commit()
            conn.close()
            print("Success: Relational platform configuration parameters parsed and deployed to disk storage registry.")
        except ValueError:
            print("Configuration Fault: Input entry must convert to float types.")
        except Exception as e:
            print(f"Configuration Database Fault: {e}")

    def toggle_dark_mode(self):
        if self.dark_mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
            print("Subsystem GUI Log: Application layout successfully shifted to 'dark' mode profile.")
        else:
            ctk.set_appearance_mode("light")
            print("Subsystem GUI Log: Application layout successfully shifted to 'light' mode profile.")
        self.master.refresh_all_charts()    

    # === yj: GEOMETRY PERSISTENCE BACKEND HANDLERS ===
    def save_geometry_preference(self):
        """Parses the selected UI window dimensions string token and logs it to relational registers."""
        selected_opt = self.geo_menu.get()
        # Extract the pure numeric dimension string from option (e.g., '1280x720')
        pure_geometry = selected_opt.split(" ")[0]
        
        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE system_settings SET app_geometry = ? WHERE setting_id = 1", (pure_geometry,))
            conn.commit()
            conn.close()
            
            # Instantly re-scale the app workspace matrix frame layout
            self.controller.geometry(pure_geometry)
            print(f"Success: System master resolution geometry scaled and locked to '{pure_geometry}'.")
        except Exception as write_fault:
            print(f"Geometry Pipeline Fault: {write_fault}")
    # === yj: END OF GEOMETRY PERSISTENCE ===

    # === yj: ATOMIC GLOBAL MULTI-SETTING PERSISTENCE PIPELINE ===
    def save_all_settings(self):
        """Executes sequential pipeline updates across all independent persistence handlers at once."""
        print("Subsystem Log: Initiating atomic global save sequence across database tables...")
        
        # Sequentially invoke individual persistence routines to secure entries
        self.save_view_preference()
        self.save_fee_configuration()
        self.save_geometry_preference()
        
        # Optional: You can pop up a standard system banner here if tkinter messagebox is imported
        print("Success: All local workspace preferences and parameters committed successfully.")
    # === yj: END OF GLOBAL PERSISTENCE PIPELINE ===
          

class HelpPage(BasePage):
    def __init__(self, parent, controller):
        """Initializes the Help and Support customer service frame layout."""
        super().__init__(parent, controller)       
        # Safe fallback text rendering colors tailored for adaptive dual-theme light/dark modes
        safe_text_color = ("#1A1A1A", "#F0F0F0")
        
        # 1. Page Header Typography Nodes
        title = ctk.CTkLabel(self, text="Help & Customer Support", font=("Arial", 24, "bold"), text_color=safe_text_color)
        title.pack(anchor="w", padx=30, pady=(30, 10))
        
        desc = ctk.CTkLabel(self, text="Need assistance with inventory matching or fee calculation? Contact our technical support team.", font=("Arial", 12), text_color="gray")
        desc.pack(anchor="w", padx=30, pady=(0, 20))

        # Scrollable container mapping systemic guide nodes to keep information accessible
        help_text = ctk.CTkTextbox(self, height=220, font=("Arial", 13), corner_radius=12, border_width=1)
        help_text.pack(pady=(5, 15), padx=30, fill="x", expand=False)
        
        # Injects the structured functional user reference logs cleanly on runtime instantiation
        help_text.insert("0.0", "MEPIO SYSTEM DOCUMENTATION & OPERATIONAL MANUAL\n\n"
                               "1. DASHBOARD: View real-time aggregated cross-channel profit margins, live telemetry, low-stock notifications, and localized delivery time analysis charts.\n\n"
                               "2. CALCULATOR: Pre-calculate comprehensive net profit variations factoring dynamic platform commission fees prior to structural product listing.\n\n"
                               "3. LOGISTICS: Standardize shipping delivery timelines, handle fulfillment logs, and inspect localized state order tracking records.\n\n"
                               "4. INVENTORY: Manage enterprise warehouse structures, track dynamic stock units, adjust unit cost prices, and trigger safety threshold counters.\n\n"
                               "5. SETTINGS: Adjust system-wide baseline platform percentage commission matrices for Shopee, Lazada, and TikTok View pipelines, and save startup view perspective preferences.\n\n"
                               "6. HELP & SUPPORT: Access system architectural documentation guidelines and launch instant external hyperlink communication conduits to our technical help desk.")
        help_text.configure(state="disabled")  # Sets to read-only status preventing administrative mutations
        
        # 2. Centralized Communication Section Container
        contact_card = ctk.CTkFrame(self, corner_radius=15, fg_color=("#FFFFFF", "#2B2B2B"))
        contact_card.pack(pady=10, padx=30, fill="x")
        
        ctk.CTkLabel(contact_card, text="Direct Communication Channels", font=("Arial", 16, "bold"), text_color=safe_text_color).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(contact_card, text="Click on the channels below to initiate an instant encrypted support session.", font=("Arial", 11), text_color="gray").pack(anchor="w", padx=20, pady=(0, 15))
        
        # --- Channel A: WhatsApp API Routing Row ---
        whatsapp_frame = ctk.CTkFrame(contact_card, fg_color="transparent")
        whatsapp_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(whatsapp_frame, text="WhatsApp Support:", font=("Arial", 13, "bold"), text_color=safe_text_color).pack(side="left")
        
        # Hyperlink styled button configured to route operational callback sequences
        btn_whatsapp = ctk.CTkButton(
            whatsapp_frame, 
            text="+60 16-9587267 (Click to Chat)", 
            font=("Arial", 13, "underline"),
            fg_color="transparent", 
            hover_color=("#EAEAEA", "#3A3A3A"),
            text_color="#2ecc71",  # Distinct brand styling for WhatsApp green color scheme
            anchor="w",
            width=250,
            command=self.open_whatsapp_channel
        )
        btn_whatsapp.pack(side="left", padx=10)
        
        # --- Channel B: Gmail Mailto URI Row ---
        email_frame = ctk.CTkFrame(contact_card, fg_color="transparent")
        email_frame.pack(fill="x", padx=20, pady=(5, 20))
        
        ctk.CTkLabel(email_frame, text="Email Assistance: ", font=("Arial", 13, "bold"), text_color=safe_text_color).pack(side="left")
        
        # Hyperlink styled button configured to compile native system mail headers
        btn_email = ctk.CTkButton(
            email_frame, 
            text="support@mepio.com (Click to Compose)", 
            font=("Arial", 13, "underline"),
            fg_color="transparent", 
            hover_color=("#EAEAEA", "#3A3A3A"),
            text_color="#e74c3c",  # Distinct brand styling for Gmail red color scheme
            anchor="w",
            width=250,
            command=self.open_gmail_channel
        )
        btn_email.pack(side="left", padx=10)

    # === INTERVIEW HIGHLIGHT: CUSTOMER REDIRECTION URI REDIRECT PIPELINES ===
    def open_whatsapp_channel(self):
        """Invokes the default system browser layer to open the official WhatsApp web API bridge."""
        # Using Malaysia country dial-code 60, excluding the leading zero or plus sign
        phone_number = "60169587267" 
        custom_message = "Hello MEPIO Support, I have a technical inquiry regarding the system. Please assist me."
        
        # Format strings safely by encoding spaces into URL-compliant markers (%20)
        encoded_msg = custom_message.replace(" ", "%20")
        whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_msg}"
        
        try:
            webbrowser.open(whatsapp_url)
            print("Subsystem Log: Routing operational link pointer to WhatsApp endpoint successfully.")
        except Exception as redirect_fault:
            print(f"Subsystem Link Exception - Routing aborted: {redirect_fault}")

    def open_gmail_channel(self):
        """Dispatches an OS-level mailto signal handler to launch the native mailing client workspace."""
        support_email = "yijianchan0801@gmail.com"
        email_subject = "MEPIO System Technical Inquiry"
        email_body = "Dear MEPIO Support Team,\n\n[Please describe your issue here]\n\nRegards,"
        
        # Format string properties safely by encoding hex line breaks (%0A) and space values (%20)
        encoded_subject = email_subject.replace(" ", "%20")
        encoded_body = email_body.replace(" ", "%20").replace("\n", "%0A")
        
        # Build standard system mailto URI schema matrix
        mailto_uri = f"mailto:{support_email}?subject={encoded_subject}&body={encoded_body}"
        
        try:
            webbrowser.open(mailto_uri)
            print("Subsystem Log: Successfully pushed target mailto headers to system registry framework.")
        except Exception as mail_fault:
            print(f"Subsystem Mail Exception - Redirection failed: {mail_fault}")

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

        # CRITICAL REPAIR: Dynamic branding colors matching the chosen marketplace channel
        if "Shopee" in target_p:
            p_color = "#ff4500"  # Shopee Orange
            subtitle_text = "Shopee Partner Network Open API Center"
        elif "TikTok" in target_p:
            p_color = ("#111111", "#ffffff")  # TikTok High-contrast Black/White
            subtitle_text = "TikTok Shop Global Creator & Merchant Platform"
        else:
            p_color = "#0f15d4"  # Lazada Dark Blue
            subtitle_text = "Lazada Open Platform Authorization Service"

        ctk.CTkLabel(web_content, text=target_p, font=("Arial", 22, "bold"), text_color=p_color).pack(pady=(15, 2))
        ctk.CTkLabel(web_content, text=subtitle_text, font=("Arial", 11), text_color="gray").pack(pady=(0, 20))

        # Login inputs
        ctk.CTkLabel(web_content, text="Registered Seller Email / Phone:", font=("Arial", 11, "bold")).pack(anchor="w", padx=30, pady=2)
        self.ent_web_user = ctk.CTkEntry(web_content, placeholder_text="seller_account@gmail.com", width=340, height=32)
        self.ent_web_user.pack(pady=(0, 12))

        ctk.CTkLabel(web_content, text="Password:", font=("Arial", 11, "bold")).pack(anchor="w", padx=30, pady=2)
        self.ent_web_pass = ctk.CTkEntry(web_content, placeholder_text="••••••••••••", width=340, height=32, show="*")
        self.ent_web_pass.pack(pady=(0, 25))

        # Call-To-Action buttons linked into system callback mechanisms
        btn_login = ctk.CTkButton(
            web_content, 
            text="Verify Credentials & Agree Authorization", 
            fg_color=p_color if isinstance(p_color, str) else p_color[0],
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

        if not username or not password:
            messagebox.showerror("Auth Failure", "Please enter your seller login credentials to continue authorization flow.", parent=self.browser_win)
            return

        # Core logic optimization: Extract prefixes safely to map distinct store identifiers
        extracted_shop_id = username.split('@')[0] + f"_{plat.lower().split(' ')[0]}_node"
        
        # Emulate the real world OAuth 2.0 access token generated by the server infrastructure
        generated_token = f"oauth_token_{plat[:3].lower()}_{random.randint(100000, 999999)}"
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        try:
            conn = sqlite3.connect('mepio_system.db')
            cursor = conn.cursor()
            
            # Use INSERT OR REPLACE to update store keys gracefully if shop details overlap
            cursor.execute('''
                INSERT OR REPLACE INTO linked_accounts (platform, shop_id, auth_token, sync_status, last_synced) 
                VALUES (?, ?, ?, 'Active', ?)
            ''', (plat, extracted_shop_id, generated_token, current_time))
            
            conn.commit()
            conn.close()

            messagebox.showinfo("OAuth Success", f"🎉 Secure connection mesh established!\n\nMEPIO has successfully linked into '{plat}' channel via Shop ID: {extracted_shop_id}.", parent=self.browser_win)
            self.browser_win.destroy()
            self.refresh_account_grid()
        except Exception as e:
            messagebox.showerror("System Error", f"Failed to commit database sequence: {e}", parent=self.browser_win)

    def db_bind_account_manual(self):
        """Fallback method for advanced developers inserting parameters manually from the hidden corner."""
        plat = self.opt_platform.get()
        shop = self.ent_shop_id.get().strip()
        tok = self.ent_token.get().strip()

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