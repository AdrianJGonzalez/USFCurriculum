import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk
import os

def get_advising_url():
    return "https://www.usf.edu/engineering/ee/undergraduate/index.aspx"

def render(frame):
    # Create a container frame for centering
    container = ttk.Frame(frame)
    container.pack(expand=True, fill='both')
    
    # Create a canvas with scrollbar
    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    # Configure the canvas
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Add back button at the top
    back_button = ttk.Button(
        scrollable_frame,
        text="← Back to Departments",
        command=lambda: frame.master.master.master.master.show_advising_page()
    )
    back_button.pack(pady=10)
    
    # Load advisor images
    advisor_images = {}
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate to the advisor images directory
        images_dir = os.path.join(current_dir, "..", "advisor_images", "Electrical_Engineering")
        
        # Load and resize images
        uysal_img = Image.open(os.path.join(images_dir, "uysal.png"))
        uysal_img = uysal_img.resize((150, 187))  # Slightly larger images
        advisor_images["Dr. Ismail Uysal"] = ImageTk.PhotoImage(uysal_img)
        
        amy_img = Image.open(os.path.join(images_dir, "amy.png"))
        amy_img = amy_img.resize((150, 187))
        advisor_images["Amy Lyn Medicielo"] = ImageTk.PhotoImage(amy_img)
    except Exception as e:
        print(f"Error loading advisor images: {e}")
        advisor_images["Dr. Ismail Uysal"] = None
        advisor_images["Amy Lyn Medicielo"] = None
    
    # Advisor information
    advisors = {
        "Dr. Ismail Uysal": {
            "title": "Undergraduate Program Director",
            "link": "https://calendly.com/iuysal/advising"
        },
        "Amy Lyn Medicielo": {
            "title": "Undergraduate Program Specialist",
            "link": "https://calendly.com/iuysal/advising"
        }
    }
    
    advising_text = """Dear students,

If you have submitted your ULDP (Upper-Level) form, it has been processed & accepted, and you would like to book an advising appointment - you've come to the right place. You have multiple options available to you for booking your appointment.

WALK-IN HOURS (Updated for Spring 2025):
• Location: Main EE office (ENB 379)
• Time: 10AM - 4PM on Mondays and Wednesdays
• First-come-first-serve basis
• Walk-in hours begin Monday, Jan 28th

*** IMPORTANT: These days are updated for Spring - they used to be Tuesday/Thursday - please note the new days! ***

ONLINE APPOINTMENTS:
• Book using the Calendly links below
• If you don't see available slots, use walk-in hours
• After booking, you'll receive a Microsoft Teams meeting invitation
• Choose ONE slot only

Remember: Once confirmed, you will receive a calendar invitation for your Teams meeting on or before your scheduled appointment."""
    
    # Create a centered frame for content
    content_frame = ttk.Frame(scrollable_frame)
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Create a frame for advisors
    advisors_frame = ttk.Frame(content_frame)
    advisors_frame.pack(fill='x', pady=20)
    
    # Add advisor information
    for name, info in advisors.items():
        advisor_frame = ttk.Frame(advisors_frame)
        advisor_frame.pack(side='left', padx=20, pady=10, expand=True)
        
        # Add image if available
        if advisor_images.get(name):
            image_label = ttk.Label(advisor_frame, image=advisor_images[name])
            image_label.pack(pady=5)
        
        # Name and title
        name_label = ttk.Label(advisor_frame, text=name, font=('Helvetica', 12, 'bold'))
        name_label.pack()
        
        title_label = ttk.Label(advisor_frame, text=info['title'])
        title_label.pack()
        
        # Link button
        link_btn = ttk.Button(
            advisor_frame,
            text="Schedule Appointment",
            command=lambda url=info['link']: webbrowser.open(url)
        )
        link_btn.pack(pady=5)
    
    # Add advising text
    text_frame = ttk.Frame(content_frame)
    text_frame.pack(fill='x', pady=20)
    
    text_label = ttk.Label(
        text_frame,
        text=advising_text,
        wraplength=600,
        justify='center',
        font=('Helvetica', 10)
    )
    text_label.pack(padx=20)
    
    # Add mousewheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)