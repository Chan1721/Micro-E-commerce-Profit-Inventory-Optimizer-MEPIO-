import customtkinter as ctk

def inventory():
    print("button pressed")

app = ctk.CTk()
app.title("MEPIO")
app.geometry("400x150")

button = ctk.CTkButton(app, text="Inventory", command=inventory)
button.grid(row=0, column=0, padx=20, pady=20)
app.grid_columnconfigure(0, weight=1)

app.mainloop()