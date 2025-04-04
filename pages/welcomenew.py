from PIL import Image, ImageTk  
import tkinter as tk  

# Initialize the main window
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
root = tk.Tk()
root.title("Welcome Page - Flowchart Application")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")  
root.resizable(True, True)  

# Colors and fonts
USF_GREEN = "#006747"
USF_GOLD = "#CFC493"
font_large = ("Arial", 24, "bold")

# Load and display the background image
def update_background_image(event=None):
    try:
        bg_image = Image.open("usflogo.jpg")  
        bg_image = bg_image.resize((root.winfo_width(), root.winfo_height()))  
        bg_image_tk = ImageTk.PhotoImage(bg_image)  

        background_label.config(image=bg_image_tk)
        background_label.image = bg_image_tk  
    except Exception as e:
        print("Error loading background image:", e)

# Background label
background_label = tk.Label(root)
background_label.place(relwidth=1, relheight=1)  

# Welcome message
welcome_label = tk.Label(root, text="Welcome to the Flowchart Application!", 
                         font=font_large, fg=USF_GOLD, bg=USF_GREEN)
welcome_label.place(relx=0.5, rely=0.1, anchor="center")  

# Bind resizing event
root.bind("<Configure>", update_background_image)

# Run the application
root.mainloop()
