import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import simpledialog
from datetime import datetime
import sys
import os
import time
import random
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Add the parent directory to the Python path to import courses
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from courses import courses  # Import the course catalog data

class CourseCatalogPopup(tk.Toplevel):
    def __init__(self, parent, semester, semester_plan_page):
        super().__init__(parent)
        self.title(f"Add Course to {semester}")
        self.semester = semester
        self.semester_plan_page = semester_plan_page
        self.course_list = None  # Initialize to None
        self.setup_ui()
        self.update_course_list()  # This will create and populate the course_list

    def setup_ui(self):
        # Configure styles
        style = ttk.Style()
        style.configure("Header.TLabel",
                       background="#a9a7a3",
                       foreground="#006747",
                       font=('Helvetica', 20, 'bold'))
        
        style.configure("Treeview",
                       background="#CAD2D8",
                       rowheight=30)
        
        style.configure("Treeview.Heading",
                       foreground="#006747",
                       font=('Helvetica', 12, 'bold'))

        # Create main container
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        header = ttk.Label(main_container, 
                          text=f"Add Course to {self.semester}",
                          style="Header.TLabel")
        header.pack(fill=tk.X, pady=(0, 10))

        # Left panel for department selection and search
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Department dropdown
        ttk.Label(left_panel, text="Department:").pack(anchor=tk.W)
        self.dept_var = tk.StringVar()
        self.dept_dropdown = ttk.Combobox(left_panel, 
                                        textvariable=self.dept_var,
                                        state="readonly")
        # Get all departments from USF courses and add "All" option
        self.dept_dropdown['values'] = ["All"] + sorted(courses["University of South Florida"].keys())
        self.dept_dropdown.set("All")  # Set default value to "All"
        self.dept_dropdown.pack(fill=tk.X, pady=(0, 10))
        self.dept_dropdown.bind('<<ComboboxSelected>>', 
                              lambda e: self.update_course_list())

        # Search box
        ttk.Label(left_panel, text="Search:").pack(anchor=tk.W)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(left_panel, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X)
        self.search_var.trace('w', lambda *args: self.update_course_list())

        # Right panel for course list
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Course list with scrollbar
        self.course_list = ttk.Treeview(right_panel,
                                      columns=("code", "name", "credits", "prereqs", "coreqs"),
                                      show="headings",
                                      selectmode="browse")
        
        # Configure columns
        self.course_list.heading("code", text="Code",
                               command=lambda: self.sort_column("code", False))
        self.course_list.heading("name", text="Name",
                               command=lambda: self.sort_column("name", False))
        self.course_list.heading("credits", text="Credits",
                               command=lambda: self.sort_column("credits", False))
        self.course_list.heading("prereqs", text="Prerequisites",
                               command=lambda: self.sort_column("prereqs", False))
        self.course_list.heading("coreqs", text="Corequisites",
                               command=lambda: self.sort_column("coreqs", False))

        # Set column widths
        self.course_list.column("code", width=100)
        self.course_list.column("name", width=200)
        self.course_list.column("credits", width=70)
        self.course_list.column("prereqs", width=150)
        self.course_list.column("coreqs", width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL,
                                command=self.course_list.yview)
        self.course_list.configure(yscrollcommand=scrollbar.set)

        # Pack course list and scrollbar
        self.course_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add course button
        add_button = ttk.Button(main_container, text="Add Course",
                              command=self.add_selected_course)
        add_button.pack(side=tk.BOTTOM, pady=10)

    def update_course_list(self):
        if not self.course_list:
            return

        # Clear existing items
        for item in self.course_list.get_children():
            self.course_list.delete(item)

        # Get selected department and search term
        selected_dept = self.dept_var.get()
        search_term = self.search_var.get().lower()

        # Get courses from USF catalog
        usf_courses = courses["University of South Florida"]
        
        if selected_dept == "All":
            # Show all courses from all departments
            for dept, dept_courses in usf_courses.items():
                for course_code, course_info in dept_courses.items():
                    # Check if course matches search term
                    if (not search_term or 
                        search_term in f"{dept} {course_code}".lower() or
                        search_term in course_info['Class Full Name'].lower() or
                        search_term in str(course_info['Credit Hours']).lower()):
                        
                        prereqs = self.decode_requirement(course_info.get('Prereqs', 'N/A'))
                        coreqs = self.decode_requirement(course_info.get('Coreqs', 'N/A'))
                        
                        self.course_list.insert("", tk.END, values=(
                            f"{dept} {course_code}",
                            course_info['Class Full Name'],
                            course_info['Credit Hours'],
                            prereqs,
                            coreqs
                        ))
        elif selected_dept in usf_courses:
            # Show courses from selected department
            dept_courses = usf_courses[selected_dept]
            for course_code, course_info in dept_courses.items():
                # Check if course matches search term
                if (not search_term or 
                    search_term in f"{selected_dept} {course_code}".lower() or
                    search_term in course_info['Class Full Name'].lower() or
                    search_term in str(course_info['Credit Hours']).lower()):
                    
                    prereqs = self.decode_requirement(course_info.get('Prereqs', 'N/A'))
                    coreqs = self.decode_requirement(course_info.get('Coreqs', 'N/A'))
                    
                    self.course_list.insert("", tk.END, values=(
                        f"{selected_dept} {course_code}",
                        course_info['Class Full Name'],
                        course_info['Credit Hours'],
                        prereqs,
                        coreqs
                    ))

    def decode_requirement(self, req, parent_op=None):
        """Decode prerequisites/corequisites requirement structure"""
        if req == 'N/A':
            return 'None'
            
        if isinstance(req, dict):
            keys = list(req.keys())
            if len(keys) == 1 and keys[0] in ["AND", "OR"]:
                op = keys[0]
                children = req[op]
                sub_strings = [self.decode_requirement(child, parent_op=op) for child in children]
                sub_strings = [s for s in sub_strings if s]
                joined = f" {op} ".join(sub_strings)
                if op == "OR" or (parent_op == "OR" and op == "AND"):
                    return f"[{joined}]"
                else:
                    return joined
            else:
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
            sub_strings = [self.decode_requirement(item, parent_op=parent_op) for item in req]
            return " ".join(sub_strings)
        else:
            return str(req)

    def add_selected_course(self):
        if not self.course_list:
            return

        selected_items = self.course_list.selection()
        if not selected_items:
            return

        # Get course information from the selected item
        selected_item = selected_items[0]  # Get first selected item
        values = self.course_list.item(selected_item)['values']
        if not values:
            return

        # Parse course code into prefix and number
        course_code = values[0]  # e.g., "EGN 3000"
        prefix, number = course_code.split()
        
        # Get course info from the catalog
        catalog_info = courses["University of South Florida"][prefix][number]
        
        # Create course info dictionary
        course_info = {
            "prefix": prefix,
            "number": number,
            "name": catalog_info['Class Full Name'],
            "credits": catalog_info['Credit Hours'],
            "is_manual": True  # Mark as manually added
        }
        
        self.semester_plan_page.add_course_to_semester(course_info, self.semester)
        self.destroy()

    def sort_column(self, col, reverse):
        if not self.course_list:
            return
            
        # Get all items in the Treeview
        items = [(self.course_list.set(k, col), k) for k in self.course_list.get_children('')]
        
        # Sort items (handle numeric columns like Credits)
        if col == "credits":
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

