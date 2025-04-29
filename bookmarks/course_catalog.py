import tkinter as tk
from tkinter import ttk, messagebox
from courses import courses

class CourseDetailsWindow(tk.Toplevel):
    def __init__(self, parent, course_info):
        super().__init__(parent)
        self.title("Course Details")
        self.geometry("700x600")
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        style = ttk.Style()
    
        # Background style for the window
        style.configure('Details.TFrame', background='#a9a7a3')
        
        # Scrollbar style
        style.configure('Details.Vertical.TScrollbar',
                        troughcolor='#a9a7a3',
                        background='#303434',
                        arrowcolor='#303434',
                        width=15)
        
        # Button style
        style.configure('Details.TButton',
                        background='#466069',
                        foreground='white',
                        font=('Helvetica', 10))
        style.map('Details.TButton',
                  background=[('active', '#303434')])
        
        # Set window background
        self.configure(bg='#a9a7a3')
        
        # Create text frame
        text_frame = ttk.Frame(self, style='Details.TFrame')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(text_frame, style='Details.Vertical.TScrollbar')
        scrollbar.pack(side='right', fill='y')
        
        # Create text widget with scrollbar
        self.details_text = tk.Text(
            text_frame,
            wrap='word',
            yscrollcommand=scrollbar.set,
            bg='#CAD2D8',
            fg='#303434',
            font=('Helvetica', 11),
            padx=10,
            pady=10
        )
        self.details_text.pack(fill='both', expand=True)
        scrollbar.config(command=self.details_text.yview)
        
        # Configure text tags for styling
        self.details_text.tag_configure('title', font=('Helvetica', 14, 'bold'), foreground='#006747')
        self.details_text.tag_configure('section', font=('Helvetica', 12, 'bold'), foreground='#303434')
        self.details_text.tag_configure('content', font=('Helvetica', 11), foreground='#303434')
        self.details_text.tag_configure('spacing', spacing1=5, spacing3=5) 

        # Format and display course details
        self.details_text.insert('end', f"{course_info['Class Full Name']}\n", ('title', 'spacing'))
        self.details_text.insert('end', "\n", 'spacing')  
        
        self.details_text.insert('end', "Description:\n", ('section', 'spacing'))
        self.details_text.insert('end', f"{course_info['Description']}\n", ('content', 'spacing'))
        self.details_text.insert('end', "\n", 'spacing')
        
        self.details_text.insert('end', "Prerequisites:\n", ('section', 'spacing'))
        self.details_text.insert('end', f"{parent.decode_requirement(course_info.get('Prereqs', 'N/A'))}\n", ('content', 'spacing'))
        self.details_text.insert('end', "\n", 'spacing')
        
        self.details_text.insert('end', "Corequisites:\n", ('section', 'spacing'))
        self.details_text.insert('end', f"{parent.decode_requirement(course_info.get('Coreqs', 'N/A'))}\n", ('content', 'spacing'))
        self.details_text.insert('end', "\n", 'spacing')
        
        self.details_text.insert('end', "Credit Hours:\n", ('section', 'spacing'))
        self.details_text.insert('end', f"{course_info['Credit Hours']}\n", ('content', 'spacing'))
        
        # Disable editing
        self.details_text.config(state='disabled')
        
        # Close button
        close_button = ttk.Button(
            self,
            text="Close",
            command=self.destroy,
            style='Details.TButton'
        )
        close_button.pack(pady=10)
    
class CourseCatalogPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        style = ttk.Style()

        # Controls the main content area background color (light blue/gray)
        style.configure('Catalog.TFrame', background='#a9a7a3')

        # Controls the left panel background color (gray)
        style.configure('LeftPanel.TFrame', background='#a9a7a3')

        # Controls the label frames (University, Department, Search boxes) in the left panel
        style.configure('Dark.TLabelframe', background='#a9a7a3', foreground='#303434')
        style.configure('Dark.TLabelframe.Label', background='#a9a7a3', foreground='#303434', anchor='center')

        # Controls the dropdown menus appearance (University and Department dropdowns)
        style.configure('Dark.TCombobox', fieldbackground='#CAD2D8', foreground='#303434')

        # Controls the search entry box appearance
        style.configure('Dark.TEntry', fieldbackground='#CAD2D8', foreground='#303434')

        style.configure('Header.TLabel', background='#a9a7a3', foreground='#006747', font=('Helvetica', 20, 'bold'))

        # Controls the main course list table appearance
        style.configure('Treeview', 
            background='#CAD2D8',       
            fieldbackground='#CAD2D8',  
            rowheight=30                 
        )

        # Controls the table column headers appearance
        style.configure('Treeview.Heading', 
            background='#a9a7a3',    
            foreground='#006747',       
            font=('Helvetica', 12, 'bold')
        )

        # Controls the selected row appearance in the table
        style.map('Treeview', background=[('selected', '#a9a7a3')]) 

        # IN create_widgets:
        header_frame = tk.Frame(self, bg='#a9a7a3', bd=1, relief='flat')

        # Places the header frame at the top, stretching horizontally
        header_frame.pack(fill='x')

        # Creates the "Course Catalog" label inside the header frame
        header = ttk.Label(
            header_frame,               
            text="Course Catalog",       
            style='Header.TLabel',     
            anchor='center',            
            background='#a9a7a3'    
        )

        # Places the header with padding above and below
        header.pack(pady=10)
        # Create main container
        main_container = ttk.Frame(self, style='Catalog.TFrame')
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create left panel for filters
        left_panel = ttk.Frame(main_container, style='LeftPanel.TFrame')
        left_panel.pack(side='left', fill='y', padx=5)
        
        # University selection
        university_frame = ttk.LabelFrame(left_panel, text="University", style='Dark.TLabelframe', labelanchor='n')
        university_frame.pack(fill='x', pady=5)
        
        self.university_var = tk.StringVar()
        university_combo = ttk.Combobox(
            university_frame,
            textvariable=self.university_var,
            values=list(courses.keys()),
            state="readonly",
            width=30,
            style='Dark.TCombobox'
        )
        university_combo.pack(fill='x', padx=10, pady=5)
        university_combo.bind('<<ComboboxSelected>>', self.update_departments)
        
        # Department selection
        department_frame = ttk.LabelFrame(left_panel, text="Department", style='Dark.TLabelframe', labelanchor='n')
        department_frame.pack(fill='x', pady=5)
        
        self.department_var = tk.StringVar()
        self.department_combo = ttk.Combobox(
            department_frame,
            textvariable=self.department_var,
            state="readonly",
            width=15,
            style='Dark.TCombobox'
        )
        self.department_combo.pack(fill='x', padx=10, pady=5)
        self.department_combo.bind('<<ComboboxSelected>>', self.update_courses)
        
        # Search frame
        search_frame = ttk.LabelFrame(left_panel, text="Search", style='Dark.TLabelframe', labelanchor='n')
        search_frame.pack(fill='x', pady=5)
        
        self.search_var = tk.StringVar() #bg is the search bar color
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, bg='#dcdad5', fg='#303434', relief='flat', highlightthickness=1, highlightbackground='#303434', insertbackground='#303434', justify='center')
        search_entry.pack(fill='x', padx=5, pady=5)
        search_entry.bind('<KeyRelease>', self.search_courses)
        clear_button = ttk.Button(search_frame, text="Clear Search", command=self.clear_search)
        clear_button.pack(pady=5)

        # Reset All button
        reset_button = ttk.Button(left_panel, text="Reset All", command=self.reset_all)
        reset_button.pack(fill='x', padx=5, pady=5)
        
        # Create right panel for course list
        right_panel = ttk.Frame(main_container, style='Catalog.TFrame')
        right_panel.pack(side='right', fill='both', expand=True, padx=5)
        
        # Course list
        self.course_list = ttk.Treeview(
            right_panel,
            columns=("Code", "Name", "Credits", "Prerequisites", "Corequisites"),
            show="headings",
            style='Treeview'
        )
        
        # Define headings and center them
        self.course_list.heading("Code", text="Course Code", anchor='center', command=lambda: self.sort_column("Code", False))
        self.course_list.heading("Name", text="Course Name", anchor='w', command=lambda: self.sort_column("Name", False))
        self.course_list.heading("Credits", text="Credits", anchor='center', command=lambda: self.sort_column("Credits", False))
        self.course_list.heading("Prerequisites", text="Prerequisites", anchor='w', command=lambda: self.sort_column("Prerequisites", False))
        self.course_list.heading("Corequisites", text="Corequisites", anchor='w', command=lambda: self.sort_column("Corequisites", False))
        
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

    def clear_search(self):
        self.search_var.set("")
        self.update_courses()    

    def reset_all(self):
            # Reset University to the first option
            if courses:
                self.university_var.set(list(courses.keys())[0])
                self.update_departments()  
            # Clear the search field
            self.search_var.set("")
            # Refresh the course list
            self.update_courses()

    def decode_requirement(self, req, parent_op=None, top_level=False):
        """
        Recursively deciphers a nested prerequisite/corequisite structure.
        
        If req is a dictionary with a single key "AND" or "OR", it processes the list of
        requirements under that operator. For a leaf requirement (with keys "Department",
        "Course Code", "Grade"), it returns a string in the form:
        "DEPT CODE (min grade GRADE)".
        
        Now, every OR group is enclosed in square brackets. Additionally, an AND group that is 
        nested inside an OR group is also enclosed in square brackets.
        """
        if req == 'N/A':
            return 'None'
            
        if isinstance(req, dict):
            keys = list(req.keys())
            # Check if this dict represents a group with an operator.
            if len(keys) == 1 and keys[0] in ["AND", "OR"]:
                op = keys[0]
                children = req[op]
                # Process each child; pass the current operator as parent_op.
                sub_strings = [self.decode_requirement(child, parent_op=op, top_level=False) for child in children]
                # Filter out any empty strings.
                sub_strings = [s for s in sub_strings if s]
                # Join using the operator.
                joined = f" {op} ".join(sub_strings)
                # Always enclose OR groups in brackets.
                # Also, if an AND group is nested inside an OR group, enclose it.
                if op == "OR" or (parent_op == "OR" and op == "AND"):
                    return f"[{joined}]"
                else:
                    return joined
            else:
                # It's a leaf requirement.
                dept = req.get("Department", "")
                code = req.get("Course Code", "")
                grade = req.get("Grade", "")
                if dept or code or grade:
                    if grade:
                        return f"{dept} {code} (min grade {grade})"
                    else:
                        return f"{dept} {code}"
                else:
                    return ""
        elif isinstance(req, list):
            # If req is a list, join the items.
            sub_strings = [self.decode_requirement(item, parent_op=parent_op, top_level=top_level) for item in req]
            return " ".join(sub_strings)
        else:
            return str(req)
            
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
                        prereqs = self.decode_requirement(course_info.get('Prereqs', 'N/A'))
                        coreqs = self.decode_requirement(course_info.get('Coreqs', 'N/A'))
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
                    prereqs = self.decode_requirement(course_info.get('Prereqs', 'N/A'))
                    coreqs = self.decode_requirement(course_info.get('Coreqs', 'N/A'))
                    self.course_list.insert("", "end", values=(
                        f"{department} {course_code}",
                        course_info['Class Full Name'],
                        course_info['Credit Hours'],
                        prereqs,
                        coreqs
                    ))
    
    def sort_column(self, col, reverse):
        # Get all items in the Treeview
        items = [(self.course_list.set(k, col), k) for k in self.course_list.get_children('')]
        
        # Sort items (handle numeric columns like Credits)
        if col == "Credits":
            def get_credit_value(x):
                try:
                    return int(x[0])
                except (ValueError, TypeError):
                    return 0
            items.sort(key=get_credit_value, reverse=reverse)
        else:
            items.sort(reverse=reverse)

        # Rearrange items in the Treeview
        for index, (val, k) in enumerate(items):
            self.course_list.move(k, '', index)

        # Toggle the sort direction for the next click
        self.course_list.heading(col, command=lambda: self.sort_column(col, not reverse))

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
                            search_term in self.decode_requirement(course_info.get('Prereqs', 'N/A')).lower() or
                            search_term in self.decode_requirement(course_info.get('Coreqs', 'N/A')).lower()):
                            
                            prereqs = self.decode_requirement(course_info.get('Prereqs', 'N/A'))
                            coreqs = self.decode_requirement(course_info.get('Coreqs', 'N/A'))
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
                        search_term in self.decode_requirement(course_info.get('Prereqs', 'N/A')).lower() or
                        search_term in self.decode_requirement(course_info.get('Coreqs', 'N/A')).lower()):
                        
                        prereqs = self.decode_requirement(course_info.get('Prereqs', 'N/A'))
                        coreqs = self.decode_requirement(course_info.get('Coreqs', 'N/A'))
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
