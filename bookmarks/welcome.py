import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class WelcomePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="Welcome.TFrame")
        self.create_widgets()

    def create_widgets(self):
        # Create a style for the frame
        style = ttk.Style()
        style.configure("Welcome.TFrame", background="#EDEBD1")
        style.configure("Welcome.TLabel", background="#EDEBD1", font=("Helvetica", 16))
        style.configure("Title.TLabel", background="#EDEBD1", font=("Helvetica", 20, "bold"), foreground="#006747")

        container = ttk.Frame(self, style="Welcome.TFrame")
        container.pack(expand=True, fill="both", padx=20, pady=20)
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(script_dir, "USF.png") 
            print(f"Attempting to load logo from: {logo_path}") 
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((900, 150), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_image)
            logo_label = ttk.Label(container, image=self.logo, style="Welcome.TLabel")
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_label = ttk.Label(container, text="[USF Logo Placeholder]", style="Welcome.TLabel")
            logo_label.pack(pady=10)

        welcome_label = ttk.Label(
            container,
            text="Welcome to the Academic Program Manager",
            style="Title.TLabel"
        )
        welcome_label.pack(pady=10)

        # Description
        description = ttk.Label(
            container,
            text="Use the tabs above to navigate through different sections:\n\n\n" +
                 "• Course Catalog - Browse available courses\n\n" +
                 "• Flowchart - View your program flowchart\n\n" +
                 "• Degree Selector - Choose your degree program\n\n" +
                 "• Upload Transcript - Upload and manage your transcripts\n\n" +
                 "• Advising - Select your department and information!",
            style="Welcome.TLabel",
            wraplength=600,
            justify="center"
        )
        description.pack(pady=10)
        footer = ttk.Label(
            container,
            text="Go Bulls!",
            style="Welcome.TLabel",
            font=("Helvetica", 14, "italic"),
            foreground="#006747" 
        )
        footer.pack(pady=10)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Academic Program Manager")
    root.geometry("800x600")
    app = WelcomePage(root)
    app.pack(expand=True, fill="both")
    root.mainloop()
