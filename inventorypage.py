import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3


class InventoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.stock = {}
        self.thresholds = {}

        # Connect to database
        self.conn = sqlite3.connect("mepio_system.db")
        self.cursor = self.conn.cursor()

        # Floating dropdown windows (initialized as None)
        self._code_dropdown_win = None
        self._name_dropdown_win = None

        # Per-item alert state
        self.alerted_items = {}

        # ── Page Header ──────────────────────────────────────────────────────
        self.header = ctk.CTkLabel(
            self, text="Inventory Management",
            font=("Arial", 24, "bold"),
            text_color="#4F6EF7"
        )
        self.header.pack(pady=(20, 6), padx=20, anchor="w")

        line = ctk.CTkFrame(self, height=2, fg_color="#E0E0E0")
        line.pack(fill="x", padx=20, pady=(0, 16))

        # ── Input Card ───────────────────────────────────────────────────────
        input_card = ctk.CTkFrame(self, corner_radius=12,
                                  fg_color=("#FFFFFF", "#2B2B2B"))
        input_card.pack(pady=(0, 10), padx=20, fill="x")

        ctk.CTkLabel(input_card, text="Add / Update Stock",
                     font=("Arial", 13, "bold"),
                     text_color=("#475569", "#94A3B8")).grid(
            row=0, column=0, columnspan=3, padx=16, pady=(12, 4), sticky="w")

        # Row 1 – Item Name & Item Code
        ctk.CTkLabel(input_card, text="Item Name:", font=("Arial", 12)).grid(
            row=1, column=0, padx=(16, 4), pady=8, sticky="w")
        self.entry_item = ctk.CTkEntry(input_card,
                                       placeholder_text="Enter item name",
                                       width=230)
        self.entry_item.grid(row=1, column=1, padx=8, pady=8)

        ctk.CTkLabel(input_card, text="Item Code / SKU:", font=("Arial", 12)).grid(
            row=1, column=2, padx=(16, 4), pady=8, sticky="w")
        self.entry_code = ctk.CTkEntry(input_card,
                                       placeholder_text="Enter item code",
                                       width=230)
        self.entry_code.grid(row=1, column=3, padx=(8, 16), pady=8)

        # Row 2 – Quantity & Threshold
        ctk.CTkLabel(input_card, text="Quantity:", font=("Arial", 12)).grid(
            row=2, column=0, padx=(16, 4), pady=8, sticky="w")
        self.entry_qty = ctk.CTkEntry(input_card,
                                      placeholder_text="Enter quantity",
                                      width=230)
        self.entry_qty.grid(row=2, column=1, padx=8, pady=8)

        ctk.CTkLabel(input_card, text="Low Stock Threshold:", font=("Arial", 12)).grid(
            row=2, column=2, padx=(16, 4), pady=8, sticky="w")
        self.entry_threshold = ctk.CTkEntry(input_card,
                                            placeholder_text="Default = 5",
                                            width=230)
        self.entry_threshold.grid(row=2, column=3, padx=(8, 16), pady=(8, 14))

        # Autocomplete bindings
        self.entry_code.bind("<KeyRelease>", self.show_code_suggestions)
        self.entry_code.bind("<FocusOut>",
                             lambda e: self.after(150, self.hide_code_dropdown))
        self.entry_item.bind("<KeyRelease>", self.show_name_suggestions)
        self.entry_item.bind("<FocusOut>",
                             lambda e: self.after(150, self.hide_name_dropdown))

        # ── Action Buttons ───────────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(4, 10), padx=20, anchor="w")

        ctk.CTkButton(
            btn_frame, text="➕  Add Item",
            command=self.gui_add_item,
            fg_color="#27ae60", hover_color="#2ecc71",
            font=("Arial", 13, "bold"), width=150, height=36, corner_radius=8
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_frame, text="➖  Remove Item",
            command=self.gui_remove_item,
            fg_color="#c0392b", hover_color="#e74c3c",
            font=("Arial", 13, "bold"), width=150, height=36, corner_radius=8
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_frame, text="⚙️  Set Threshold",
            command=self.set_threshold,
            fg_color="#4F6EF7", hover_color="#3B55D4",
            font=("Arial", 13, "bold"), width=150, height=36, corner_radius=8
        ).pack(side="left")

        # ── Stock Table Card ─────────────────────────────────────────────────
        stock_card = ctk.CTkFrame(self, corner_radius=12,
                                  fg_color=("#FFFFFF", "#2B2B2B"))
        stock_card.pack(pady=(0, 10), padx=20, fill="both", expand=True)

        # Card header row
        card_header = ctk.CTkFrame(stock_card, fg_color="transparent")
        card_header.pack(fill="x", padx=16, pady=(14, 0))

        ctk.CTkLabel(card_header, text="Current Stock",
                     font=("Arial", 16, "bold")).pack(side="left")

        self.alert_label = ctk.CTkLabel(card_header, text="",
                                        font=("Arial", 12, "bold"),
                                        text_color="#e74c3c")
        self.alert_label.pack(side="right")

        # Search bar
        search_frame = ctk.CTkFrame(stock_card, fg_color="transparent")
        search_frame.pack(fill="x", padx=16, pady=(8, 0))

        ctk.CTkLabel(search_frame, text="Search:", font=("Arial", 12)).pack(side="left", padx=(0, 6))
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search by name or SKU...", width=250)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_stock())

        # Filter buttons
        self.filter_mode = "all"

        self.btn_filter_all = ctk.CTkButton(search_frame, text="All", width=60,
            fg_color="#4F6EF7", hover_color="#3B55D4",
            command=lambda: self.set_filter("all"))
        self.btn_filter_all.pack(side="left", padx=4)

        self.btn_filter_low = ctk.CTkButton(search_frame, text="Low Stock", width=90,
            fg_color="#c0392b", hover_color="#e74c3c",
            command=lambda: self.set_filter("low"))
        self.btn_filter_low.pack(side="left", padx=4)

        self.btn_filter_ok = ctk.CTkButton(search_frame, text="OK", width=60,
            fg_color="#27ae60", hover_color="#2ecc71",
            command=lambda: self.set_filter("ok"))
        self.btn_filter_ok.pack(side="left", padx=4)

        # Column headers
        col_header = ctk.CTkFrame(stock_card,
                                  fg_color=("#F1F5F9", "#1D1E1F"),
                                  corner_radius=6)
        col_header.pack(fill="x", padx=16, pady=(10, 4))

        for col_text, col_width, col_anchor in [
            ("SKU / Code",   120, "w"),
            ("Product Name", 260, "w"),
            ("Qty",           60, "center"),
            ("Threshold",     80, "center"),
            ("Status",       100, "center"),
        ]:
            ctk.CTkLabel(col_header, text=col_text,
                         font=("Arial", 11, "bold"),
                         text_color=("#64748B", "#94A3B8"),
                         width=col_width, anchor=col_anchor).pack(
                side="left", padx=8, pady=6)

        # Scrollable rows container
        self.scroll_frame = ctk.CTkScrollableFrame(
            stock_card, fg_color="transparent", corner_radius=0)
        self.scroll_frame.pack(fill="both", expand=True, padx=8, pady=(0, 12))

        # Load data
        self.load_stock_from_db()

    # ── Database methods ─────────────────────────────────────────────────────

    def load_stock_from_db(self):
        self.cursor.execute(
            "SELECT sku, product_name, local_stock FROM inventory")
        for code, name, qty in self.cursor.fetchall():
            self.stock[code] = {"name": name, "qty": qty, "threshold": 5}
        self.refresh_stock()

    def add_item(self, code, name, quantity, threshold=5):
        if code in self.stock:
            self.stock[code]["qty"] += quantity
        else:
            self.stock[code] = {"name": name, "qty": quantity,
                                "threshold": threshold}
        self.cursor.execute(
            """INSERT INTO inventory (sku, product_name, local_stock)
               VALUES (?, ?, ?)
               ON CONFLICT(sku)
               DO UPDATE SET local_stock = local_stock + excluded.local_stock""",
            (code, name, quantity)
        )
        self.conn.commit()
        self.refresh_stock()

    def erase_item(self, code, quantity):
        if code in self.stock:
            current_qty = self.stock[code]["qty"]
            if quantity > current_qty:
                messagebox.showerror(
                    "Error",
                    f"Cannot remove {quantity}. Only {current_qty} in stock.")
                return
            new_qty = current_qty - quantity
            self.stock[code]["qty"] = new_qty
            if new_qty == 0:
                del self.stock[code]
            self.cursor.execute(
                "UPDATE inventory SET local_stock = local_stock - ? WHERE sku = ?",
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
            threshold = (int(self.entry_threshold.get())
                         if self.entry_threshold.get() else 5)
            self.add_item(code, item, qty, threshold)
        except ValueError:
            messagebox.showerror("Error",
                                 "Quantity and threshold must be numbers")

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
            messagebox.showerror("Error",
                                 "Enter an item code to set threshold")
            return
        if code not in self.stock:
            messagebox.showerror("Error",
                                 f"Item '{code}' not found in stock")
            return
        try:
            value = int(self.entry_threshold.get())
            self.stock[code]["threshold"] = value
            messagebox.showinfo("Threshold Updated",
                                f"Low stock threshold for '{code}' set to {value}")
            self.refresh_stock()
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Threshold must be a number")

    def set_filter(self, mode):
        self.filter_mode = mode
        # Update button colours to show which is active
        inactive_color = ("#E2E8F0", "#3d3d3d")
        inactive_text = ("#475569", "#F8FAFC")
        self.btn_filter_all.configure(fg_color=inactive_color, text_color=inactive_text)
        self.btn_filter_low.configure(fg_color=inactive_color, text_color=inactive_text)
        self.btn_filter_ok.configure(fg_color=inactive_color, text_color=inactive_text)

        if mode == "all":
            self.btn_filter_all.configure(fg_color="#4F6EF7", text_color="white")
        elif mode == "low":
            self.btn_filter_low.configure(fg_color="#c0392b", text_color="white")
        elif mode == "ok":
            self.btn_filter_ok.configure(fg_color="#27ae60", text_color="white")

        self.refresh_stock()

    # ── Stock list renderer ──────────────────────────────────────────────────

    def refresh_stock(self):
        # Clear existing rows
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        low_items = []

        # get search text and filter mode
        search = self.search_entry.get().strip().lower()

        if not self.stock:
            ctk.CTkLabel(self.scroll_frame,
                         text="No items in stock. Add your first item above.",
                         font=("Arial", 12, "italic"),
                         text_color=("#94A3B8", "#64748B")).pack(
                pady=30, expand=True)
        else:
            for code, data in self.stock.items():
                name, qty, threshold = (data["name"], data["qty"],
                                        data["threshold"])
                is_low = qty <= threshold

                # skip if search text doesn't match name or code
                if search and search not in name.lower() and search not in code.lower():
                    continue

                # skip if filter doesn't match
                if self.filter_mode == "low" and not is_low:
                    continue
                if self.filter_mode == "ok" and is_low:
                    continue

                # Row card
                row = ctk.CTkFrame(
                    self.scroll_frame,
                    fg_color=("#FEF2F2" if is_low else "#F8FAFC",
                              "#3B1E1E" if is_low else "#1D1E1F"),
                    corner_radius=8,
                    cursor="hand2"
                )
                row.pack(fill="x", padx=4, pady=3)

                # Helper: bind click on a widget and propagate to row
                def _bind_click(widget, c=code, n=name):
                    widget.bind("<Button-1>",
                                lambda e, c=c, n=n: self._select_row(c, n))

                _bind_click(row)

                # SKU
                lbl_code = ctk.CTkLabel(row, text=code,
                             font=("Consolas", 12, "bold"),
                             text_color=("#475569", "#CBD5E1"),
                             width=120, anchor="w", cursor="hand2")
                lbl_code.pack(side="left", padx=(12, 4), pady=10)
                _bind_click(lbl_code)

                # Name
                lbl_name = ctk.CTkLabel(row, text=name,
                             font=("Arial", 12),
                             text_color=("#1E293B", "#F1F5F9"),
                             width=260, anchor="w", cursor="hand2")
                lbl_name.pack(side="left", padx=4, pady=10)
                _bind_click(lbl_name)

                # Qty
                lbl_qty = ctk.CTkLabel(row, text=str(qty),
                             font=("Arial", 13, "bold"),
                             text_color=("#e74c3c" if is_low
                                         else "#1E293B", "#e74c3c" if is_low
                                         else "#F1F5F9"),
                             width=60, anchor="center", cursor="hand2")
                lbl_qty.pack(side="left", padx=4, pady=10)
                _bind_click(lbl_qty)

                # Threshold
                lbl_thresh = ctk.CTkLabel(row, text=str(threshold),
                             font=("Arial", 12),
                             text_color=("#64748B", "#94A3B8"),
                             width=80, anchor="center", cursor="hand2")
                lbl_thresh.pack(side="left", padx=4, pady=10)
                _bind_click(lbl_thresh)

                # Status badge
                badge_text = "⚠ Low Stock" if is_low else "✓ OK"
                badge_fg = "#e74c3c" if is_low else "#27ae60"
                lbl_badge = ctk.CTkLabel(row, text=badge_text,
                             font=("Arial", 10, "bold"),
                             text_color="white",
                             fg_color=badge_fg,
                             corner_radius=5,
                             width=90, cursor="hand2")
                lbl_badge.pack(side="left", padx=(4, 12), pady=10)
                _bind_click(lbl_badge)

                if is_low:
                    low_items.append((code, name, threshold))
                    if not self.alerted_items.get(code, False):
                        self.alerted_items[code] = True
                        messagebox.showwarning(
                            "Low Stock Alert",
                            f"⚠️ '{name}' ({code}) is running low!\n"
                            f"Current stock: {qty}  |  Threshold: {threshold}"
                        )
                else:
                    if code in self.alerted_items:
                        self.alerted_items[code] = False

        # Update alert label
        if low_items:
            self.alert_label.configure(
                text="⚠ Low stock: " + ",  ".join(
                    f"{name} ({code})" for code, name, _ in low_items
                )
            )
        else:
            self.alert_label.configure(text="✓ All items stocked")

    def _select_row(self, code, name):
        self.entry_code.delete(0, tk.END)
        self.entry_code.insert(0, code)
        self.entry_item.delete(0, tk.END)
        self.entry_item.insert(0, name)

    # ── Autocomplete helpers ─────────────────────────────────────────────────

    def _make_dropdown(self, entry_widget, items, on_select_cb):
        win = tk.Toplevel(self)
        win.wm_overrideredirect(True)
        win.attributes("-topmost", True)

        entry_widget.update_idletasks()
        x = entry_widget.winfo_rootx()
        y = entry_widget.winfo_rooty() + entry_widget.winfo_height()
        width = entry_widget.winfo_width()

        listbox = tk.Listbox(
            win,
            font=("Consolas", 11),
            bg="#ffffff", fg="#2c3e50",
            selectbackground="#4F6EF7", selectforeground="white",
            highlightthickness=1, highlightcolor="#4F6EF7",
            bd=0, relief="flat",
            activestyle="none",
        )
        listbox.pack(fill="both", expand=True)

        for item in items:
            listbox.insert(tk.END, item)

        row_height = 20
        visible = min(len(items), 6)
        win.geometry(f"{width}x{visible * row_height + 4}+{x}+{y}")

        listbox.bind("<ButtonRelease-1>",
                     lambda e: on_select_cb(
                         listbox.get(listbox.curselection())))
        listbox.bind("<Return>",
                     lambda e: on_select_cb(
                         listbox.get(listbox.curselection())))
        return win

    def show_code_suggestions(self, event=None):
        typed = self.entry_code.get().strip()
        self.hide_code_dropdown()
        query = "%" + typed + "%" if typed else "%"
        self.cursor.execute(
            "SELECT sku FROM inventory WHERE sku LIKE ? LIMIT 10", (query,))
        codes = [row[0] for row in self.cursor.fetchall()]
        if not codes:
            return
        self._code_dropdown_win = self._make_dropdown(
            self.entry_code, codes, self._select_code)

    def hide_code_dropdown(self):
        if self._code_dropdown_win:
            self._code_dropdown_win.destroy()
            self._code_dropdown_win = None

    def _select_code(self, selected_code):
        self.hide_code_dropdown()
        self.entry_code.delete(0, tk.END)
        self.entry_code.insert(0, selected_code)
        self.cursor.execute(
            "SELECT product_name FROM inventory WHERE sku = ?",
            (selected_code,))
        result = self.cursor.fetchone()
        if result:
            self.entry_item.delete(0, tk.END)
            self.entry_item.insert(0, result[0])

    def show_name_suggestions(self, event=None):
        typed = self.entry_item.get().strip()
        self.hide_name_dropdown()
        query = "%" + typed + "%" if typed else "%"
        self.cursor.execute(
            "SELECT product_name, sku FROM inventory "
            "WHERE product_name LIKE ? LIMIT 10", (query,))
        rows = self.cursor.fetchall()
        if not rows:
            return
        display_items = [f"{name}  [{sku}]" for name, sku in rows]
        self._name_rows = rows
        self._name_dropdown_win = self._make_dropdown(
            self.entry_item, display_items, self._select_name)

    def hide_name_dropdown(self):
        if self._name_dropdown_win:
            self._name_dropdown_win.destroy()
            self._name_dropdown_win = None

    def _select_name(self, selected_display):
        self.hide_name_dropdown()
        try:
            name, rest = selected_display.rsplit("  [", 1)
            sku = rest.rstrip("]")
        except ValueError:
            return
        self.entry_item.delete(0, tk.END)
        self.entry_item.insert(0, name)
        self.entry_code.delete(0, tk.END)
        self.entry_code.insert(0, sku)

    # Legacy compatibility
    def fill_code_entry(self, selected_code):
        self._select_code(selected_code)

    def update_listbox_theme(self):
        # No-op: theme is now handled via CTk fg_color tuples
        pass