import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from tkinter import ttk
from datetime import datetime
import sys
import os

# Add the parent directory to the Python path to import courses
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from courses import courses  # Import the course catalog data

class CourseCatalogPopup(tk.Toplevel):
    def __init__(self, parent, semester, callback):
        super().__init__(parent)
        self.semester = semester
        self.callback = callback
        self.title(f"Add Course to {semester}")
        self.geometry("800x600")
        
        # Initialize variables
        self.search_var = tk.StringVar()
        self.dept_var = tk.StringVar()
        self.course_list = None
        
        # Create main container
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel for course list
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        # Department selection
        dept_frame = ttk.Frame(left_panel)
        dept_frame.pack(fill='x', pady=5)
        
        ttk.Label(dept_frame, text="Department:").pack(side='left')
        self.dept_var.trace('w', self.update_course_list)
        dept_dropdown = ttk.Combobox(
            dept_frame,
            textvariable=self.dept_var,
            values=["All"] + self.get_departments(),
            state="readonly"
        )
        dept_dropdown.pack(side='left', fill='x', expand=True, padx=5)
        dept_dropdown.set("All")  # Set default to "All"
        
        # Search box
        search_frame = ttk.Frame(left_panel)
        search_frame.pack(fill='x', pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var.trace('w', self.update_course_list)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Course list
        self.course_list = tk.Listbox(
            left_panel,
            width=40,
            height=30
        )
        self.course_list.pack(fill='both', expand=True)
        
        # Right panel for course details
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side='left', fill='both', expand=True)
        
        # Course details
        details_frame = ttk.LabelFrame(right_panel, text="Course Details")
        details_frame.pack(fill='both', expand=True)
        
        self.details_text = tk.Text(
            details_frame,
            wrap='word',
            height=20,
            state='disabled'
        )
        self.details_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Add button
        add_button = ttk.Button(
            right_panel,
            text="Add Course",
            command=self.add_selected_course
        )
        add_button.pack(pady=10)
        
        # Bind selection event
        self.course_list.bind('<<ListboxSelect>>', self.show_course_details)
        
        # Initialize course list
        self.update_course_list()
        
    def get_departments(self):
        """Get list of departments from the course catalog"""
        return list(courses["University of South Florida"].keys())
        
    def update_course_list(self, *args):
        try:
            if not hasattr(self, 'course_list') or self.course_list is None:
                return
                
            search_term = self.search_var.get().lower()
            selected_dept = self.dept_var.get()
            self.course_list.delete(0, tk.END)
            
            if selected_dept == "All":
                # Show all courses from all departments
                for dept, dept_courses in courses["University of South Florida"].items():
                    for course_code, course_info in dept_courses.items():
                        course_name = course_info.get("Class Full Name", "")
                        if (not search_term or 
                            search_term in course_code.lower() or 
                            search_term in course_name.lower()):
                            self.course_list.insert(tk.END, f"{dept} {course_code} - {course_name}")
            else:
                # Show courses from selected department
                dept_courses = courses["University of South Florida"].get(selected_dept, {})
                for course_code, course_info in dept_courses.items():
                    course_name = course_info.get("Class Full Name", "")
                    if (not search_term or 
                        search_term in course_code.lower() or 
                        search_term in course_name.lower()):
                        self.course_list.insert(tk.END, f"{course_code} - {course_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update course list: {str(e)}")
        
    def show_course_details(self, event):
        selection = self.course_list.curselection()
        if not selection:
            return
            
        course_str = self.course_list.get(selection[0])
        if self.dept_var.get() == "All":
            dept, rest = course_str.split(' ', 1)
            course_code = rest.split(' - ')[0]
        else:
            dept = self.dept_var.get()
            course_code = course_str.split(' - ')[0]
        
        # Find course in catalog
        course_info = courses["University of South Florida"][dept][course_code]
        self.details_text.config(state='normal')
        self.details_text.delete(1.0, tk.END)
        
        # Format course details
        details = (
            f"Course: {dept} {course_code}\n"
            f"Name: {course_info['Class Full Name']}\n"
            f"Credits: {course_info['Credit Hours']}\n"
            f"Description: {course_info['Description']}\n"
            f"Prerequisites: {self.format_requirements(course_info.get('Prereqs', 'N/A'))}\n"
            f"Corequisites: {self.format_requirements(course_info.get('Coreqs', 'N/A'))}"
        )
        
        self.details_text.insert(1.0, details)
        self.details_text.config(state='disabled')
                
    def format_requirements(self, reqs):
        """Format prerequisites or corequisites for display"""
        if reqs == "N/A":
            return "N/A"
            
        if isinstance(reqs, dict):
            if "AND" in reqs:
                return " AND ".join(self.format_requirement(r) for r in reqs["AND"])
            elif "OR" in reqs:
                return " OR ".join(self.format_requirement(r) for r in reqs["OR"])
        elif isinstance(reqs, list):
            return ", ".join(self.format_requirement(r) for r in reqs)
            
        return str(reqs)
        
    def format_requirement(self, req):
        """Format a single requirement"""
        if isinstance(req, dict):
            return f"{req['Department']} {req['Course Code']} (Grade: {req['Grade']})"
        return str(req)
                
    def add_selected_course(self):
        selection = self.course_list.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a course first!")
            return
            
        course_str = self.course_list.get(selection[0])
        if self.dept_var.get() == "All":
            dept, rest = course_str.split(' ', 1)
            course_code = rest.split(' - ')[0]
        else:
            dept = self.dept_var.get()
            course_code = course_str.split(' - ')[0]
        
        # Get course info
        course_info = courses["University of South Florida"][dept][course_code]
        course_data = {
            "prefix": dept,
            "number": course_code,
            "name": course_info["Class Full Name"],
            "credits": course_info["Credit Hours"]
        }
        
        self.callback(self.semester, course_data)
        self.destroy()

