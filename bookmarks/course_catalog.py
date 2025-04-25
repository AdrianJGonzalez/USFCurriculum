import tkinter as tk
from tkinter import ttk, messagebox
from courses import courses

class CourseDetailsWindow(tk.Toplevel):
    def __init__(self, parent, course_info):
        super().__init__(parent)
        self.title("Course Details")
        self.geometry("500x400")
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(self)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.details_text = tk.Text(
            text_frame,
            wrap='word',
            yscrollcommand=scrollbar.set
        )
        self.details_text.pack(fill='both', expand=True)
        scrollbar.config(command=self.details_text.yview)
        
        # Format and display course details
        details = f"Course: {course_info['Class Full Name']}\n\n"
        details += f"Description:\n{course_info['Description']}\n\n"
        details += f"Prerequisites: {self.format_prerequisites(course_info.get('Prereqs', 'N/A'))}\n"
        details += f"Corequisites: {self.format_prerequisites(course_info.get('Coreqs', 'N/A'))}\n"
        details += f"Credit Hours: {course_info['Credit Hours']}"
        
        self.details_text.insert('1.0', details)
        self.details_text.config(state='disabled')
        
        # Close button
        close_button = ttk.Button(
            self,
            text="Close",
            command=self.destroy
        )
        close_button.pack(pady=10)
    
    def format_prerequisites(self, prereqs):
        if prereqs == 'N/A':
            return 'None'
        if isinstance(prereqs, dict):
            if 'AND' in prereqs:
                return ' AND '.join(self.format_prerequisites(p) for p in prereqs['AND'])
            if 'OR' in prereqs:
                return ' OR '.join(self.format_prerequisites(p) for p in prereqs['OR'])
            return f"{prereqs['Department']} {prereqs['Course Code']} (min grade: {prereqs['Grade']})"
        return str(prereqs)

class CourseCatalogPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header = ttk.Label(
            self,
            text="Course Catalog",
            font=("Helvetica", 14)
        )
        header.pack(pady=10)
        
        # Create main container
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create left panel for filters
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side='left', fill='y', padx=5)
        
        # University selection
        university_frame = ttk.LabelFrame(left_panel, text="University")
        university_frame.pack(fill='x', pady=5)
        
        self.university_var = tk.StringVar()
        university_combo = ttk.Combobox(
            university_frame,
            textvariable=self.university_var,
            values=list(courses.keys()),
            state="readonly",
            width=30
        )
        university_combo.pack(fill='x', padx=10, pady=5)
        university_combo.bind('<<ComboboxSelected>>', self.update_departments)
        
        # Department selection
        department_frame = ttk.LabelFrame(left_panel, text="Department")
        department_frame.pack(fill='x', pady=5)
        
        self.department_var = tk.StringVar()
        self.department_combo = ttk.Combobox(
            department_frame,
            textvariable=self.department_var,
            state="readonly",
            width=15  # Half of university width
        )
        self.department_combo.pack(fill='x', padx=10, pady=5)
        self.department_combo.bind('<<ComboboxSelected>>', self.update_courses)
        
        # Search frame
        search_frame = ttk.LabelFrame(left_panel, text="Search")
        search_frame.pack(fill='x', pady=5)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(fill='x', padx=5, pady=5)
        search_entry.bind('<KeyRelease>', self.search_courses)
        
        # Create right panel for course list
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side='right', fill='both', expand=True, padx=5)
        
        # Course list
        self.course_list = ttk.Treeview(
            right_panel,
            columns=("Code", "Name", "Credits", "Prerequisites", "Corequisites"),
            show="headings"
        )
        
        # Define headings and center them
        self.course_list.heading("Code", text="Course Code", anchor='center')
        self.course_list.heading("Name", text="Course Name", anchor='w')
        self.course_list.heading("Credits", text="Credits", anchor='center')
        self.course_list.heading("Prerequisites", text="Prerequisites", anchor='w')
        self.course_list.heading("Corequisites", text="Corequisites", anchor='w')
        
        # Set column widths and alignment
        self.course_list.column("Code", width=100, anchor='center')
        self.course_list.column("Name", width=200, anchor='w')
        self.course_list.column("Credits", width=60, anchor='center')
        self.course_list.column("Prerequisites", width=200, anchor='w')
        self.course_list.column("Corequisites", width=200, anchor='w')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=self.course_list.yview)
        self.course_list.configure(yscrollcommand=scrollbar.set)
        
        self.course_list.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click event
        self.course_list.bind('<Double-1>', self.show_course_details)
        
        # Initialize with first university
        if courses:
            self.university_var.set(list(courses.keys())[0])
            self.update_departments()
    
    def update_departments(self, event=None):
        university = self.university_var.get()
        if university in courses:
            departments = ["All"] + list(courses[university].keys())
            self.department_combo['values'] = departments
            self.department_var.set("All")
            self.update_courses()
    
    def update_courses(self, event=None):
        university = self.university_var.get()
        department = self.department_var.get()
        
        # Clear existing items
        for item in self.course_list.get_children():
            self.course_list.delete(item)
        
        if university in courses:
            if department == "All":
                # Show all courses from all departments
                for dept, dept_courses in courses[university].items():
                    for course_code, course_info in dept_courses.items():
                        prereqs = self.format_prerequisites(course_info.get('Prereqs', 'N/A'))
                        coreqs = self.format_prerequisites(course_info.get('Coreqs', 'N/A'))
                        self.course_list.insert("", "end", values=(
                            f"{dept} {course_code}",
                            course_info['Class Full Name'],
                            course_info['Credit Hours'],
                            prereqs,
                            coreqs
                        ))
            elif department in courses[university]:
                # Show courses from selected department
                for course_code, course_info in courses[university][department].items():
                    prereqs = self.format_prerequisites(course_info.get('Prereqs', 'N/A'))
                    coreqs = self.format_prerequisites(course_info.get('Coreqs', 'N/A'))
                    self.course_list.insert("", "end", values=(
                        f"{department} {course_code}",
                        course_info['Class Full Name'],
                        course_info['Credit Hours'],
                        prereqs,
                        coreqs
                    ))
    
    def format_prerequisites(self, prereqs):
        if prereqs == 'N/A':
            return 'None'
        if isinstance(prereqs, dict):
            if 'AND' in prereqs:
                return ' AND '.join(self.format_prerequisites(p) for p in prereqs['AND'])
            if 'OR' in prereqs:
                return ' OR '.join(self.format_prerequisites(p) for p in prereqs['OR'])
            return f"{prereqs['Department']} {prereqs['Course Code']} (min grade: {prereqs['Grade']})"
        return str(prereqs)
    
    def search_courses(self, event=None):
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.course_list.get_children():
            self.course_list.delete(item)
        
        university = self.university_var.get()
        department = self.department_var.get()
        
        if university in courses:
            if department == "All":
                # Show all courses from all departments
                for dept, dept_courses in courses[university].items():
                    for course_code, course_info in dept_courses.items():
                        # Check if any field matches the search term
                        if (search_term in f"{dept} {course_code}".lower() or
                            search_term in course_info['Class Full Name'].lower() or
                            search_term in str(course_info['Credit Hours']).lower() or
                            search_term in self.format_prerequisites(course_info.get('Prereqs', 'N/A')).lower() or
                            search_term in self.format_prerequisites(course_info.get('Coreqs', 'N/A')).lower()):
                            
                            prereqs = self.format_prerequisites(course_info.get('Prereqs', 'N/A'))
                            coreqs = self.format_prerequisites(course_info.get('Coreqs', 'N/A'))
                            self.course_list.insert("", "end", values=(
                                f"{dept} {course_code}",
                                course_info['Class Full Name'],
                                course_info['Credit Hours'],
                                prereqs,
                                coreqs
                            ))
            elif department in courses[university]:
                # Show courses from selected department
                for course_code, course_info in courses[university][department].items():
                    # Check if any field matches the search term
                    if (search_term in f"{department} {course_code}".lower() or
                        search_term in course_info['Class Full Name'].lower() or
                        search_term in str(course_info['Credit Hours']).lower() or
                        search_term in self.format_prerequisites(course_info.get('Prereqs', 'N/A')).lower() or
                        search_term in self.format_prerequisites(course_info.get('Coreqs', 'N/A')).lower()):
                        
                        prereqs = self.format_prerequisites(course_info.get('Prereqs', 'N/A'))
                        coreqs = self.format_prerequisites(course_info.get('Coreqs', 'N/A'))
                        self.course_list.insert("", "end", values=(
                            f"{department} {course_code}",
                            course_info['Class Full Name'],
                            course_info['Credit Hours'],
                            prereqs,
                            coreqs
                        ))
    
    def show_course_details(self, event):
        selected_items = self.course_list.selection()
        if not selected_items:
            return
        
        item = selected_items[0]
        values = self.course_list.item(item)['values']
        course_code = values[0]
        department, code = course_code.split()
        
        university = self.university_var.get()
        course_info = courses[university][department][code]
        
        # Create and show the details window
        CourseDetailsWindow(self, course_info)
