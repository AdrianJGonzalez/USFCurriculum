#This module is a test for displaying data from the "courses.py" file. 
import tkinter as tk
from tkinter import scrolledtext
import courses  # This module should define the courses dictionary
import json

def decode_requirement(req, parent_op=None, top_level=False):
    """
    Recursively deciphers a nested prerequisite/corequisite structure.
    
    If req is a dictionary with a single key "AND" or "OR", it processes the list of
    requirements under that operator. For a leaf requirement (with keys "Department",
    "Course Code", "Grade"), it returns a string in the form:
    "DEPT CODE (min grade GRADE)".
    
    If the current group is nested and its parent's operator is "OR", the result is enclosed in square brackets.
    """
    if isinstance(req, dict):
        keys = list(req.keys())
        # Check if this dict represents a group with an operator
        if len(keys) == 1 and keys[0] in ["AND", "OR"]:
            op = keys[0]
            children = req[op]
            # Process each child; for children, pass the current operator as parent_op.
            sub_strings = [decode_requirement(child, parent_op=op, top_level=False) for child in children]
            # Filter out any empty strings
            sub_strings = [s for s in sub_strings if s]
            # Join using the operator.
            joined = f" {op} ".join(sub_strings)
            # If this group is nested inside an OR group, enclose it in square brackets.
            if not top_level and parent_op == "OR":
                return f"[{joined}]"
            else:
                return joined
        else:
            # It's a leaf requirement
            dept = req.get("Department", "")
            code = req.get("Course Code", "")
            grade = req.get("Grade", "")
            if dept or code or grade:
                # Format each course; if a grade is provided, include it.
                if grade:
                    return f"{dept} {code} (min grade {grade})"
                else:
                    return f"{dept} {code}"
            else:
                return ""
    elif isinstance(req, list):
        # If req is a list, join the items (not typical in our structure)
        sub_strings = [decode_requirement(item, parent_op=parent_op, top_level=top_level) for item in req]
        return " ".join(sub_strings)
    else:
        return str(req)

def display_courses():
    # Create the main window.
    window = tk.Tk()
    window.title("All Courses Information")
    window.geometry("900x700")
    
    # Create a scrolled text widget.
    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 10))
    text_area.pack(expand=True, fill=tk.BOTH)
    
    output = ""
    # Iterate through the courses dictionary.
    for university, depts in courses.courses.items():
        output += f"University: {university}\n"
        output += "=" * (len("University: ") + len(university)) + "\n\n"
        for dept, courses_dict in depts.items():
            for course_code, details in courses_dict.items():
                output += f"Department: {dept}\n"
                output += f"Class Code: {course_code}\n"
                output += f"Class Full Name: {details.get('Class Full Name', 'N/A')}\n"
                output += f"Description: {details.get('Description', 'N/A')}\n"
                
                # Decipher Corequisites.
                coreqs = details.get("Coreqs", "N/A")
                if isinstance(coreqs, (dict, list)):
                    coreqs_str = decode_requirement(coreqs, top_level=True)
                else:
                    coreqs_str = str(coreqs)
                output += f"CoReqs: {coreqs_str}\n\n"
                
                # Decipher Prerequisites.
                prereqs = details.get("Prereqs", "N/A")
                if isinstance(prereqs, (dict, list)):
                    prereqs_str = decode_requirement(prereqs, top_level=True)
                else:
                    prereqs_str = str(prereqs)
                output += f"Prereqs: {prereqs_str}\n\n"
                
                output += f"Credit Hours: {details.get('Credit Hours', 'N/A')}\n"
                output += "-" * 50 + "\n\n"
    
    text_area.insert(tk.END, output)
    text_area.config(state=tk.DISABLED)
    
    window.mainloop()

if __name__ == '__main__':
    display_courses()
