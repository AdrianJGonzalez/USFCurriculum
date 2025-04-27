import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

# Add the parent directory to the Python path to import courses
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from courses import courses

NONE_VAL = "N/A"

class CourseRequirementFrame(tk.Frame):
    def __init__(self, master, parent_group, bg_color="white"):
        super().__init__(master, bg=bg_color)
        self.parent_group = parent_group
        self.bg_color = bg_color
        
        # Operator label that shows parent's group type ("AND:" or "OR:")
        self.operator_label = tk.Label(self, text=self.parent_group.group_type.get() + ": ", bg=bg_color)
        self.operator_label.pack(side=tk.LEFT, padx=5)
        
        # Entry for Department
        self.dept_entry = tk.Entry(self, width=10)
        self.dept_entry.pack(side=tk.LEFT, padx=5)
        # Entry for Course Code
        self.code_entry = tk.Entry(self, width=10)
        self.code_entry.pack(side=tk.LEFT, padx=5)
        # Entry for Minimum Grade
        self.grade_entry = tk.Entry(self, width=5)
        self.grade_entry.pack(side=tk.LEFT, padx=5)
        
        # Remove button for this requirement
        remove_button = tk.Button(self, text="Remove", command=self.remove_self, fg="red", bg=bg_color)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # Bind to parent's group_type variable
        self.parent_group.group_type.trace_add("write", self.update_operator_label)
    
    def update_operator_label(self, *args):
        new_text = self.parent_group.group_type.get() + ": "
        self.operator_label.config(text=new_text)
    
    def remove_self(self):
        if self in self.parent_group.children_frames:
            self.parent_group.children_frames.remove(self)
        self.destroy()
    
    def get_structure(self):
        dept = self.dept_entry.get().strip()
        code = self.code_entry.get().strip()
        grade = self.grade_entry.get().strip()
        if dept or code or grade:
            return {
                "Department": dept if dept else NONE_VAL,
                "Course Code": code if code else NONE_VAL,
                "Grade": grade if grade else NONE_VAL
            }
        else:
            return None
            
    def set_values(self, data):
        if isinstance(data, dict):
            self.dept_entry.insert(0, data.get("Department", ""))
            self.code_entry.insert(0, data.get("Course Code", ""))
            self.grade_entry.insert(0, data.get("Grade", ""))

class GroupFrame(tk.Frame):
    def __init__(self, master, is_top_level=False, remove_callback=None, bg_color="#cad2d8", default_type="AND"):
        super().__init__(master, bd=2, relief=tk.RIDGE, padx=5, pady=5, bg=bg_color)
        self.is_top_level = is_top_level
        self.remove_callback = remove_callback
        self.bg_color = bg_color
        self.children_frames = []
        
        # Group type selection
        self.group_type = tk.StringVar(value=default_type)
        type_label = tk.Label(self, text="Group Type:", bg=bg_color)
        type_label.pack(side=tk.LEFT)
        self.type_menu = tk.OptionMenu(self, self.group_type, "AND", "OR")
        self.type_menu.pack(side=tk.LEFT)
        
        # Add buttons
        add_req_button = tk.Button(self, text="Add Requirement", command=self.add_requirement, bg=bg_color)
        add_req_button.pack(side=tk.LEFT, padx=5)
        add_group_button = tk.Button(self, text="Add Nested Group", command=self.add_group, bg=bg_color)
        add_group_button.pack(side=tk.LEFT, padx=5)
        
        if not self.is_top_level:
            remove_button = tk.Button(self, text="Remove Group", command=self.remove_self, fg="red", bg=bg_color)
            remove_button.pack(side=tk.RIGHT, padx=5)
        
        self.children_container = tk.Frame(self, bg=bg_color)
        self.children_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def add_requirement(self):
        req = CourseRequirementFrame(self.children_container, self, bg_color=self.bg_color)
        req.pack(fill=tk.X, pady=2)
        self.children_frames.append(req)
        return req
    
    def add_group(self):
        group = GroupFrame(self.children_container, is_top_level=False, remove_callback=self.remove_child, bg_color=self.bg_color)
        group.pack(fill=tk.X, pady=2)
        self.children_frames.append(group)
        return group
    
    def remove_child(self, child):
        if child in self.children_frames:
            self.children_frames.remove(child)
    
    def remove_self(self):
        if self.remove_callback:
            self.remove_callback(self)
        self.destroy()
    
    def get_structure(self):
        children_list = []
        for child in self.children_frames:
            child_struct = child.get_structure()
            if child_struct:
                children_list.append(child_struct)
        if not children_list:
            return None
        return {self.group_type.get(): children_list}
        
    def set_structure(self, data):
        if not data:
            return
            
        if isinstance(data, dict):
            # Handle AND/OR groups
            for group_type, requirements in data.items():
                self.group_type.set(group_type)
                if isinstance(requirements, list):
                    for req in requirements:
                        if isinstance(req, dict):
                            if "Department" in req:
                                # This is a leaf requirement
                                new_req = self.add_requirement()
                                new_req.set_values(req)
                            else:
                                # This is a nested group
                                new_group = self.add_group()
                                new_group.set_structure(req)

class CourseEditorPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        style = ttk.Style()
        style.configure("Header.TLabel", background='#dcdad5', foreground='#006747')
        header = ttk.Label(
            self,
            text="Course Editor",
            font=('Helvetica', 20, 'bold'),
            style="Header.TLabel"
        )
        header.pack(pady=20)
        
        # Course selection frame
        selection_frame = ttk.LabelFrame(self, text="Select Existing Course or Create New")
        selection_frame.pack(fill='x', padx=10, pady=5)
        
        # Department dropdown
        dept_frame = ttk.Frame(selection_frame)
        dept_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(dept_frame, text="Department:").pack(side='left')
        self.dept_var = tk.StringVar()
        self.dept_var.trace('w', self.update_courses)
        self.dept_dropdown = ttk.Combobox(
            dept_frame,
            textvariable=self.dept_var,
            values=self.get_departments(),
            state="readonly"
        )
        self.dept_dropdown.pack(side='left', padx=5)
        
        # Course dropdown
        course_frame = ttk.Frame(selection_frame)
        course_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(course_frame, text="Course:").pack(side='left')
        self.course_var = tk.StringVar()
        self.course_var.trace('w', self.load_course)
        self.course_dropdown = ttk.Combobox(
            course_frame,
            textvariable=self.course_var,
            state="readonly"
        )
        self.course_dropdown.pack(side='left', padx=5)
        
        # Course details frame
        details_frame = ttk.LabelFrame(self, text="Course Details")
        details_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Department
        dept_entry_frame = ttk.Frame(details_frame)
        dept_entry_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(dept_entry_frame, text="Department:").pack(side='left')
        self.dept_entry = ttk.Entry(dept_entry_frame)
        self.dept_entry.pack(side='left', padx=5)
        
        # Course code
        code_frame = ttk.Frame(details_frame)
        code_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(code_frame, text="Course Code:").pack(side='left')
        self.code_entry = ttk.Entry(code_frame)
        self.code_entry.pack(side='left', padx=5)
        
        # Course name
        name_frame = ttk.Frame(details_frame)
        name_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(name_frame, text="Course Name:").pack(side='left')
        self.name_entry = ttk.Entry(name_frame, width=50)
        self.name_entry.pack(side='left', padx=5)
        
        # Description
        desc_frame = ttk.Frame(details_frame)
        desc_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(desc_frame, text="Description:").pack(anchor='w')
        self.desc_entry = tk.Text(desc_frame, height=4, width=50,)
        self.desc_entry.pack(fill='x', padx=5, pady=2)
        
        # Credit hours
        credit_frame = ttk.Frame(details_frame)
        credit_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(credit_frame, text="Credit Hours:").pack(side='left')
        self.credit_entry = ttk.Entry(credit_frame, width=5)
        self.credit_entry.pack(side='left', padx=5)
        
        # Prerequisites
        prereq_frame = ttk.LabelFrame(details_frame, text="Prerequisites")
        prereq_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.prereq_top_group = GroupFrame(prereq_frame, is_top_level=True, bg_color="#cad2d8")
        self.prereq_top_group.pack(fill='both', expand=True)
        
        # Corequisites
        coreq_frame = ttk.LabelFrame(details_frame, text="Corequisites")
        coreq_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.coreq_top_group = GroupFrame(coreq_frame, is_top_level=True, bg_color="lightgreen")
        self.coreq_top_group.pack(fill='both', expand=True)
        
        # Buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save Course", command=self.save_course).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete Course", command=self.delete_course).pack(side='left', padx=5)
        
    def get_departments(self):
        return sorted(courses["University of South Florida"].keys())
        
    def update_courses(self, *args):
        dept = self.dept_var.get()
        if dept:
            course_list = sorted(courses["University of South Florida"][dept].keys())
            self.course_dropdown['values'] = course_list
        else:
            self.course_dropdown['values'] = []
        self.course_var.set('')
        
    def load_course(self, *args):
        dept = self.dept_var.get()
        course_code = self.course_var.get()
        
        if dept and course_code:
            course_data = courses["University of South Florida"][dept][course_code]
            
            # Clear existing data
            self.clear_fields()
            
            # Fill in the fields
            self.dept_entry.insert(0, dept)
            self.code_entry.insert(0, course_code)
            self.name_entry.insert(0, course_data["Class Full Name"])
            self.desc_entry.insert("1.0", course_data.get("Description", ""))
            self.credit_entry.insert(0, str(course_data["Credit Hours"]))
            
            # Load prerequisites
            if course_data.get("Prereqs") != NONE_VAL:
                self.prereq_top_group.set_structure(course_data["Prereqs"])
                
            # Load corequisites
            if course_data.get("Coreqs") != NONE_VAL:
                self.coreq_top_group.set_structure(course_data["Coreqs"])
                
    def save_course(self):
        try:
            university = "University of South Florida"
            dept = self.dept_entry.get().strip().upper()
            course_code = self.code_entry.get().strip()
            full_name = self.name_entry.get().strip()
            description = self.desc_entry.get("1.0", tk.END).strip()
            credit_hours = self.credit_entry.get().strip()
            
            # Get the nested prerequisites and corequisites structures
            prereq_structure = self.prereq_top_group.get_structure()
            coreq_structure = self.coreq_top_group.get_structure()
            
            # Validate required fields
            if not (dept and course_code and full_name and credit_hours):
                messagebox.showerror("Error", "Department, Course Code, Name, and Credit Hours are required!")
                return
                
            if university not in courses:
                courses[university] = {}
            if dept not in courses[university]:
                courses[university][dept] = {}
                
            # Build the course dictionary
            courses[university][dept][course_code] = {
                "Class Full Name": full_name,
                "Description": description,
                "Prereqs": prereq_structure if prereq_structure else NONE_VAL,
                "Coreqs": coreq_structure if coreq_structure else NONE_VAL,
                "Credit Hours": int(credit_hours)
            }
            
            # Write to courses.py
            courses_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "courses.py")
            with open(courses_path, "w") as f:
                f.write("courses = " + json.dumps(courses, indent=4))
                
            # Update dropdowns
            self.dept_dropdown['values'] = self.get_departments()
            if dept in courses[university]:
                self.dept_var.set(dept)
                self.course_dropdown['values'] = sorted(courses[university][dept].keys())
                self.course_var.set(course_code)
                
            messagebox.showinfo("Success", "Course saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save course: {str(e)}")
            
    def clear_fields(self):
        self.dept_entry.delete(0, tk.END)
        self.code_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete("1.0", tk.END)
        self.credit_entry.delete(0, tk.END)
        
        # Recreate prerequisite and corequisite groups
        self.prereq_top_group.destroy()
        self.coreq_top_group.destroy()
        
        prereq_frame = self.prereq_top_group.master
        coreq_frame = self.coreq_top_group.master
        
        self.prereq_top_group = GroupFrame(prereq_frame, is_top_level=True, bg_color="white")
        self.prereq_top_group.pack(fill='both', expand=True)
        
        self.coreq_top_group = GroupFrame(coreq_frame, is_top_level=True, bg_color="lightgreen")
        self.coreq_top_group.pack(fill='both', expand=True)
        
    def delete_course(self):
        dept = self.dept_var.get()
        course_code = self.course_var.get()
        
        if not (dept and course_code):
            messagebox.showerror("Error", "Please select a course to delete!")
            return
            
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {dept} {course_code}?"):
            try:
                del courses["University of South Florida"][dept][course_code]
                
                # If department is empty, remove it
                if not courses["University of South Florida"][dept]:
                    del courses["University of South Florida"][dept]
                    
                # Write changes to courses.py
                courses_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "courses.py")
                with open(courses_path, "w") as f:
                    f.write("courses = " + json.dumps(courses, indent=4))
                    
                # Update dropdowns
                self.dept_dropdown['values'] = self.get_departments()
                self.dept_var.set('')
                self.course_dropdown['values'] = []
                self.course_var.set('')
                
                # Clear fields
                self.clear_fields()
                
                messagebox.showinfo("Success", "Course deleted successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete course: {str(e)}")
