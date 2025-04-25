import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk
import os

def get_advising_url():
    return "https://www.usf.edu/engineering/ee/undergraduate/index.aspx"

def render(frame, images_dir):
    # Create a container frame for content
    content_frame = ttk.Frame(frame)
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Add back button at the top
    back_button = ttk.Button(
        content_frame,
        text="← Back to Departments",
        command=lambda: frame.master.master.show_advising_page()
    )
    back_button.pack(pady=10)
    
    # Store PhotoImage references to prevent garbage collection
    photo_images = []
    
    # Load advisor images
    advisor_images = {}
    try:
        # Navigate to the department's images directory
        dept_images_dir = os.path.join(images_dir, "College_of_Engineering", "Electrical_Engineering")
        print(f"Looking for images in: {dept_images_dir}")
        print(f"Directory exists: {os.path.exists(dept_images_dir)}")
        print(f"Directory contents: {os.listdir(dept_images_dir)}")
        
        # Load and resize images
        uysal_path = os.path.join(dept_images_dir, "uysal.png")
        print(f"Loading Uysal image from: {uysal_path}")
        print(f"File exists: {os.path.exists(uysal_path)}")
        uysal_img = Image.open(uysal_path)
        uysal_img = uysal_img.resize((150, 187))  # Slightly larger images
        uysal_photo = ImageTk.PhotoImage(uysal_img)
        photo_images.append(uysal_photo)  # Store reference
        advisor_images["Dr. Ismail Uysal"] = uysal_photo
        
        amy_path = os.path.join(dept_images_dir, "amy.png")
        print(f"Loading Amy image from: {amy_path}")
        print(f"File exists: {os.path.exists(amy_path)}")
        amy_img = Image.open(amy_path)
        amy_img = amy_img.resize((150, 187))
        amy_photo = ImageTk.PhotoImage(amy_img)
        photo_images.append(amy_photo)  # Store reference
        advisor_images["Amy Lyn Medicielo"] = amy_photo
    except Exception as e:
        print(f"Error loading advisor images: {e}")
        print(f"Current working directory: {os.getcwd()}")
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
    
    # Create a frame for advisors
    advisors_frame = ttk.Frame(content_frame)
    advisors_frame.pack(fill='x', pady=20)
    
    # Add advisor information
    for name, info in advisors.items():
        advisor_frame = ttk.Frame(advisors_frame)
        advisor_frame.pack(side='left', padx=20, pady=10, expand=True)
        
        # Add image if available
        if advisor_images.get(name):
            print(f"Displaying image for {name}")
            image_label = tk.Label(advisor_frame, image=advisor_images[name])
            image_label.image = advisor_images[name]  # Keep a reference
            image_label.pack(pady=5)
            print(f"Image label created for {name}")
        else:
            print(f"No image available for {name}")
        
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
    
    # Create a frame for the advising text with a border
    text_frame = ttk.LabelFrame(content_frame, text="Advising Information", padding=10)
    text_frame.pack(fill='x', pady=20, padx=20)
    
    # Split the text into sections for better formatting
    sections = advising_text.split('\n\n')
    
    for i, section in enumerate(sections):
        # Create a frame for each section
        section_frame = ttk.Frame(text_frame)
        section_frame.pack(fill='x', pady=5)
        
        # Use different fonts for different sections
        if i == 0:  # Greeting
            font = ('Helvetica', 11)
            justify = 'left'
        elif 'WALK-IN HOURS' in section or 'ONLINE APPOINTMENTS' in section:  # Headers
            font = ('Helvetica', 11, 'bold')
            justify = 'left'
        elif '*** IMPORTANT' in section:  # Important notice
            font = ('Helvetica', 10, 'italic')
            justify = 'center'
        else:  # Regular text
            font = ('Helvetica', 10)
            justify = 'left'
        
        text_label = ttk.Label(
            section_frame,
            text=section,
            wraplength=550,
            justify=justify,
            font=font
        )
        text_label.pack(padx=10, pady=2) 