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
        # Header
        header = ttk.Label(
            self,
            text="Academic Advising",
            font=("Helvetica", 14)
        )
        header.pack(pady=20)
        
        # Main content frame
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Create selection frame
        self.selection_frame = ttk.Frame(self.content_frame)
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
        
        # Advising content frame
        self.advising_frame = ttk.Frame(self.content_frame)
        
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
        if self.dept_var.get():
            self.dept_btn.configure(state="normal")
            self.load_advising_module()
        else:
            self.dept_btn.configure(state="disabled")
            self.hide_advising()
            
    def load_advising_module(self):
        college = self.college_var.get()
        dept = self.dept_var.get()
        
        if college and dept and college in self.colleges and dept in self.colleges[college]['departments']:
            module_name = self.colleges[college]['departments'][dept]
            
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Navigate to the departments directory
            module_path = os.path.join(current_dir, "advising", "Departments", f"{module_name}.py")
            # Get the images directory path
            images_dir = os.path.join(current_dir, "advising", "advisor_images")
            
            try:
                # Load the module
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Clear any existing widgets in the frame
                for widget in self.advising_frame.winfo_children():
                    widget.destroy()
                
                # Hide the selection frame and show the advising frame
                self.selection_frame.pack_forget()
                self.advising_frame.pack(expand=True, fill='both')
                
                # Call the module's render function with the images directory
                module.render(self.advising_frame, images_dir)
                
            except Exception as e:
                print(f"Error loading advising module: {e}")
                self.hide_advising()
                
    def hide_advising(self):
        self.advising_frame.pack_forget()
        self.selection_frame.pack(expand=True, fill='both')
        # Unbind mousewheel when hiding
        self.unbind_all("<MouseWheel>")
            
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
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'get_advising_url'):
                    webbrowser.open(module.get_advising_url())
            except Exception as e:
                print(f"Error getting department URL: {e}") 