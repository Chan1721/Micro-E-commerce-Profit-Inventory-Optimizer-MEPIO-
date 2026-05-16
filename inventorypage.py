import customtkinter as ctk
import tkinter as tk 
ctk.set_appearance_mode("light")

class InventoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller = None,):
        super().__init__(parent, fg_color =("white", "#2b2b2b"))
        self.controller = controller
        self.stock = {}
        self.low_stock_threshold = 5

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

    # main code
    def add_item(self, item_name, quantity):
        if item_name in self.stock:
            self.stock[item_name] += quantity
        else:
            self.stock[item_name] = quantity
        self.refresh_stock() # refresh listbox
        print(f"Added {quantity} of {item_name}. Total: {self.stock[item_name]}")

    def erase_item(self, item_name, quantity):
        if item_name in self.stock:
            if self.stock[item_name] >= quantity:
                self.stock[item_name] -= quantity
                if self.stock[item_name] == 0:
                    del self.stock[item_name]
        self.refresh_stock()

    def gui_add_item(self):
        item = self.entry_item.get()
        try:
            qty = int(self.entry_qty.get())
            self.add_item(item, qty)
        except ValueError:
            print("Quantity must be a number")

    def gui_remove_item(self):
        item = self.entry_item.get()
        try:
            qty = int (self.entry_qty.get())
            self.erase_item(item,qty)
        except ValueError:
            print("Quantity must be a number")

    def update_listbox_theme(self):
        mode = ctk.get_appearance_mode().lower()
        colors = self.listbox_colors[mode]
        self.stock_list.config(bg = colors["bg"], fg = colors["fg"])

    def refresh_stock(self):
        if hasattr(self, "stock_list"):
            self.update_listbox_theme()
            self.stock_list.delete(0, tk.END)
            low_items = []
            for item, qty in self.stock.items():
                self.stock_list.insert(tk.END, f"· {item:<20} | {qty}")
                if qty <= self.low_stock_threshold:
                    low_items.append(item)

            if low_items:
                self.alert_label.configure(
                    text = f"⚠️ Low stock alert: {', '.join(low_items)}"
                )
            else:
                self.alert_label.configure(text = "")

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("500x400")
    inv_page = InventoryPage(app)
    inv_page.pack(fill = "both", expand = True)
    app.mainloop()
