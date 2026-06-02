import customtkinter as ctk
import tkinter as tk 
from tkinter import messagebox # import messagebox for stock
import sqlite3

ctk.set_appearance_mode("light")

class InventoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller = None,):
        super().__init__(parent, fg_color =("white", "#2b2b2b"))
        self.controller = controller
        self.stock = {}
        self.thresholds = {}

        # Connect to database
        self.conn = sqlite3.connect("mepio_system.db")
        self.cursor = self.conn.cursor()

    # GUI stuffs
        self.header = ctk.CTkLabel(
            self, text="Inventory Management", 
            font=("Helvetica", 24, "bold"), 
            text_color=("#3498db", "#3498db")
        )
        self.header.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Decorative separator line
        line = ctk.CTkFrame(self, height=2, fg_color=("#E0E0E0", "#3d3d3d"))
        line.pack(fill="x", padx=20, pady=(0, 20))

        # Input Section
        input_frame = ctk.CTkFrame(self, corner_radius = 12, fg_color =("#FFFFFF", "#252525"))
        input_frame.pack(pady = 10, padx = 20, fill = "x")

        ctk.CTkLabel(input_frame, text = "Item Name:", font = ("Arial", 13)). grid(row = 0, column = 0, padx = 15, pady = 10, sticky = "w")
        self.entry_item = ctk.CTkEntry(input_frame, placeholder_text= "Enter item name", width = 250)
        self.entry_item.grid(row = 0, column = 1, padx = 15, pady = 10)

        self.entry_code = ctk.CTkEntry(input_frame, placeholder_text="Enter item code", width=250)
        self.entry_code.grid(row=0, column=2, padx=15, pady=10)

        # Bind key release events to trigger autocomplete dropdowns
        self.entry_code.bind("<KeyRelease>", self.show_code_suggestions)
        self.entry_code.bind("<FocusOut>", lambda e: self.after(150, self.hide_code_dropdown))

        self.entry_item.bind("<KeyRelease>", self.show_name_suggestions)
        self.entry_item.bind("<FocusOut>", lambda e: self.after(150, self.hide_name_dropdown))

        # Floating dropdown windows (initialized as None)
        self._code_dropdown_win = None
        self._name_dropdown_win = None

        ctk.CTkLabel(input_frame, text = "Quantity", font = ("Arial", 13)). grid(row = 1, column = 0, padx = 15, pady = 10, sticky = "w")
        self.entry_qty = ctk.CTkEntry(input_frame, placeholder_text= "Enter quantity", width = 250)
        self.entry_qty.grid(row = 1, column = 1, padx = 15, pady = 10)

        ctk.CTkLabel(input_frame, text="Low Stock Threshold:", font=("Arial", 13)).grid(row=2, column=0, padx=15, pady=10, sticky="w")
        self.entry_threshold = ctk.CTkEntry(input_frame, placeholder_text="Default = 5", width=250)
        self.entry_threshold.grid(row=2, column=1, padx=15, pady=10)

        self.threshold_label = ctk.CTkLabel(self, text = "Low Stock Threshold", font = ("Arial", 12), text_color = "#3498db")
        self.threshold_label.pack(pady = 5)

        # Button section
        btn_frame = ctk.CTkFrame(self, fg_color = "transparent")
        btn_frame.pack(pady = 10)

        self.btn_add = ctk.CTkButton(
            btn_frame, text = "➕ Add Item",
            command = self.gui_add_item,
            fg_color = "#27ae60", hover_color = "#2ecc71", width = 150
        )
        self.btn_add.pack(side = "left", padx = 10)

        self.btn_remove = ctk.CTkButton(
            btn_frame, text = "➖ Remove Item",
            command = self.gui_remove_item,
            fg_color = "#c0392b", hover_color = "#e74c3c", width = 150
        )
        self.btn_remove.pack(side = "left", padx = "10")

        self.btn_set_threshold = ctk.CTkButton(
            btn_frame, text = "⚙️ Set Threshold",
            command = self.set_threshold,
            fg_color = "#2980b9", hover_color = "#3498db", width = 150
        )
        self.btn_set_threshold.pack(side = "left", padx = 10)


        # Stock display
        display_frame = ctk.CTkFrame(self, corner_radius = 12, fg_color = "#1a1a1a")
        display_frame.pack(pady = 20, padx = 20, fill = "both", expand = True)

        ctk.CTkLabel(display_frame, text = "Current Stock", font = ("Arial", 16, "bold")).pack(pady = 10)

        self.listbox_colors = {
            "light": {"bg": "#ecf0f1", "fg": "#2c3e50"},
            "dark": {"bg": "#2c3e50", "fg": "#ecf0f1"}
        }

        self.stock_list = tk.Listbox(
            display_frame, height = 12, width = 50,
            bg = "#ecf0f1", fg="#2c3e50",
            font = ("Consolas", 12),
            highlightthickness = 0, bd = 0
        )
        self.stock_list.bind("<<ListboxSelect>>", self.on_item_select)
        self.stock_list.pack(pady = 10, padx = 10, fill = "both", expand = True)

        self.alert_label = ctk.CTkLabel(self, text = "", font = ("Arial", 13), text_color = "red")
        self.alert_label.pack(pady = 5)
        self.alerted_items = set()

        # Load stock after stock_list exists to prevent bug
        self.load_stock_from_db()

    # main code
    # --- Database integration methods ---
    def load_stock_from_db(self):
        self.cursor.execute("SELECT sku, product_name, local_stock FROM inventory")
        for code, name, qty in self.cursor.fetchall():
            self.stock[code] = {"name": name, "qty": qty, "threshold": 5}
        self.refresh_stock()

    def add_item(self, code, name, quantity, threshold=5):
        if code in self.stock:
            # Increment existing quantity
            self.stock[code]["qty"] += quantity
        else:
            # Create new entry
            self.stock[code] = {"name": name, "qty": quantity, "threshold": threshold}

        self.refresh_stock()

        # Save to Database
        self.cursor.execute(
            """INSERT INTO inventory (sku, product_name, local_stock)
            VALUES (?, ?, ?)
            ON CONFLICT(sku) DO UPDATE SET local_stock = local_stock + excluded.local_stock""",
            (code, name, quantity)
        )
        self.conn.commit()
        self.refresh_stock()


    def erase_item(self, code, quantity):
        if code in self.stock:
            current_qty = self.stock[code]["qty"]

            if quantity > current_qty:
                messagebox.showerror("Error", f"Cannot remove {quantity}. Only {current_qty} in stock.")
                return

            new_qty = current_qty - quantity
            self.stock[code]["qty"] = new_qty
            if new_qty == 0:
                del self.stock[code]

            # Update Database by SKU
            self.cursor.execute(
                """UPDATE inventory SET local_stock = local_stock - ?
                WHERE sku = ?""",
                (quantity, code)
            )
            self.conn.commit()
        self.refresh_stock()


    def gui_add_item(self):
        item = self.entry_item.get().strip()
        code = self.entry_code.get().strip()
        if not item or not code:
            messagebox.showerror("Error", "Item name and code can't be empty")
            return
        try:
            qty = int(self.entry_qty.get())
            threshold = int(self.entry_threshold.get()) if self.entry_threshold.get() else 5
            # Pass all required arguments: code, name, qty, threshold
            self.add_item(code, item, qty, threshold)
        except ValueError:
            messagebox.showerror("Error", "Quantity and threshold must be numbers")

    def gui_remove_item(self):
        code = self.entry_code.get().strip()
        if not code:
            messagebox.showerror("Error", "Item code cannot be empty")
            return
        try:
            qty = int(self.entry_qty.get())
            self.erase_item(code, qty)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")


    def set_threshold(self):
        code = self.entry_code.get().strip()
        if not code:
            messagebox.showerror("Error", "Enter an item name to set threshold")
            return
        try:
            value = int(self.entry_threshold.get())
            self.thresholds[code]["threshold"] = value
            self.threshold_label.configure(text = f"Current Threshold: {value}")
            messagebox.showinfo("Threshold Updated", f"Low stock threshold set to {value}")
            self.refresh_stock()
        except ValueError:
            messagebox.showerror("Invalid Input", "Threshold must be a number")

    def update_listbox_theme(self):
        mode = ctk.get_appearance_mode().lower()
        colors = self.listbox_colors[mode]
        self.stock_list.config(bg = colors["bg"], fg = colors["fg"])

    def refresh_stock(self):
        self.stock_list.delete(0, tk.END)
        low_items = []
        for code, data in self.stock.items():
            name, qty, threshold = data["name"], data["qty"], data["threshold"]
            self.stock_list.insert(tk.END, f"· {code} {name:<20} | {qty} (Threshold: {threshold})")
            if qty <= threshold:
                low_items.append((code, name, threshold))

        # Track new alerts for items that just went low
        new_alerts = []
        for code, name, threshold in low_items:
            if code not in self.alerted_items:
                new_alerts.append(f"{code} {name} (≤ {threshold})")
                self.alerted_items.add(code)

        # Show popup if any new item went low
        if new_alerts:
            messagebox.showwarning(
                "Low Stock Alert", 
                f"The following items are running low:\n{', '.join(new_alerts)}"
            )

        # Update label with all currently low items
        if low_items:
            self.alert_label.configure(
                text=f"⚠️ Low stock alert: {', '.join([f'{code} {name} (≤ {threshold})' for code, name, threshold in low_items])}"
            )
        else:
            self.alert_label.configure(text="")
            # Reset alerts when everything recovers
            self.alerted_items.clear()

    def on_item_select(self, event):
        try:
            selection = self.stock_list.curselection()
            if not selection:
                return
            index = selection[0]
            line = self.stock_list.get(index)

            parts = line.split("|")
            code_and_name = parts[0].replace("·", "").strip()
            code, name = code_and_name.split(" ", 1)

            self.entry_code.delete(0, tk.END)
            self.entry_code.insert(0, code)

            self.entry_item.delete(0, tk.END)
            self.entry_item.insert(0, name)
        except Exception as e:
            messagebox.showerror("Error", f"Selection failed : {e}")

    # ── Autocomplete helpers ────────────────────────────────────────────────

    def _make_dropdown(self, entry_widget, items, on_select_cb):
        """Create a floating Toplevel listbox anchored below entry_widget."""
        win = tk.Toplevel(self)
        win.wm_overrideredirect(True)          # no title bar / border
        win.attributes("-topmost", True)

        # Position directly below the entry field
        entry_widget.update_idletasks()
        x = entry_widget.winfo_rootx()
        y = entry_widget.winfo_rooty() + entry_widget.winfo_height()
        width = entry_widget.winfo_width()

        listbox = tk.Listbox(
            win,
            font=("Consolas", 11),
            bg="#ffffff", fg="#2c3e50",
            selectbackground="#3498db", selectforeground="white",
            highlightthickness=1, highlightcolor="#3498db",
            bd=0, relief="flat",
            activestyle="none",
        )
        listbox.pack(fill="both", expand=True)

        for item in items:
            listbox.insert(tk.END, item)

        # Auto-size height (max 6 rows)
        row_height = 20
        visible = min(len(items), 6)
        win.geometry(f"{width}x{visible * row_height + 4}+{x}+{y}")

        listbox.bind("<ButtonRelease-1>", lambda e: on_select_cb(listbox.get(listbox.curselection())))
        listbox.bind("<Return>",          lambda e: on_select_cb(listbox.get(listbox.curselection())))

        return win

    # ── SKU code dropdown ───────────────────────────────────────────────────

    def show_code_suggestions(self, event=None):
        typed = self.entry_code.get().strip()
        self.hide_code_dropdown()

        query = "%" + typed + "%" if typed else "%"
        self.cursor.execute(
            "SELECT sku FROM inventory WHERE sku LIKE ? LIMIT 10", (query,)
        )
        codes = [row[0] for row in self.cursor.fetchall()]
        if not codes:
            return

        self._code_dropdown_win = self._make_dropdown(
            self.entry_code, codes, self._select_code
        )

    def hide_code_dropdown(self):
        if self._code_dropdown_win:
            self._code_dropdown_win.destroy()
            self._code_dropdown_win = None

    def _select_code(self, selected_code):
        self.hide_code_dropdown()
        self.entry_code.delete(0, tk.END)
        self.entry_code.insert(0, selected_code)
        # Auto-fill item name
        self.cursor.execute(
            "SELECT product_name FROM inventory WHERE sku = ?", (selected_code,)
        )
        result = self.cursor.fetchone()
        if result:
            self.entry_item.delete(0, tk.END)
            self.entry_item.insert(0, result[0])

    # ── Item name dropdown ──────────────────────────────────────────────────

    def show_name_suggestions(self, event=None):
        typed = self.entry_item.get().strip()
        self.hide_name_dropdown()

        query = "%" + typed + "%" if typed else "%"
        self.cursor.execute(
            "SELECT product_name, sku FROM inventory WHERE product_name LIKE ? LIMIT 10",
            (query,)
        )
        rows = self.cursor.fetchall()
        if not rows:
            return

        display_items = [f"{name}  [{sku}]" for name, sku in rows]
        self._name_rows = rows   # store for lookup on select

        self._name_dropdown_win = self._make_dropdown(
            self.entry_item, display_items, self._select_name
        )

    def hide_name_dropdown(self):
        if self._name_dropdown_win:
            self._name_dropdown_win.destroy()
            self._name_dropdown_win = None

    def _select_name(self, selected_display):
        self.hide_name_dropdown()
        # Parse name and sku back out of "name  [sku]"
        try:
            name, rest = selected_display.rsplit("  [", 1)
            sku = rest.rstrip("]")
        except ValueError:
            return
        self.entry_item.delete(0, tk.END)
        self.entry_item.insert(0, name)
        self.entry_code.delete(0, tk.END)
        self.entry_code.insert(0, sku)

    # Legacy fill helper (kept for compatibility)
    def fill_code_entry(self, selected_code):
        self._select_code(selected_code)
    
if __name__ == "__main__":
    app = MEPIOApp()
    def on_theme_change(event = None):
        if "inv" in app.pages:
            app.pages["inv"].update_listbox_theme()
    app.bind("<<AppearanceModeChanged>>", on_theme_change)
    app.mainloop()