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

        self.build_ui()

    def build_ui(self):
        # Scrollable area
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig("all", width=e.width))

        # Content header
        header = ttk.Label(
            self.scrollable_frame,
            text="Academic Advising",
            font=("Helvetica", 20, 'bold'),
            foreground='#006747'
        )
        header.pack(pady=10)

        # Dropdowns and instructions
        college_frame = ttk.LabelFrame(self.scrollable_frame, text="Select Your College")
        college_frame.pack(fill='x', pady=10, padx=20)

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

        dept_frame = ttk.LabelFrame(self.scrollable_frame, text="Select Your Department")
        dept_frame.pack(fill='x', pady=10, padx=20)

        self.dept_var = tk.StringVar()
        self.dept_var.trace('w', self.update_link)

        self.dept_dropdown = ttk.Combobox(
            dept_frame,
            textvariable=self.dept_var,
            state="readonly",
            width=30
        )
        self.dept_dropdown.pack(padx=10, pady=10)

        self.link_frame = ttk.Frame(self.scrollable_frame)
        self.link_frame.pack(fill='x', pady=10)

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
            self.scrollable_frame,
            text="Select your college and department to access advising resources.",
            wraplength=800,
            justify="center"
        )
        instructions.pack(pady=20)

        # Hidden section that only appears if EE is selected
        self.after_selection_frame = ttk.Frame(self.scrollable_frame)
        self.after_selection_frame.pack(fill='x', padx=20, pady=10)
        self.after_selection_frame.pack_forget()

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
            self.after_selection_frame.pack(fill='x', padx=20, pady=10)
            self.dept_btn.configure(state="normal")
        else:
            self.dept_btn.configure(state="disabled")
            for widget in self.after_selection_frame.winfo_children():
                widget.destroy()
            self.after_selection_frame.pack_forget()

    def display_advisor_info(self):
        for widget in self.after_selection_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.after_selection_frame, text="Dear Students,", font=("Helvetica", 14), justify="center").pack(pady=(10, 5), anchor="center")
        ttk.Label(
            self.after_selection_frame,
            text="If you have submitted your ULDP (Upper-Level Degree Progression) form, it has been processed & accepted, and you would like to book an advising appointment - you've come to the right place. You have multiple options available to you for booking an appointment.",
            wraplength=800, justify="left"
        ).pack(pady=(0, 20))

        ttk.Label(self.after_selection_frame, text="WALK-IN HOURS (Updated for Spring 2025):", font=("Helvetica", 12, "bold")).pack()
        walkin_points = [
            "Location: Main EE Office (ENB 379)",
            "Time: 10 AM- 4 PM on Mondays and Wednesdays",
            "First-come-first-serve basis",
            "Walk-in hours begin Monday, Jan 28th"
        ]
        for point in walkin_points:
            ttk.Label(self.after_selection_frame, text=f"• {point}", font=("Helvetica", 10, "bold")).pack(anchor="center")

        ttk.Label(
            self.after_selection_frame,
            text="**** IMPORTANT: These days are updates for Spring - they used to be Tuesday/Thursday - please note the new days! ****",
            wraplength=800, justify="center"
        ).pack(pady=(20, 10))

        ttk.Label(self.after_selection_frame, text="ONLINE APPOINTMENTS:", font=("Helvetica", 12, "bold")).pack()
        online_points = [
            "Book using the Calendly links below",
            "If you don't see available slots, use walk-in hours",
            "After booking, you'll receive a Microsoft Teams meeting invitation",
            "Choose ONE slot only"
        ]
        for point in online_points:
            ttk.Label(self.after_selection_frame, text=f"• {point}", font=("Helvetica", 10, "bold")).pack(anchor="center")

        ttk.Label(
            self.after_selection_frame,
            text="Remember: Once confirmed, you will receive a calendar invitation for your Teams meeting on or before your scheduled appointment.",
            wraplength=800, justify="center"
        ).pack(pady=(10, 20))

        self.create_advisor_block("uysal.png", "Ismail Uysal", "Undergraduate Program Director", "https://calendly.com/iuysal/advising?month=2025-04")
        self.create_advisor_block("amy.png", "Amy Lyn Medicielo", "Undergraduate Program Specialist", "https://calendly.com/amedicielo/usf-advising-meeting")

    def create_advisor_block(self, img_file, name, title, link):
        frame = ttk.Frame(self.after_selection_frame)
        frame.pack(pady=15)

        try:
            img = Image.open(img_file).resize((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            label = ttk.Label(frame, image=img_tk)
            label.image = img_tk
            label.pack()
        except Exception as e:
            print(f"Error loading {img_file}: {e}")

        ttk.Label(frame, text=name, font=("Helvetica", 14, 'bold'), foreground="#006747").pack()
        ttk.Label(frame, text=title, font=("Helvetica", 12), foreground="#006747").pack()
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
