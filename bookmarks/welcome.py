import tkinter as tk
from tkinter import ttk

class WelcomePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        
    def create_widgets(self):
        # Welcome label
        welcome_label = ttk.Label(
            self,
            text="Welcome to the Academic Program Manager",
            font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)
        
        # Description
        description = ttk.Label(
            self,
            text="Use the tabs above to navigate through different sections:\n\n" +
                 "• Course Catalog - Browse available courses\n" +
                 "• Flowchart - View your program flowchart\n" +
                 "• Degree Selector - Choose your degree program\n" +
                 "• Upload Transcript - Upload and manage your transcripts\n" +
                 "• Advising - Select your department and information!",
            wraplength=600
        )
        description.pack(pady=20)
