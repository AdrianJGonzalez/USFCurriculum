import tkinter as tk
from tkinter import ttk

class TrackSelector(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.track_vars = {}  # Dictionary to store checkbox variables
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header = ttk.Label(
            self,
            text="Select Your Track(s)",
            font=("Helvetica", 14)
        )
        header.pack(pady=10)
        
        # Create main container
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel for track selection
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        # Create track selection area
        track_frame = ttk.LabelFrame(left_panel, text="Electrical Engineering Tracks")
        track_frame.pack(fill='x', expand=True, padx=5, pady=5)
        
        # Define tracks
        tracks = [
            "1 - Bioelectrical Systems",
            "2 - Communication Systems",
            "3 - Energy, Power and Sustainability",
            "4 - Mechatronics, Robotics and Embedded Systems",
            "5 - Wireless Circuits and Systems",
            "6 - Micro and Nano-Scale Systems",
            "7 - Systems and Security"
        ]
        
        # Create checkboxes for each track
        for track in tracks:
            var = tk.BooleanVar()
            self.track_vars[track] = var
            checkbox = ttk.Checkbutton(
                track_frame,
                text=track,
                variable=var,
                command=self.update_course_list
            )
            checkbox.pack(anchor='w', padx=20, pady=5)
        
        # Right panel for course list
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side='left', fill='both', expand=True)
        
        # Create course list area
        course_frame = ttk.LabelFrame(right_panel, text="Track Courses")
        course_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create Treeview for courses
        columns = ("Track", "PFX", "Number", "Course Name", "Semester")
        self.course_tree = ttk.Treeview(course_frame, columns=columns, show="headings", height=20)
        
        # Define column headings
        self.course_tree.heading("Track", text="Track")
        self.course_tree.heading("PFX", text="PFX")
        self.course_tree.heading("Number", text="Number")
        self.course_tree.heading("Course Name", text="Course Name")
        self.course_tree.heading("Semester", text="Semester")
        
        # Set column widths
        self.course_tree.column("Track", width=50)
        self.course_tree.column("PFX", width=50)
        self.course_tree.column("Number", width=80)
        self.course_tree.column("Course Name", width=300)
        self.course_tree.column("Semester", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(course_frame, orient="vertical", command=self.course_tree.yview)
        self.course_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the Treeview and scrollbar
        self.course_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initialize course data
        self.track_courses = {
            "1": {  # Bioelectrical Systems
                "Spring": [
                    ("EEE", "4410", "System on a Chip"),
                    ("EEE", "4506", "Biomedical Image Processing"),
                    ("EEE", "4271", "Bioelectronics"),
                    ("EEL", "4935", "Intro to Bioengineering")
                ],
                "Fall": [
                    ("EEE", "4260C", "Bioelectricity"),
                    ("EEE", "4274", "MEMS I: Chem/Biomed Sensors")
                ]
            },
            "2": {  # Communication Systems
                "Spring": [
                    ("EEL", "4727C", "Dig Sgnl Process Fld Prgrmble")
                ],
                "Fall": [
                    ("EEL", "4595", "Mobile/Personal Communication"),
                    ("EEL", "4756", "Digital Signal Processing")
                ]
            },
            "3": {  # Energy, Power and Sustainability
                "Spring": [
                    ("EEL", "4206L", "Power Lab"),
                    ("EEL", "4241", "Power Electronics"),
                    ("EEL", "4935", "Design of Solar Power Plants"),
                    ("EEL", "4212", "Energy Delivery Systems")
                ],
                "Fall": [
                    ("EEL", "4206L", "Power Lab"),
                    ("EEL", "4251", "Power System Analysis"),
                    ("EEL", "4224", "Electrical Machines and Drives"),
                    ("EEL", "4283", "Sustainable Energy")
                ]
            },
            "4": {  # Mechatronics, Robotics and Embedded Systems
                "Spring": [
                    ("EEL", "4657L", "Linear Controls Laboratory"),
                    ("EEL", "4740", "EmbedSys"),
                    ("EGN", "3060", "Mechatronics for Innovation")
                ],
                "Fall": [
                    ("EEL", "4657L", "Linear Controls Laboratory"),
                    ("EEL", "4743L", "Microprocessor Laboratory"),
                    ("EEL", "4744", "Microprocessor Principles/Apps"),
                    ("EEL", "4936", "Digital Control Theory")
                ]
            },
            "5": {  # Wireless Circuits and Systems
                "Spring": [
                    ("EEL", "4422", "RF/Microwave Circuits II"),
                    ("EEL", "4461", "Antenna Theory"),
                    ("EEL", "4935", "RF/MW Power Design"),
                    ("EEL", "4936", "Wireless Comm. Lab")
                ],
                "Fall": [
                    ("EEL", "4420", "Radio Freq Microwave Measuremt"),
                    ("EEL", "4421", "RF/Microwave Circuits I"),
                    ("EEL", "4935", "MMIC Design"),
                    ("EEL", "4935", "Wireless Sensor Networks")
                ]
            },
            "6": {  # Micro and Nano-Scale Systems
                "Spring": [
                    ("EEL", "3116L", "Laboratory II"),
                    ("EEL", "4936", "Nanostruc/Matl-Sustainable Sys"),
                    ("EEL", "4301", "Electronics II"),
                    ("EEL", "4567", "Electro-Optics")
                ],
                "Fall": [
                    ("EEL", "3116L", "Laboratory II"),
                    ("EEE", "4274", "MEMS I: Chem/Biomed Sensors"),
                    ("EEE", "4359", "Analog CMOS/VLSI Design"),
                    ("EEL", "4936", "Integrated Circuit Technology")
                ]
            },
            "7": {  # Systems and Security
                "Spring": [
                    ("EEE", "4748", "Cryptography and Data Security"),
                    ("EEE", "4774", "Data Analytics"),
                    ("EEE", "4746", "Wireless Mobile Computing & Security"),
                    ("EEE", "4423", "Quantum Computing and Communications")
                ],
                "Fall": [
                    ("EEL", "4782", "Data Network Systems & Security"),
                    ("EEL", "4872", "AI and Security in Cyber Physical Systems"),
                    ("EEL", "4743L", "Microprocessor Lab"),
                    ("EEL", "4935", "Wireless Sensor Networks")
                ]
            }
        }
    
    def update_course_list(self):
        # Clear current items
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        # Add courses for selected tracks
        for track, var in self.track_vars.items():
            if var.get():
                track_num = track[0]  # Get the track number from the track name
                if track_num in self.track_courses:
                    for semester, courses in self.track_courses[track_num].items():
                        for pfx, number, name in courses:
                            self.course_tree.insert("", "end", values=(
                                track_num,
                                pfx,
                                number,
                                name,
                                semester
                            ))
