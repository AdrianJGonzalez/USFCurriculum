import tkinter as tk

class FAQPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Frequently Asked Questions", font=("Helvetica", 16))
        label.pack(pady=20)
        # Add your FAQ content here!
