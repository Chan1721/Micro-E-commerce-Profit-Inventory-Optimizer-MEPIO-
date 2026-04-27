import customtkinter as ctk
import tkinter as tk 

class InventoryPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.stock = {}

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

def main():
    system = InventoryPage()
    while True:
        print("\n--- Stock System Menu ---")
        print("1. Add Item")
        print("2. Erase Item")
        print("3. Stock List")
        print("4. Exit")

        choice = input("Enter related number to perform action (1-4): ")

        if choice == "1":
            item = input("Enter item name: ")
            qty = int(input("Enter quantity: "))
            system.add_item(item, qty)
        elif choice == "2":
            item = input("Enter item name:")
            qty = int(input("Enter quantity: "))
            system.erase_item(item, qty)
        elif choice == "3":
            system.view_stock()
        elif choice == "4":
            print("Exiting system. Bye!")
            break
        else:
            print("Invalid actions. Please try again")

if __name__ == "__main__":
    main()
