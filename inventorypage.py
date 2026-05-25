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
        self.stock_list.pack(pady = 10, padx = 10, fill = "both", expand = True)

        self.alert_label = ctk.CTkLabel(self, text = "", font = ("Arial", 13), text_color = "red")
        self.alert_label.pack(pady = 5)

        # Load stock after stock_list exists to prevent bug
        self.load_stock_from_db()

    # main code
    # --- Database integration methods ---
    def load_stock_from_db(self):
        self.cursor.execute("SELECT product_name, local_stock FROM inventory")
        for item, qty in self.cursor.fetchall():
            self.stock[item] = qty
            self.thresholds[item] = 5
        self.refresh_stock()


    def add_item(self, item_name, quantity, threshold = 5):
        self.stock[item_name] = self.stock.get(item_name, 0) + quantity
        self.thresholds[item_name] = threshold  # default threshold
        self.refresh_stock()

        # Save to Database
        self.cursor.execute(
            """INSERT INTO inventory (sku, product_name, local_stock)
            VALUES (?, ?, ?)
            ON CONFLICT(sku) DO UPDATE SET local_stock = local_stock + excluded.local_stock""",
            (item_name, item_name, quantity)
        )
        self.conn.commit()
        self.refresh_stock()

    def erase_item(self, item_name, quantity):
        if item_name in self.stock:
            current_qty = self.stock[item_name]

            if quantity > current_qty:
                messagebox.showerror("Error", f"Cannot remove {quantity}. Only {current_qty} in stock.")
                return
            
            new_qty = current_qty - quantity
            self.stock[item_name] = new_qty
            if new_qty == 0:
                del self.stock[item_name]

            # Update Database
            self.cursor.execute(
                """UPDATE inventory SET local_stock = local_stock - ?
                WHERE product_name = ?""",
                (new_qty, item_name)
            )
            self.conn.commit()
        self.refresh_stock()

    def gui_add_item(self):
        item = self.entry_item.get().strip()
        if not item:
            messagebox.showerror("Error", "Item name can't be empty")
            return
        try:
            qty = int(self.entry_qty.get())
            threshold = int(self.entry_threshold.get()) if self.entry_threshold.get() else 5
            self.add_item(item, qty, threshold)
        except ValueError:
            messagebox.showerror("Error", "Quantity and threshold must be numbers")

    def gui_remove_item(self):
        item = self.entry_item.get().strip()
        if not item:
            messagebox.showerror("Error", "Item name cannot be empty")
            return
        try:
            qty = int(self.entry_qty.get())
            self.erase_item(item, qty)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")

    def set_threshold(self):
        item = self.entry_item.get().strip()
        if not item:
            messagebox.showerror("Error", "Enter an item name to set threshold")
            return
        try:
            value = int(self.entry_threshold.get())
            self.thresholds[item] = value
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
        for item, qty in self.stock.items():
            threshold = self.thresholds.get(item, 5)
            self.stock_list.insert(tk.END, f"· {item:<20} | {qty} (Threshold: {threshold})")
            if qty <= threshold:
                low_items.append(f"{item} (≤ {threshold})")

        if low_items:
            messagebox.showwarning(
                "Low Stock Alert",
                f"The following items are running low:\n{', '.join(low_items)}"
            )
            self.alert_label.configure(
                text = f"⚠️ Low stock alert: {', '.join(low_items)}"
            )
        else:
            self.alert_label.configure(text = "")


if __name__ == "__main__":
    app = MEPIOApp()
    def on_theme_change(event = None):
        if "inv" in app.pages:
            app.pages["inv"].update_listbox_theme()
    app.bind("<<AppearanceModeChanged>>", on_theme_change)
    app.mainloop()
