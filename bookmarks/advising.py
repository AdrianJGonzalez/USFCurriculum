import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk
import os
import importlib.util

class AdvisingPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.colleges = {
            "College of Engineering": {
                "url": "https://www.usf.edu/engineering/about/index.aspx",
                "departments": {
                    "Electrical Engineering": "electrical_engineering_adv",
                    "Computer Science and Engineering": "cse_adv",
                    "Chemical Engineering": "chemical_engineering_adv",
                    "Civil Engineering": "civil_engineering_adv",
                    "Industrial Engineering": "industrial_engineering_adv",
                    "Mechanical Engineering": "mechanical_engineering_adv"
                }
            },
            "College of Arts and Sciences": {
                "url": "https://www.usf.edu/arts-sciences/index.aspx",
                "departments": {
                    "Mathematics": "math_adv",
                    "Physics": "physics_adv",
                    "Chemistry": "chemistry_adv"
                }
            }
        }
        
        self.current_advising_module = None
        self.create_widgets()
        
    def create_widgets(self):
        # Main content frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=10)

        # Header frame for "Academic Advising"
        header = ttk.Label(
            self.main_frame,
            text="Academic Advising",
            font=("Helvetica", 20, 'bold'),
            foreground='#006747'
        )
        header.grid(row=0, column=0, padx=10, pady=20, columnspan=2)

        # Create a 2-column grid layout (left side for selection, right side for advisor display)
        self.main_frame.grid_columnconfigure(0, weight=1, uniform="equal")  # Left column (selection)
        self.main_frame.grid_columnconfigure(1, weight=1, uniform="equal")  # Right column (advisor info)

        # Left half frame for college and department selection
        left_half_frame = ttk.Frame(self.main_frame)
        left_half_frame.grid(row=1, column=0, sticky="nsew")

        # Create selection frame
        self.selection_frame = ttk.Frame(left_half_frame)
        self.selection_frame.pack(expand=True, fill='both')

        # College selection
        college_frame = ttk.LabelFrame(self.selection_frame, text="Select Your College")
        college_frame.pack(fill='x', pady=10)

        self.college_var = tk.StringVar()
        self.college_var.trace('w', self.update_departments)

        college_dropdown = ttk.Combobox(
            college_frame,
            textvariable=self.college_var,
            values=list(self.colleges.keys()),
            state="readonly",
            width=30
        )
        college_dropdown.pack(padx=10, pady=10)

        # Department selection
        self.dept_frame = ttk.LabelFrame(self.selection_frame, text="Select Your Department")
        self.dept_frame.pack(fill='x', pady=10)

        self.dept_var = tk.StringVar()
        self.dept_var.trace('w', self.update_link)

        self.dept_dropdown = ttk.Combobox(
            self.dept_frame,
            textvariable=self.dept_var,
            state="readonly",
            width=30
        )
        self.dept_dropdown.pack(padx=10, pady=10)

        # Link frame
        self.link_frame = ttk.Frame(self.selection_frame)
        self.link_frame.pack(fill='x', pady=20)

        # College info button
        self.college_btn = ttk.Button(
            self.link_frame,
            text="Visit College Website",
            command=self.open_college_page,
            state="disabled"
        )
        self.college_btn.pack(pady=5)

        # Department info button
        self.dept_btn = ttk.Button(
            self.link_frame,
            text="Visit Department Advising",
            command=self.open_dept_page,
            state="disabled"
        )
        self.dept_btn.pack(pady=5)

        # Instructions
        instructions = ttk.Label(
            self.selection_frame,
            text="Select your college and department to access advising resources.",
            wraplength=400,
            justify="center"
        )
        instructions.pack(pady=20)

        # Right half frame for displaying advisor info
        self.right_half_frame = ttk.Frame(self.main_frame)
        self.right_half_frame.grid(row=1, column=1, sticky="nsew")

        # Advising content frame
        self.advising_frame = ttk.Frame(self.right_half_frame)

    def show_advising_page(self):
        # Hide the advising frame and show the selection frame
        self.advising_frame.pack_forget()
        self.selection_frame.pack(expand=True, fill='both')

    def update_departments(self, *args):
        college = self.college_var.get()
        if college:
            self.dept_dropdown['values'] = list(self.colleges[college]['departments'].keys())
            self.dept_var.set('')  # Clear department selection
            self.college_btn.configure(state="normal")
            self.dept_btn.configure(state="disabled")
            self.hide_advising()
        else:
            self.dept_dropdown['values'] = []
            self.dept_var.set('')
            self.college_btn.configure(state="disabled")
            self.dept_btn.configure(state="disabled")
            self.hide_advising()

    def update_link(self, *args):
        dept = self.dept_var.get()
        if dept == "Electrical Engineering":
            self.display_advisor_info()  # Show the advisor info on the right side
            self.dept_btn.configure(state="normal")
        else:
            self.dept_btn.configure(state="disabled")
            self.hide_advising()

    def display_advisor_info(self):
        # Clear any existing widgets in the right frame before adding new ones
        for widget in self.advising_frame.winfo_children():
            widget.destroy()

        # Display the "Electrical Engineering Advisor Info" text
        advisor_label = ttk.Label(
            self.advising_frame,
            text="Electrical Engineering Advisor Info",
            font=("Helvetica", 16),
            foreground="#006747"
        )
        advisor_label.pack(pady=10)

        # Display the image (make sure to place uysal.png in the same directory as the script)
        try:
            img = Image.open("uysal.png")
            img = img.resize((200, 200))  # Resize the image if necessary
            img_tk = ImageTk.PhotoImage(img)
            img_label = ttk.Label(self.advising_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to the image
            img_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")

        # Display the advisor details
        advisor_name = ttk.Label(
            self.advising_frame,
            text="Ismail Uysal",
            font=("Helvetica", 14, 'bold'),
            foreground="#006747"
        )
        advisor_name.pack(pady=5)

        # Display the role line (Undergraduate Program Director)
        role_label = ttk.Label(
            self.advising_frame,
            text="Undergraduate Program Director",
            font=("Helvetica", 12),
            foreground="#006747"
        )
        role_label.pack(pady=5)

        # Display the "Schedule Appointment" button
        schedule_btn = ttk.Button(
            self.advising_frame,
            text="Schedule Appointment",
            command=self.open_schedule_appointment
        )
        schedule_btn.pack(pady=10)

        # Show the advisor info frame
        self.advising_frame.pack(expand=True, fill="both")

    def open_schedule_appointment(self):
        # Open the Calendly link for scheduling an appointment
        url = "https://calendly.com/iuysal/advising?month=2025-04"
        webbrowser.open(url)

    def hide_advising(self):
        self.advising_frame.pack_forget()
        self.selection_frame.pack(expand=True, fill='both')

    def open_college_page(self):
        college = self.college_var.get()
        if college and college in self.colleges:
            webbrowser.open(self.colleges[college]['url'])

    def open_dept_page(self):
        college = self.college_var.get()
        dept = self.dept_var.get()
        if college and dept and college in self.colleges and dept in self.colleges[college]['departments']:
            module_name = self.colleges[college]['departments'][dept]
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Navigate to the departments directory
            module_path = os.path.join(current_dir, "advising", "Departments", f"{module_name}.py")

            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec is not None and spec.loader is not None:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, 'get_advising_url'):
                        webbrowser.open(module.get_advising_url())
                else:
                    raise ImportError(f"Could not load module spec for {module_name} at {module_path}")
            except Exception as e:
                print(f"Error getting department URL: {e}")

