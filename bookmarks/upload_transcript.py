import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import json
import PyPDF2
from typing import Optional

class TranscriptPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        style = ttk.Style()
        style.configure('Transcript.Treeview', background='#dcdad5', fieldbackground='#dcdad5')
        style.configure('Transcript.Treeview.Heading', background='#dcdad5', foreground='#303434')
        style.configure('TranscriptFrame.TFrame', background='#dcdad5')
        style.configure('TranscriptLabel.TLabel', background='#dcdad5')
        style.configure('Transcript.TLabelframe', background='#dcdad5')
        style.configure('Transcript.TLabelframe.Label', background='#dcdad5')
        self.courses = []
        self.flowchart = None  # Reference to flowchart
        self.create_widgets()
        
    def create_widgets(self):
        # Configure styles
        style = ttk.Style()
        style.layout('Custom.Vertical.TScrollbar', [
            ('Vertical.Scrollbar.trough', {
                'children': [
                    ('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})
                ],
                'sticky': 'ns'
            })
        ])

        style.configure('Custom.Vertical.TScrollbar',
            troughcolor='#dcdad5',    # Background color of scrollbar track
            background='#303434',     # Thumb (slider) color
            width=22                  # <-- Make vertical scrollbar thicker (adjust here)
        )

        # Configure Treeview styles
        style.configure('Transcript.Treeview', 
                       background='#dcdad5', 
                       fieldbackground='#dcdad5')
        style.configure('Transcript.Treeview.Heading', 
                       background='#dcdad5', 
                       foreground='#303434')
        
        # Configure Frame and Label styles
        style.configure('TranscriptFrame.TFrame', 
                       background='#dcdad5')
        style.configure('TranscriptLabel.TLabel',
                       background='#dcdad5')
        
        # Configure LabelFrame styles - need to configure both the frame and its label
        style.configure('Transcript.TLabelframe', 
                       background='#dcdad5')
        style.configure('Transcript.TLabelframe.Label', 
                       background='#dcdad5')

        # Set main frame background
        self.configure(style='TranscriptFrame.TFrame')
        
        # Header
        header = ttk.Label(
            self,
            text="Upload Transcript",
            font=('Helvetica', 20, 'bold'),
            foreground='#006747',
            style='TranscriptLabel.TLabel'
        )
        header.pack(pady=10)
        #PDF scaling notes
        note1 = ttk.Label(
            self,
            text="* PDF Needs to Scale Down to 88%",
            font=('Helvetica', 10),
            style='TranscriptLabel.TLabel'
        )
        note1.pack(pady=(0, 0))

        note2 = ttk.Label(
            self,
            text="* To Save Transcript at 88% Scaled: Print this page -> More settings -> Scale -> 88 -> Save",
            font=('Helvetica', 10),
            style='TranscriptLabel.TLabel'
        )
        note2.pack(pady=(0, 10))       
        # Upload frame
        upload_frame = ttk.LabelFrame(
            self, 
            text="Upload Your Transcript",
            style='Transcript.TLabelframe'
        )
        upload_frame.pack(fill='x', padx=10, pady=5)
        
        # Upload button
        upload_btn = ttk.Button(
            upload_frame,
            text="Choose File",
            command=self.upload_file
        )
        upload_btn.pack(padx=5, pady=10)
        
        # File name label
        self.file_label = ttk.Label(
            upload_frame, 
            text="No file selected",
            style='TranscriptLabel.TLabel'
        )
        self.file_label.pack(pady=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(
            self, 
            text="Upload Status",
            style='Transcript.TLabelframe'
        )
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = ttk.Label(
            status_frame, 
            text="Ready to upload",
            style='TranscriptLabel.TLabel'
        )
        self.status_label.pack(pady=5)
        
        # Create a frame for the semester boxes with horizontal scrolling
        self.semester_frame = ttk.Frame(
            self,
            style='TranscriptFrame.TFrame'
        )
        self.semester_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create canvas with horizontal scrollbar
        self.canvas = tk.Canvas(
            self.semester_frame,
            bg='#dcdad5',
            highlightthickness=0  # Remove canvas border
        )
        self.h_scrollbar = ttk.Scrollbar(
            self.semester_frame, 
            orient="horizontal", 
            command=self.canvas.xview
        )
        self.v_scrollbar = ttk.Scrollbar(
            self.semester_frame,
            orient="vertical",
            command=self.canvas.yview,
            style='Custom.Vertical.TScrollbar'
        )
        self.scrollable_frame = ttk.Frame(
            self.canvas,
            style='TranscriptFrame.TFrame'
        )
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set,yscrollcommand=self.v_scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="top", fill="both", expand=True)
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.v_scrollbar.pack(side="right", fill="x")
        
        # Bind mousewheel to scroll vertically
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)

        # Create totals frame
        totals_frame = ttk.Frame(
            self,
            style='TranscriptFrame.TFrame'
        )
        totals_frame.pack(fill='x', padx=10, pady=5)
        
        # Total credits label
        self.total_credits_label = ttk.Label(
            totals_frame,
            text="Total Credits: 0.0",
            font=("Helvetica", 10, "bold"),
            style='TranscriptLabel.TLabel'
        )
        self.total_credits_label.pack(side='left', padx=5)
        
        # Completed credits label
        self.completed_credits_label = ttk.Label(
            totals_frame,
            text="Completed Credits: 0.0",
            font=("Helvetica", 10, "bold"),
            style='TranscriptLabel.TLabel'
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
            except Exception as e:
                if "Invalid PDF" in str(e):
                    messagebox.showerror("Error", "Invalid PDF file. Please select a valid PDF transcript.")
                    self.status_label.config(text="Invalid PDF file")
                else:
                    messagebox.showerror("Error", f"Failed to process transcript: {str(e)}")
                    self.status_label.config(text="Failed to process transcript")
    
    def extract_courses(self, pdf_path):
        courses = []
        current_college = None
        current_semester = None
        current_year = None

        # USF style: term + year + two dates anywhere on the line
        usf_date_range_regex = re.compile(
            r'(Fall|Spring|Summer)\s+(\d{4}).*?(\d{1,2}/\d{1,2}/\d{4}).*?(\d{1,2}/\d{1,2}/\d{4})',
            re.IGNORECASE
        )
        # Other schools: just term + year
        no_range_semester_regex = re.compile(
            r'^(Fall|Spring|Summer)\s+(\d{4})$',
            re.IGNORECASE
        )

        # Generic institution detection
        inst_regex = re.compile(
            r'\b(College|University|Institute|School|Academy|Polytechnic|CC)\b',
            re.IGNORECASE
        )
        header_blacklist = [
            "transcript", "unofficial", "print", "order", "name:",
            "address:", "student", "test scores", "campus",
            "grade", "credits", "attempted", "earned",
            "quality", "points", "gpa", "admitted",
            "undergraduate", "transfer"
        ]

        def detect_college_name(line: str) -> Optional[str]:
            stripped = line.strip()
            # ignore descriptive lines with commas
            if ',' in stripped:
                return None
            # skip any line with digits
            if any(ch.isdigit() for ch in stripped):
                return None
            low = stripped.lower()
            # skip known header/footer keywords
            if any(kw in low for kw in header_blacklist):
                return None
            # match generic institution keywords
            if inst_regex.search(stripped):
                # Special case for USF
                if "usf" in low or "university of south florida" in low:
                    return "The University of South Florida"
                # Special case for HCC
                if "hillsborough" in low or "hcc" in low:
                    return "HCC"
                # Special case for Valencia
                if "valencia" in low:
                    return "Valencia College"
                return stripped
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
            remainder = [tok for tok in toks[1:] if tok.upper() != 'T']
            # find grade from right
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
                "Department": dept,
                "Course Number": num,
                "Course Name": name,
                "Grade": grade,
                "Credit Hours": credits
            }

        # read all text lines
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
            # USF term with date-range
            m_usf = usf_date_range_regex.search(line)
            if m_usf:
                current_semester = m_usf.group(1).capitalize()
                current_year = m_usf.group(2)
                current_college = "The University of South Florida"
                continue
            # other-school term/year
            m_nr = no_range_semester_regex.match(line)
            if m_nr:
                current_semester = m_nr.group(1).capitalize()
                current_year = m_nr.group(2)
                continue
            # detect college headers
            col = detect_college_name(line)
            if col:
                current_college = col
                continue
            # parse course lines
            info = parse_course_line(line)
            if not info:
                continue
            if not (current_college and current_semester and current_year):
                continue

            # Set transfer flag based on college
            is_transfer = current_college != "The University of South Florida"
            
            course_data = {
                "College": current_college,
                **info,
                "Semester": current_semester,
                "Year": current_year,
                "is_transfer": is_transfer
            }
            courses.append(course_data)

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
        
        # Group semesters by year
        year_groups = {}
        for semester, year in sorted_semesters:
            if year not in year_groups:
                year_groups[year] = []
            year_groups[year].append((semester, year))
        
        # Sort years
        sorted_years = sorted(year_groups.keys())
        
        # Update flowchart if available
        if self.flowchart:
            self.flowchart.load_from_transcript(self.courses)
        
        # Calculate totals
        total_credits = 0.0
        completed_credits = 0.0
        
        # Create a horizontal frame for all years
        year_container = ttk.Frame(self.scrollable_frame)
        year_container.pack(fill='both', expand=True)
        
        # Create year columns side by side
        for i, year in enumerate(sorted_years):
            # Create a frame for the year
            year_frame = ttk.LabelFrame(
                year_container,
                text=str(year),
                width=250
            )
            year_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            
            # Create semester boxes stacked within the year
            for j, (semester, _) in enumerate(year_groups[year]):
                # Create a frame for each semester
                semester_frame = ttk.LabelFrame(
                    year_frame,
                    text=semester,
                    width=250
                )
                semester_frame.pack(fill='x', padx=5, pady=5, expand=True)
                
                # Create treeview for courses
                tree = ttk.Treeview(
                    semester_frame,
                    columns=("Course", "Name", "Grade", "Credits"),
                    show="headings",
                    height=min(len(semester_groups[(semester, year)]), 8),
                    style='Transcript.Treeview'
                )
                
                # Define headings
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
                semester_total = 0
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
                    credits = float(course['Credit Hours'])
                    total_credits += credits
                    semester_total += credits
                    if course['Grade'] != 'IP':
                        completed_credits += credits
                
                tree.pack(fill='both', expand=True, padx=5, pady=5)
                
                # Add total credits for the semester
                total_label = ttk.Label(
                    semester_frame,
                    text=f"Total Credits: {semester_total}",
                    font=("Helvetica", 10, "bold")
                )
                total_label.pack(anchor='e', padx=5, pady=2)
            
            # Configure column weight
            year_container.grid_columnconfigure(i, weight=1)
        
        # Update overall totals
        self.total_credits_label.config(text=f"Total Credits: {total_credits:.1f}")
        self.completed_credits_label.config(text=f"Completed Credits: {completed_credits:.1f}")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_shift_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
