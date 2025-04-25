import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import json
import PyPDF2

class TranscriptPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.courses = []
        self.flowchart = None  # Reference to flowchart
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header = ttk.Label(
            self,
            text="Upload Transcript",
            font=("Helvetica", 14)
        )
        header.pack(pady=10)
        
        # Upload frame
        upload_frame = ttk.LabelFrame(self, text="Upload Your Transcript")
        upload_frame.pack(fill='x', padx=10, pady=5)
        
        # Upload button
        upload_btn = ttk.Button(
            upload_frame,
            text="Choose File",
            command=self.upload_file
        )
        upload_btn.pack(padx=5, pady=10)
        
        # File name label
        self.file_label = ttk.Label(upload_frame, text="No file selected")
        self.file_label.pack(pady=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(self, text="Upload Status")
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready to upload")
        self.status_label.pack(pady=5)
        
        # Create a frame for the semester boxes
        self.semester_frame = ttk.Frame(self)
        self.semester_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create a canvas with scrollbar for the semester boxes
        self.canvas = tk.Canvas(self.semester_frame)
        self.scrollbar = ttk.Scrollbar(self.semester_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Enable mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Create totals frame
        totals_frame = ttk.Frame(self)
        totals_frame.pack(fill='x', padx=10, pady=5)
        
        # Total credits label
        self.total_credits_label = ttk.Label(
            totals_frame,
            text="Total Credits: 0.0",
            font=("Helvetica", 10, "bold")
        )
        self.total_credits_label.pack(side='left', padx=5)
        
        # Completed credits label
        self.completed_credits_label = ttk.Label(
            totals_frame,
            text="Completed Credits: 0.0",
            font=("Helvetica", 10, "bold")
        )
        self.completed_credits_label.pack(side='left', padx=5)
    
    def upload_file(self):
        filename = filedialog.askopenfilename(
            title="Select Transcript",
            filetypes=(
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            )
        )
        if filename:
            self.file_label.config(text=filename)
            self.status_label.config(text="Processing transcript...")
            try:
                self.courses = self.extract_courses(filename)
                if not self.courses:
                    messagebox.showwarning("Warning", "No courses found in the transcript")
                    self.status_label.config(text="No courses found")
                    return
                self.display_courses()
                self.status_label.config(text="Transcript processed successfully")
            except PyPDF2.errors.PdfReadError:
                messagebox.showerror("Error", "Invalid PDF file. Please select a valid PDF transcript.")
                self.status_label.config(text="Invalid PDF file")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process transcript: {str(e)}")
                self.status_label.config(text="Failed to process transcript")
    
    def extract_courses(self, pdf_path):
        courses = []
        current_college = None
        current_semester = None
        current_year = None

        usf_date_range_regex = re.compile(
            r'(Fall|Spring|Summer)\s+(\d{4}).*?(\d{1,2}/\d{1,2}/\d{4}).*?(\d{1,2}/\d{1,2}/\d{4})',
            re.IGNORECASE
        )
        no_range_semester_regex = re.compile(
            r'^(Fall|Spring|Summer)\s+(\d{4})$',
            re.IGNORECASE
        )

        def detect_college_name(line: str):
            t = line.lower()
            if "hillsborough cc" in t:
                return "Hillsborough CC"
            return None

        valid_grades = {
            "A","A+","A-","B","B+","B-","C","C+","C-",
            "D","D+","D-","F","IP","S"
        }
        dept_num_regex = re.compile(r'^([A-Za-z]+)(\d{3,4}[A-Za-z]?)$')

        def parse_course_line(line: str):
            toks = line.split()
            if len(toks) < 4:
                return None
            m = dept_num_regex.match(toks[0])
            if not m:
                return None

            dept, num = m.group(1), m.group(2)
            remainder = [tok for tok in toks[1:] if tok != 'T']

            idx = next((i for i in range(len(remainder)-1, -1, -1)
                        if remainder[i] in valid_grades), None)
            if idx is None or idx+1 >= len(remainder):
                return None

            grade = remainder[idx]
            try:
                credits = int(remainder[idx+1])
            except ValueError:
                return None

            name = " ".join(remainder[:idx])
            return {
                "College":       current_college,
                "Department":    dept,
                "Course Number": num,
                "Course Name":   name,
                "Grade":         grade,
                "Credit Hours":  credits
            }

        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            lines = []
            for page in reader.pages:
                text = page.extract_text() or ""
                lines.extend(text.splitlines())

        for raw in lines:
            line = raw.strip()
            if not line:
                continue

            m_usf = usf_date_range_regex.search(line)
            if m_usf:
                current_semester = m_usf.group(1).capitalize()
                current_year     = m_usf.group(2)
                current_college  = "The University of South Florida"
                continue

            m_nr = no_range_semester_regex.match(line)
            if m_nr:
                current_semester = m_nr.group(1).capitalize()
                current_year     = m_nr.group(2)
                continue

            col = detect_college_name(line)
            if col:
                current_college = col
                continue

            info = parse_course_line(line)
            if not info:
                continue
            if not (current_college and current_semester and current_year):
                continue

            courses.append({
                "College":       current_college,
                "Department":    info["Department"],
                "Course Number": info["Course Number"],
                "Course Name":   info["Course Name"],
                "Grade":         info["Grade"],
                "Credit Hours":  info["Credit Hours"],
                "Semester":      current_semester,
                "Year":         current_year
            })

        return courses

    def set_flowchart(self, flowchart):
        """Set reference to flowchart page"""
        self.flowchart = flowchart
        
    def display_courses(self):
        # Clear existing semester boxes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Group courses by semester and year
        semester_groups = {}
        for course in self.courses:
            key = (course['Semester'], course['Year'])
            if key not in semester_groups:
                semester_groups[key] = []
            semester_groups[key].append(course)
        
        # Sort semesters chronologically and group by year
        sorted_semesters = sorted(semester_groups.keys(), 
                                key=lambda x: (x[1], {'Spring': 0, 'Summer': 1, 'Fall': 2}[x[0]]))
        
        # Update flowchart if available
        if self.flowchart:
            self.flowchart.load_from_transcript(self.courses)
            
        # Group semesters by year
        year_groups = {}
        for semester, year in sorted_semesters:
            if year not in year_groups:
                year_groups[year] = []
            year_groups[year].append((semester, year))
        
        # Calculate totals
        total_credits = 0.0
        completed_credits = 0.0
        
        # Create a frame for the grid layout
        grid_frame = ttk.Frame(self.scrollable_frame)
        grid_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        current_row = 0
        for year, year_semesters in year_groups.items():
            # Create a frame for each year
            year_frame = ttk.Frame(grid_frame)
            year_frame.grid(row=current_row, column=0, columnspan=3, sticky="ew", pady=(10, 0))
            
            # Add year label
            year_label = ttk.Label(year_frame, text=year, font=("Helvetica", 12, "bold"))
            year_label.pack(anchor='w', padx=5)
            
            # Create semester boxes for this year
            for i, (semester, year) in enumerate(year_semesters):
                # Create a frame for each semester
                semester_frame = ttk.LabelFrame(
                    grid_frame,
                    text=f"{semester} {year}",
                    width=250
                )
                
                # Calculate grid position
                semester_frame.grid(row=current_row + 1, column=i, padx=5, pady=5, sticky="nsew")
                
                # Create treeview for courses
                tree = ttk.Treeview(
                    semester_frame,
                    columns=("Course", "Name", "Grade", "Credits"),
                    show="headings",
                    height=min(len(semester_groups[(semester, year)]), 8)
                )
                
                # Define headings and set column widths
                tree.heading("Course", text="Course")
                tree.heading("Name", text="Name")
                tree.heading("Grade", text="Grade")
                tree.heading("Credits", text="Credits")
                
                # Set column widths
                tree.column("Course", width=80)
                tree.column("Name", width=120)
                tree.column("Grade", width=50)
                tree.column("Credits", width=50)
                
                # Add courses to treeview
                for course in semester_groups[(semester, year)]:
                    # Truncate course name if too long
                    course_name = course['Course Name']
                    if len(course_name) > 20:
                        course_name = course_name[:17] + "..."
                    
                    tree.insert("", "end", values=(
                        f"{course['Department']} {course['Course Number']}",
                        course_name,
                        course['Grade'],
                        course['Credit Hours']
                    ))
                    
                    # Update totals
                    total_credits += float(course['Credit Hours'])
                    if course['Grade'] != 'IP':
                        completed_credits += float(course['Credit Hours'])
                
                tree.pack(fill='both', expand=True, padx=5, pady=5)
                
                # Add total credits for the semester
                semester_total = sum(course['Credit Hours'] for course in semester_groups[(semester, year)])
                total_label = ttk.Label(
                    semester_frame,
                    text=f"Total Credits: {semester_total}",
                    font=("Helvetica", 10, "bold")
                )
                total_label.pack(anchor='e', padx=5, pady=2)
                
                # Configure grid weights
                grid_frame.grid_columnconfigure(i, weight=1)
            
            # Move to next year's row
            current_row += 2
        
        # Update overall totals
        self.total_credits_label.config(text=f"Total Credits: {total_credits:.1f}")
        self.completed_credits_label.config(text=f"Completed Credits: {completed_credits:.1f}")

    def _on_mousewheel(self, event):
        # Handle mouse wheel scrolling
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
