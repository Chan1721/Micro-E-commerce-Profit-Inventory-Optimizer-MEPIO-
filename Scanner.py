import customtkinter as ctk
import qrcode
from PIL import Image
import os

ctk.set_appearance_mode("Light")

class BarcodeScannerPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MEPIO - Barcode to QR Code Linker")
        self.geometry("800x450")

        # --- Mock Database ---
        self.mock_db = {
            "9551234567890": "LIP-001-RED",
            "9559876543210": "MAS-002-BLK",
            "9555566677788": "EYE-003-BRW"
        }

        # --- Main Layout ---
        self.grid_columnconfigure(0, weight=1) # Left side: Control Panel
        self.grid_columnconfigure(1, weight=1) # Right side: QR Code Display Panel
        self.grid_rowconfigure(0, weight=1)

        # =========================================================================
        # LEFT PANEL: Device Scanner Controls
        # =========================================================================
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        ctk.CTkLabel(self.left_frame, text="Device Scan Linker", font=("Arial", 18, "bold"), text_color="#3498db").pack(anchor="w", pady=(0, 20))
        
        # Guide Info
        guide_text = ("1. Connect your device (Phone scanner app or Wireless gun) to PC.\n"
                      "2. Click the input box below to focus your cursor.\n"
                      "3. Scan any retail product barcode.")
        ctk.CTkLabel(self.left_frame, text=guide_text, justify="left", font=("Arial", 11), text_color="gray").pack(anchor="w", pady=(0, 20))

        # Barcode Entry (The target field where the scanner inputs data)
        ctk.CTkLabel(self.left_frame, text="Active Barcode Input Field:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(5, 2))
        
        self.barcode_entry = ctk.CTkEntry(self.left_frame, placeholder_text="Click here & Scan...", width=280, height=35, fg_color="#F1F5F9")
        self.barcode_entry.pack(anchor="w", pady=(0, 10))
        
        # CRITICAL STEP: Bind the Enter key (<Return>) to capture device signal completed
        self.barcode_entry.bind("<Return>", self.process_device_scan)
        
        # Status Label
        self.lbl_status = ctk.CTkLabel(self.left_frame, text="Status: Waiting for device signal...", font=("Arial", 11, "italic"), text_color="gray")
        self.lbl_status.pack(anchor="w", pady=5)

        # =========================================================================
        # RIGHT PANEL: Dynamic QR Code Display
        # =========================================================================
        self.right_frame = ctk.CTkFrame(self, corner_radius=15, fg_color=("#FFFFFF", "#252525"))
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        ctk.CTkLabel(self.right_frame, text="Generated SKU QR Code", font=("Arial", 14, "bold")).pack(pady=15)

        # Placeholder label where the QR code image will be displayed
        self.qr_display_label = ctk.CTkLabel(self.right_frame, text="[ No QR Generated Yet ]", text_color="gray")
        self.qr_display_label.pack(expand=True, fill="both", padx=20, pady=20)

    def process_device_scan(self, event):
        """Triggered automatically when the phone/scanner finishes typing and sends an Enter key."""
        raw_barcode = self.barcode_entry.get().strip()
        
        if not raw_barcode:
            return

        # Clear the entry box immediately so it's ready for the next product scan
        self.barcode_entry.delete(0, ctk.END)

        # Look up SKU from database
        sku_code = self.mock_db.get(raw_barcode)

        if sku_code:
            self.lbl_status.configure(text=f"Status: Match Found! SKU -> {sku_code}", text_color="#27ae60")
            
            # Generate the QR Code in background
            qr_file = self.generate_qr_image(sku_code)
            
            # Update the UI with the newly generated image
            self.display_qr_code(qr_file)
        else:
            self.lbl_status.configure(text=f"Status: Error! Barcode [{raw_barcode}] not registered.", text_color="#e74c3c")
            self.qr_display_label.configure(image=None, text="[ Match Failed ]")

    def generate_qr_image(self, text_data):
        """Helper to create a temporary QR Code image file"""
        qr = qrcode.QRCode(version=1, box_size=6, border=2)
        qr.add_data(text_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        file_path = f"temp_{text_data}.png"
        img.save(file_path)
        return file_path

    def display_qr_code(self, file_path):
        """Loads the image file and updates the CTkLabel view"""
        pil_image = Image.open(file_path)
        
        # Convert PIL image to CTkImage for high-DPI scaling support
        ctk_qr_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(180, 180))
        
        # Apply to label
        self.qr_display_label.configure(image=ctk_qr_image, text="")
        
        # Optional: Clean up the file from disk if you don't want to clutter the folder
        # os.remove(file_path)

if __name__ == "__main__":
    app = BarcodeScannerPage()
    app.mainloop()