class CourseDetailsPopup(tk.Toplevel):
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
        
        # Get course details from the catalog
        try:
            catalog_info = courses["University of South Florida"][course_info['prefix']][course_info['number']]
            
            # Format and display course details
            details = f"Course: {course_info['prefix']} {course_info['number']}\n\n"
            details += f"Name: {course_info['name']}\n\n"
            details += f"Credits: {course_info['credits']}\n\n"
            
            if course_info.get('is_transfer', False):
                details += f"Transfer Course from: {course_info.get('college', 'Unknown')}\n\n"
            
            details += f"Description:\n{catalog_info.get('Description', 'No description available.')}\n\n"
            
            prereqs = catalog_info.get('Prereqs', 'N/A')
            if isinstance(prereqs, dict):
                if 'AND' in prereqs:
                    prereq_text = ' AND '.join(f"{p['Department']} {p['Course Code']} (Grade: {p['Grade']})" 
                                             for p in prereqs['AND'])
                elif 'OR' in prereqs:
                    prereq_text = ' OR '.join(f"{p['Department']} {p['Course Code']} (Grade: {p['Grade']})" 
                                            for p in prereqs['OR'])
                else:
                    prereq_text = str(prereqs)
            else:
                prereq_text = str(prereqs)
            
            details += f"Prerequisites: {prereq_text}\n\n"
            
            coreqs = catalog_info.get('Coreqs', 'N/A')
            if isinstance(coreqs, dict):
                if 'AND' in coreqs:
                    coreq_text = ' AND '.join(f"{p['Department']} {p['Course Code']} (Grade: {p['Grade']})" 
                                            for p in coreqs['AND'])
                elif 'OR' in coreqs:
                    coreq_text = ' OR '.join(f"{p['Department']} {p['Course Code']} (Grade: {p['Grade']})" 
                                           for p in coreqs['OR'])
                else:
                    coreq_text = str(coreqs)
            else:
                coreq_text = str(coreqs)
            
            details += f"Corequisites: {coreq_text}"
            
        except KeyError:
            details = f"Course: {course_info['prefix']} {course_info['number']}\n\n"
            details += f"Name: {course_info['name']}\n\n"
            details += f"Credits: {course_info['credits']}\n\n"
            if course_info.get('is_transfer', False):
                details += f"Transfer Course from: {course_info.get('college', 'Unknown')}\n\n"
            details += "Additional details not available in the course catalog."
        
        self.details_text.insert('1.0', details)
        self.details_text.config(state='disabled')
        
        # Close button
        close_button = ttk.Button(
            self,
            text="Close",
            command=self.destroy
        )
        close_button.pack(pady=10)

class FlowchartPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.courses = {}  # Dictionary to store courses by semester
        self.dragged_item = None
        self.dragged_tags = None
        self.drag_shadow = None
        self.highlighted_semester = None
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header = ttk.Label(
            self,
            text="Academic Flowchart",
            font=("Helvetica", 14)
        )
        header.pack(pady=10)
        
        # Control buttons frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Semester selection frame
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
        self.year_entry.insert(0, "2024")
        
        # Add semester button
        add_semester_btn = ttk.Button(
            semester_frame,
            text="Add Semester",
            command=self.add_semester
        )
        add_semester_btn.pack(side='left', padx=5)
        
        # Add course button
        add_course_btn = ttk.Button(
            control_frame,
            text="Add Course",
            command=self.add_course_dialog
        )
        add_course_btn.pack(side='left', padx=5)
        
        # Clear flowchart button
        clear_btn = ttk.Button(
            control_frame,
            text="Clear Flowchart",
            command=self.clear_flowchart
        )
        clear_btn.pack(side='left', padx=5)
        
        # Create main canvas with scrollbars
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg='white',
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
        self.column_width = 250  # Width for course boxes
        self.box_height = 80  # Height for course boxes
        self.header_height = 40  # New smaller height for semester headers
        self.box_padding = 10
        
        # Bind mouse wheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Bind drag and drop events
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        
        # Add double-click binding for course details
        self.canvas.tag_bind('course_box', '<Double-Button-1>', self.show_course_details)
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
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
                course_tag = next((tag for tag in tags if '_' in tag and not any(tag.startswith(prefix) for prefix in ['delete_', 'course_', 'semester_'])), None)
                if course_tag:
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
        if hasattr(self, 'dragged_items') and self.dragged_items:
            # Move the dragged items and shadow
            x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            
            # Calculate offset from original position
            if self.original_positions:
                first_item = self.original_positions[0]
                offset_x = x - first_item['x']
                offset_y = y - first_item['y']
                
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
                        x, y,
                        x + first_item['width'],
                        y + first_item['height']
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
            
            # Ensure semester headers stay on top
            for semester in self.courses.keys():
                self.canvas.tag_raise(f"semester_{semester}")
            
    def end_drag(self, event):
        if hasattr(self, 'dragged_items') and self.dragged_items:
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
            
            # Find which semester column the course was dropped in
            for i, semester in enumerate(sorted_semesters):
                column_x = i * (self.column_width + self.box_padding) + self.box_padding
                if column_x <= x <= column_x + self.column_width:
                    # Only proceed if we're actually moving to a different semester
                    if original_semester != semester:
                        # Check if it's a transfer course
                        if (original_semester in self.courses and 
                            0 <= course_index < len(self.courses[original_semester]) and
                            self.courses[original_semester][course_index].get('is_transfer', False)):
                            
                            # Show warning
                            if not messagebox.askyesno("Warning", 
                                "This is a transfer course. Moving it to a different semester might affect your academic progress. Are you sure you want to move it?"):
                                # If user selects "No", cancel the move
                                need_update = True
                                break
                        
                        # Move course to new semester
                        course = self.courses[original_semester].pop(course_index)
                        self.courses[semester].append(course)
                        need_update = True
                    break
            
            # Clean up
            self.dragged_items = None
            self.dragged_tags = None
            self.original_positions = None
            if self.drag_shadow:
                self.canvas.delete(self.drag_shadow)
                self.drag_shadow = None
            if self.highlighted_semester:
                self.canvas.itemconfig(f"semester_{self.highlighted_semester}", fill='lightblue')
                self.highlighted_semester = None
            
            # Only update the flowchart if we actually moved something or need to reset
            if need_update:
                self.update_flowchart()
            
    def clear_flowchart(self):
        if messagebox.askyesno("Clear Flowchart", "Are you sure you want to clear the entire flowchart?"):
            self.courses = {}
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
                tags=('semester_header', f'semester_{semester}')
            )
            header_text = self.canvas.create_text(
                x + self.column_width/2,
                self.box_padding + self.header_height/2,
                text=semester,
                font=('Helvetica', 10, 'bold'),
                tags=('semester_header', f'semester_{semester}')
            )
            
            # Draw course boxes starting immediately after header
            for j, course in enumerate(self.courses[semester]):
                y = self.box_padding + self.header_height + (j * (self.box_height + self.box_padding))
                
                # Determine box color based on course type
                if course.get('is_transfer', False):
                    box_fill = 'lightyellow'  # Transfer courses
                elif course.get('is_manual', False):
                    box_fill = '#E6F3FF'  # Manually added courses (light blue)
                else:
                    box_fill = 'white'  # Regular transcript courses
                
                box = self.canvas.create_rectangle(
                    x, y,
                    x + self.column_width, y + self.box_height,
                    fill=box_fill,
                    outline='black',
                    tags=('course_box', f'{semester}_{j}')
                )
                
                # Add course text with more details
                course_text = (
                    f"{course['prefix']} {course['number']}\n"
                    f"{course['name']}\n"
                    f"Credits: {course.get('credits', 'N/A')}"
                )
                
                # Add transfer label if applicable
                if course.get('is_transfer', False):
                    course_text += f"\nTransfer: {course.get('college', 'Unknown')}"
                elif course.get('is_manual', False):
                    course_text += "\nManually Added"
                
                text_item = self.canvas.create_text(
                    x + self.column_width/2,
                    y + self.box_height/2,
                    text=course_text,
                    font=('Helvetica', 9),
                    justify='center',
                    tags=('course_box', f'{semester}_{j}')
                )
                
                # Add delete button
                delete_btn = self.canvas.create_rectangle(
                    x + self.column_width - 20, y,
                    x + self.column_width, y + 20,
                    fill='red',
                    outline='black',
                    tags=('delete_btn', f'delete_{semester}_{j}')
                )
                self.canvas.create_text(
                    x + self.column_width - 10, y + 10,
                    text='X',
                    font=('Helvetica', 8, 'bold'),
                    tags=('delete_btn', f'delete_{semester}_{j}')
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
        CourseCatalogPopup(self, semester, self.add_course)
        
    def load_from_transcript(self, transcript_data):
        """Load courses from transcript data"""
        if not transcript_data:
            messagebox.showerror("Error", "No transcript data provided!")
            return
            
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
                
            # Format course data to match expected structure
            course_data = {
                "prefix": course['Department'],
                "number": course['Course Number'],
                "name": course['Course Name'],
                "credits": course['Credit Hours'],
                "is_transfer": True,  # Mark as transfer course
                "college": course['College']  # Store original college
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
