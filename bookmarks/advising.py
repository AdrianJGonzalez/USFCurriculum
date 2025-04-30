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
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=10)

        header = ttk.Label(
            self.main_frame,
            text="Academic Advising",
            font=("Helvetica", 20, 'bold'),
            foreground='#006747'
        )
        header.pack(pady=10)

        self.selection_frame = ttk.Frame(self.main_frame)
        self.selection_frame.pack(fill='x')

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

        self.link_frame = ttk.Frame(self.selection_frame)
        self.link_frame.pack(fill='x', pady=20)

        self.college_btn = ttk.Button(
            self.link_frame,
            text="Visit College Website",
            command=self.open_college_page,
            state="disabled"
        )
        self.college_btn.pack(pady=5)

        self.dept_btn = ttk.Button(
            self.link_frame,
            text="Visit Department Advising",
            command=self.open_dept_page,
            state="disabled"
        )
        self.dept_btn.pack(pady=5)

        instructions = ttk.Label(
            self.selection_frame,
            text="Select your college and department to access advising resources.",
            wraplength=800,
            justify="center"
        )
        instructions.pack(pady=20)

        # Scrollable Advising Section
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        def resize_scrollable_frame(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", resize_scrollable_frame)

        self.advising_frame = self.scrollable_frame

    def update_departments(self, *args):
        college = self.college_var.get()
        if college:
            self.dept_dropdown['values'] = list(self.colleges[college]['departments'].keys())
            self.dept_var.set('')
            self.college_btn.configure(state="normal")
            self.dept_btn.configure(state="disabled")
        else:
            self.dept_dropdown['values'] = []
            self.dept_var.set('')
            self.college_btn.configure(state="disabled")
            self.dept_btn.configure(state="disabled")

    def update_link(self, *args):
        dept = self.dept_var.get()
        if dept == "Electrical Engineering":
            self.display_advisor_info()
            self.dept_btn.configure(state="normal")
        else:
            self.dept_btn.configure(state="disabled")

    def display_advisor_info(self):
        for widget in self.advising_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.scrollable_frame, text="Dear Students,", font=("Helvetica", 14), justify="center").pack(pady=(10, 5), anchor="center")
        ttk.Label(self.advising_frame, text="\nIf you have submitted your ULDP (Upper-Level Degree Progression) form, it has been processed & accepted, and you would like to book an advising appointment - you've come to the right place. You have multiple options available to you for booking an appointment.", wraplength=900, justify="left").pack(pady=(10, 20))

        ttk.Label(self.advising_frame, text="WALK-IN HOURS (Updated for Spring 2025):", font=("Helvetica", 12, "bold"), justify="center").pack()
        walkin_points = [
            "Location: Main EE Office (ENB 379)",
            "Time: 10 AM- 4 PM on Mondays and Wednesdays",
            "First-come-first-serve basis",
            "Walk-in hours begin Monday, Jan 28th"
        ]
        for point in walkin_points:
            ttk.Label(self.advising_frame, text=f"• {point}", font=("Helvetica", 10, "bold"), justify="left").pack(anchor="center")

        ttk.Label(self.advising_frame, text="\n**** IMPORTANT: These days are updates for Spring - they used to be Tuesday/Thursday - please note the new days! ****", wraplength=900, justify="center").pack(pady=(20, 10))
        ttk.Label(self.advising_frame, text="ONLINE APPOINTMENTS:", font=("Helvetica", 12, "bold"), justify="center").pack()
        online_points = [
            "Book using the Calendly links below",
            "If you don't see available slots, use walk-in hours",
            "After booking, you'll receive a Microsoft Teams meeting invitation",
            "Choose ONE slot only"
        ]
        for point in online_points:
            ttk.Label(self.advising_frame, text=f"• {point}", font=("Helvetica", 10, "bold"), justify="left").pack(anchor="center")

        ttk.Label(self.advising_frame, text="\nRemember: Once confirmed, you will receive a calendar invitation for your Teams meeting on or before your scheduled appointment.", wraplength=900, justify="center").pack(pady=(10, 10))

        self.create_advisor_block("uysal.png", "Ismail Uysal", "Undergraduate Program Director", "https://calendly.com/iuysal/advising?month=2025-04")
        self.create_advisor_block("amy.png", "Amy Lyn Medicielo", "Undergraduate Program Specialist", "https://calendly.com/amedicielo/usf-advising-meeting")

    def create_advisor_block(self, img_file, name, title, link):
        frame = ttk.Frame(self.advising_frame)
        frame.pack(pady=10, fill='x')

        try:
            img = Image.open(img_file).resize((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            img_label = ttk.Label(frame, image=img_tk)
            img_label.image = img_tk
            img_label.pack(pady=5)
        except Exception as e:
            print(f"Error loading {img_file}: {e}")

        ttk.Label(frame, text=name, font=("Helvetica", 14, 'bold'), foreground="#006747").pack(pady=2)
        ttk.Label(frame, text=title, font=("Helvetica", 12), foreground="#006747").pack(pady=2)
        ttk.Button(frame, text="Schedule Appointment", command=lambda: webbrowser.open(link)).pack(pady=5)

    def open_college_page(self):
        college = self.college_var.get()
        if college in self.colleges:
            webbrowser.open(self.colleges[college]["url"])

    def open_dept_page(self):
        college = self.college_var.get()
        dept = self.dept_var.get()
        if college and dept and dept in self.colleges[college]['departments']:
            module_name = self.colleges[college]['departments'][dept]
            current_dir = os.path.dirname(os.path.abspath(__file__))
            module_path = os.path.join(current_dir, "advising", "Departments", f"{module_name}.py")
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, 'get_advising_url'):
                        webbrowser.open(module.get_advising_url())
            except Exception as e:
                print(f"Error getting department URL: {e}")