class CourseDetailsPopup(tk.Toplevel):
    def __init__(self, parent, course_info):
        super().__init__(parent)
        self.title("Course Details")
        self.geometry("500x400")
        self.parent = parent
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(self)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Safely get course information with defaults
        prefix = course_info.get('prefix', '').strip().upper()
        number = course_info.get('number', '').strip()
        name = course_info.get('name', '')
        credits = course_info.get('credits', 0)
        college = course_info.get('college', 'Unknown')
        grade = course_info.get('grade', '')
        is_transfer = course_info.get('is_transfer', False)
        
        # Determine text color tag based on college
        is_usf = college == "The University of South Florida"
        
        self.details_text = tk.Text(
            text_frame,
            wrap='word',
            yscrollcommand=scrollbar.set,
            background='#E6F3FF' if is_usf else 'white'
        )
        self.details_text.pack(fill='both', expand=True)
        scrollbar.config(command=self.details_text.yview)
        
        # Configure text tags for colors
        self.details_text.tag_configure('usf_text', foreground='#006747')
        self.details_text.tag_configure('normal_text', foreground='black')
        
        # Get course details from the catalog
        try:
            # Try to find the course in the catalog
            usf_courses = courses["University of South Florida"]
            catalog_info = None
            text_tag = 'usf_text' if is_usf else 'normal_text'
            
            # First try exact match
            if prefix in usf_courses and number in usf_courses[prefix]:
                catalog_info = usf_courses[prefix][number]
            else:
                # Try case-insensitive match
                for dept in usf_courses:
                    if dept.upper() == prefix:
                        for num in usf_courses[dept]:
                            if num == number:  # Try exact number match first
                                catalog_info = usf_courses[dept][num]
                                prefix = dept  # Use the correct case from catalog
                                number = num
                                break
                            elif num.upper() == number.upper():  # Then try case-insensitive
                                catalog_info = usf_courses[dept][num]
                                prefix = dept  # Use the correct case from catalog
                                number = num
                                break
                        if catalog_info:
                            break
            
            # Format and display course details
            self.details_text.insert('end', f"Course: {prefix} {number}\n\n", text_tag)
            self.details_text.insert('end', f"Name: {name}\n\n", text_tag)
            self.details_text.insert('end', f"Credits: {credits}\n\n", text_tag)
            
            if grade:
                self.details_text.insert('end', f"Grade: {grade}\n\n", text_tag)
            
            if is_transfer:
                self.details_text.insert('end', f"Transfer Course from: {college}\n\n", text_tag)
            
            if catalog_info:
                self.details_text.insert('end', "Description:\n", 'normal_text')
                self.details_text.insert('end', f"{catalog_info.get('Description', 'No description available.')}\n\n", text_tag)
                
                prereqs = catalog_info.get('Prereqs', 'N/A')
                if isinstance(prereqs, dict):
                    if 'AND' in prereqs:
                        prereq_text = self.format_requirement_list(prereqs['AND'], 'AND')
                    elif 'OR' in prereqs:
                        prereq_text = self.format_requirement_list(prereqs['OR'], 'OR')
                    else:
                        prereq_text = str(prereqs)
                else:
                    prereq_text = str(prereqs)
                
                self.details_text.insert('end', "Prerequisites: ", 'normal_text')
                self.details_text.insert('end', f"{prereq_text}\n\n", text_tag)
                
                coreqs = catalog_info.get('Coreqs', 'N/A')
                if isinstance(coreqs, dict):
                    if 'AND' in coreqs:
                        coreq_text = self.format_requirement_list(coreqs['AND'], 'AND')
                    elif 'OR' in coreqs:
                        coreq_text = self.format_requirement_list(coreqs['OR'], 'OR')
                    else:
                        coreq_text = str(coreqs)
                else:
                    coreq_text = str(coreqs)
                
                self.details_text.insert('end', "Corequisites: ", 'normal_text')
                self.details_text.insert('end', coreq_text, text_tag)
            else:
                self.details_text.insert('end', "Additional details not available in the course catalog.\n", 'normal_text')
                self.details_text.insert('end', "(This could be due to course code changes or catalog updates)\n\n", 'normal_text')
            
        except Exception as e:
            text_tag = 'usf_text' if is_usf else 'normal_text'
            self.details_text.insert('end', f"Course: {prefix} {number}\n\n", text_tag)
            self.details_text.insert('end', f"Name: {name}\n\n", text_tag)
            self.details_text.insert('end', f"Credits: {credits}\n\n", text_tag)
            if is_transfer:
                self.details_text.insert('end', f"Transfer Course from: {college}\n\n", text_tag)
            self.details_text.insert('end', "Additional details not available in the course catalog.\n", 'normal_text')
            self.details_text.insert('end', f"Error: {str(e)}\n\n", 'normal_text')
        
        self.details_text.config(state='disabled')
        
        # Close button
        close_button = ttk.Button(
            self,
            text="Close",
            command=self.on_close
        )
        close_button.pack(pady=10)

        # Bind window close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Clear any drag state in the parent
        if hasattr(self.parent, 'drag_start_pos'):
            self.parent.drag_start_pos = None
        if hasattr(self.parent, 'drag_start_time'):
            self.parent.drag_start_time = None
        if hasattr(self.parent, 'dragged_items'):
            self.parent.dragged_items = None
        if hasattr(self.parent, 'dragged_tags'):
            self.parent.dragged_tags = None
        if hasattr(self.parent, 'original_positions'):
            self.parent.original_positions = None
        if hasattr(self.parent, 'drag_shadow'):
            if self.parent.drag_shadow:
                self.parent.canvas.delete(self.parent.drag_shadow)
            self.parent.drag_shadow = None
        if hasattr(self.parent, 'highlighted_semester'):
            if self.parent.highlighted_semester:
                self.parent.canvas.itemconfig(f"semester_{self.parent.highlighted_semester}", fill='lightblue')
            self.parent.highlighted_semester = None
        
        # Destroy the window
        self.destroy()

    def format_requirement_list(self, req_list, operator='AND'):
        """Helper function to format a list of requirements"""
        if not req_list:
            return ''
        
        formatted = []
        for req in req_list:
            if isinstance(req, dict):
                if 'OR' in req:
                    # Handle nested OR condition
                    nested = self.format_requirement_list(req['OR'], 'OR')
                    if nested:
                        formatted.append(f"({nested})")
                elif 'Department' in req:
                    # Handle individual course requirement
                    dept = req.get('Department', '')
                    code = req.get('Course Code', '')
                    grade = req.get('Grade', '')
                    if dept and code:
                        formatted.append(f"{dept} {code} (Grade: {grade})")
            elif isinstance(req, str):
                formatted.append(req)
        
        return f" {operator} ".join(formatted)

class SemesterPlanPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.courses = {}
        self.column_width = 220
        self.box_padding = 20
        self.course_height = 40
        self.drag_threshold = 5  # pixels to move before starting drag
        self.drag_timer = None
        self.drag_start_time = None
        self.drag_start_pos = None
        self.dragged_items = None
        self.dragged_tags = None
        self.original_positions = None
        self.drag_shadow = None
        self.highlighted_semester = None
        self.example_semesters = []  # Track example semesters
        self.transcript_semesters = []  # Track transcript-loaded semesters
        self.create_widgets()
        self.load_plan()  # Load saved plan on startup
        self.winfo_toplevel().protocol("WM_DELETE_WINDOW", self.reset_on_close)

    def create_widgets(self):
        # Configure styles
        style = ttk.Style()
        style.configure('Transcript.Treeview', 
                       background='#dcdad5', 
                       fieldbackground='#dcdad5')
        style.configure('Transcript.Treeview.Heading', 
                       background='#dcdad5', 
                       foreground='#303434')
        style.configure('TranscriptFrame.TFrame', 
                       background='#dcdad5')
        style.configure('TranscriptLabel.TLabel',
                       background='#dcdad5')
        style.configure('Transcript.TLabelframe', 
                       background='#dcdad5')
        style.configure('Transcript.TLabelframe.Label', 
                       background='#dcdad5')

        # Set main frame background
        self.configure(style='TranscriptFrame.TFrame')
        
        # Header
        header = ttk.Label(
            self,
            text="Semester Plan",
            font=('Helvetica', 20, 'bold'),
            foreground='#006747',
            style='TranscriptLabel.TLabel'
        )
        header.pack(pady=10)
        
        # Control buttons frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Semester selection frame (left side)
        semester_frame = ttk.Frame(control_frame)
        semester_frame.pack(side='left', padx=5)
        
        # Semester type dropdown
        self.semester_type = ttk.Combobox(
            semester_frame,
            values=["Fall", "Spring", "Summer"],
            state="readonly",
            width=10
        )
        self.semester_type.set("Fall")
        self.semester_type.pack(side='left', padx=5)
        
        # Year entry
        self.year_entry = ttk.Entry(semester_frame, width=6)
        self.year_entry.pack(side='left', padx=5)
        self.year_entry.insert(0, "")
        
        # Add semester button
        add_semester_btn = ttk.Button(
            semester_frame,
            text="Add Semester",
            command=self.add_semester
        )
        add_semester_btn.pack(side='left', padx=5)
        
        # Clear semester plan button
        clear_btn = ttk.Button(
            control_frame,
            text="Clear Plan",
            command=self.clear_semester_plan
        )
        clear_btn.pack(side='left', padx=5)
        
        # Save plan button
        save_btn = ttk.Button(
            control_frame,
            text="Save Plan",
            command=self.save_plan
        )
        save_btn.pack(side='left', padx=5)
        
        # Example button (right side)
        example_btn = ttk.Button(
            control_frame,
            text="Example",
            command=self.load_example
        )
        example_btn.pack(side='right', padx=5)
        
        # Clear example button (right side)
        clear_example_btn = ttk.Button(
            control_frame,
            text="Clear Example",
            command=self.clear_example
        )
        clear_example_btn.pack(side='right', padx=5)
        
        # Create main canvas with scrollbars
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg='#cad2d8',
            scrollregion=(0, 0, 2000, 2000)
        )
        
        # Add scrollbars
        h_scroll = ttk.Scrollbar(
            self.canvas_frame,
            orient='horizontal',
            command=self.canvas.xview
        )
        v_scroll = ttk.Scrollbar(
            self.canvas_frame,
            orient='vertical',
            command=self.canvas.yview
        )
        
        self.canvas.configure(
            xscrollcommand=h_scroll.set,
            yscrollcommand=v_scroll.set
        )
        
        # Grid layout for canvas and scrollbars
        self.canvas.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Initialize semester columns
        self.semester_columns = []
        self.box_height = 80  # Height for course boxes
        self.header_height = 40  # Height for semester headers
        
        # Bind mouse wheel for horizontal scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Bind drag and drop events
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        
        # Add double-click binding for course details
        self.canvas.tag_bind('course_box', '<Double-Button-1>', self.show_course_details)

    def _on_mousewheel(self, event):
        # Handle mouse wheel scrolling for horizontal scroll
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def add_semester(self):
        semester_type = self.semester_type.get()
        year = self.year_entry.get()
        
        if not year.isdigit():
            messagebox.showerror("Error", "Please enter a valid year!")
            return
            
        semester = f"{semester_type} {year}"
        
        if semester in self.courses:
            messagebox.showerror("Error", "This semester already exists!")
            return
            
        # Create new semester column
        self.courses[semester] = []
        self.update_flowchart()

    def load_example(self):
        """Load an example semester plan matching the provided flowchart, starting from Fall 2025"""
        # Clear existing example semesters first
        self.clear_example()
        
        # Define the semesters based on the flowchart (Fall 2025 to Spring 2029)
        example_semesters = [
            "Fall 2025", "Spring 2026",  # Year 1
            "Fall 2026", "Spring 2027", "Summer 2027",  # Year 2
            "Fall 2027", "Spring 2028",  # Year 3
            "Fall 2028", "Spring 2029"  # Year 4
        ]
        self.example_semesters.extend(example_semesters)
        
        # Initialize example courses dictionary
        example_courses = {semester: [] for semester in example_semesters}
        
        # Get the USF course catalog
        usf_courses = courses["University of South Florida"]
        
        # Helper function to add a course to a semester
        def add_course_to_semester(semester, dept, course_code, placeholder_name=None, placeholder_credits=None):
            if dept in usf_courses and course_code in usf_courses[dept]:
                course_info = usf_courses[dept][course_code]
                course_data = {
                    "prefix": dept,
                    "number": course_code,
                    "name": course_info['Class Full Name'],
                    "credits": course_info['Credit Hours'],
                    "is_manual": True,
                    "college": "The University of South Florida",
                    "is_transfer": False
                }
            else:
                # Placeholder for courses not found in catalog (e.g., electives)
                course_data = {
                    "prefix": dept,
                    "number": course_code,
                    "name": placeholder_name or f"{dept} {course_code}",
                    "credits": placeholder_credits or 3,  # Default to 3 credits if not specified
                    "is_manual": True,
                    "college": "The University of South Florida",
                    "is_transfer": False
                }
            example_courses[semester].append(course_data)
        
        # Year 1: Fall 2025 (14 hrs)
        add_course_to_semester("Fall 2025", "EGN", "3000", "Foundations of Engineering")
        add_course_to_semester("Fall 2025", "MAC", "2281", "Calculus I")
        add_course_to_semester("Fall 2025", "EGN", "3000L", "Foundations of Engineering Lab (Creative Thinking)")
        add_course_to_semester("Fall 2025", "CHM", "2045", "Chemistry for Engineering")
        add_course_to_semester("Fall 2025", "CHM", "2045L", "Chemistry for Engineering Lab")
        add_course_to_semester("Fall 2025", "ENC", "1101", "Composition I")
        
        # Year 1: Spring 2026 (14 hrs)
        add_course_to_semester("Spring 2026", "MAC", "2282", "Calculus II")
        add_course_to_semester("Spring 2026", "PHY", "2048", "General Physics I")
        add_course_to_semester("Spring 2026", "EEE", "3394", "Electrical Science I")
        add_course_to_semester("Spring 2026", "CHM", "2045L", "Chemistry for Engineering Lab")  # Repeated as in flowchart
        add_course_to_semester("Spring 2026", "PHY", "2048L", "General Physics I Lab")
        add_course_to_semester("Spring 2026", "ENC", "1102", "Composition II")
        
        # Year 2: Fall 2026 (15 hrs)
        add_course_to_semester("Fall 2026", "MAC", "2283", "Calculus III")
        add_course_to_semester("Fall 2026", "EGN", "3433", "Modeling Analysis for Engineering")
        add_course_to_semester("Fall 2026", "EGN", "3373", "Electrical Systems I")
        add_course_to_semester("Fall 2026", "EGN", "3420", "Engineering Analysis")
        add_course_to_semester("Fall 2026", "EEL", "3705", "Fundamentals of Digital Circuits")
        
        # Year 2: Spring 2027 (14 hrs)
        add_course_to_semester("Spring 2027", "EGN", "3443", "Probability & Statistics for Engineering (Info & Data Lit)")
        add_course_to_semester("Spring 2027", "ENC", "3246", "Communication for Engineering")
        add_course_to_semester("Spring 2027", "EEL", "3472C", "Electrical Science II - Electromagnetic")
        add_course_to_semester("Spring 2027", "EEL", "2161", "EE Computer Methods")
        add_course_to_semester("Spring 2027", "EEL", "3705L", "Fundamentals of Digital Circuits Lab")
        
        # Year 2: Summer 2027 (9 hrs)
        add_course_to_semester("Summer 2027", "EGN", "3615", "Engineering Economics (Human & Cultural Diversity)")
        add_course_to_semester("Summer 2027", "HUM", "GENED", "St. GenEd Core Humanities Elective", 3)
        add_course_to_semester("Summer 2027", "SOC", "GENED", "St. GenEd Core Social Science Elective", 3)
        
        # Year 3: Fall 2027 (15 hrs)
        add_course_to_semester("Fall 2027", "EEL", "3115L", "Lab I (Circuits)")
        add_course_to_semester("Fall 2027", "EGN", "3374", "Electrical Systems II")
        add_course_to_semester("Fall 2027", "EEL", "3163C", "Computer Tools")
        add_course_to_semester("Fall 2027", "EGS", "3070", "Professional Formation of Engineering I")
        add_course_to_semester("Fall 2027", "EEE", "CORE", "EE Core Elective", 3)
        
        # Year 3: Spring 2028 (15 hrs)
        add_course_to_semester("Spring 2028", "EEL", "4906", "EE Design I")
        add_course_to_semester("Spring 2028", "EEL", "4102", "Signals & Systems")
        add_course_to_semester("Spring 2028", "EEL", "4835", "Programming Design")
        add_course_to_semester("Spring 2028", "EGS", "3071", "Professional Formation of Engineering II")
        add_course_to_semester("Spring 2028", "EEE", "CORE", "EE Core Elective", 3)
        
        # Year 4: Fall 2028 (16 hrs)
        add_course_to_semester("Fall 2028", "EEL", "4914", "EE Design I (Senior Standing)")
        add_course_to_semester("Fall 2028", "EEE", "DESIGN", "EE Design I", 3)
        add_course_to_semester("Fall 2028", "EEE", "TRACK", "EE Track Elective", 3)
        add_course_to_semester("Fall 2028", "EEE", "TRACK", "EE Track Elective", 3)
        add_course_to_semester("Fall 2028", "EEE", "TECH", "EE Technical Elective", 3)
        add_course_to_semester("Fall 2028", "EGS", "3072", "Professional Formation of Engineering III")
        
        # Year 4: Spring 2029 (16 hrs)
        add_course_to_semester("Spring 2029", "EEL", "4914", "EE Design II (Senior Standing)")  # Repeated as in flowchart
        add_course_to_semester("Spring 2029", "EEE", "DESIGN", "EE Design II", 3)
        add_course_to_semester("Spring 2029", "EEE", "TRACK", "EE Track Elective", 3)
        add_course_to_semester("Spring 2029", "EEE", "TRACK", "EE Track Elective", 3)
        add_course_to_semester("Spring 2029", "EEE", "TECH", "EE Technical Elective", 3)
        add_course_to_semester("Spring 2029", "EEE", "TECHLAB", "EE Technical Elective Lab", 1)
        
        # Add the example semesters and courses to self.courses
        for semester in example_semesters:
            self.courses[semester] = example_courses[semester]
        
        # Update the flowchart
        self.update_flowchart()

    def clear_example(self):
        """Clear only the example semesters"""
        if not self.example_semesters:
            return
            
        # Remove example semesters from the courses dictionary
        for semester in self.example_semesters:
            if semester in self.courses:
                del self.courses[semester]
        
        # Clear the example semesters list
        self.example_semesters = []
        
        # Update the flowchart
        self.update_flowchart()

    def clear_transcript(self):
        """Clear only the transcript-loaded semesters"""
        if not self.transcript_semesters:
            return
        
        for semester in self.transcript_semesters:
            if semester in self.courses:
                del self.courses[semester]
        
        self.transcript_semesters = []
        self.update_flowchart()

    def add_course_dialog(self):
        if not self.courses:
            messagebox.showerror("Error", "Please add a semester first!")
            return
            
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Add Course")
        dialog.geometry("300x200")
        
        # Course details frame
        details_frame = ttk.Frame(dialog)
        details_frame.pack(padx=10, pady=10)
        
        # Course prefix
        ttk.Label(details_frame, text="Prefix:").grid(row=0, column=0, sticky='w')
        prefix_entry = ttk.Entry(details_frame)
        prefix_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Course number
        ttk.Label(details_frame, text="Number:").grid(row=1, column=0, sticky='w')
        number_entry = ttk.Entry(details_frame)
        number_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Course name
        ttk.Label(details_frame, text="Name:").grid(row=2, column=0, sticky='w')
        name_entry = ttk.Entry(details_frame)
        name_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Credits
        ttk.Label(details_frame, text="Credits:").grid(row=3, column=0, sticky='w')
        credits_entry = ttk.Entry(details_frame)
        credits_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Semester selection
        ttk.Label(details_frame, text="Semester:").grid(row=4, column=0, sticky='w')
        semester_var = tk.StringVar()
        semester_dropdown = ttk.Combobox(
            details_frame,
            textvariable=semester_var,
            values=self.get_sorted_semesters(),
            state="readonly"
        )
        semester_dropdown.grid(row=4, column=1, padx=5, pady=5)
        semester_dropdown.set(self.get_sorted_semesters()[0] if self.courses else "")
        
        def add_course():
            course_info = {
                "prefix": prefix_entry.get(),
                "number": number_entry.get(),
                "name": name_entry.get(),
                "credits": credits_entry.get()
            }
            self.add_course(semester_var.get(), course_info)
            dialog.destroy()
            
        # Add button
        ttk.Button(
            dialog,
            text="Add",
            command=add_course
        ).pack(pady=10)
        
    def start_drag(self, event):
        # Cancel any existing drag timer
        if self.drag_timer:
            self.after_cancel(self.drag_timer)
            self.drag_timer = None

        # Store initial position and start timer
        self.drag_start_pos = (event.x, event.y)
        self.drag_start_time = time.time()
        self.drag_timer = self.after(200, self.check_drag_start, event)  # 200ms delay

    def check_drag_start(self, event):
        if not hasattr(self, 'drag_start_pos') or not self.drag_start_pos:
            return
            
        # Check if mouse is still at roughly the same position
        current_pos = (event.x, event.y)
        dx = abs(current_pos[0] - self.drag_start_pos[0])
        dy = abs(current_pos[1] - self.drag_start_pos[1])
        
        if dx < self.drag_threshold and dy < self.drag_threshold:
            # Find the clicked item
            x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            items = self.canvas.find_closest(x, y)

            if items:
                tags = self.canvas.gettags(items[0])
                # Only start drag if clicking on course box, not delete button or semester header
                if ('course_box' in tags and 
                    not any(tag.startswith('delete_') for tag in tags) and
                    not any(tag.startswith('semester_') for tag in tags)):
                    # Find the course tag (format: semester_index)
                    course_tag = next((tag for tag in tags if '_' in tag and not any(tag.startswith(prefix) for prefix in ['delete_', 'course_', 'semester_'])), '')
                    if course_tag:
                        self.dragged_course = course_tag
                        self.dragged_items = self.canvas.find_withtag(course_tag)
                        self.dragged_tags = tags

                        # Store original positions and dimensions
                        self.original_positions = []
                        for item in self.dragged_items:
                            bbox = self.canvas.bbox(item)
                            if bbox:
                                self.original_positions.append({
                                    'item': item,
                                    'x': bbox[0],
                                    'y': bbox[1],
                                    'width': bbox[2] - bbox[0],
                                    'height': bbox[3] - bbox[1]
                                })

                        # Create shadow effect
                        if self.original_positions:
                            first_item = self.original_positions[0]
                            self.drag_shadow = self.canvas.create_rectangle(
                                first_item['x'], first_item['y'],
                                first_item['x'] + first_item['width'],
                                first_item['y'] + first_item['height'],
                                fill='gray',
                                outline='black',
                                stipple='gray50',
                                tags='shadow'
                            )
                            self.canvas.tag_lower(self.drag_shadow)

                            # Raise all dragged items above the shadow but below semester headers
                            for pos in self.original_positions:
                                self.canvas.tag_raise(pos['item'])
                                # Ensure semester headers stay on top
                                for semester in self.courses.keys():
                                    self.canvas.tag_raise(f"semester_{semester}")

    def drag(self, event):
        if not hasattr(self, 'dragged_items') or not self.dragged_items:
            return
            
        # Move the dragged items and shadow
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        
        # Calculate offset from original position
        if self.original_positions:
            first_item = self.original_positions[0]
            # Calculate center offset
            center_x = first_item['x'] + first_item['width']/2
            center_y = first_item['y'] + first_item['height']/2
            offset_x = x - center_x
            offset_y = y - center_y
            
            # Update positions of all dragged items
            for pos in self.original_positions:
                if self.canvas.type(pos['item']) == 'rectangle':
                    self.canvas.coords(
                        pos['item'],
                        pos['x'] + offset_x,
                        pos['y'] + offset_y,
                        pos['x'] + offset_x + pos['width'],
                        pos['y'] + offset_y + pos['height']
                    )
                else:  # text item
                    self.canvas.coords(
                        pos['item'],
                        pos['x'] + offset_x + pos['width']/2,
                        pos['y'] + offset_y + pos['height']/2
                    )
            
            # Update shadow position
            if self.drag_shadow:
                self.canvas.coords(
                    self.drag_shadow,
                    x - first_item['width']/2,
                    y - first_item['height']/2,
                    x + first_item['width']/2,
                    y + first_item['height']/2
                )
        
        # Check for semester highlight
        sorted_semesters = self.get_sorted_semesters()
        for i, semester in enumerate(sorted_semesters):
            column_x = i * (self.column_width + self.box_padding) + self.box_padding
            if column_x <= x <= column_x + self.column_width:
                if self.highlighted_semester != semester:
                    # Remove old highlight
                    if self.highlighted_semester:
                        self.canvas.itemconfig(f"semester_{self.highlighted_semester}", fill='lightblue')
                    
                    # Add new highlight
                    self.highlighted_semester = semester
                    self.canvas.itemconfig(f"semester_{semester}", fill='lightgreen')
                break
        else:
            # Remove highlight if not over any semester
            if self.highlighted_semester:
                self.canvas.itemconfig(f"semester_{self.highlighted_semester}", fill='lightblue')
                self.highlighted_semester = None

    def end_drag(self, event):
        # Cancel any pending drag timer
        if self.drag_timer:
            self.after_cancel(self.drag_timer)
            self.drag_timer = None
            
        # Reset drag state
        self.drag_start_pos = None
        self.drag_start_time = None
        
        if hasattr(self, 'dragged_items') and self.dragged_items and hasattr(self, 'dragged_tags') and self.dragged_tags:
            # Get the original semester and course index
            original_semester = None
            course_index = None
            for tag in self.dragged_tags:
                if '_' in tag and not any(tag.startswith(prefix) for prefix in ['delete_', 'course_']):
                    try:
                        original_semester, course_idx = tag.split('_')
                        course_index = int(course_idx)
                        break
                    except (ValueError, IndexError):
                        continue
            
            # Find the new semester column
            x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            sorted_semesters = self.get_sorted_semesters()
            
            # Track if we need to update the flowchart
            need_update = False
            move_course = False
            dropped_in_valid_column = False
            target_semester = None
            
            # Find which semester column the course was dropped in
            for i, semester in enumerate(sorted_semesters):
                column_x = i * (self.column_width + self.box_padding) + self.box_padding
                if column_x <= x <= column_x + self.column_width:
                    dropped_in_valid_column = True
                    target_semester = semester
                    break
            
            # Handle the drop
            if dropped_in_valid_column and target_semester and original_semester and course_index is not None:
                if original_semester != target_semester:
                    # Get the course info
                    course = self.courses[original_semester][course_index]
                    college = course.get('college', '')
                    is_usf = college == "The University of South Florida"
                    
                    # Show warning based on course type
                    warning_message = None
                    if is_usf:
                        warning_message = "This is a USF course. Moving it to a different semester might affect your academic progress. Are you sure you want to move it?"
                    
                    # Only move if user confirms or if no warning needed
                    if warning_message:
                        if messagebox.askyesno("Warning", warning_message):
                            move_course = True
                    else:
                        move_course = True
                        
                    if move_course:
                        # Move course to new semester
                        course = self.courses[original_semester].pop(course_index)
                        self.courses[target_semester].append(course)
                        need_update = True
            
            # Clean up drag shadow and highlight
            if self.drag_shadow:
                self.canvas.delete(self.drag_shadow)
                self.drag_shadow = None
            if self.highlighted_semester:
                self.canvas.itemconfig(f"semester_{self.highlighted_semester}", fill='lightblue')
                self.highlighted_semester = None
            
            # If we're not moving the course, return it to its original position
            if not move_course:
                self.return_items_to_original_position()
                # Ensure semester headers are visible and on top
                for semester in self.courses.keys():
                    # Recreate semester header if needed
                    i = sorted_semesters.index(semester)
                    x = i * (self.column_width + self.box_padding) + self.box_padding
                    
                    # Check for both box and text
                    header_box = self.canvas.find_withtag(f"semester_{semester}_box")
                    header_text = self.canvas.find_withtag(f"semester_{semester}_text")
                    
                    if not header_box:
                        # Recreate header box
                        self.canvas.create_rectangle(
                            x, self.box_padding,
                            x + self.column_width, self.box_padding + self.header_height,
                            fill='lightblue',
                            outline='black',
                            tags=('semester_header', f'semester_{semester}_box')
                        )
                    
                    if not header_text:
                        # Recreate header text
                        self.canvas.create_text(
                            x + self.column_width/2,
                            self.box_padding + self.header_height/2,
                            text=semester,
                            font=('Helvetica', 12, 'bold'),
                            tags=('semester_header', f'semester_{semester}_text')
                        )
                    
                    # Ensure headers are on top
                    self.canvas.tag_raise(f"semester_{semester}_box")
                    self.canvas.tag_raise(f"semester_{semester}_text")
            
            # Clean up drag state
            self.dragged_items = None
            self.dragged_tags = None
            self.original_positions = None
            
            # Update the flowchart if needed
            if need_update:
                self.update_flowchart()

    def return_items_to_original_position(self):
        """Return dragged items to their original positions"""
        if not self.original_positions:
            return
            
        for pos in self.original_positions:
            if not self.canvas.winfo_exists():
                return
                
            try:
                if self.canvas.type(pos['item']) == 'rectangle':
                    self.canvas.coords(
                        pos['item'],
                        pos['x'],
                        pos['y'],
                        pos['x'] + pos['width'],
                        pos['y'] + pos['height']
                    )
                else:  # text item
                    self.canvas.coords(
                        pos['item'],
                        pos['x'] + pos['width']/2,
                        pos['y'] + pos['height']/2
                    )
            except tk.TclError:
                # Item might have been deleted
                continue

    def clear_semester_plan(self):
        if messagebox.askyesno("Clear Plan", "Are you sure you want to clear the entire semester plan?"):
            self.courses = {}
            self.example_semesters = []  # Clear example semesters tracking as well
            self.transcript_semesters = [] #Clear transcript semesters tracking
            self.update_flowchart()

    def add_course(self, semester, course_info):
        if semester not in self.courses:
            self.courses[semester] = []
            
        # Mark the course as manually added
        course_info['is_manual'] = True
        self.courses[semester].append(course_info)
        self.update_flowchart()
        
    def remove_course(self, semester, course_index):
        if semester in self.courses and 0 <= course_index < len(self.courses[semester]):
            course = self.courses[semester][course_index]
            course_name = f"{course['prefix']} {course['number']}: {course['name']}"
            
            if messagebox.askyesno("Delete Course", 
                                 f"Are you sure you want to delete this course?\n\n{course_name}",
                                 icon='warning'):
                del self.courses[semester][course_index]
                self.update_flowchart()
            
    def get_semester_order(self, semester):
        """Convert semester name to a sortable value"""
        parts = semester.split()
        if len(parts) != 2:
            return (0, 0)  # Default to start if format is wrong
            
        season, year = parts
        year = int(year)
        
        # Assign season order (Spring = 1, Summer = 2, Fall = 3)
        season_order = {
            "Spring": 1,
            "Summer": 2,
            "Fall": 3
        }.get(season, 0)
        
        return (year, season_order)
        
    def get_sorted_semesters(self):
        """Return semesters sorted chronologically"""
        return sorted(
            self.courses.keys(),
            key=self.get_semester_order
        )
        
    def update_flowchart(self):
        # Clear canvas
        self.canvas.delete("all")
        
        # First, draw all semester headers
        for i, semester in enumerate(self.get_sorted_semesters()):
            x = i * (self.column_width + self.box_padding) + self.box_padding
            
            # Draw semester header with new height
            header_box = self.canvas.create_rectangle(
                x, self.box_padding,
                x + self.column_width, self.box_padding + self.header_height,
                fill='lightblue',
                outline='black',
                tags=('semester_header', f'semester_{semester}_box')
            )
            header_text = self.canvas.create_text(
                x + self.column_width/2,
                self.box_padding + self.header_height/2,
                text=semester,
                font=('Helvetica', 12, 'bold'),
                tags=('semester_header', f'semester_{semester}_text')
            )
            
            # Draw course boxes starting immediately after header
            for j, course in enumerate(self.courses[semester]):
                y = self.box_padding + self.header_height + (j * (self.box_height + self.box_padding))
                
                # Get course info
                college = course.get('college', '')
                is_transfer = course.get('is_transfer', True)  # Default to True for safety
                is_manual = course.get('is_manual', False)
                is_usf = college == "The University of South Florida"
                
                # Determine box color based on course type
                if is_usf:
                    box_fill = '#80B0A6'  # USF mint green for background
                    text_color = 'black'  # Black text for better contrast
                elif is_transfer:
                    box_fill = 'lightyellow'  # Light yellow for transfer courses
                    text_color = 'black'
                elif is_manual:
                    box_fill = '#E6F3FF'  # Light blue for manually added courses
                    text_color = 'black'
                else:
                    box_fill = 'white'  # White for regular courses
                    text_color = 'black'
                
                # Create course box group tag for all elements of this course
                course_group_tag = f'{semester}_{j}'
                
                # Main course box
                box = self.canvas.create_rectangle(
                    x, y,
                    x + self.column_width, y + self.box_height,
                    fill=box_fill,
                    outline='black',
                    width=1,
                    tags=('course_box', course_group_tag)
                )
                
                # Course text with wrapping
                course_text = (
                    f"{course['prefix']} {course['number']}\n"
                    f"{course['name']}\n"
                    f"Credits: {course.get('credits', 'N/A')}"
                )
                
                # Add transfer label if applicable
                if is_transfer:
                    # Abbreviate The University of South Florida to USF
                    display_college = "USF" if is_usf else college
                    course_text += f"\nTransfer: {display_college}"
                elif is_manual:
                    course_text += "\nManually Added"
                
                # Adjusted font size and added wrapping
                text_item = self.canvas.create_text(
                    x + self.column_width/2,
                    y + self.box_height/2,
                    text=course_text,
                    font=('Helvetica', 8),
                    justify='center',
                    fill=text_color,
                    width=self.column_width - 10,
                    tags=('course_box', course_group_tag)
                )
                
                # Delete button - create as a group
                delete_btn_size = 20
                delete_btn_x = x + self.column_width - delete_btn_size
                delete_btn_y = y
                
                # Delete button background
                delete_btn = self.canvas.create_rectangle(
                    delete_btn_x, delete_btn_y,
                    delete_btn_x + delete_btn_size, delete_btn_y + delete_btn_size,
                    fill='red',
                    outline='black',
                    tags=('delete_btn', f'delete_{semester}_{j}', course_group_tag)
                )
                
                # Delete button X
                self.canvas.create_text(
                    delete_btn_x + delete_btn_size/2,
                    delete_btn_y + delete_btn_size/2,
                    text='X',
                    fill='white',
                    font=('Helvetica', 8, 'bold'),
                    tags=('delete_btn', f'delete_{semester}_{j}', course_group_tag)
                )
                
                # Bind delete button with specific tag
                self.canvas.tag_bind(
                    f'delete_{semester}_{j}',
                    '<Button-1>',
                    lambda e, s=semester, idx=j: self.remove_course(s, idx)
                )
            
            # Add "Add Course" button below the last course
            button_y = self.box_padding + self.header_height + (len(self.courses[semester]) * (self.box_height + self.box_padding))
            button = self.canvas.create_rectangle(
                x, button_y,
                x + self.column_width, button_y + 30,
                fill='lightgreen',
                outline='black',
                tags=('add_button', semester)
            )
            self.canvas.create_text(
                x + self.column_width/2,
                button_y + 15,
                text="Add Course",
                font=('Helvetica', 9, 'bold'),
                tags=('add_button', semester)
            )
            
            # Bind add button
            self.canvas.tag_bind(
                semester,
                '<Button-1>',
                lambda e, s=semester: self.open_course_catalog(s)
            )
        
        # Update scroll region
        total_width = len(self.courses) * (self.column_width + self.box_padding) + self.box_padding
        total_height = max(
            (self.box_padding + self.header_height + 
             len(courses) * (self.box_height + self.box_padding) + 30)  # 30 for add button
            for courses in self.courses.values()
        ) if self.courses else 1000
        
        self.canvas.configure(scrollregion=(0, 0, total_width, total_height))
        
    def open_course_catalog(self, semester):
        CourseCatalogPopup(self, semester, self)
        
    def load_from_transcript(self, transcript_data):
        """Load courses from transcript data"""
        if not transcript_data:
            messagebox.showerror("Error", "No transcript data provided!")
            return

        self.clear_transcript()    
        # Clear existing courses
        self.courses = {}
        
        # Add courses from transcript
        for course in transcript_data:
            if not course:  # Skip empty courses
                continue
                
            # Create semester name from Semester and Year
            semester_name = f"{course['Semester']} {course['Year']}"
            
            # Create semester if it doesn't exist
            if semester_name not in self.courses:
                self.courses[semester_name] = []
                if semester_name not in self.transcript_semesters:
                    self.transcript_semesters.append(semester_name)

            # Format course data to match expected structure
            course_data = {
                "prefix": course.get('Department', ''),
                "number": course.get('Course Number', ''),
                "name": course.get('Course Name', ''),
                "credits": course.get('Credit Hours', 0),
                "grade": course.get('Grade', ''),
                "college": course.get('College', 'Unknown'),
                "is_transfer": course.get('College', '') != "The University of South Florida"
            }
            
            # Add course to the semester
            self.courses[semester_name].append(course_data)
                    
        # Update the flowchart display
        self.update_flowchart()

    def show_course_details(self, event):
        # Get the clicked item
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        items = self.canvas.find_closest(x, y)
        
        if items:
            tags = self.canvas.gettags(items[0])
            # Check if we clicked on a course box
            if 'course_box' in tags:
                # Clear any existing drag state
                self.drag_start_pos = None
                self.drag_start_time = None
                self.dragged_items = None
                self.dragged_tags = None
                self.original_positions = None
                if self.drag_shadow:
                    self.canvas.delete(self.drag_shadow)
                    self.drag_shadow = None
                if self.highlighted_semester:
                    self.canvas.itemconfig(f"semester_{self.highlighted_semester}", fill='lightblue')
                    self.highlighted_semester = None
                
                # Find the semester_index tag
                course_tag = next((tag for tag in tags 
                                 if '_' in tag and 
                                 not any(tag.startswith(prefix) 
                                       for prefix in ['delete_', 'course_'])), None)
                if course_tag:
                    try:
                        semester, index = course_tag.split('_')
                        index = int(index)
                        # Get course info
                        course_info = self.courses[semester][index]
                        # Show details popup
                        CourseDetailsPopup(self, course_info)
                    except (ValueError, KeyError, IndexError):
                        pass

    def add_course_to_semester(self, course_info, semester):
        """Add a course to the specified semester"""
        if semester not in self.courses:
            self.courses[semester] = []
            
        # Add the course to the semester
        self.courses[semester].append(course_info)
        
        # Update the flowchart display
        self.update_flowchart()

    def save_plan(self):
        """Prompt user to choose a location and save the semester plan as a PDF"""
        try:
            # Open a file save dialog to let the user choose the location and filename
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save Semester Plan As",
                initialfile="semester_plan.pdf"
            )
            
            # If the user cancels the dialog, filepath will be an empty string
            if not filepath:
                return  # Exit the method if the user cancels
            
            # Generate PDF at the user-specified location
            self.generate_pdf(self.courses, filepath)
            messagebox.showinfo("Success", f"Semester plan saved to {filepath}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save semester plan: {str(e)}")

    def generate_pdf(self, courses, filepath):
        """Generate a PDF of the semester plan with tables per semester, including total credits"""
        try:
            # Create PDF document at the specified filepath
            doc = SimpleDocTemplate(filepath, pagesize=letter, 
                                  leftMargin=0.5*inch, rightMargin=0.5*inch,
                                  topMargin=0.5*inch, bottomMargin=0.5*inch)
            
            # Define styles
            styles = getSampleStyleSheet()
            title_style = styles['Title']
            heading_style = ParagraphStyle(
                name='SemesterHeading',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=12
            )
            
            # Content for the PDF
            content = []
            
            # Add title
            content.append(Paragraph("Semester Plan", title_style))
            content.append(Spacer(1, 0.2*inch))
            
            # If no courses, add a note
            if not courses:
                content.append(Paragraph("No semesters to display.", styles['Normal']))
            else:
                # Sort semesters chronologically
                sorted_semesters = sorted(courses.keys(), key=self.get_semester_order)
                
                for semester in sorted_semesters:
                    # Add semester heading
                    content.append(Paragraph(semester, heading_style))
                    
                    # Prepare table data
                    table_data = [[
                        "Course Code",
                        "Name",
                        "Credits"
                    ]]
                    
                    # Add courses for this semester
                    total_credits = 0
                    for course in courses[semester]:
                        credits = course.get('credits', 0)
                        # Handle credits as string or int, default to 0 if not a number
                        try:
                            credits_value = int(credits) if credits else 0
                        except (ValueError, TypeError):
                            credits_value = 0
                        total_credits += credits_value
                        
                        table_data.append([
                            f"{course.get('prefix', '')} {course.get('number', '')}",
                            course.get('name', ''),
                            str(credits_value)
                        ])
                    
                    # Add total credits row
                    table_data.append([
                        "Total Credits",
                        "",
                        str(total_credits)
                    ])
                    
                    # Create table
                    table = Table(table_data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        # Style the total credits row
                        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ]))
                    
                    # Add table to content
                    content.append(table)
                    content.append(Spacer(1, 0.2*inch))
            
            # Build the PDF
            doc.build(content)
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {str(e)}")

    def load_plan(self):
        """Initialize an empty semester plan on startup"""
        # Clear example and transcript semesters tracking
        self.example_semesters = []
        self.transcript_semesters = []
        self.courses = {}  # Start with an empty plan
        self.update_flowchart()

    def reset_on_close(self):
        """Close the program without saving"""
        self.winfo_toplevel().destroy()
