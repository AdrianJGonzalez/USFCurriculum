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
        header.grid(row=0, column=0, padx=10, pady=20, columnspan=2)

        self.main_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.main_frame.grid_columnconfigure(1, weight=1, uniform="equal")

        left_half_frame = ttk.Frame(self.main_frame)
        left_half_frame.grid(row=1, column=0, sticky="nsew")

        self.selection_frame = ttk.Frame(left_half_frame)
        self.selection_frame.pack(expand=True, fill='both')

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
            wraplength=400,
            justify="center"
        )
        instructions.pack(pady=20)

        self.right_half_frame = ttk.Frame(self.main_frame)
        self.right_half_frame.grid(row=1, column=1, sticky="nsew")
        self.advising_frame = ttk.Frame(self.right_half_frame)

    def show_advising_page(self):
        self.advising_frame.pack_forget()
        self.selection_frame.pack(expand=True, fill='both')

    def update_departments(self, *args):
        college = self.college_var.get()
        if college:
            self.dept_dropdown['values'] = list(self.colleges[college]['departments'].keys())
            self.dept_var.set('')
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
            self.display_advisor_info()
            self.dept_btn.configure(state="normal")
        else:
            self.dept_btn.configure(state="disabled")
            self.hide_advising()

    def display_advisor_info(self):
        for widget in self.advising_frame.winfo_children():
            widget.destroy()

        advisor_label = ttk.Label(
            self.advising_frame,
            text="Electrical Engineering Advisor Info",
            font=("Helvetica", 16),
            foreground="#006747"
        )
        advisor_label.pack(pady=10)

        container = ttk.Frame(self.advising_frame)
        container.pack(pady=10, expand=True, fill='both')

        left = ttk.Frame(container)
        left.pack(side='left', expand=True, fill='both', padx=10)

        right = ttk.Frame(container)
        right.pack(side='left', expand=True, fill='both', padx=10)

        self.create_advisor_block(left, "uysal.png", "Ismail Uysal", "Undergraduate Program Director", "https://calendly.com/iuysal/advising?month=2025-04")
        self.create_advisor_block(right, "amy.png", "Amy Lyn Medicielo", "Undergraduate Program Specialist", "https://calendly.com/amedicielo/usf-advising-meeting")

        self.advising_frame.pack(expand=True, fill="both")

    def create_advisor_block(self, frame, img_file, name, title, link):
        try:
            img = Image.open(img_file).resize((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            img_label = ttk.Label(frame, image=img_tk)
            img_label.image = img_tk
            img_label.pack(pady=5)
        except Exception as e:
            print(f"Error loading {img_file}: {e}")

        name_label = ttk.Label(frame, text=name, font=("Helvetica", 14, 'bold'), foreground="#006747")
        name_label.pack(pady=2)

        title_label = ttk.Label(frame, text=title, font=("Helvetica", 12), foreground="#006747")
        title_label.pack(pady=2)

        button = ttk.Button(frame, text="Schedule Appointment", command=lambda: webbrowser.open(link))
        button.pack(pady=5)

    def open_schedule_appointment(self):
        webbrowser.open("https://calendly.com/iuysal/advising?month=2025-04")

    def hide_advising(self):
        self.advising_frame.pack_forget()
        self.selection_frame.pack(expand=True, fill='both')

    def open_college_page(self):
        college = self.college_var.get()
        if college in self.colleges:
            webbrowser.open(self.colleges[college]['url'])

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

