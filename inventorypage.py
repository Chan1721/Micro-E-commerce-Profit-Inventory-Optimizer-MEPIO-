import customtkinter as ctk
import tkinter as tk 

class InventoryPage(ctk.CTkFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.stock = {}

    # GUI stuffs
    self.label = label = ctk.CTkLabel(self, text = "Inventory Management", font = ("Arial", 20))
    self.label.pack(pady=10)

    self.entry_item = ctk.CTkEntry(self, placeholder_text = "Item name")
    self.entry_item.pack(pady = 5)

    self.entry_qty = ctk.CTkEntry(self, placeholer_text = "Quantity")
    self.entry_qty.pack(pady = 5)

    self.btn_add = ctk.CTkButton(self, text = "Add Item", command = self.gui_add_item)
    self.btn_add.pack(pady = 5)

    self.btn_remove = ctk.CTkButton(self, text = "Remove Item", command = self.gui_remove_item)
    self.btn_remove.pack(pady = 5)

    self.stock_list = tk.Listbox(self,height = 10, width = 40)
    self.stock_list.pack(pady = 10)


    def add_item(self, item_name, quantity):
        if item_name in self.stock:
            self.stock[item_name] += quantity
        else:
            self.stock[item_name] = quantity
        print(f"Added {quantity} of {item_name}. Total: {self.stock[item_name]}")

    def erase_item(self, item_name, quantity):
        if item_name in self.stock:
            if self.stock[item_name] >= quantity:
                self.stock[item_name] -= quantity
                print(f"Removed {quantity} of {item_name}. Remaining: {self.stock[item_name]}")
                if self.stock[item_name] == 0:
                    del self.stock[item_name]
                    print(f"{item_name} is now out of stock.")
            else:
                print(f"not enough {item_name} in stock for erase.")
        else:
            print(f"{item_name} is not avaliable in stock.")
            

    def view_stock(self):
        if not self.stock:
            print("Stock is empty.")
        else:
            print("Current Stock")
            for item, qty in self.stock.items():
                print(f"-{item}: {qty}")

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

def refresh_stock(self):
    if hasattr(self, "stock_list"):
        self.stock_list.delete(0, tk.END)
        for item, qty in self.stock.items():
            self.stock_list.insert(tk.END, f"{item}: {qty}")

if __name__ == "__main__":
    main()
