import customtkinter as ctk #shortcut for customtkinter as ctk

def Inventory():
    print("button pressed")
def Dashboard():
    print("button pressed")
def button3():
    print("button pressed")
def button4():
    print("button pressed")

app = ctk.CTk() # intializes the app, this is the main window of the program 
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MEPIO")
        self.geometry("1920x1080")
        
        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

    def button_callback(self):
        print("button pressed")
app.mainloop()