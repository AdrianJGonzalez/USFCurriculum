import tkinter as tk
from tkinter import messagebox
import courses  # Assumes you have a courses module to import and update
import json

NONE_VAL = "N/A"

# -------------------------------
# Leaf Frame: A single course requirement with operator indicator
# -------------------------------
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
        
        # Bind to parent's group_type variable so that the indicator updates if the group operator changes.
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

# -------------------------------
# Group Frame: A container that can hold either CourseRequirementFrames (leaves)
# or nested GroupFrames (subgroups). Each group has its own operator indicator.
# -------------------------------
class GroupFrame(tk.Frame):
    def __init__(self, master, is_top_level=False, remove_callback=None, bg_color="white", default_type="AND"):
        super().__init__(master, bd=2, relief=tk.RIDGE, padx=5, pady=5, bg=bg_color)
        self.is_top_level = is_top_level
        self.remove_callback = remove_callback  # Callback to remove this group from a parent group
        self.bg_color = bg_color
        self.children_frames = []  # List of child frames (either CourseRequirementFrame or GroupFrame)
        
        # Group type selection: AND or OR
        self.group_type = tk.StringVar(value=default_type)
        type_label = tk.Label(self, text="Group Type:", bg=bg_color)
        type_label.pack(side=tk.LEFT)
        self.type_menu = tk.OptionMenu(self, self.group_type, "AND", "OR")
        self.type_menu.pack(side=tk.LEFT)
        
        # Buttons to add a leaf requirement or a nested group
        add_req_button = tk.Button(self, text="Add Requirement", command=self.add_requirement, bg=bg_color)
        add_req_button.pack(side=tk.LEFT, padx=5)
        add_group_button = tk.Button(self, text="Add Nested Group", command=self.add_group, bg=bg_color)
        add_group_button.pack(side=tk.LEFT, padx=5)
        
        # For non–top-level groups, provide a remove button
        if not self.is_top_level:
            remove_button = tk.Button(self, text="Remove Group", command=self.remove_self, fg="red", bg=bg_color)
            remove_button.pack(side=tk.RIGHT, padx=5)
        
        # Container frame for child elements
        self.children_container = tk.Frame(self, bg=bg_color)
        self.children_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def add_requirement(self):
        req = CourseRequirementFrame(self.children_container, self, bg_color=self.bg_color)
        req.pack(fill=tk.X, pady=2)
        self.children_frames.append(req)
    
    def add_group(self):
        group = GroupFrame(self.children_container, is_top_level=False, remove_callback=self.remove_child, bg_color=self.bg_color)
        group.pack(fill=tk.X, pady=2)
        self.children_frames.append(group)
    
    def remove_child(self, child):
        if child in self.children_frames:
            self.children_frames.remove(child)
    
    def remove_self(self):
        if self.remove_callback:
            self.remove_callback(self)
        self.destroy()
    
    def get_structure(self):
        # Recursively traverse children and build a list
        children_list = []
        for child in self.children_frames:
            if isinstance(child, CourseRequirementFrame):
                child_struct = child.get_structure()
                if child_struct:
                    children_list.append(child_struct)
            elif isinstance(child, GroupFrame):
                child_struct = child.get_structure()
                if child_struct:
                    children_list.append(child_struct)
        if not children_list:
            return None
        # Return the group as a dictionary with the group type as key
        return {self.group_type.get(): children_list}

# -------------------------------
# Save Function: Builds the final nested structure and writes to courses.py
# -------------------------------
def save_courses():
    try:
        university = "University of South Florida"
        dept = dept_entry.get().strip().upper()
        course_code = code_entry.get().strip()
        full_name = name_entry.get().strip()
        description = desc_entry.get("1.0", tk.END).strip()
        credit_hours = credit_entry.get().strip()
        
        # Get the nested prerequisites and corequisites structures
        prereq_structure = prereq_top_group.get_structure()
        coreq_structure = coreq_top_group.get_structure()
        
        # Check required course fields
        if not (dept and course_code and full_name and credit_hours):
            messagebox.showerror("Error", "Department, Course Code, Name, and Credit Hours are required!")
            return
        
        if university not in courses.courses:
            courses.courses[university] = {}
        if dept not in courses.courses[university]:
            courses.courses[university][dept] = {}
        
        # Build the final course dictionary
        courses.courses[university][dept][course_code] = {
            "Class Full Name": full_name,
            "Description": description,
            "Prereqs": prereq_structure if prereq_structure else NONE_VAL,
            "Coreqs": coreq_structure if coreq_structure else NONE_VAL,
            "Credit Hours": int(credit_hours)
        }
        
        # Write the updated courses dictionary to courses.py
        with open("courses.py", "w") as f:
            f.write("courses = " + json.dumps(courses.courses, indent=4))
        
        print("Courses successfully saved to courses.py")
        messagebox.showinfo("Success", "Courses saved successfully!")
    except Exception as e:
        print(f"Error saving courses: {e}")
        messagebox.showerror("Error", f"Failed to save courses: {e}")

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()
root.title("Course Dictionary Manager")
root.geometry("800x800")

# Course Basic Information
tk.Label(root, text="Department (e.g., ACG):").pack()
dept_entry = tk.Entry(root)
dept_entry.pack()

tk.Label(root, text="Course Code (e.g., 2021):").pack()
code_entry = tk.Entry(root)
code_entry.pack()

tk.Label(root, text="Class Full Name:").pack()
name_entry = tk.Entry(root, width=50)
name_entry.pack()

tk.Label(root, text="Description:").pack()
desc_entry = tk.Text(root, height=4, width=50)
desc_entry.pack()

tk.Label(root, text="Credit Hours:").pack()
credit_entry = tk.Entry(root)
credit_entry.pack()

# Prerequisites Section (Nested Grouping)
tk.Label(root, text="Prerequisites (Nested Groups for AND/OR Conditions):").pack(pady=10)
prereq_frame_main = tk.Frame(root, bd=2, relief=tk.SUNKEN)
prereq_frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
# Top-level group for prerequisites (white background)
prereq_top_group = GroupFrame(prereq_frame_main, is_top_level=True, bg_color="white")
prereq_top_group.pack(fill=tk.BOTH, expand=True)

# Corequisites Section (Nested Grouping)
tk.Label(root, text="Corequisites (Nested Groups for AND/OR Conditions):").pack(pady=10)
coreq_frame_main = tk.Frame(root, bd=2, relief=tk.SUNKEN)
coreq_frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
# Top-level group for corequisites (lightgreen background)
coreq_top_group = GroupFrame(coreq_frame_main, is_top_level=True, bg_color="lightgreen")
coreq_top_group.pack(fill=tk.BOTH, expand=True)

# Action Buttons
tk.Button(root, text="Save Course", command=save_courses).pack(pady=10)
tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

root.mainloop()
