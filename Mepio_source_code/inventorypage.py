import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import datetime
import subprocess

class InventoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.stock = {}
        self.thresholds = {}

        # Connect to database
        self.conn = sqlite3.connect("mepio_system.db")
        self.cursor = self.conn.cursor()

        # FIX (bug 5): make sure the table actually exists before we try to
        # ALTER it. Previously the ALTER TABLE below assumed the table was
        # already created somewhere else; if InventoryPage is ever the first
        # thing to touch the DB, "ALTER TABLE inventory ADD COLUMN..." raises
        # sqlite3.OperationalError: no such table: inventory, and the bare
        # except swallowed that too, so every query afterwards blew up.
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS inventory (
                   sku TEXT PRIMARY KEY,
                   product_name TEXT,
                   local_stock INTEGER DEFAULT 0,
                   threshold INTEGER DEFAULT 5
               )"""
        )
        self.conn.commit()

        # Make sure the inventory table can actually persist a per-item low
        # stock threshold — previously this only lived in memory (self.stock)
        # and was lost on every restart, and the Dashboard's "Low Stock" card
        # had no way to read it at all.
        try:
            self.cursor.execute(
                "ALTER TABLE inventory ADD COLUMN threshold INTEGER DEFAULT 5")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass  # column already exists

        # Floating dropdown windows (initialized as None)
        self._code_dropdown_win = None
        self._name_dropdown_win = None

        # Per-item alert state
        self.alerted_items = {}

        # FIX (bug 6): suppress low-stock popups while we're doing the very
        # first load from the DB, so the app doesn't open to a wall of
        # blocking messageboxes for items that were already low last time
        # the app was closed. Alerts still fire for items that *become* low
        # during the session.
        self._suppress_alerts = False

        # In-line qty edit state
        self._qty_edit_active = None
        self._qty_committed = False

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
        # FIX (bug 8): pressing Down from the entry moves focus into the
        # dropdown listbox so keyboard users can actually reach it and use
        # Enter to select — previously the listbox's <Return> binding was
        # unreachable because the entry always kept keyboard focus.
        self.entry_code.bind(
            "<Down>", lambda e: self._focus_dropdown_listbox(self._code_dropdown_win))

        self.entry_item.bind("<KeyRelease>", self.show_name_suggestions)
        self.entry_item.bind("<FocusOut>",
                             lambda e: self.after(150, self.hide_name_dropdown))
        self.entry_item.bind(
            "<Down>", lambda e: self._focus_dropdown_listbox(self._name_dropdown_win))

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

        # NEW FEATURE: Delete Item entirely (removes the row from inventory,
        # regardless of its current quantity). This is different from
        # "Remove Item", which only decrements quantity. Quantity reaching 0
        # no longer auto-deletes an item anywhere in this file — deleting is
        # now always an explicit, confirmed action.
        ctk.CTkButton(
            btn_frame, text="🗑  Delete Item",
            command=self.gui_delete_item,
            fg_color="#7f1d1d", hover_color="#991b1b",
            font=("Arial", 13, "bold"), width=150, height=36, corner_radius=8
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_frame, text="⚙️  Set Threshold",
            command=self.set_threshold,
            fg_color="#4F6EF7", hover_color="#3B55D4",
            font=("Arial", 13, "bold"), width=150, height=36, corner_radius=8
        ).pack(side="left")

        # 👇 NEW FEATURE: Print Restock Invoice Popup Button
        ctk.CTkButton(
            btn_frame, text="📄  Print Restock Invoice",
            command=self.open_invoice_popup,
            fg_color="#8e44ad", hover_color="#732d91",
            font=("Arial", 13, "bold"), width=190, height=36, corner_radius=8
        ).pack(side="left", padx=(10, 0))

        # 👇 NEW FEATURE: Open the local folder to view saved invoices
        ctk.CTkButton(
            btn_frame, text="📂  View Saved Invoices",
            command=self.open_invoice_folder,
            fg_color="#34495e", hover_color="#2c3e50",
            font=("Arial", 13, "bold"), width=190, height=36, corner_radius=8
        ).pack(side="left", padx=(10, 0))

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
            "SELECT sku, product_name, local_stock, threshold FROM inventory")
        for code, name, qty, threshold in self.cursor.fetchall():
            self.stock[code] = {
                "name": name, "qty": qty,
                "threshold": threshold if threshold is not None else 5
            }
        # FIX (bug 6): don't pop up "low stock" modals for a fresh page load —
        # only for items that go low during the live session.
        self._suppress_alerts = True
        self.refresh_stock()
        self._suppress_alerts = False

    def add_item(self, code, name, quantity, threshold=None):
        # FIX (bug 3): the "Remove Item" flow already guarded against
        # over-removal and negative results, but "Add Item" had no guard at
        # all — a negative quantity here used to silently subtract stock.
        if quantity <= 0:
            messagebox.showerror("Error", "Quantity to add must be a positive number")
            return

        if code in self.stock:
            self.stock[code]["qty"] += quantity
            self.stock[code]["name"] = name
            # FIX (bug 2): previously a threshold typed in while restocking
            # an existing item was silently ignored (both in memory and in
            # the DB, since the ON CONFLICT clause never touched the
            # threshold column). Now it's honored if the user provided one;
            # otherwise the existing threshold is kept.
            if threshold is not None:
                self.stock[code]["threshold"] = threshold
            effective_threshold = self.stock[code]["threshold"]
        else:
            effective_threshold = threshold if threshold is not None else 5
            self.stock[code] = {"name": name, "qty": quantity,
                                "threshold": effective_threshold}

        self.cursor.execute(
            """INSERT INTO inventory (sku, product_name, local_stock, threshold)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(sku)
               DO UPDATE SET local_stock = local_stock + excluded.local_stock,
                             product_name = excluded.product_name,
                             threshold = excluded.threshold""",
            (code, name, quantity, effective_threshold)
        )
        self.conn.commit()
        self.refresh_stock()
        self._notify_dashboard()

    def erase_item(self, code, quantity):
        # FIX (bug 4): previously this silently no-op'd if the code wasn't
        # in stock, giving the user no feedback at all (unlike set_threshold,
        # which does validate). Now it reports the same way.
        if code not in self.stock:
            messagebox.showerror("Error", f"Item '{code}' not found in stock")
            return

        if quantity <= 0:
            messagebox.showerror("Error", "Quantity to remove must be a positive number")
            return

        current_qty = self.stock[code]["qty"]
        if quantity > current_qty:
            messagebox.showerror(
                "Error",
                f"Cannot remove {quantity}. Only {current_qty} in stock.")
            return

        new_qty = current_qty - quantity
        self.stock[code]["qty"] = new_qty
        # NOTE: quantity reaching 0 no longer deletes the item. The item
        # stays visible (as an out-of-stock / low-stock row) until the user
        # explicitly deletes it with the new "Delete Item" feature.
        self.cursor.execute(
            "UPDATE inventory SET local_stock = ? WHERE sku = ?",
            (new_qty, code)
        )
        self.conn.commit()
        self.refresh_stock()
        self._notify_dashboard()

    def delete_item(self, code):
        """NEW FEATURE: permanently remove an item from inventory, regardless
        of its current quantity. This is the only place an item is ever
        removed from self.stock / the database — quantity changes never do
        this anymore."""
        if code not in self.stock:
            messagebox.showerror("Error", f"Item '{code}' not found in stock")
            return

        self.cursor.execute("DELETE FROM inventory WHERE sku = ?", (code,))
        self.conn.commit()
        del self.stock[code]
        self.alerted_items.pop(code, None)
        self.refresh_stock()
        self._notify_dashboard()

    def gui_add_item(self):
        item = self.entry_item.get().strip()
        code = self.entry_code.get().strip()
        if not item or not code:
            messagebox.showerror("Error", "Item name and code can't be empty")
            return
        try:
            qty = int(self.entry_qty.get())
            threshold_str = self.entry_threshold.get().strip()
            threshold = int(threshold_str) if threshold_str else None
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

    def gui_delete_item(self):
        """NEW FEATURE: toolbar entry point for deleting an item by SKU,
        using the same 'Item Code / SKU' field as the other actions."""
        code = self.entry_code.get().strip()
        if not code:
            messagebox.showerror("Error", "Enter an item code to delete")
            return
        if code not in self.stock:
            messagebox.showerror("Error", f"Item '{code}' not found in stock")
            return

        name = self.stock[code]["name"]
        confirmed = messagebox.askyesno(
            "Confirm Delete",
            f"Permanently delete '{name}' ({code}) from inventory?\n"
            f"This cannot be undone."
        )
        if confirmed:
            self.delete_item(code)

    def gui_delete_item_row(self, code, name):
        """NEW FEATURE: per-row delete button in the stock table."""
        confirmed = messagebox.askyesno(
            "Confirm Delete",
            f"Permanently delete '{name}' ({code}) from inventory?\n"
            f"This cannot be undone."
        )
        if confirmed:
            self.delete_item(code)

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
            self.cursor.execute(
                "UPDATE inventory SET threshold = ? WHERE sku = ?",
                (value, code))
            self.conn.commit()
            messagebox.showinfo("Threshold Updated",
                                f"Low stock threshold for '{code}' set to {value}")
            self.refresh_stock()
            self._notify_dashboard()
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

        # FIX (bug 7): low-stock detection and alert bookkeeping used to run
        # only inside the filtered/searched render loop, so an item hidden
        # by the current search text or the "OK" filter never got its alert
        # state updated. Now we compute low-stock status and fire alerts for
        # *every* item in self.stock first, independent of what's displayed,
        # and only apply search/filter when deciding what to render.
        low_status = {}
        low_items = []
        for code, data in self.stock.items():
            is_low = data["qty"] <= data["threshold"]
            low_status[code] = is_low
            if is_low:
                low_items.append((code, data["name"], data["threshold"]))
                if not self.alerted_items.get(code, False):
                    self.alerted_items[code] = True
                    if not self._suppress_alerts:
                        messagebox.showwarning(
                            "Low Stock Alert",
                            f"⚠️ '{data['name']}' ({code}) is running low!\n"
                            f"Current stock: {data['qty']}  |  Threshold: {data['threshold']}"
                        )
            else:
                if code in self.alerted_items:
                    self.alerted_items[code] = False

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
                is_low = low_status[code]

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

                # Qty with +/- buttons and click-to-edit
                qty_frame = ctk.CTkFrame(row, fg_color="transparent")
                qty_frame.pack(side="left", padx=4, pady=10)

                btn_minus = ctk.CTkButton(qty_frame, text="-", width=26, height=26,
                    font=("Arial", 13, "bold"),
                    fg_color=("#E2E8F0", "#3d3d3d"), hover_color=("#CBD5E1", "#555"),
                    text_color=("#475569", "#F8FAFC"), corner_radius=6,
                    command=lambda c=code: self.change_qty(c, -1))
                btn_minus.pack(side="left", padx=(0, 4))

                lbl_qty = ctk.CTkLabel(qty_frame, text=str(qty),
                             font=("Arial", 13, "bold"),
                             text_color=("#e74c3c" if is_low else "#1E293B",
                                         "#e74c3c" if is_low else "#F1F5F9"),
                             width=30, anchor="center", cursor="xterm")
                lbl_qty.pack(side="left")
                lbl_qty.bind(
                    "<Button-1>",
                    lambda e, c=code, f=qty_frame, l=lbl_qty, q=qty:
                        self.start_qty_edit(c, f, l, q)
                )

                btn_plus = ctk.CTkButton(qty_frame, text="+", width=26, height=26,
                    font=("Arial", 13, "bold"),
                    fg_color=("#E2E8F0", "#3d3d3d"), hover_color=("#CBD5E1", "#555"),
                    text_color=("#475569", "#F8FAFC"), corner_radius=6,
                    command=lambda c=code: self.change_qty(c, 1))
                btn_plus.pack(side="left", padx=(4, 0))

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

                # NEW FEATURE: per-row delete button
                btn_delete = ctk.CTkButton(
                    row, text="🗑", width=30, height=26,
                    font=("Arial", 12),
                    fg_color="transparent",
                    hover_color=("#FEE2E2", "#4B1F1F"),
                    text_color="#c0392b",
                    corner_radius=6,
                    command=lambda c=code, n=name: self.gui_delete_item_row(c, n)
                )
                btn_delete.pack(side="right", padx=(4, 12), pady=10)

        # Update alert label
        if low_items:
            self.alert_label.configure(
                text="⚠ Low stock: " + ",  ".join(
                    f"{name} ({code})" for code, name, _ in low_items
                )
            )
        else:
            self.alert_label.configure(text="✓ All items stocked")

    def change_qty(self, code, amount):
        if code not in self.stock:
            return
        new_qty = self.stock[code]["qty"] + amount
        if new_qty < 0:
            messagebox.showerror("Error", "Stock cannot go below 0")
            return
        self.stock[code]["qty"] = new_qty
        # NOTE: quantity reaching 0 no longer deletes the item — it stays in
        # the list (shown as out of stock / low stock) until explicitly
        # deleted via the new "Delete Item" feature.
        self.cursor.execute("UPDATE inventory SET local_stock = ? WHERE sku = ?", (new_qty, code))
        self.conn.commit()
        self.refresh_stock()
        self._notify_dashboard()

    # ── In-line quantity editing ─────────────────────────────────────────────

    def start_qty_edit(self, code, qty_frame, lbl_qty, current_qty):
        """Replace the qty label with an editable entry box so the user can
        type an exact new quantity directly in the row."""
        if code not in self.stock:
            return

        # Avoid opening two editors on the same row
        if self._qty_edit_active == code:
            return
        self._qty_edit_active = code
        self._qty_committed = False

        lbl_qty.pack_forget()

        edit_var = tk.StringVar(value=str(current_qty))
        entry = ctk.CTkEntry(
            qty_frame,
            textvariable=edit_var,
            width=44, height=26,
            font=("Arial", 13, "bold"),
            justify="center",
            corner_radius=6
        )
        # Insert the entry where the label used to be (between - and + buttons)
        entry.pack(side="left")
        entry.focus_set()
        entry.select_range(0, tk.END)

        def commit(event=None):
            # FIX (bug 9): committing via Enter destroys the entry, which
            # itself fires a synthetic <FocusOut> also bound to commit —
            # without this guard commit_qty_edit ran a second time on an
            # already-destroyed widget for every Enter-confirmed edit.
            if self._qty_committed:
                return
            self._qty_committed = True
            self.commit_qty_edit(code, edit_var.get(), qty_frame, entry, lbl_qty)

        def cancel(event=None):
            if self._qty_committed:
                return
            self._qty_committed = True
            self._qty_edit_active = None
            entry.destroy()
            lbl_qty.pack(side="left")

        entry.bind("<Return>", commit)
        entry.bind("<KP_Enter>", commit)
        entry.bind("<FocusOut>", commit)
        entry.bind("<Escape>", cancel)

    def commit_qty_edit(self, code, new_value, qty_frame, entry, lbl_qty):
        self._qty_edit_active = None

        # Entry may already be destroyed if Escape/commit ran twice
        try:
            entry.destroy()
        except Exception:
            pass

        if code not in self.stock:
            self.refresh_stock()
            return

        new_value = new_value.strip()
        try:
            new_qty = int(new_value)
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be a whole number")
            self.refresh_stock()
            return

        if new_qty < 0:
            messagebox.showerror("Error", "Stock cannot go below 0")
            self.refresh_stock()
            return

        self.set_qty_direct(code, new_qty)

    def set_qty_direct(self, code, new_qty):
        """Set an item's quantity to an exact value (used by in-line editing)."""
        if code not in self.stock:
            return
        self.stock[code]["qty"] = new_qty
        # NOTE: quantity reaching 0 no longer deletes the item — see
        # delete_item() for the only place that removes an item now.
        self.cursor.execute(
            "UPDATE inventory SET local_stock = ? WHERE sku = ?",
            (new_qty, code)
        )
        self.conn.commit()
        self.refresh_stock()
        self._notify_dashboard()

    def _notify_dashboard(self):
        """Pushes the latest inventory numbers up to the Dashboard's
        'Low Stock' KPI card (and other charts) so it never shows stale
        data after an add/remove/threshold change made here."""
        if self.controller is not None and hasattr(self.controller, "refresh_all_charts"):
            try:
                self.controller.refresh_all_charts()
            except Exception:
                pass

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

        def _select_current(event=None):
            # FIX (bug 8): the old binding did listbox.get(listbox.curselection())
            # unconditionally, which raises IndexError if Return fires (or the
            # binding is reached some other way) with nothing selected — e.g.
            # right after the dropdown opens and no item has been highlighted
            # yet. It was also unreachable in practice since the entry widget
            # always kept keyboard focus; see the <Down> bindings above that
            # move focus here so this is now actually usable.
            selection = listbox.curselection()
            if not selection:
                return "break"
            on_select_cb(listbox.get(selection[0]))
            return "break"

        listbox.bind("<ButtonRelease-1>", _select_current)
        listbox.bind("<Return>", _select_current)
        return win

    def _focus_dropdown_listbox(self, win):
        """FIX (bug 8) helper: move keyboard focus from the entry into the
        floating suggestion listbox and highlight the first item, so arrow
        keys / Enter can be used to pick a suggestion."""
        if win is None:
            return "break"
        for child in win.winfo_children():
            if isinstance(child, tk.Listbox):
                child.focus_set()
                if child.size() > 0:
                    child.selection_clear(0, tk.END)
                    child.selection_set(0)
                    child.activate(0)
                return "break"
        return "break"

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

    # =========================================================================
    # NEW FEATURE: Restock Invoice Generator & UI Popup Engine
    # =========================================================================
    def open_invoice_popup(self):
        # 1. Grab current values from the inventory UI input fields
        item_name = self.entry_item.get().strip()
        item_code = self.entry_code.get().strip()
        qty_str = self.entry_qty.get().strip()

        # 2. Block the popup if the user hasn't filled in the basic product details
        if not item_name or not item_code or not qty_str:
            messagebox.showwarning("Missing Details", "Please enter Item Name, Code/SKU, and Quantity first before printing an invoice.")
            return

        try:
            qty = int(qty_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be a valid number.")
            return

        # 3. Create the modern popup window (Toplevel)
        self.invoice_win = ctk.CTkToplevel(self)
        self.invoice_win.title("Generate Supplier Invoice")
        self.invoice_win.geometry("400x350")
        self.invoice_win.grab_set()  # Focus locks on this popup
        self.invoice_win.resizable(False, False)

        # 4. Render popup UI components
        ctk.CTkLabel(self.invoice_win, text="Supplier Details", font=("Arial", 16, "bold"), text_color="#8e44ad").pack(pady=(20, 10))
        ctk.CTkLabel(self.invoice_win, text=f"Product: {item_name} [{item_code}]\nRestock Qty: {qty} units", font=("Arial", 12)).pack(pady=(0, 15))

        # Supplier Name Input
        ctk.CTkLabel(self.invoice_win, text="Supplier Company Name:", font=("Arial", 12, "bold")).pack(anchor="w", padx=40)
        self.ent_supplier = ctk.CTkEntry(self.invoice_win, placeholder_text="e.g., China Plastic Factory", width=320)
        self.ent_supplier.pack(pady=(5, 15))

        # Unit Cost Input
        ctk.CTkLabel(self.invoice_win, text="Unit Cost Price (RM):", font=("Arial", 12, "bold")).pack(anchor="w", padx=40)
        self.ent_unit_cost = ctk.CTkEntry(self.invoice_win, placeholder_text="e.g., 2.50", width=320)
        self.ent_unit_cost.pack(pady=(5, 20))

        # Action Button to generate the TXT
        btn_generate = ctk.CTkButton(
            self.invoice_win, 
            text="Generate & Print Invoice", 
            fg_color="#27ae60", hover_color="#219150", 
            font=("Arial", 13, "bold"),
            command=lambda: self.generate_txt_invoice(item_code, item_name, qty)
        )
        btn_generate.pack()

    def generate_txt_invoice(self, sku, name, qty):
        # 1. Retrieve the manual supplier inputs
        supplier_name = self.ent_supplier.get().strip()
        cost_str = self.ent_unit_cost.get().strip()

        if not supplier_name or not cost_str:
            messagebox.showwarning("Missing Details", "Please fill in all supplier information.", parent=self.invoice_win)
            return

        try:
            unit_cost = float(cost_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Unit Cost must be a valid decimal/number.", parent=self.invoice_win)
            return

        # 2. Calculate the grand total
        total_amount = qty * unit_cost
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
        invoice_no = f"INV-RESTOCK-{datetime.datetime.now().strftime('%H%M%S')}"

        # 3. Construct the highly professional invoice string
        invoice_content = f"""=========================================
          MEPIO RESTOCK INVOICE          
=========================================
Date       : {current_date}
Invoice No : {invoice_no}
Supplier   : {supplier_name}
-----------------------------------------
SKU        : {sku}
Item Name  : {name}
Quantity   : {qty} Units
Unit Cost  : RM {unit_cost:.2f}
-----------------------------------------
TOTAL AMOUNT DUE: RM {total_amount:.2f}
=========================================
Status: System Recorded & Reconciled
"""
        
        # 4. Save to a local TXT file
        filename = f"Restock_Invoice_{sku}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(invoice_content)

        # 5. Automatically open the file using macOS or Windows system commands
        import sys
        try:
            if sys.platform == "darwin":  # macOS detected
                subprocess.run(['open', filename])
            else:  # Windows fallback
                os.startfile(filename)
        except Exception as e:
            print(f"Failed to auto-open file: {e}")

        # 6. Close the popup and notify user
        self.invoice_win.destroy()
        messagebox.showinfo("Success", f"Invoice generated and opened automatically!\nSaved locally as: {filename}")

    # =========================================================================
    # NEW FEATURE: Auto-open system file explorer to view past invoices
    # =========================================================================
    def open_invoice_folder(self):
        import os
        import sys
        import subprocess
        
        try:
            current_dir = os.getcwd()
            
            # macOS
            if sys.platform == "darwin":  
                subprocess.run(['open', current_dir])
            else:  # windows fallback
                os.startfile(current_dir)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {e}")