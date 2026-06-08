import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import threading
import queue
import socket

from flask import Flask, request, jsonify


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

        # Scanner server stuff
        self.scan_queue = queue.Queue()
        self.scanner_server = None
        self.scanner_running = False

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

        self.btn_scan = ctk.CTkButton(
            btn_frame, text="📱  Scan Barcode",
            command=self.toggle_scanner,
            fg_color="#f39c12", hover_color="#e67e22",
            font=("Arial", 13, "bold"), width=160, height=36, corner_radius=8
        )
        self.btn_scan.pack(side="left", padx=(10, 0))

        self.scan_status_label = ctk.CTkLabel(btn_frame, text="", font=("Arial", 11), text_color="#27ae60")
        self.scan_status_label.pack(side="left", padx=(10, 0))

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

    # ── Barcode scanner (phone over WiFi) ───────────────────────────────────

    def get_local_ip(self):
        # Get the PC's local IP address so phone can connect
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    def toggle_scanner(self):
        if self.scanner_running:
            self.stop_scanner()
        else:
            self.start_scanner()

    def start_scanner(self):
        ip = self.get_local_ip()
        port = 5050

        # Simple Flask app — just two routes
        app = Flask(__name__)
        app.logger.disabled = True
        import logging
        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)

        @app.route("/")
        def index():
            # Webpage that opens phone camera and scans barcode
            html = """<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MEPIO Barcode Scanner</title>
  <script src="https://unpkg.com/@zxing/library@latest/umd/index.min.js"></script>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; padding: 20px; background: #f8fafc; }
    h2 { color: #4F6EF7; }
    #video { width: 100%; max-width: 400px; border-radius: 12px; }
    #result { margin-top: 20px; font-size: 20px; font-weight: bold; color: #27ae60; }
    #status { color: #888; font-size: 14px; margin-top: 8px; }
  </style>
</head>
<body>
  <h2>MEPIO Barcode Scanner</h2>
  <p id="status">Starting camera...</p>
  <video id="video" autoplay muted playsinline></video>
  <div id="result"></div>
  <script>
    const codeReader = new ZXing.BrowserMultiFormatReader();
    codeReader.decodeFromVideoDevice(null, "video", (result, err) => {
      if (result) {
        document.getElementById("result").innerText = "Scanned: " + result.text;
        document.getElementById("status").innerText = "Sending to app...";
        fetch("/scan", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({sku: result.text})
        }).then(() => {
          document.getElementById("status").innerText = "Sent! Scan another item.";
        });
      }
    });
    document.getElementById("status").innerText = "Point camera at barcode";
  </script>
</body>
</html>"""
            return html

        @app.route("/scan", methods=["POST"])
        def receive_scan():
            data = request.get_json()
            if data and "sku" in data:
                self.scan_queue.put(data["sku"])
            return jsonify({"ok": True})

        # Run Flask in a background thread so it doesn't freeze the app
        self.scanner_running = True
        self.scanner_thread = threading.Thread(
            target=lambda: app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False),
            daemon=True
        )
        self.scanner_thread.start()

        # Update UI
        self.btn_scan.configure(text="🛑  Stop Scanner", fg_color="#c0392b", hover_color="#e74c3c")
        self.scan_status_label.configure(text=f"Open on phone: http://{ip}:{port}")

        # Start polling the queue every 500ms
        self.poll_scan_queue()

        # Show a popup with the QR/link so user can easily open on phone
        self.show_scanner_popup(ip, port)

    def stop_scanner(self):
        self.scanner_running = False
        self.btn_scan.configure(text="📱  Scan Barcode", fg_color="#f39c12", hover_color="#e67e22")
        self.scan_status_label.configure(text="")

    def poll_scan_queue(self):
        # Check if a new scan came in
        try:
            sku = self.scan_queue.get_nowait()
            self.entry_code.delete(0, tk.END)
            self.entry_code.insert(0, sku)
            # Also auto-fill item name if SKU exists in DB
            self.cursor.execute("SELECT product_name FROM inventory WHERE sku = ?", (sku,))
            result = self.cursor.fetchone()
            if result:
                self.entry_item.delete(0, tk.END)
                self.entry_item.insert(0, result[0])
            self.scan_status_label.configure(text=f"Scanned: {sku} ✓")
        except queue.Empty:
            pass

        # Keep polling while scanner is on
        if self.scanner_running:
            self.after(500, self.poll_scan_queue)

    def show_scanner_popup(self, ip, port):
        # Show a small window with the link and a QR code
        popup = ctk.CTkToplevel(self)
        popup.title("Barcode Scanner")
        popup.geometry("340x220")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(popup, text="📱 Phone Scanner Active",
                     font=("Arial", 16, "bold"), text_color="#4F6EF7").pack(pady=(20, 4))
        ctk.CTkLabel(popup, text="Open this URL on your phone browser:",
                     font=("Arial", 12), text_color="gray").pack()

        url = f"http://{ip}:{port}"
        ctk.CTkLabel(popup, text=url,
                     font=("Arial", 14, "bold"), text_color="#27ae60").pack(pady=(6, 4))

        ctk.CTkLabel(popup, text="Make sure your phone is on the same WiFi.",
                     font=("Arial", 11), text_color="gray").pack()

        # Try to show QR code if qrcode library is available
        try:
            import qrcode
            from PIL import Image, ImageTk
            import io

            qr = qrcode.make(url)
            qr = qr.resize((120, 120))
            qr_img = ImageTk.PhotoImage(qr)
            lbl_qr = tk.Label(popup, image=qr_img, bg="#FFFFFF")
            lbl_qr.image = qr_img  # keep reference
            lbl_qr.pack(pady=8)
        except ImportError:
            ctk.CTkLabel(popup, text="(Install qrcode + Pillow for QR code display)",
                         font=("Arial", 10), text_color="gray").pack(pady=8)

        ctk.CTkButton(popup, text="Close", width=100,
                      command=popup.destroy).pack(pady=(0, 16))

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

                # Qty with +/- buttons
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
                             width=30, anchor="center")
                lbl_qty.pack(side="left")

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

    def change_qty(self, code, amount):
        if code not in self.stock:
            return
        new_qty = self.stock[code]["qty"] + amount
        if new_qty < 0:
            messagebox.showerror("Error", "Stock cannot go below 0")
            return
        self.stock[code]["qty"] = new_qty
        if new_qty == 0:
            del self.stock[code]
            self.cursor.execute("DELETE FROM inventory WHERE sku = ?", (code,))
        else:
            self.cursor.execute("UPDATE inventory SET local_stock = ? WHERE sku = ?", (new_qty, code))
        self.conn.commit()
        self.refresh_stock()

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