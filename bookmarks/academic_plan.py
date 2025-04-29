import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Course:
    code: str
    name: str
    terms: str

@dataclass
class TrackState:
    name: str
    selected_courses: List[Optional[Course]]
    is_selected: bool = False
    checkbox_var: tk.BooleanVar = field(default_factory=lambda: tk.BooleanVar(value=False))

class AcademicPlanPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg='white', height=900, width=8000)
        self.h_scroll = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set)
        self.canvas.pack(side='top', fill='both', expand=True)
        self.h_scroll.pack(side='bottom', fill='x')
        
        # Initialize course status dictionary
        self.course_status = {}
        
        # Initialize track database
        self.initialize_track_database()
        
        # Initialize track states
        self.track_states: Dict[str, TrackState] = {}
        for track_name in self.TRACK_DATABASE:
            self.track_states[track_name] = TrackState(
                name=track_name,
                selected_courses=[None] * 3  # 3 course slots per track
            )
        
        # Initialize selected_track_electives
        self.selected_track_electives: List[Optional[Course]] = [None] * 8
        
        # Bind mouse wheel to horizontal scrolling
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)
        self.canvas.bind('<Shift-MouseWheel>', self.on_mousewheel)
        self.canvas.bind('<Button-4>', self.on_mousewheel)
        self.canvas.bind('<Button-5>', self.on_mousewheel)
        
        # Define colors and styles
        self.COLORS = {
            'empty_box': '#006747',  # USF Green
            'empty_box_text': 'white',
            'selected_box': 'white',
            'selected_box_text': 'black',
            'unselected_box': '#E6F3FF',  # Light blue
            'unselected_box_text': 'gray',
            'info_button': '#4FC3F7',
            'clear_button': '#FF0000',
            'title_bg': 'lightgray'
        }
        
        # Track UI elements
        self.track_ui_elements = {}
        
        self.draw_general_education_requirements()
        self.draw_required_ee_coursework()
        self.draw_track_selection()
        self.draw_core_electives()
        self.draw_tech_electives()

    def initialize_track_database(self):
        """Initialize the track and course database"""
        self.TRACK_DATABASE = {
            "Bioelectrical Systems": [
                Course("EEE 4215", "Biomedical Optical Spectroscopy & Imaging", "F"),
                Course("EEE 4260C", "Bioelectricity", "F"),
                Course("EEE 4271", "Bioelectronics", "S"),
                Course("EEE 4410", "System on a Chip", "Last Sem. S 2021"),
                Course("EEE 4506", "Biomedical Image Processing", "Last Sem. S 2021"),
                Course("EEL 3116L", "Laboratory II", "F, S")
            ],
            "Communication Systems": [
                Course("EEE 4423", "Quantum Computing & Communications", "S"),
                Course("EEE 4746", "Wireless Mobile Computing & Security", "F"),
                Course("EEL 4423C", "Wireless Circuits & Systems Design Laboratory", "F, S"),
                Course("EEL 4540", "Radar Systems", "F"),
                Course("EEL 4595", "Mobile and Personal Communication", "Last Sem. F 2021"),
                Course("EEL 4727C", "Dig. Sig. Process. w/ Field Programmable", "S"),
                Course("EEL 4756", "Digital Signal Processing", "F"),
                Course("EEL 4513L", "Wireless Communication Systems Lab", "Not Offered"),
                Course("EEL 4743L", "Microprocessor Laboratory", "F")
            ],
            "Energy, Power, & Sustainability": [
                Course("EEL 4212", "Energy Delivery Systems", "S"),
                Course("EEL 4214", "Electric (Utility) Distribution Systems", "Not Offered"),
                Course("EEL 4224", "Electric Machines & Drives", "F"),
                Course("EEL 4241", "Power Electronics", "S"),
                Course("EEL 4251", "Power System Analysis", "F"),
                Course("EEL 4252", "Power Systems II", "Last Sem. S 2021"),
                Course("EEL 4271", "Power System Protection", "F"),
                Course("EEL 4283", "Sustainable Energy", "Last Sem. F 2021"),
                Course("EEL 4206L", "Electromechanical Energy System Lab", "F, S")
            ],
            "Mechatronics, Robotics, & Embedded Systems": [
                Course("EEL 3100", "Network Analysis and Design", "Last Sem. F 2022"),
                Course("EEL 4663", "Applied Robotics", "F"),
                Course("EEL 4680", "Applied Mechatronics", "S"),
                Course("EEL 4740", "Embedded Systems", "S"),
                Course("EEL 4744", "Microprocessor Principles & Applications", "F"),
                Course("EEL 4657L", "Linear Controls Laboratory", "F, S"),
                Course("EEL 4743L", "Microprocessor Laboratory", "F")
            ],
            "Micro & Nano-scale Systems": [
                Course("EEE 3302", "Electronics I EEE 4274", "F, S"),
                Course("EEE 4359", "Analog CMOS/VLSI Design", "S"),
                Course("EEL 4567", "Electro-Optics", "Last Sem. S 2022"),
                Course("EEL 3116L", "Laboratory II", "F, S")
            ],
            "Wireless Circuits and Systems": [
                Course("EEL 4420", "Radio Freq Microwave Measurement", "F"),
                Course("EEL 4421", "RF/Microwave Circuits I", "F"),
                Course("EEL 4422", "RF/Microwave Circuits II", "S"),
                Course("EEL 4461", "Antenna Theory", "S"),
                Course("EEL 4540", "Radar Systems", "F"),
                Course("EEL 4513L", "Wireless Communication Systems Lab", "Not Offered")
            ],
            "Systems and Security": [
                Course("EEE 4746", "Wireless Mobile Computing & Security", "F"),
                Course("EEE 4748", "Cryptography & Data Security", "S"),
                Course("EEE 4774", "Data Analytics", "S"),
                Course("EEL 4782", "Data Networks, Systems & Security", "F"),
                Course("EEL 4872", "AI & Security in Cyber Physical Systems", "F"),
                Course("EEL 4743L", "Microprocessor Laboratory", "F")
            ]
        }

    def draw_track_selection(self):
        """Draw the track selection interface"""
        # Clear any existing UI elements
        self.canvas.delete("track_selection")
        
        # Position and dimensions
        start_x = 3000
        start_y = 230
        box_width = 450
        box_height = 50
        gap = 10

        # Draw title
        title_box_height = 60
        self.canvas.create_rectangle(
            start_x-5, start_y, 
            start_x + box_width, start_y + title_box_height,
            fill=self.COLORS['title_bg'], outline='black', width=2,
            tags="track_selection"
        )
        self.canvas.create_text(
            start_x + box_width/2, 
            start_y + title_box_height/2,
            text="Select Your Track", 
            font=("Helvetica", 14, "bold"),
            tags="track_selection"
        )

        # Draw track checkboxes
        for i, track_name in enumerate(self.TRACK_DATABASE.keys()):
            y = start_y + title_box_height + gap + i * (box_height + gap)
            
            # Create checkbox frame
            self.canvas.create_rectangle(
                start_x-5, y, 
                start_x + box_width, y + box_height, 
                outline='black', width=2,
                tags="track_selection"
            )
            
            # Create checkbox
            var = tk.BooleanVar(value=self.track_states[track_name].is_selected)
            var.trace_add('write', lambda *args, tn=track_name: self.on_track_selection(tn))
            checkbutton = tk.Checkbutton(
                self.canvas,
                text=track_name,
                variable=var,
                bg='white',
                font=("Helvetica", 11),
            )
            self.canvas.create_window(
                start_x, y + box_height/2,
                window=checkbutton, 
                anchor='w',
                tags="track_selection"
            )
            
            # Store UI reference
            self.track_states[track_name].checkbox_var = var

        # Set up course box area
        self.track_boxes_start_x = start_x + box_width + 100
        self.track_boxes_start_y = start_y

        # Draw initial course boxes
        self.draw_course_boxes()
        
        # Update scroll region
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def draw_course_boxes(self):
        """Draw the course selection boxes for all tracks"""
        # Clear only track course boxes, preserving ENC and core course boxes
        for item in self.canvas.find_withtag("course_box"):
            if not any(tag in self.canvas.gettags(item) for tag in ['enc_1101_box', 'enc_1102_box', 'hum_selector_box', 'soc_selector_box']):
                self.canvas.delete(item)
        
        # Dimensions
        box_w = 220
        box_h = 90
        h_gap = 40
        v_gap = 40
        x0 = self.track_boxes_start_x
        y0 = self.track_boxes_start_y

        # Get selected tracks
        selected_tracks = [
            name for name, state in self.track_states.items() 
            if state.is_selected
        ]

        # Draw boxes for each track position (1-3)
        for row, track_label in enumerate(["Track 1:", "Track 2:", "Track 3 (Optional):"]):
            # Draw track label
            self.canvas.create_text(
                x0, y0 + row * (box_h + v_gap) - 10,
                text=track_label,
                font=("Helvetica", 13, "bold"),
                anchor='w',
                tags="course_box"
            )
            
            if row < len(selected_tracks):
                self.canvas.create_text(
                    x0 + box_w + h_gap + 110,
                    y0 + row * (box_h + v_gap) - 15,
                    text=selected_tracks[row],
                    font=("Helvetica", 13, "bold"),
                    tags="course_box"
                )
                
                track_state = self.track_states[selected_tracks[row]]
                for col in range(3):
                    self.draw_single_course_box(
                        track_state,
                        col,
                        x0 + col * (box_w + h_gap),
                        y0 + row * (box_h + v_gap)
                    )
            else:
                for col in range(3):
                    self.draw_empty_box(
                        x0 + col * (box_w + h_gap),
                        y0 + row * (box_h + v_gap)
                    )

    def draw_single_course_box(self, track_state: TrackState, box_number: int, x: int, y: int):
        """Draw a single course selection box"""
        box_width = 220
        box_height = 90
        
        # Create main box
        box = self.canvas.create_rectangle(
            x, y, x + box_width, y + box_height,
            outline='black', width=2,
            tags="course_box"
        )
        
        # Determine box state and appearance
        course = track_state.selected_courses[box_number]
        if course:
            # Course is selected
            bg_color = self.COLORS['selected_box']
            text_color = self.COLORS['selected_box_text']
            text = f"{course.code}\n{course.name}\n{course.terms}"
            font = ("Helvetica", 11)  # Slightly smaller font for better fit
        else:
            # Empty box
            bg_color = self.COLORS['empty_box']
            text_color = self.COLORS['empty_box_text']
            text = f"Add {track_state.name}\nCourse"
            font = ("Helvetica", 12, "bold")
        
        # Create background
        bg = self.canvas.create_rectangle(
            x+2, y+2, x+box_width-2, y+box_height-2,
            fill=bg_color, outline='',
            tags="course_box"
        )
        self.canvas.tag_lower(bg, box)
        
        # Create text
        text_id = self.canvas.create_text(
            x + box_width/2, y + box_height/2,
            text=text,
            font=font,
            fill=text_color,
            width=box_width-16,
            justify='center',
            tags="course_box"
        )
        
        # Create buttons
        if course:
            # Info button
            info_btn = tk.Button(
                self.canvas,
                text="i",
                font=("Helvetica", 8, "bold"),
                width=2, height=1,
                bg=self.COLORS['info_button'],
                fg='white',
                command=lambda: self.show_course_info(track_state, box_number)
            )
            self.canvas.create_window(
                x + 2, y + 2,
                window=info_btn,
                anchor='nw',
                tags="course_box"
            )
            
            # Clear button
            clear_btn = tk.Button(
                self.canvas,
                text="×",
                font=("Helvetica", 8, "bold"),
                width=2, height=1,
                bg=self.COLORS['clear_button'],
                fg='white',
                command=lambda: self.clear_course(track_state, box_number)
            )
            self.canvas.create_window(
                x + box_width - 25, y + 2,
                window=clear_btn,
                anchor='nw',
                tags="course_box"
            )
        
        # Add click binding for empty boxes
        if not course:
            for item in (box, bg, text_id):
                self.canvas.tag_bind(
                    item,
                    '<Button-1>',
                    lambda e, ts=track_state, bn=box_number, cx=x, cy=y: 
                        self.open_course_selector(ts, bn, cx, cy)
                )

    def draw_empty_box(self, x: int, y: int):
        """Draw an empty box for unselected track positions"""
        box_width = 220
        box_height = 90
        
        # Create box with light blue background
        self.canvas.create_rectangle(
            x, y, x + box_width, y + box_height,
            outline='black', width=2,
            tags="course_box"
        )
        self.canvas.create_rectangle(
            x+2, y+2, x+box_width-2, y+box_height-2,
            fill=self.COLORS['unselected_box'],
            outline='',
            tags="course_box"
        )

    def on_track_selection(self, track_name: str):
        """Handle track selection/deselection"""
        is_selected = self.track_states[track_name].checkbox_var.get()
        
        # Count currently selected tracks
        selected_count = sum(
            1 for state in self.track_states.values()
            if state.checkbox_var.get()
        )
        
        # Enforce maximum of 3 tracks
        if selected_count > 3:
            self.track_states[track_name].checkbox_var.set(False)
            return
        
        # Update track state
        self.track_states[track_name].is_selected = is_selected
        
        # Clear all selected courses if track is unchecked
        if not is_selected:
            self.track_states[track_name].selected_courses = [None] * 3
        
        # Redraw course boxes
        self.draw_course_boxes()

    def open_course_selector(self, track_state: TrackState, box_number: int, x: int, y: int):
        """Open the course selection dialog"""
        try:
            # Create and configure the window
            selector = tk.Toplevel(self)
            selector.title(f"Select {track_state.name} Course")
            
            # Calculate window position relative to main window
            main_x = self.winfo_rootx()
            main_y = self.winfo_rooty()
            window_x = main_x + x + 50
            window_y = main_y + y + 50
            
            # Ensure window is visible on screen
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            window_width = 500
            window_height = 400
            
            if window_x + window_width > screen_width:
                window_x = screen_width - window_width - 50
            if window_y + window_height > screen_height:
                window_y = screen_height - window_height - 50
                
            selector.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
            selector.grab_set()
            selector.configure(bg=self.COLORS['unselected_box'])

            # Create main frame
            main_frame = tk.Frame(selector, bg=self.COLORS['unselected_box'])
            main_frame.pack(fill='both', expand=True, padx=20, pady=20)

            # Title
            title_label = tk.Label(
                main_frame,
                text=f"Choose a {track_state.name} Course:",
                font=("Helvetica", 12, "bold"),
                bg=self.COLORS['unselected_box']
            )
            title_label.pack(pady=(0, 10))

            # Course list
            tree_frame = tk.Frame(main_frame)
            tree_frame.pack(fill='both', expand=True)
            
            tree_scroll = ttk.Scrollbar(tree_frame)
            tree_scroll.pack(side='right', fill='y')
            
            style = ttk.Style()
            style.configure("Treeview", font=("Helvetica", 11), rowheight=30)
            style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
            
            tree = ttk.Treeview(
                tree_frame,
                columns=("Code", "Name", "Term"),
                show="headings",
                height=6,
                selectmode="browse",
                yscrollcommand=tree_scroll.set
            )
            
            tree.column("Code", width=120, anchor="center")
            tree.column("Name", width=250, anchor="w")
            tree.column("Term", width=100, anchor="center")
            
            tree.heading("Code", text="Course Code")
            tree.heading("Name", text="Course Name")
            tree.heading("Term", text="Term(s)")
            
            # Populate courses
            for course in self.TRACK_DATABASE[track_state.name]:
                tree.insert("", "end", values=(course.code, course.name, course.terms))
            
            tree.pack(side='left', fill='both', expand=True)
            tree_scroll.config(command=tree.yview)
            
            # Buttons
            button_frame = tk.Frame(main_frame, bg=self.COLORS['unselected_box'])
            button_frame.pack(fill='x', pady=(20, 0))
            
            def select_course():
                try:
                    selection = tree.selection()
                    if not selection:
                        return
                    
                    values = tree.item(selection[0])['values']
                    if values:
                        # Create course object
                        course = Course(values[0], values[1], values[2])
                        # Update track state
                        track_state.selected_courses[box_number] = course
                        # Redraw course boxes
                        self.draw_course_boxes()
                        selector.destroy()
                except Exception as e:
                    print(f"Error in select_course: {e}")
                    selector.destroy()

            def cancel():
                selector.destroy()

            # Create buttons
            ok_button = tk.Button(
                button_frame,
                text="Select",
                command=select_course,
                font=("Helvetica", 11, "bold"),
                bg=self.COLORS['empty_box'],
                fg='white',
                width=10,
                relief='flat',
                activebackground='#004F2D',
                activeforeground='white'
            )
            ok_button.pack(side='right', padx=5)
            
            cancel_button = tk.Button(
                button_frame,
                text="Cancel",
                command=cancel,
                font=("Helvetica", 11),
                bg=self.COLORS['unselected_box'],
                width=10
            )
            cancel_button.pack(side='right', padx=5)
            
            # Bind events
            tree.bind('<Double-1>', lambda e: select_course())
            selector.bind('<Return>', lambda e: select_course())
            selector.bind('<Escape>', lambda e: cancel())
            
            # Select current course if one exists
            current_course = track_state.selected_courses[box_number]
            if current_course:
                for item in tree.get_children():
                    if tree.item(item)['values'][0] == current_course.code:
                        tree.selection_set(item)
                        tree.see(item)
                        break
                        
        except Exception as e:
            print(f"Error opening course selector: {e}")
            return None

    def clear_course(self, track_state: TrackState, box_number: int):
        """Clear a selected course"""
        track_state.selected_courses[box_number] = None
        self.draw_course_boxes()

    def show_course_info(self, track_state: TrackState, box_number: int):
        """Show detailed course information"""
        course = track_state.selected_courses[box_number]
        if not course:
            return

        win = tk.Toplevel(self)
        win.title(f"Course Info: {course.code}")
        win.geometry("400x200")
        win.configure(bg=self.COLORS['unselected_box'])

        frame = tk.Frame(win, bg=self.COLORS['unselected_box'])
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        info_text = f"Course Code: {course.code}\nName: {course.name}\nTerms Offered: {course.terms}"
        text = tk.Label(
            frame,
            text=info_text,
            font=("Helvetica", 13),
            bg=self.COLORS['unselected_box'],
            fg=self.COLORS['empty_box'],
            justify='left'
        )
        text.pack(fill='both', expand=True, padx=10, pady=10)

        btn = tk.Button(
            frame,
            text="Close",
            command=win.destroy,
            bg=self.COLORS['empty_box'],
            fg='white',
            font=("Helvetica", 11, 'bold'),
            relief='flat',
            activebackground='#004F2D',
            activeforeground='white'
        )
        btn.pack(pady=10)

    def handle_mousewheel(self, event):
        """Handle mousewheel scrolling for horizontal canvas movement"""
        # Handle different event types for different systems
        if event.num == 4:  # Linux scroll up
            self.canvas.xview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas.xview_scroll(1, "units")
        else:  # Windows and macOS
            # Convert vertical scroll to horizontal
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_mousewheel(self, event):
        """Alias for handle_mousewheel for backward compatibility"""
        return self.handle_mousewheel(event)
#########################################################################################################################
    def draw_general_education_requirements(self):
        # Group label
        group_x = 100
        group_y = 60
        self.canvas.create_text(group_x + 200, group_y, text="               General Education Requirements", font=("Helvetica", 16, "bold"), anchor='n')

        box_width = 220
        box_height = 90
        box_gap = 40
        left_margin = group_x + 140
        top_margin = group_y + 40

        # ENC 1101 (interactive)
        enc1101_y = top_margin
        enc1101_box = self.canvas.create_rectangle(left_margin, enc1101_y, left_margin + box_width, enc1101_y + box_height, 
                                                outline='black', width=2, fill='white',
                                                tags=('course_box', 'enc_1101_box'))
        enc1101_text = self.canvas.create_text(
            left_margin + box_width/2,
            enc1101_y + box_height/2,
            text="ENC 1101\nComposition I\n3 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        # Add info button
        info_btn1 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#4FC3F7', fg='white',
                            command=lambda: self.show_course_details_box('ENC', '1101'))
        self.canvas.create_window(left_margin + 2, enc1101_y + 2, window=info_btn1, anchor='nw')

        # Add status button for ENC 1101
        self.status_btn_enc1101 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_enc1101.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "ENC 1101", enc1101_box, self.status_btn_enc1101))
        self.canvas.create_window(left_margin + box_width, enc1101_y + box_height, 
                                window=self.status_btn_enc1101, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("ENC 1101", enc1101_box, self.status_btn_enc1101)

        # ENC 1102 (below ENC 1101, interactive)
        enc1102_y = enc1101_y + box_height + box_gap
        enc1102_box = self.canvas.create_rectangle(left_margin, enc1102_y, left_margin + box_width, enc1102_y + box_height, 
                                                outline='black', width=2, fill='white',
                                                tags=('course_box', 'enc_1102_box'))
        enc1102_text = self.canvas.create_text(
            left_margin + box_width/2,
            enc1102_y + box_height/2,
            text="ENC 1102\nComposition II\n3 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        # Add info button
        info_btn2 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#4FC3F7', fg='white',
                            command=lambda: self.show_course_details_box('ENC', '1102'))
        self.canvas.create_window(left_margin+2, enc1102_y+2, window=info_btn2, anchor='nw')

        # Add status button for ENC 1102
        self.status_btn_enc1102 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_enc1102.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "ENC 1102", enc1102_box, self.status_btn_enc1102))
        self.canvas.create_window(left_margin + box_width, enc1102_y + box_height, 
                                window=self.status_btn_enc1102, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("ENC 1102", enc1102_box, self.status_btn_enc1102)

        # GenEd Core Humanities (course selector)
        hum_y = enc1102_y + box_height + box_gap
        self.selected_humanities_course = getattr(self, 'selected_humanities_course', None) or None
        self.hum_box = self.canvas.create_rectangle(left_margin, hum_y, left_margin + box_width, hum_y + box_height, outline='black', width=2, tags=('course_box', 'hum_selector_box'))
        # Add green background if no course selected
        if not self.selected_humanities_course:
            self.hum_bg = self.canvas.create_rectangle(left_margin+2, hum_y+2, left_margin+box_width-2, hum_y+box_height-2, fill='#006747', outline='')
            self.canvas.tag_lower(self.hum_bg, self.hum_box)
        else:
            self.hum_bg = None
        # Prepare display text
        display_text = self.get_humanities_display_text(self.selected_humanities_course)
        hum_font = ("Helvetica", 13) if self.selected_humanities_course else ("Helvetica", 12, "bold")
        hum_fill = 'white' if not self.selected_humanities_course else 'black'
        self.hum_text = self.canvas.create_text(
            left_margin + box_width/2,
            hum_y + box_height/2,
            text=display_text,
            font=hum_font,
            fill=hum_fill,
            width=box_width-16,
            justify='center'
        )
        # Add info button (only if course is selected)
        self.hum_info_btn = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                    width=2, height=1, bg='#4FC3F7', fg='white',
                                    command=self.show_selected_humanities_info)
        self.canvas.create_window(left_margin + 2, hum_y + 2, window=self.hum_info_btn, anchor='nw')
        # Add clear button (only if course is selected)
        self.hum_clear_btn = tk.Button(self.canvas, text="×", font=("Helvetica", 8, "bold"), 
                                     width=2, height=1, bg='#FF0000', fg='white',
                                     command=self.clear_humanities_selection)
        self.canvas.create_window(left_margin + box_width - 25, hum_y+2, window=self.hum_clear_btn, anchor='nw')

        # Add status button for Humanities
        self.status_btn_hum = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black', state='disabled')
        self.status_btn_hum.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "GenEd Humanities", self.hum_box, self.status_btn_hum))
        self.canvas.create_window(left_margin + box_width, hum_y + box_height, 
                                window=self.status_btn_hum, anchor='se')

        # Update button visibility
        self.update_humanities_buttons()
        self.canvas.tag_bind(self.hum_box, '<Button-1>', lambda e: self.open_humanities_selector(left_margin, hum_y, box_width, box_height))
        self.canvas.tag_bind(self.hum_text, '<Button-1>', lambda e: self.open_humanities_selector(left_margin, hum_y, box_width, box_height))
        if self.hum_bg:
            self.canvas.tag_bind(self.hum_bg, '<Button-1>', lambda e: self.open_humanities_selector(left_margin, hum_y, box_width, box_height))

        # GenEd Core Social Sciences
        soc_y = hum_y + box_height + box_gap
        self.selected_social_course = getattr(self, 'selected_social_course', None) or None
        self.soc_box = self.canvas.create_rectangle(left_margin, soc_y, left_margin + box_width, soc_y + box_height, outline='black', width=2, tags=('course_box', 'soc_selector_box'))
        # Add green background if no course selected
        if not self.selected_social_course:
            self.soc_bg = self.canvas.create_rectangle(left_margin+2, soc_y+2, left_margin+box_width-2, soc_y+box_height-2, fill='#006747', outline='')
            self.canvas.tag_lower(self.soc_bg, self.soc_box)
        else:
            self.soc_bg = None
        # Prepare display text
        display_text = self.get_social_display_text(self.selected_social_course)
        soc_font = ("Helvetica", 13) if self.selected_social_course else ("Helvetica", 12, "bold")
        soc_fill = 'white' if not self.selected_social_course else 'black'
        self.soc_text = self.canvas.create_text(
            left_margin + box_width/2,
            soc_y + box_height/2,
            text=display_text,
            font=soc_font,
            fill=soc_fill,
            width=box_width-16,
            justify='center'
        )
        # Add info button (only if course is selected)
        self.soc_info_btn = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                    width=2, height=1, bg='#4FC3F7', fg='white',
                                    command=self.show_selected_social_info)
        self.canvas.create_window(left_margin + 2, soc_y + 2, window=self.soc_info_btn, anchor='nw')
        # Add clear button (only if course is selected)
        self.soc_clear_btn = tk.Button(self.canvas, text="×", font=("Helvetica", 8, "bold"), 
                                     width=2, height=1, bg='#FF0000', fg='white',
                                     command=self.clear_social_selection)
        self.canvas.create_window(left_margin + box_width - 25, soc_y + 2, window=self.soc_clear_btn, anchor='nw')

        # Add status button for Social Studies
        self.status_btn_soc = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black', state='disabled')
        self.status_btn_soc.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "GenEd Social Studies", self.soc_box, self.status_btn_soc))
        self.canvas.create_window(left_margin + box_width, soc_y + box_height, 
                                window=self.status_btn_soc, anchor='se')

        # Update button visibility and bind events
        self.update_social_buttons()
        self.canvas.tag_bind(self.soc_box, '<Button-1>', lambda e: self.open_social_selector(left_margin, soc_y, box_width, box_height))
        self.canvas.tag_bind(self.soc_text, '<Button-1>', lambda e: self.open_social_selector(left_margin, soc_y, box_width, box_height))
        if self.soc_bg:
            self.canvas.tag_bind(self.soc_bg, '<Button-1>', lambda e: self.open_social_selector(left_margin, soc_y, box_width, box_height))

        # EGN 3000 (below GenEd Core Social Sciences)
        egn3000_y = soc_y + box_height + box_gap
        egn3000_box = self.canvas.create_rectangle(left_margin, egn3000_y, left_margin + box_width, egn3000_y + box_height, outline='black', width=2)
        egn3000_text = self.canvas.create_text(
            left_margin + box_width/2,
            egn3000_y + box_height/2,
            text="EGN 3000\nFoundations of\nEngineering\nRequired F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        # Add info button
        info_btn3 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#4FC3F7', fg='white',
                            command=lambda: self.show_course_details_box('EGN', '3000'))
        self.canvas.create_window(left_margin + 2, egn3000_y + 2, window=info_btn3, anchor='nw')

        # Add status button for EGN 3000
        self.status_btn_egn3000 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_egn3000.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EGN 3000", egn3000_box, self.status_btn_egn3000))
        self.canvas.create_window(left_margin + box_width, egn3000_y + box_height, 
                                window=self.status_btn_egn3000, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EGN 3000", egn3000_box, self.status_btn_egn3000)

        # EGN 3000L (below EGN 3000)
        egn3000l_y = egn3000_y + box_height + box_gap
        egn3000l_box = self.canvas.create_rectangle(left_margin, egn3000l_y, left_margin + box_width, egn3000l_y + box_height, outline='black', width=2)
        egn3000l_text = self.canvas.create_text(
            left_margin + box_width/2,
            egn3000l_y + box_height/2,
            text="EGN 3000L\nFoundations of\nEng Lab\n3 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        # Add info button
        info_btn4 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#4FC3F7', fg='white',
                            command=lambda: self.show_course_details_box('EGN', '3000L'))
        self.canvas.create_window(left_margin + 2, egn3000l_y + 2, window=info_btn4, anchor='nw')

        # Add status button for EGN 3000L
        self.status_btn_egn3000l = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_egn3000l.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EGN 3000L", egn3000l_box, self.status_btn_egn3000l))
        self.canvas.create_window(left_margin + box_width, egn3000l_y + box_height, 
                                window=self.status_btn_egn3000l, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EGN 3000L", egn3000l_box, self.status_btn_egn3000l)

        # Set scroll region
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def get_humanities_display_text(self, course_code):
        if not course_code:
            return "Add GenEd Core Humanities"
        try:
            from courses import courses
        except ImportError:
            return course_code
        # Map code to department and number
        prefix, number = course_code.split()
        course_info = None
        if prefix in courses["University of South Florida"] and number in courses["University of South Florida"][prefix]:
            course_info = courses["University of South Florida"][prefix][number]
        if course_info:
            name = course_info.get('Class Full Name', '')
            credits = course_info.get('Credit Hours', '3')
            # Assume all are F, S, Su for now
            return f"{course_code}\n{name}\n{credits} hrs F, S, Su"
        else:
            return course_code

    def get_social_display_text(self, course_code):
        if not course_code:
            return "Add GenEd Core Social Studies"
        try:
            from courses import courses
        except ImportError:
            return course_code
        # Map code to department and number
        prefix, number = course_code.split()
        course_info = None
        if prefix in courses["University of South Florida"] and number in courses["University of South Florida"][prefix]:
            course_info = courses["University of South Florida"][prefix][number]
        if course_info:
            name = course_info.get('Class Full Name', '')
            credits = course_info.get('Credit Hours', '3')
            # Assume all are F, S, Su for now
            return f"{course_code}\n{name}\n{credits} hrs F, S, Su"
        else:
            return course_code

    def draw_required_ee_coursework(self):
        # Section label
        group_x = 700
        group_y = 40
        self.canvas.create_text(group_x + 350, group_y+20, text="Required EE Coursework", font=("Helvetica", 16, "bold"), anchor='n')

        # Constants for layout
        box_width = 220  # Increased to match first group
        box_height = 90  # Increased to match first group
        h_gap = 60  # Gap between columns
        v_gap = 40   # Gap between rows
        left = group_x + 40
        top = group_y + 60
        
        positions = {}

        # Draw all boxes
        for name, (x, y) in positions.items():
            self.canvas.create_rectangle(x, y, x + box_width, y + box_height, outline='black', width=2)
            self.canvas.create_text(x + box_width/2, y + box_height/2, text=name, font=("Helvetica", 13), justify='center')

        # --- Next column of boxes (to the left of the existing grid) ---
        col2_left = left
        col2_y = top
        col2_gap = box_height + v_gap

        # Row 1: leave blank (no box)

        # Row 2: MAC 2281 / MAC 2311
        mac_box = self.canvas.create_rectangle(col2_left, col2_y + col2_gap, col2_left + box_width, col2_y + col2_gap + box_height, outline='black', width=2)
        mac_text = self.canvas.create_text(
            col2_left + box_width/2,
            col2_y + col2_gap + box_height/2,
            text="MAC 2281\nOr MAC 2311\nCalculus I\n4 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        def show_mac_info():
            try:
                from courses import courses
            except ImportError:
                messagebox.showerror("Error", "Course catalog not available.")
                return
            details = ""
            for prefix, number in [("MAC", "2281"), ("MAC", "2311")]:
                course_info = None
                if prefix in courses["University of South Florida"] and number in courses["University of South Florida"][prefix]:
                    course_info = courses["University of South Florida"][prefix][number]
                if course_info:
                    details += (
                        f"Course: {prefix} {number}\n\n"
                        f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
                        f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
                        f"Description: {course_info.get('Description', 'N/A')}\n\n"
                        f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
                        f"Corequisites: {course_info.get('Coreqs', 'N/A')}\n\n"
                    )
            if not details:
                details = "No details found for MAC 2281 or MAC 2311."
            win = tk.Toplevel(self)
            win.title("Course Info: MAC 2281 / MAC 2311")
            win.geometry("540x420")
            win.configure(bg='#E6F3FF')
            frame = tk.Frame(win, bg='#E6F3FF')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            text_frame = tk.Frame(frame, bg='#E6F3FF')
            text_frame.pack(fill='both', expand=True)
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side='right', fill='y')
            text = tk.Text(
                text_frame,
                font=("Helvetica", 12),
                wrap='word',
                bg='#E6F3FF',
                fg='#006747',
                yscrollcommand=scrollbar.set,
                borderwidth=0,
                highlightthickness=0
            )
            text.insert('1.0', details)
            text.config(state='disabled')
            text.pack(fill='both', expand=True, padx=10, pady=10)
            scrollbar.config(command=text.yview)
            btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
            btn.pack(pady=10)
        info_btn_mac = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=show_mac_info)
        self.canvas.create_window(col2_left + 2, col2_y + col2_gap + 2, window=info_btn_mac, anchor='nw')

        # Add status button for MAC 2281/2311
        self.status_btn_mac = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_mac.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "MAC 2281/2311", mac_box, self.status_btn_mac))
        self.canvas.create_window(col2_left + box_width, col2_y + col2_gap + box_height, 
                                window=self.status_btn_mac, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("MAC 2281/2311", mac_box, self.status_btn_mac)

        # Row 3: PHY 2048
        phy_box = self.canvas.create_rectangle(col2_left, col2_y + 2*col2_gap, col2_left + box_width, col2_y + 2*col2_gap + box_height, outline='black', width=2)
        phy_text = self.canvas.create_text(
            col2_left + box_width/2,
            col2_y + 2*col2_gap + box_height/2,
            text="PHY 2048\nGeneral\nPhysics I\n3 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_phy = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('PHY', '2048'))
        self.canvas.create_window(col2_left + 2, col2_y + 2*col2_gap + 2, window=info_btn_phy, anchor='nw')

        # Add status button for PHY 2048
        self.status_btn_phy = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_phy.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "PHY 2048", phy_box, self.status_btn_phy))
        self.canvas.create_window(col2_left + box_width, col2_y + 2*col2_gap + box_height, 
                                window=self.status_btn_phy, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("PHY 2048", phy_box, self.status_btn_phy)

        # Row 4: PHY 2048L
        phyl_box = self.canvas.create_rectangle(col2_left, col2_y + 3*col2_gap, col2_left + box_width, col2_y + 3*col2_gap + box_height, outline='black', width=2)
        phyl_text = self.canvas.create_text(
            col2_left + box_width/2,
            col2_y + 3*col2_gap + box_height/2,
            text="PHY 2048L\nGeneral\nPhysics I Lab\n1 hr F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_phyl = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('PHY', '2048L'))
        self.canvas.create_window(col2_left + 2, col2_y + 3*col2_gap + 2, window=info_btn_phyl, anchor='nw')

        # Add status button for PHY 2048L
        self.status_btn_phyl = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_phyl.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "PHY 2048L", phyl_box, self.status_btn_phyl))
        self.canvas.create_window(col2_left + box_width, col2_y + 3*col2_gap + box_height, 
                                window=self.status_btn_phyl, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("PHY 2048L", phyl_box, self.status_btn_phyl)

        # Row 5: EEL 3705
        eel_box = self.canvas.create_rectangle(col2_left, col2_y + 4*col2_gap, col2_left + box_width, col2_y + 4*col2_gap + box_height, outline='black', width=2)
        eel_text = self.canvas.create_text(
            col2_left + box_width/2,
            col2_y + 4*col2_gap + box_height/2,
            text="EEL 3705\nFund. Of Digital\nCircuits\n3 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_eel = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '3705'))
        self.canvas.create_window(col2_left + 2, col2_y + 4*col2_gap + 2, window=info_btn_eel, anchor='nw')

        # Row 6: EEL 3705L
        eell_box = self.canvas.create_rectangle(col2_left, col2_y + 5*col2_gap, col2_left + box_width, col2_y + 5*col2_gap + box_height, outline='black', width=2)
        eell_text = self.canvas.create_text(
            col2_left + box_width/2,
            col2_y + 5*col2_gap + box_height/2,
            text="EEL 3705L\nLogic Design\nLab\n1 hr F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_eell = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '3705L'))
        self.canvas.create_window(col2_left + 2, col2_y + 5*col2_gap + 2, window=info_btn_eell, anchor='nw')

        # Add status button for EEL 3705
        self.status_btn_eel = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_eel.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EEL 3705", eel_box, self.status_btn_eel))
        self.canvas.create_window(col2_left + box_width, col2_y + 4*col2_gap + box_height, 
                                window=self.status_btn_eel, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EEL 3705", eel_box, self.status_btn_eel)

        # Add status button for EEL 3705L
        self.status_btn_eell = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_eell.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EEL 3705L", eell_box, self.status_btn_eell))
        self.canvas.create_window(col2_left + box_width, col2_y + 5*col2_gap + box_height, 
                                window=self.status_btn_eell, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EEL 3705L", eell_box, self.status_btn_eell)

        # Shift the rest of the grid to the right
        left = left + box_width + h_gap

        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        # --- Start of new (third) column: Row 1: EGN 3433 / MAP 2302 ---
        col3_left = left
        col3_y = top
        col3_gap = box_height + v_gap

        # Row 1: EGN 3433 / MAP 2302
        mod_box = self.canvas.create_rectangle(col3_left, col3_y, col3_left + box_width, col3_y + box_height, outline='black', width=2)
        mod_text = self.canvas.create_text(
            col3_left + box_width/2,
            col3_y + box_height/2,
            text="EGN 3433\nOr MAP 2302\nMod Anly Eng\n3 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        def show_mod_info():
            try:
                from courses import courses
            except ImportError:
                messagebox.showerror("Error", "Course catalog not available.")
                return
            details = ""
            for prefix, number in [("EGN", "3433"), ("MAP", "2302")]:
                course_info = None
                if prefix in courses["University of South Florida"] and number in courses["University of South Florida"][prefix]:
                    course_info = courses["University of South Florida"][prefix][number]
                if course_info:
                    details += (
                        f"Course: {prefix} {number}\n\n"
                        f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
                        f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
                        f"Description: {course_info.get('Description', 'N/A')}\n\n"
                        f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
                        f"Corequisites: {course_info.get('Coreqs', 'N/A')}\n\n"
                    )
            if not details:
                details = "No details found for EGN 3433 or MAP 2302."
            win = tk.Toplevel(self)
            win.title("Course Info: EGN 3433 / MAP 2302")
            win.geometry("540x420")
            win.configure(bg='#E6F3FF')
            frame = tk.Frame(win, bg='#E6F3FF')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            text_frame = tk.Frame(frame, bg='#E6F3FF')
            text_frame.pack(fill='both', expand=True)
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side='right', fill='y')
            text = tk.Text(
                text_frame,
                font=("Helvetica", 12),
                wrap='word',
                bg='#E6F3FF',
                fg='#006747',
                yscrollcommand=scrollbar.set,
                borderwidth=0,
                highlightthickness=0
            )
            text.insert('1.0', details)
            text.config(state='disabled')
            text.pack(fill='both', expand=True, padx=10, pady=10)
            scrollbar.config(command=text.yview)
            btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
            btn.pack(pady=10)
        info_btn_mod = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=show_mod_info)
        self.canvas.create_window(col3_left + 2, col3_y + 2, window=info_btn_mod, anchor='nw')

        # Add status button for EGN 3433/MAP 2302
        self.status_btn_mod = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_mod.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EGN 3433/MAP 2302", mod_box, self.status_btn_mod))
        self.canvas.create_window(col3_left + box_width, col3_y + box_height, 
                                window=self.status_btn_mod, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EGN 3433/MAP 2302", mod_box, self.status_btn_mod)

        # Row 2: MAC 2282 / MAC 2312
        mac2_box = self.canvas.create_rectangle(col3_left, col3_y + col3_gap, col3_left + box_width, col3_y + col3_gap + box_height, outline='black', width=2)
        mac2_text = self.canvas.create_text(
            col3_left + box_width/2,
            col3_y + col3_gap + box_height/2,
            text="MAC 2282\nOr MAC 2312\nCalculus II\n4 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        def show_mac2_info():
            try:
                from courses import courses
            except ImportError:
                messagebox.showerror("Error", "Course catalog not available.")
                return
            details = ""
            for prefix, number in [("MAC", "2282"), ("MAC", "2312")]:
                course_info = None
                if prefix in courses["University of South Florida"] and number in courses["University of South Florida"][prefix]:
                    course_info = courses["University of South Florida"][prefix][number]
                if course_info:
                    details += (
                        f"Course: {prefix} {number}\n\n"
                        f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
                        f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
                        f"Description: {course_info.get('Description', 'N/A')}\n\n"
                        f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
                        f"Corequisites: {course_info.get('Coreqs', 'N/A')}\n\n"
                    )
            if not details:
                details = "No details found for MAC 2282 or MAC 2312."
            win = tk.Toplevel(self)
            win.title("Course Info: MAC 2282 / MAC 2312")
            win.geometry("540x420")
            win.configure(bg='#E6F3FF')
            frame = tk.Frame(win, bg='#E6F3FF')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            text_frame = tk.Frame(frame, bg='#E6F3FF')
            text_frame.pack(fill='both', expand=True)
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side='right', fill='y')
            text = tk.Text(
                text_frame,
                font=("Helvetica", 12),
                wrap='word',
                bg='#E6F3FF',
                fg='#006747',
                yscrollcommand=scrollbar.set,
                borderwidth=0,
                highlightthickness=0
            )
            text.insert('1.0', details)
            text.config(state='disabled')
            text.pack(fill='both', expand=True, padx=10, pady=10)
            scrollbar.config(command=text.yview)
            btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
            btn.pack(pady=10)
        info_btn_mac2 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=show_mac2_info)
        self.canvas.create_window(col3_left + 2, col3_y + col3_gap + 2, window=info_btn_mac2, anchor='nw')

        # Add status button for MAC 2282/2312
        self.status_btn_mac2 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_mac2.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "MAC 2282/2312", mac2_box, self.status_btn_mac2))
        self.canvas.create_window(col3_left + box_width, col3_y + col3_gap + box_height, 
                                window=self.status_btn_mac2, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("MAC 2282/2312", mac2_box, self.status_btn_mac2)

        # Row 4: CHS 2440L / CHM 2045L
        chs_box = self.canvas.create_rectangle(col3_left, col3_y + 3*col3_gap, col3_left + box_width, col3_y + 3*col3_gap + box_height, outline='black', width=2)
        chs_text = self.canvas.create_text(
            col3_left + box_width/2,
            col3_y + 3*col3_gap + box_height/2,
            text="CHS 2440L\nOr CHM 2045L\nChemistry Lab\n1 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        def show_chs_info():
            try:
                from courses import courses
            except ImportError:
                messagebox.showerror("Error", "Course catalog not available.")
                return
            details = ""
            for prefix, number in [("CHS", "2440L"), ("CHM", "2045L")]:
                course_info = None
                if prefix in courses["University of South Florida"] and number in courses["University of South Florida"][prefix]:
                    course_info = courses["University of South Florida"][prefix][number]
                if course_info:
                    details += (
                        f"Course: {prefix} {number}\n\n"
                        f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
                        f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
                        f"Description: {course_info.get('Description', 'N/A')}\n\n"
                        f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
                        f"Corequisites: {course_info.get('Coreqs', 'N/A')}\n\n"
                    )
            if not details:
                details = "No details found for CHS 2440L or CHM 2045L."
            win = tk.Toplevel(self)
            win.title("Course Info: CHS 2440L / CHM 2045L")
            win.geometry("540x420")
            win.configure(bg='#E6F3FF')
            frame = tk.Frame(win, bg='#E6F3FF')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            text_frame = tk.Frame(frame, bg='#E6F3FF')
            text_frame.pack(fill='both', expand=True)
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side='right', fill='y')
            text = tk.Text(
                text_frame,
                font=("Helvetica", 12),
                wrap='word',
                bg='#E6F3FF',
                fg='#006747',
                yscrollcommand=scrollbar.set,
                borderwidth=0,
                highlightthickness=0
            )
            text.insert('1.0', details)
            text.config(state='disabled')
            text.pack(fill='both', expand=True, padx=10, pady=10)
            scrollbar.config(command=text.yview)
            btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
            btn.pack(pady=10)
        info_btn_chs = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=show_chs_info)
        self.canvas.create_window(col3_left + 2, col3_y + 3*col3_gap + 2, window=info_btn_chs, anchor='nw')

        # Add status button for CHS 2440L/CHM 2045L
        self.status_btn_chs = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_chs.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "CHS 2440L/CHM 2045L", chs_box, self.status_btn_chs))
        self.canvas.create_window(col3_left + box_width, col3_y + 3*col3_gap + box_height, 
                                window=self.status_btn_chs, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("CHS 2440L/CHM 2045L", chs_box, self.status_btn_chs)

        # Row 5: ENC 3246
        enc_box = self.canvas.create_rectangle(col3_left, col3_y + 4*col3_gap, col3_left + box_width, col3_y + 4*col3_gap + box_height, outline='black', width=2)
        enc_text = self.canvas.create_text(
            col3_left + box_width/2,
            col3_y + 4*col3_gap + box_height/2,
            text="ENC 3246\nCommunication\nfor Engineers\n3 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_enc = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('ENC', '3246'))
        self.canvas.create_window(col3_left + 2, col3_y + 4*col3_gap + 2, window=info_btn_enc, anchor='nw')

        # Add status button for ENC 3246
        self.status_btn_enc = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_enc.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "ENC 3246", enc_box, self.status_btn_enc))
        self.canvas.create_window(col3_left + box_width, col3_y + 4*col3_gap + box_height, 
                                window=self.status_btn_enc, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("ENC 3246", enc_box, self.status_btn_enc)

        # Row 6: EGS 2070
        egs2070_box = self.canvas.create_rectangle(col3_left, col3_y + 5*col3_gap, col3_left + box_width, col3_y + 5*col3_gap + box_height, outline='black', width=2)
        egs2070_text = self.canvas.create_text(
            col3_left + box_width/2,
            col3_y + 5*col3_gap + box_height/2,
            text="EGS 2070\nProf. Formation\nof Eng. I\n1 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egs2070 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGS', '2070'))
        self.canvas.create_window(col3_left + 2, col3_y + 5*col3_gap + 2, window=info_btn_egs2070, anchor='nw')

        # Add status button for EGS 2070
        self.status_btn_egs2070 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_egs2070.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EGS 2070", egs2070_box, self.status_btn_egs2070))
        self.canvas.create_window(col3_left + box_width, col3_y + 5*col3_gap + box_height, 
                                window=self.status_btn_egs2070, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EGS 2070", egs2070_box, self.status_btn_egs2070)

        # Start of fourth column
        col4_left = col3_left + box_width + h_gap
        col4_y = top
        col4_gap = box_height + v_gap

        # Row 1: EGN 3373
        egn_box = self.canvas.create_rectangle(col4_left, col4_y, col4_left + box_width, col4_y + box_height, outline='black', width=2)
        egn_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + box_height/2,
            text="EGN 3373\nElectrical\nSystems I\n3 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egn = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGN', '3373'))
        self.canvas.create_window(col4_left + 2, col4_y + 2, window=info_btn_egn, anchor='nw')

        # Add status button for EGN 3373
        self.status_btn_egn = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_egn.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EGN 3373", egn_box, self.status_btn_egn))
        self.canvas.create_window(col4_left + box_width, col4_y + box_height, 
                                window=self.status_btn_egn, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EGN 3373", egn_box, self.status_btn_egn)

        # Row 2: MAC 2283 / MAC 2313
        mac3_box = self.canvas.create_rectangle(col4_left, col4_y + col4_gap, col4_left + box_width, col4_y + col4_gap + box_height, outline='black', width=2)
        mac3_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + col4_gap + box_height/2,
            text="MAC 2283\nOr MAC 2313\nCalculus III\n4 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        def show_mac3_info():
            try:
                from courses import courses
            except ImportError:
                messagebox.showerror("Error", "Course catalog not available.")
                return
            details = ""
            for prefix, number in [("MAC", "2283"), ("MAC", "2313")]:
                course_info = None
                if prefix in courses["University of South Florida"] and number in courses["University of South Florida"][prefix]:
                    course_info = courses["University of South Florida"][prefix][number]
                if course_info:
                    details += (
                        f"Course: {prefix} {number}\n\n"
                        f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
                        f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
                        f"Description: {course_info.get('Description', 'N/A')}\n\n"
                        f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
                        f"Corequisites: {course_info.get('Coreqs', 'N/A')}\n\n"
                    )
            if not details:
                details = "No details found for MAC 2283 or MAC 2313."
            win = tk.Toplevel(self)
            win.title("Course Info: MAC 2283 / MAC 2313")
            win.geometry("540x420")
            win.configure(bg='#E6F3FF')
            frame = tk.Frame(win, bg='#E6F3FF')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            text_frame = tk.Frame(frame, bg='#E6F3FF')
            text_frame.pack(fill='both', expand=True)
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side='right', fill='y')
            text = tk.Text(
                text_frame,
                font=("Helvetica", 12),
                wrap='word',
                bg='#E6F3FF',
                fg='#006747',
                yscrollcommand=scrollbar.set,
                borderwidth=0,
                highlightthickness=0
            )
            text.insert('1.0', details)
            text.config(state='disabled')
            text.pack(fill='both', expand=True, padx=10, pady=10)
            scrollbar.config(command=text.yview)
            btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
            btn.pack(pady=10)
        info_btn_mac3 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=show_mac3_info)
        self.canvas.create_window(col4_left + 2, col4_y + col4_gap + 2, window=info_btn_mac3, anchor='nw')

        # Add status button for MAC 2283/2313
        self.status_btn_mac3 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_mac3.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "MAC 2283/2313", mac3_box, self.status_btn_mac3))
        self.canvas.create_window(col4_left + box_width, col4_y + col4_gap + box_height, 
                                window=self.status_btn_mac3, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("MAC 2283/2313", mac3_box, self.status_btn_mac3)

        # Row 3: EEE 3394
        eee_box = self.canvas.create_rectangle(col4_left, col4_y + 2*col4_gap, col4_left + box_width, col4_y + 2*col4_gap + box_height, outline='black', width=2)
        eee_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + 2*col4_gap + box_height/2,
            text="EEE 3394\nEE Science 1:\nElectronic Mtrls\n3 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_eee = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEE', '3394'))
        self.canvas.create_window(col4_left + 2, col4_y + 2*col4_gap + 2, window=info_btn_eee, anchor='nw')

        # Add status button for EEE 3394
        self.status_btn_eee = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_eee.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EEE 3394", eee_box, self.status_btn_eee))
        self.canvas.create_window(col4_left + box_width, col4_y + 2*col4_gap + box_height, 
                                window=self.status_btn_eee, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EEE 3394", eee_box, self.status_btn_eee)

        # Row 4: CHS 2440 / CHM 2045
        chs_chem_box = self.canvas.create_rectangle(col4_left, col4_y + 3*col4_gap, col4_left + box_width, col4_y + 3*col4_gap + box_height, outline='black', width=2)
        chs_chem_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + 3*col4_gap + box_height/2,
            text="CHS 2440\nOr CHM 2045\nChemistry\n3 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        def show_chs_chem_lecture_info():
            try:
                from courses import courses
            except ImportError:
                messagebox.showerror("Error", "Course catalog not available.")
                return
            details = ""
            for prefix, number in [("CHS", "2440"), ("CHM", "2045")]:
                course_info = None
                if prefix in courses["University of South Florida"] and number in courses["University of South Florida"][prefix]:
                    course_info = courses["University of South Florida"][prefix][number]
                if course_info:
                    details += (
                        f"Course: {prefix} {number}\n\n"
                        f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
                        f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
                        f"Description: {course_info.get('Description', 'N/A')}\n\n"
                        f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
                        f"Corequisites: {course_info.get('Coreqs', 'N/A')}\n\n"
                    )
            if not details:
                details = "No details found for CHS 2440 or CHM 2045."
            win = tk.Toplevel(self)
            win.title("Course Info: CHS 2440 / CHM 2045")
            win.geometry("540x420")
            win.configure(bg='#E6F3FF')
            frame = tk.Frame(win, bg='#E6F3FF')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            text_frame = tk.Frame(frame, bg='#E6F3FF')
            text_frame.pack(fill='both', expand=True)
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side='right', fill='y')
            text = tk.Text(
                text_frame,
                font=("Helvetica", 12),
                wrap='word',
                bg='#E6F3FF',
                fg='#006747',
                yscrollcommand=scrollbar.set,
                borderwidth=0,
                highlightthickness=0
            )
            text.insert('1.0', details)
            text.config(state='disabled')
            text.pack(fill='both', expand=True, padx=10, pady=10)
            scrollbar.config(command=text.yview)
            btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
            btn.pack(pady=10)
        info_btn_chs_chem = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=show_chs_chem_lecture_info)
        self.canvas.create_window(col4_left + 2, col4_y + 3*col4_gap + 2, window=info_btn_chs_chem, anchor='nw')

        # Add status button for CHS 2440/CHM 2045
        self.status_btn_chs_chem = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_chs_chem.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "CHS 2440/CHM 2045", chs_chem_box, self.status_btn_chs_chem))
        self.canvas.create_window(col4_left + box_width, col4_y + 3*col4_gap + box_height, 
                                window=self.status_btn_chs_chem, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("CHS 2440/CHM 2045", chs_chem_box, self.status_btn_chs_chem)

        # Row 5: EGN 3615
        egn_econ_box = self.canvas.create_rectangle(col4_left, col4_y + 4*col4_gap, col4_left + box_width, col4_y + 4*col4_gap + box_height, outline='black', width=2)
        egn_econ_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + 4*col4_gap + box_height/2,
            text="EGN 3615\nEng Economics\n3 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egn_econ = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGN', '3615'))
        self.canvas.create_window(col4_left + 2, col4_y + 4*col4_gap + 2, window=info_btn_egn_econ, anchor='nw')

        # Add status button for EGN 3615
        self.status_btn_egn_econ = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_egn_econ.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EGN 3615", egn_econ_box, self.status_btn_egn_econ))
        self.canvas.create_window(col4_left + box_width, col4_y + 4*col4_gap + box_height, 
                                window=self.status_btn_egn_econ, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EGN 3615", egn_econ_box, self.status_btn_egn_econ)

        # Row 6: EGS 3071
        egs3071_box = self.canvas.create_rectangle(col4_left, col4_y + 5*col4_gap, col4_left + box_width, col4_y + 5*col4_gap + box_height, outline='black', width=2)
        egs3071_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + 5*col4_gap + box_height/2,
            text="EGS 3071\nProf. Formation\nof Eng. II\n1 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egs3071 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGS', '3071'))
        self.canvas.create_window(col4_left + 2, col4_y + 5*col4_gap + 2, window=info_btn_egs3071, anchor='nw')

        # Add status button for EGS 3071
        self.status_btn_egs3071 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_egs3071.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EGS 3071", egs3071_box, self.status_btn_egs3071))
        self.canvas.create_window(col4_left + box_width, col4_y + 5*col4_gap + box_height, 
                                window=self.status_btn_egs3071, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EGS 3071", egs3071_box, self.status_btn_egs3071)

        # Start of fifth column
        col5_left = col4_left + box_width + h_gap
        col5_y = top
        col5_gap = box_height + v_gap

        # Row 4: EGN 3420
        egn_analysis_box = self.canvas.create_rectangle(col5_left, col5_y + 3*col5_gap, col5_left + box_width, col5_y + 3*col5_gap + box_height, outline='black', width=2)
        egn_analysis_text = self.canvas.create_text(
            col5_left + box_width/2,
            col5_y + 3*col5_gap + box_height/2,
            text="EGN 3420\nEngineering\nAnalysis\n3 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egn_analysis = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGN', '3420'))
        self.canvas.create_window(col5_left + 2, col5_y + 3*col5_gap + 2, window=info_btn_egn_analysis, anchor='nw')

        # Add status button for EGN 3420
        self.status_btn_egn_analysis = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_egn_analysis.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EGN 3420", egn_analysis_box, self.status_btn_egn_analysis))
        self.canvas.create_window(col5_left + box_width, col5_y + 3*col5_gap + box_height, 
                                window=self.status_btn_egn_analysis, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EGN 3420", egn_analysis_box, self.status_btn_egn_analysis)

        # Row 6: EGS 3072
        egs_box = self.canvas.create_rectangle(col5_left, col5_y + 5*col5_gap, col5_left + box_width, col5_y + 5*col5_gap + box_height, outline='black', width=2)
        egs_text = self.canvas.create_text(
            col5_left + box_width/2,
            col5_y + 5*col5_gap + box_height/2,
            text="EGS 3072\nProf. Formation\nof Eng. III\n1 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egs = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGS', '3072'))
        self.canvas.create_window(col5_left + 2, col5_y + 5*col5_gap + 2, window=info_btn_egs, anchor='nw')

        # Add status button for EGS 3072
        self.status_btn_egs3072 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                                width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_egs3072.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EGS 3072", egs_box, self.status_btn_egs3072))
        self.canvas.create_window(col5_left + box_width, col5_y + 5*col5_gap + box_height, 
                                window=self.status_btn_egs3072, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EGS 3072", egs_box, self.status_btn_egs3072)

        # Start of sixth column
        col6_left = col5_left + box_width + h_gap
        col6_y = top
        col6_gap = box_height + v_gap

        # Row 2: EEL 3472C
        eel_science_box = self.canvas.create_rectangle(col6_left, col6_y + col6_gap, col6_left + box_width, col6_y + col6_gap + box_height, outline='black', width=2)
        eel_science_text = self.canvas.create_text(
            col6_left + box_width/2,
            col6_y + col6_gap + box_height/2,
            text="EEL 3472C\nEE Science II -\nElectroMag\n3 hrs F, S, Su",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_eel_science = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '3472C'))
        self.canvas.create_window(col6_left + 2, col6_y + col6_gap + 2, window=info_btn_eel_science, anchor='nw')

        # Add status button for EEL 3472C
        self.status_btn_eel_science = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_eel_science.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EEL 3472C", eel_science_box, self.status_btn_eel_science))
        self.canvas.create_window(col6_left + box_width, col6_y + col6_gap + box_height, 
                                window=self.status_btn_eel_science, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EEL 3472C", eel_science_box, self.status_btn_eel_science)

        # Row 6: EEL 2161
        eel_comp_box = self.canvas.create_rectangle(col6_left, col6_y + 5*col6_gap, col6_left + box_width, col6_y + 5*col6_gap + box_height, outline='black', width=2)
        eel_comp_text = self.canvas.create_text(
            col6_left + box_width/2,
            col6_y + 5*col6_gap + box_height/2,
            text="EEL 2161\nEE Comp.\nMethods\n1 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_eel_comp = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '2161'))
        self.canvas.create_window(col6_left + 2, col6_y + 5*col6_gap + 2, window=info_btn_eel_comp, anchor='nw')

        # Add status button for EEL 2161
        self.status_btn_eel_comp = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_eel_comp.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EEL 2161", eel_comp_box, self.status_btn_eel_comp))
        self.canvas.create_window(col6_left + box_width, col6_y + 5*col6_gap + box_height, 
                                window=self.status_btn_eel_comp, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EEL 2161", eel_comp_box, self.status_btn_eel_comp)

        # Shift the rest of the grid to the right
        left = left + box_width + h_gap

        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        # Start of seventh column
        col7_left = col6_left + box_width + h_gap
        col7_y = top
        col7_gap = box_height + v_gap

        # Row 1: EEL 3115L
        lab1_box = self.canvas.create_rectangle(col7_left, col7_y, col7_left + box_width, col7_y + box_height, outline='black', width=2)
        lab1_text = self.canvas.create_text(
            col7_left + box_width/2,
            col7_y + box_height/2,
            text="EEL 3115L\nLab I (circuits)\n1 hr F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_lab1 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '3115L'))
        self.canvas.create_window(col7_left + 2, col7_y + 2, window=info_btn_lab1, anchor='nw')

        # Add status button for EEL 3115L
        self.status_btn_lab1 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_lab1.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EEL 3115L", lab1_box, self.status_btn_lab1))
        self.canvas.create_window(col7_left + box_width, col7_y + box_height, 
                                window=self.status_btn_lab1, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EEL 3115L", lab1_box, self.status_btn_lab1)

        # Row 2: EGN 3374
        egn_sys2_box = self.canvas.create_rectangle(col7_left, col7_y + col7_gap, col7_left + box_width, col7_y + col7_gap + box_height, outline='black', width=2)
        egn_sys2_text = self.canvas.create_text(
            col7_left + box_width/2,
            col7_y + col7_gap + box_height/2,
            text="EGN 3374\nElectrical\nSystems II\n3 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egn_sys2 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGN', '3374'))
        self.canvas.create_window(col7_left + 2, col7_y + col7_gap + 2, window=info_btn_egn_sys2, anchor='nw')

        # Add status button for EGN 3374
        self.status_btn_egn_sys2 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_egn_sys2.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EGN 3374", egn_sys2_box, self.status_btn_egn_sys2))
        self.canvas.create_window(col7_left + box_width, col7_y + col7_gap + box_height, 
                                window=self.status_btn_egn_sys2, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EGN 3374", egn_sys2_box, self.status_btn_egn_sys2)

        # Row 4: EEL 4102
        signals_box = self.canvas.create_rectangle(col7_left, col7_y + 3*col7_gap, col7_left + box_width, col7_y + 3*col7_gap + box_height, outline='black', width=2)
        signals_text = self.canvas.create_text(
            col7_left + box_width/2,
            col7_y + 3*col7_gap + box_height/2,
            text="EEL 4102\nSignals &\nSystems\n3 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_signals = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '4102'))
        self.canvas.create_window(col7_left + 2, col7_y + 3*col7_gap + 2, window=info_btn_signals, anchor='nw')

        # Row 5: EEL 3163C
        comp_tools_box = self.canvas.create_rectangle(col7_left, col7_y + 4*col7_gap, col7_left + box_width, col7_y + 4*col7_gap + box_height, outline='black', width=2)
        comp_tools_text = self.canvas.create_text(
            col7_left + box_width/2,
            col7_y + 4*col7_gap + box_height/2,
            text="EEL 3163C\nComp Tools\n1 hr F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_comp_tools = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '3163C'))
        self.canvas.create_window(col7_left + 2, col7_y + 4*col7_gap + 2, window=info_btn_comp_tools, anchor='nw')

        # Add status button for EEL 3163C
        self.status_btn_comp_tools = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_comp_tools.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EEL 3163C", comp_tools_box, self.status_btn_comp_tools))
        self.canvas.create_window(col7_left + box_width, col7_y + 4*col7_gap + box_height, 
                                window=self.status_btn_comp_tools, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EEL 3163C", comp_tools_box, self.status_btn_comp_tools)

        # Row 6: EEL 4835
        prog_design_box = self.canvas.create_rectangle(col7_left, col7_y + 5*col7_gap, col7_left + box_width, col7_y + 5*col7_gap + box_height, outline='black', width=2)
        prog_design_text = self.canvas.create_text(
            col7_left + box_width/2,
            col7_y + 5*col7_gap + box_height/2,
            text="EEL 4835\nProgramming\nDesign\n3 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_prog_design = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '4835'))
        self.canvas.create_window(col7_left + 2, col7_y + 5*col7_gap + 2, window=info_btn_prog_design, anchor='nw')

        # Add status button for EEL 4835
        self.status_btn_prog_design = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_prog_design.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EEL 4835", prog_design_box, self.status_btn_prog_design))
        self.canvas.create_window(col7_left + box_width, col7_y + 5*col7_gap + box_height, 
                                window=self.status_btn_prog_design, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EEL 4835", prog_design_box, self.status_btn_prog_design)

        # Shift the rest of the grid to the right
        left = left + box_width + h_gap

        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        info_btn_signals = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '4102'))
        self.canvas.create_window(col7_left + 2, col7_y + 3*col7_gap + 2, window=info_btn_signals, anchor='nw')

        # Add status button for EEL 4102
        self.status_btn_signals = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_signals.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EEL 4102", signals_box, self.status_btn_signals))
        self.canvas.create_window(col7_left + box_width, col7_y + 3*col7_gap + box_height, 
                                window=self.status_btn_signals, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EEL 4102", signals_box, self.status_btn_signals)

        # Row 5: EEL 3163C
        comp_tools_box = self.canvas.create_rectangle(col7_left, col7_y + 4*col7_gap, col7_left + box_width, col7_y + 4*col7_gap + box_height, outline='black', width=2)

    def get_core_elective_display_text(self, course_code):
        if not course_code:
            return "Add Core\nElective"
        try:
            from courses import courses
        except ImportError:
            return course_code
        # Map code to department and number
        prefix, number = course_code.split()
        course_info = None
        if prefix in courses["University of South Florida"] and number in courses["University of South Florida"][prefix]:
            course_info = courses["University of South Florida"][prefix][number]
        if course_info:
            name = course_info.get('Class Full Name', '')
            credits = course_info.get('Credit Hours', '3')
            return f"{course_code}\n{name}\n{credits} hrs F, S"
        else:
            return course_code

    def open_core_elective_selector(self, box_number, x, y, w, h):
        selector = tk.Toplevel(self)
        selector.title("Select Gateway Course")
        selector.geometry(f"500x400+{int(self.winfo_rootx() + x + w//2)}+{int(self.winfo_rooty() + y + h//2)}")
        selector.grab_set()
        selector.configure(bg='#E6F3FF')

        # Create main frame
        main_frame = tk.Frame(selector, bg='#E6F3FF')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title label
        title_label = tk.Label(main_frame, 
                             text="Choose a Gateway Course:", 
                             font=("Helvetica", 12, "bold"),
                             bg='#E6F3FF')
        title_label.pack(pady=(0, 10))
        
        # Create frame for Treeview
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Create Treeview and scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        # Configure style for Treeview
        style = ttk.Style()
        style.configure("Treeview", 
                       font=("Helvetica", 11),
                       rowheight=30)
        style.configure("Treeview.Heading", 
                       font=("Helvetica", 11, "bold"))
        
        # Create Treeview
        tree = ttk.Treeview(tree_frame, 
                           columns=("Code", "Name", "Credits"),
                           show="headings",
                           height=6,
                           selectmode="browse",
                           yscrollcommand=tree_scroll.set)
        
        # Configure columns
        tree.column("Code", width=120, anchor="center")
        tree.column("Name", width=250, anchor="w")
        tree.column("Credits", width=80, anchor="center")
        
        # Configure headings
        tree.heading("Code", text="Course Code")
        tree.heading("Name", text="Course Name")
        tree.heading("Credits", text="Credits")
        
        # Gateway courses data
        gateway_courses = [
            ("EEE 3302", "Electronics I", "F, S", "3"),
            ("EEL 4512C", "Communication Systems", "F, S", "3"),
            ("EGN 3375", "Electromechanical Systems", "F, S", "3"),
            ("EEL 4657", "Linear Control Systems", "F, S", "3"),
            ("EEE 4351C", "Semiconductor Devices", "F, S", "3"),
            ("EEL 4423C", "Wireless Circuits/Systems Lab", "F, S", "3")
        ]
        
        # Insert courses into Treeview
        for course in gateway_courses:
            tree.insert("", "end", values=course)
        
        tree.pack(side='left', fill='both', expand=True)
        tree_scroll.config(command=tree.yview)
        
        # Select current course if set
        current_course = getattr(self, f'selected_core_elective_{box_number}', None)
        if current_course:
            for item in tree.get_children():
                if tree.item(item)['values'][0] == current_course:
                    tree.selection_set(item)
                    tree.see(item)
                    break
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg='#E6F3FF')
        button_frame.pack(fill='x', pady=(20, 0))
        
        def set_course():
            selection = tree.selection()
            if not selection:
                return
            values = tree.item(selection[0])['values']
            if values:
                setattr(self, f'selected_core_elective_{box_number}', values[0])
                text_widget = getattr(self, f'core_text_{box_number}')
                bg_item = getattr(self, f'core_bg_{box_number}', None)
                if bg_item:
                    self.canvas.delete(bg_item)
                    setattr(self, f'core_bg_{box_number}', None)
                display_text = f"{values[0]}\n{values[1]}\n{values[2]} hrs F, S"
                self.canvas.itemconfig(text_widget, 
                                    text=display_text,
                                    fill='black',
                                    font=("Helvetica", 13))
                self.update_core_elective_buttons(box_number)
                
                # Set initial status to "Not Started"
                box_items = [item for item in self.canvas.find_all() if self.canvas.type(item) == 'rectangle']
                box = box_items[box_number - 1] if box_items else None
                if box:
                    status_btn = getattr(self, f'core_status_btn_{box_number}')
                    self.show_course_status_menu_default(f"Gateway Course {box_number}", box, status_btn)
                selector.destroy()
        
        def cancel():
            selector.destroy()
        
        # Create buttons
        ok_button = tk.Button(button_frame,
                            text="Select",
                            command=set_course,
                            font=("Helvetica", 11, "bold"),
                            bg='#006747',
                            fg='white',
                            width=10,
                            relief='flat',
                            activebackground='#004F2D',
                            activeforeground='white')
        ok_button.pack(side='right', padx=5)
        
        cancel_button = tk.Button(button_frame,
                                text="Cancel",
                                command=cancel,
                                font=("Helvetica", 11),
                                bg='#E6F3FF',
                                width=10)
        cancel_button.pack(side='right', padx=5)
        
        # Bind double-click to select
        tree.bind('<Double-1>', lambda e: set_course())
        
        # Bind Return key to select
        selector.bind('<Return>', lambda e: set_course())
        selector.bind('<Escape>', lambda e: cancel())
        
        # Center the window on the screen
        selector.update_idletasks()
        width = selector.winfo_width()
        height = selector.winfo_height()
        x = (selector.winfo_screenwidth() // 2) - (width // 2)
        y = (selector.winfo_screenheight() // 2) - (height // 2)
        selector.geometry(f'{width}x{height}+{x}+{y}')

    def clear_core_elective_selection(self, box_number):
        setattr(self, f'selected_core_elective_{box_number}', None)
        text_widget = getattr(self, f'core_text_{box_number}')
        box = getattr(self, f'core_box_{box_number}')
        
        # Get the coordinates for the green background
        box_coords = self.canvas.coords(box)
        
        # Delete old background if it exists
        old_bg = getattr(self, f'core_bg_{box_number}', None)
        if old_bg:
            self.canvas.delete(old_bg)
        
        # Create new green background
        bg = self.canvas.create_rectangle(
            box_coords[0]+2, box_coords[1]+2, 
            box_coords[2]-2, box_coords[3]-2, 
            fill='#006747', outline=''
        )
        self.canvas.tag_lower(bg, box)
        setattr(self, f'core_bg_{box_number}', bg)
        
        # Update text
        self.canvas.itemconfig(text_widget, 
                             text="Add Gateway\nCourse",
                             font=("Helvetica", 12, "bold"),
                             fill='white')
        
        # Clear the course status
        if f"Gateway Course {box_number}" in self.course_status:
            del self.course_status[f"Gateway Course {box_number}"]
        
        # Reset box color to white
        if box:
            self.canvas.itemconfig(box, fill='')
        
        self.update_core_elective_buttons(box_number)

    def show_selected_core_elective_info(self, box_number):
        course = getattr(self, f'selected_core_elective_{box_number}', None)
        if course:
            prefix, number = course.split()
            try:
                from courses import courses
                course_info = courses["University of South Florida"][prefix][number]
                details = (
                    f"Course: {prefix} {number}\n\n"
                    f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
                    f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
                    f"Description: {course_info.get('Description', 'N/A')}\n\n"
                    f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
                    f"Corequisites: {course_info.get('Coreqs', 'N/A')}"
                )
            except (ImportError, KeyError):
                # If courses.py is not available or course not found, show basic info
                gateway_courses = {
                    "EEE 3302": ("Electronics I", "3"),
                    "EEL 4512C": ("Communication Systems", "3"),
                    "EGN 3375": ("Electromechanical Systems", "3"),
                    "EEL 4657": ("Linear Control Systems", "3"),
                    "EEE 4351C": ("Semiconductor Devices", "3"),
                    "EEL 4423C": ("RF & Microwave Circuits", "3")
                }
                name, credits = gateway_courses.get(course, ("N/A", "3"))
                details = (
                    f"Course: {course}\n\n"
                    f"Name: {name}\n\n"
                    f"Credits: {credits}\n\n"
                    f"Availability: Fall, Spring"
                )
            win = tk.Toplevel(self)
            win.title(f"Course Info: {course}")
            win.geometry("540x420")
            win.configure(bg='#E6F3FF')
            frame = tk.Frame(win, bg='#E6F3FF')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            text_widget = tk.Text(frame, font=("Helvetica", 13), bg='#E6F3FF', fg='#006747', wrap='word', borderwidth=0, highlightthickness=0)
            text_widget.insert('1.0', details)
            text_widget.config(state='disabled')
            text_widget.pack(fill='both', expand=True, padx=10, pady=10)
            btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
            btn.pack(pady=10)

    def update_core_elective_buttons(self, box_number):
        info_btn = getattr(self, f'core_info_btn_{box_number}')
        clear_btn = getattr(self, f'core_clear_btn_{box_number}')
        status_btn = getattr(self, f'core_status_btn_{box_number}')
        box = getattr(self, f'core_box_{box_number}')
        
        if getattr(self, f'selected_core_elective_{box_number}', None):
            info_btn.config(state='normal')
            clear_btn.config(state='normal')
            status_btn.config(state='normal')
            # Set initial "Not Started" state if no status exists
            if f"Gateway Course {box_number}" not in self.course_status:
                self.show_course_status_menu_default(f"Gateway Course {box_number}", box, status_btn)
        else:
            info_btn.config(state='disabled')
            clear_btn.config(state='disabled')
            status_btn.config(state='disabled', text="○", bg='lightgray')
            # Clear any existing status
            if f"Gateway Course {box_number}" in self.course_status:
                del self.course_status[f"Gateway Course {box_number}"]
            # Reset box color
            if box:
                self.canvas.itemconfig(box, fill='')

    def draw_core_electives(self):
        # Position to the left of track selection
        core_start_x = 2600  # Adjusted position
        core_start_y = 230   # Aligned with track selection
        box_width = 220
        box_height = 90
        core_gap = 40

        # Draw title
        self.canvas.create_text(core_start_x + box_width/2, core_start_y - 20,
                              text="Core Electives", font=("Helvetica", 16, "bold"))

        # Create 4 core elective boxes
        for i in range(4):
            y = core_start_y + i * (box_height + core_gap)
            self.create_core_elective_box(i+1, core_start_x, y)

        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def open_humanities_selector(self, left_margin, hum_y, box_width, box_height):
        selector = tk.Toplevel(self)
        selector.title("Select Humanities Course")
        selector.geometry(f"500x400+{int(self.winfo_rootx() + left_margin + box_width//2)}+{int(self.winfo_rooty() + hum_y + box_height//2)}")
        selector.grab_set()
        tk.Label(selector, text="Choose a course:", font=("Helvetica", 12)).pack(pady=10)
        options = [
            ("ARH 2000", "Art Appreciation"),
            ("HUM 1020", "Introduction to Humanities"),
            ("LIT 2000", "Introduction to Literature"),
            ("MUL 2010", "Music Appreciation"),
            ("PHI 2010", "Introduction to Philosophy"),
            ("THE 2000", "Theatre Appreciation")
        ]
        # Try to get course info from courses.py
        try:
            from courses import courses
        except ImportError:
            courses_dict = {}
        else:
            courses_dict = courses["University of South Florida"]
        # Prepare data for table
        table_data = []
        for code, name in options:
            prefix, number = code.split()
            info = courses_dict.get(prefix, {}).get(number, {})
            credits = info.get('Credit Hours', '3')
            table_data.append((code, name, credits))
        # Treeview setup (no prereq/coreq columns)
        columns = ("Code", "Name", "Credits")
        tree = ttk.Treeview(selector, columns=columns, show="headings", height=6)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110 if col=="Code" else 180, anchor='center')
        for row in table_data:
            tree.insert("", "end", values=row)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        # Select the current course if set
        if self.selected_humanities_course:
            for iid in tree.get_children():
                if tree.item(iid)['values'][0] == self.selected_humanities_course:
                    tree.selection_set(iid)
                    tree.see(iid)
                    break
        def set_course():
            sel = tree.selection()
            if not sel:
                return
            values = tree.item(sel[0])['values']
            self.selected_humanities_course = values[0]
            display_text = f"{values[0]}\n{values[1]}\n{values[2]} hrs F, S, Su"
            self.canvas.itemconfig(self.hum_text, text=display_text)
            self.update_humanities_buttons()
            # Set default "Not Started" state
            self.show_course_status_menu_default("GenEd Humanities", self.hum_box, self.status_btn_hum)
            selector.destroy()
        btn = tk.Button(selector, text="OK", command=set_course, font=("Helvetica", 11, 'bold'), bg='#006747', fg='white', relief='flat', activebackground='#004F2D', activeforeground='white')
        btn.pack(pady=10)
        selector.bind('<Return>', lambda e: set_course())

    def open_social_selector(self, left_margin, soc_y, box_width, box_height):
        selector = tk.Toplevel(self)
        selector.title("Select Social Studies Course")
        selector.geometry(f"500x400+{int(self.winfo_rootx() + left_margin + box_width//2)}+{int(self.winfo_rooty() + soc_y + box_height//2)}")
        selector.grab_set()
        tk.Label(selector, text="Choose a course:", font=("Helvetica", 12)).pack(pady=10)
        options = [
            ("AMH 2010", "American History I"),
            ("AMH 2020", "American History II"),
            ("ANT 2000", "Introduction to Anthropology"),
            ("ECO 2013", "Economic Principles"),
            ("POS 2041", "American National Government"),
            ("PSY 2012", "Introduction to Psychology")
        ]
        # Try to get course info from courses.py
        try:
            from courses import courses
        except ImportError:
            courses_dict = {}
        else:
            courses_dict = courses["University of South Florida"]
        # Prepare data for table
        table_data = []
        for code, name in options:
            prefix, number = code.split()
            info = courses_dict.get(prefix, {}).get(number, {})
            credits = info.get('Credit Hours', '3')
            table_data.append((code, name, credits))
        # Treeview setup (no prereq/coreq columns)
        columns = ("Code", "Name", "Credits")
        tree = ttk.Treeview(selector, columns=columns, show="headings", height=6)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110 if col=="Code" else 180, anchor='center')
        for row in table_data:
            tree.insert("", "end", values=row)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        # Select the current course if set
        if self.selected_social_course:
            for iid in tree.get_children():
                if tree.item(iid)['values'][0] == self.selected_social_course:
                    tree.selection_set(iid)
                    tree.see(iid)
                    break
        def set_course():
            sel = tree.selection()
            if not sel:
                return
            values = tree.item(sel[0])['values']
            self.selected_social_course = values[0]
            display_text = f"{values[0]}\n{values[1]}\n{values[2]} hrs F, S, Su"
            self.canvas.itemconfig(self.soc_text, text=display_text)
            self.update_social_buttons()
            # Set default "Not Started" state
            self.show_course_status_menu_default("GenEd Social Studies", self.soc_box, self.status_btn_soc)
            selector.destroy()
        btn = tk.Button(selector, text="OK", command=set_course, font=("Helvetica", 11, 'bold'), bg='#006747', fg='white', relief='flat', activebackground='#004F2D', activeforeground='white')
        btn.pack(pady=10)
        selector.bind('<Return>', lambda e: set_course())

    def show_course_status_menu_default(self, course_code, box_id, button):
        """Set the default 'Not Started' state for a newly selected course"""
        self.course_status[course_code] = "Not Started"
        self.canvas.itemconfig(box_id, fill="#FF0000")  # Changed from #FFA100 to #FF0000
        button.configure(text="○", bg="lightgray")

    def update_humanities_buttons(self):
        if self.selected_humanities_course:
            self.hum_info_btn.config(state='normal')
            self.hum_clear_btn.config(state='normal')
            self.status_btn_hum.config(state='normal')  # Enable status button when course is selected
            if self.hum_bg:  # Remove green background when course is selected
                self.canvas.delete(self.hum_bg)
                self.hum_bg = None
            # Set initial "Not Started" state if no status exists
            if "GenEd Humanities" not in self.course_status:
                self.show_course_status_menu_default("GenEd Humanities", self.hum_box, self.status_btn_hum)
        else:
            self.hum_info_btn.config(state='disabled')
            self.hum_clear_btn.config(state='disabled')
            self.status_btn_hum.config(state='disabled', text="○", bg='lightgray')  # Reset and disable status button
            # Clear any existing status
            if "GenEd Humanities" in self.course_status:
                del self.course_status["GenEd Humanities"]
            # Restore green background and white text for "Add GenEd" prompt
            if not self.hum_bg:
                coords = self.canvas.coords(self.hum_box)
                self.hum_bg = self.canvas.create_rectangle(
                    coords[0]+2, coords[1]+2, coords[2]-2, coords[3]-2,
                    fill='#006747', outline=''
                )
                self.canvas.tag_lower(self.hum_bg, self.hum_box)
            self.canvas.itemconfig(self.hum_box, fill='')  # Remove any fill color from the box itself
            self.canvas.itemconfig(self.hum_text, fill='white', 
                                 text="Add GenEd Core Humanities",
                                 font=("Helvetica", 12, "bold"))

    def update_social_buttons(self):
        if self.selected_social_course:
            self.soc_info_btn.config(state='normal')
            self.soc_clear_btn.config(state='normal')
            self.status_btn_soc.config(state='normal')  # Enable status button when course is selected
            if self.soc_bg:  # Remove green background when course is selected
                self.canvas.delete(self.soc_bg)
                self.soc_bg = None
            # Set initial "Not Started" state if no status exists
            if "GenEd Social Studies" not in self.course_status:
                self.show_course_status_menu_default("GenEd Social Studies", self.soc_box, self.status_btn_soc)
        else:
            self.soc_info_btn.config(state='disabled')
            self.soc_clear_btn.config(state='disabled')
            self.status_btn_soc.config(state='disabled', text="○", bg='lightgray')  # Reset and disable status button
            # Clear any existing status
            if "GenEd Social Studies" in self.course_status:
                del self.course_status["GenEd Social Studies"]
            # Restore green background and white text for "Add GenEd" prompt
            if not self.soc_bg:
                coords = self.canvas.coords(self.soc_box)
                self.soc_bg = self.canvas.create_rectangle(
                    coords[0]+2, coords[1]+2, coords[2]-2, coords[3]-2,
                    fill='#006747', outline=''
                )
                self.canvas.tag_lower(self.soc_bg, self.soc_box)
            self.canvas.itemconfig(self.soc_box, fill='')  # Remove any fill color from the box itself
            self.canvas.itemconfig(self.soc_text, fill='white',
                                 text="Add GenEd Core Social Studies",
                                 font=("Helvetica", 12, "bold"))

    def clear_humanities_selection(self):
        self.selected_humanities_course = None
        self.update_humanities_buttons()  # This will handle restoring the green background

    def clear_social_selection(self):
        self.selected_social_course = None
        self.update_social_buttons()  # This will handle restoring the green background

    def show_selected_humanities_info(self):
        if self.selected_humanities_course:
            prefix, number = self.selected_humanities_course.split()
            self.show_course_details_box(prefix, number)

    def show_selected_social_info(self):
        if self.selected_social_course:
            prefix, number = self.selected_social_course.split()
            self.show_course_details_box(prefix, number)

    def show_course_details_box(self, prefix, number):
        """Display detailed course information in a popup window."""
        try:
            from courses import courses
            course_info = courses["University of South Florida"][prefix][number]
            details = (
                f"Course: {prefix} {number}\n\n"
                f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
                f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
                f"Description: {course_info.get('Description', 'N/A')}\n\n"
                f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
                f"Corequisites: {course_info.get('Coreqs', 'N/A')}"
            )
        except (ImportError, KeyError):
            # Fallback course details dictionary for when courses.py is not available
            course_details = {
                'ENC 1101': {
                    'name': 'Composition I',
                    'description': 'This course emphasizes the development of effective written communication through analysis and understanding of audience, situation, and purpose.',
                    'prerequisites': 'None',
                    'credits': '3',
                    'terms': 'Fall, Spring, Summer'
                },
                'ENC 1102': {
                    'name': 'Composition II',
                    'description': 'This course emphasizes critical reading, writing, and research. Students will develop strategies for writing effective arguments and papers.',
                    'prerequisites': 'ENC 1101 with a minimum grade of C-',
                    'credits': '3',
                    'terms': 'Fall, Spring, Summer'
                },
                'EEL 4906': {
                    'name': 'Senior Design I',
                    'description': 'First part of the senior design experience, focusing on project planning, requirements gathering, and preliminary design.',
                    'prerequisites': 'Senior Standing in Electrical Engineering',
                    'credits': '3',
                    'terms': 'Fall, Spring'
                },
                'EEL 4914': {
                    'name': 'Senior Design II',
                    'description': 'Second part of the senior design experience, focusing on project implementation, testing, and final documentation.',
                    'prerequisites': 'EEL 4906',
                    'credits': '3',
                    'terms': 'Fall, Spring'
                }
            }

            # Get course code and info
            course_code = f'{prefix} {number}'
            course_info = course_details.get(course_code, {
                'name': 'N/A',
                'description': 'Course information not available',
                'prerequisites': 'N/A',
                'credits': '3',
                'terms': 'N/A'
            })
            
            details = (
                f"Course: {course_code}\n\n"
                f"Name: {course_info['name']}\n\n"
                f"Credits: {course_info['credits']}\n\n"
                f"Description: {course_info['description']}\n\n"
                f"Prerequisites: {course_info['prerequisites']}\n\n"
                f"Terms Offered: {course_info['terms']}"
            )

        # Create popup window
        win = tk.Toplevel(self)
        win.title(f"Course Info: {prefix} {number}")
        win.geometry("540x420")
        win.configure(bg='#E6F3FF')

        # Create main frame
        frame = tk.Frame(win, bg='#E6F3FF')
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create text widget
        text_widget = tk.Text(frame, font=("Helvetica", 13), bg='#E6F3FF', fg='#006747', 
                             wrap='word', borderwidth=0, highlightthickness=0)
        text_widget.insert('1.0', details)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)

        # Add close button
        btn = tk.Button(frame, text="Close", command=win.destroy, 
                       bg='#006747', fg='white', font=("Helvetica", 11, 'bold'),
                       relief='flat', activebackground='#004F2D', activeforeground='white')
        btn.pack(pady=10)

    def open_track1_course_selector(self, box_number, x, y, w, h):
        selector = tk.Toplevel(self)
        selector.title("Select Bioelectrical Systems Course")
        selector.geometry(f"500x400+{int(self.winfo_rootx() + x + w//2)}+{int(self.winfo_rooty() + y + h//2)}")
        selector.grab_set()
        selector.configure(bg='#E6F3FF')

        main_frame = tk.Frame(selector, bg='#E6F3FF')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        title_label = tk.Label(main_frame, 
                             text="Choose a Bioelectrical Systems Course:", 
                             font=("Helvetica", 12, "bold"),
                             bg='#E6F3FF')
        title_label.pack(pady=(0, 10))
        
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True)
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 11), rowheight=30)
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        tree = ttk.Treeview(tree_frame, 
                           columns=("Code", "Name", "Term"),
                           show="headings",
                           height=6,
                           selectmode="browse",
                           yscrollcommand=tree_scroll.set)
        tree.column("Code", width=120, anchor="center")
        tree.column("Name", width=250, anchor="w")
        tree.column("Term", width=100, anchor="center")
        tree.heading("Code", text="Course Code")
        tree.heading("Name", text="Course Name")
        tree.heading("Term", text="Term(s)")
        
        # Use TRACK_COURSE_DATABASES instead of hardcoded list
        track1_courses = self.TRACK_COURSE_DATABASES["Bioelectrical Systems"]
        for course in track1_courses:
            tree.insert("", "end", values=course)
            
        tree.pack(side='left', fill='both', expand=True)
        tree_scroll.config(command=tree.yview)
        current_course = getattr(self, f'selected_track1_course_{box_number}', None)
        if current_course:
            for item in tree.get_children():
                if tree.item(item)['values'][0] == current_course:
                    tree.selection_set(item)
                    tree.see(item)
                    break
        button_frame = tk.Frame(main_frame, bg='#E6F3FF')
        button_frame.pack(fill='x', pady=(20, 0))
        def set_course():
            selection = tree.selection()
            if not selection:
                return
            values = tree.item(selection[0])['values']
            if values:
                setattr(self, f'selected_track1_course_{box_number}', values[0])
                text_widget = getattr(self, f'track1_text_{box_number}')
                bg_item = getattr(self, f'track1_bg_{box_number}', None)
                if bg_item:
                    self.canvas.delete(bg_item)
                    setattr(self, f'track1_bg_{box_number}', None)
                display_text = f"{values[0]}\n{values[1]}\n{values[2]}"
                self.canvas.itemconfig(text_widget, 
                                    text=display_text,
                                    fill='black',
                                    font=("Helvetica", 13))
                self.update_track1_buttons(box_number)
                selector.destroy()
        def cancel():
            selector.destroy()
        ok_button = tk.Button(button_frame,
                            text="Select",
                            command=set_course,
                            font=("Helvetica", 11, "bold"),
                            bg='#006747',
                            fg='white',
                            width=10,
                            relief='flat',
                            activebackground='#004F2D',
                            activeforeground='white')
        ok_button.pack(side='right', padx=5)
        cancel_button = tk.Button(button_frame,
                                text="Cancel",
                                command=cancel,
                                font=("Helvetica", 11),
                                bg='#E6F3FF',
                                width=10)
        cancel_button.pack(side='right', padx=5)
        tree.bind('<Double-1>', lambda e: set_course())
        selector.bind('<Return>', lambda e: set_course())
        selector.bind('<Escape>', lambda e: cancel())
        selector.update_idletasks()
        width = selector.winfo_width()
        height = selector.winfo_height()
        x = (selector.winfo_screenwidth() // 2) - (width // 2)
        y = (selector.winfo_screenheight() // 2) - (height // 2)
        selector.geometry(f'{width}x{height}+{x}+{y}')

    def create_track1_course_box(self, box_number, x, y):
        box_width = 220
        box_height = 90
        box = self.canvas.create_rectangle(x, y, x + box_width, y + box_height, outline='black', width=2)
        setattr(self, f'track1_box_{box_number}', box)
        bg = self.canvas.create_rectangle(x+2, y+2, x+box_width-2, y+box_height-2, fill='#006747', outline='')
        self.canvas.tag_lower(bg, box)
        setattr(self, f'track1_bg_{box_number}', bg)
        text = self.canvas.create_text(
            x + box_width/2,
            y + box_height/2,
            text="Add Track 1\nCourse",
            font=("Helvetica", 12, "bold"),
            fill='white',
            width=box_width-16,
            justify='center'
        )
        setattr(self, f'track1_text_{box_number}', text)
        info_btn = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#4FC3F7', fg='white',
                            command=lambda: self.show_selected_track1_info(box_number))
        self.canvas.create_window(x + 2, y + 2, window=info_btn, anchor='nw')
        setattr(self, f'track1_info_btn_{box_number}', info_btn)
        clear_btn = tk.Button(self.canvas, text="×", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#FF0000', fg='white',
                            command=lambda: self.clear_track1_selection(box_number))
        self.canvas.create_window(x + box_width - 25, y + 2, window=clear_btn, anchor='nw')
        setattr(self, f'track1_clear_btn_{box_number}', clear_btn)
        self.update_track1_buttons(box_number)
        self.canvas.tag_bind(box, '<Button-1>', 
            lambda e: self.open_track1_course_selector(box_number, x, y, box_width, box_height))
        self.canvas.tag_bind(text, '<Button-1>', 
            lambda e: self.open_track1_course_selector(box_number, x, y, box_width, box_height))
        self.canvas.tag_bind(bg, '<Button-1>', 
            lambda e: self.open_track1_course_selector(box_number, x, y, box_width, box_height))

    def clear_track1_selection(self, box_number):
        setattr(self, f'selected_track1_course_{box_number}', None)
        text_widget = getattr(self, f'track1_text_{box_number}')
        box_coords = self.canvas.coords(text_widget)
        x = box_coords[0] - 110
        y = box_coords[1] - 45
        bg = self.canvas.create_rectangle(x+2, y+2, x+218, y+88, fill='#006747', outline='')
        self.canvas.tag_lower(bg)
        setattr(self, f'track1_bg_{box_number}', bg)
        self.canvas.itemconfig(text_widget, 
                             text="Add Track 1\nCourse",
                             font=("Helvetica", 12, "bold"),
                             fill='white')
        self.update_track1_buttons(box_number)

    def show_selected_track1_info(self, box_number):
        course = getattr(self, f'selected_track1_course_{box_number}', None)
        if course:
            # Show a simple info popup for now
            details = course
            win = tk.Toplevel(self)
            win.title(f"Course Info: {course}")
            win.geometry("400x200")
            win.configure(bg='#E6F3FF')
            frame = tk.Frame(win, bg='#E6F3FF')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            text = tk.Label(frame, text=details, font=("Helvetica", 13), bg='#E6F3FF', fg='#006747', justify='left')
            text.pack(fill='both', expand=True, padx=10, pady=10)
            btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
            btn.pack(pady=10)

    def update_track1_buttons(self, box_number):
        info_btn = getattr(self, f'track1_info_btn_{box_number}')
        clear_btn = getattr(self, f'track1_clear_btn_{box_number}')
        if getattr(self, f'selected_track1_course_{box_number}', None):
            info_btn.config(state='normal')
            clear_btn.config(state='normal')
        else:
            info_btn.config(state='disabled')
            clear_btn.config(state='disabled')

    def draw_track1_course_boxes(self, track_name, x, y):
        box_width = 220
        box_height = 90
        gap = 40
        for i in range(3):
            # Draw a white rectangle to clear any previous content in this box area
            self.canvas.create_rectangle(
                x + i * (box_width + gap), y,
                x + i * (box_width + gap) + box_width, y + box_height,
                fill='white', outline='white')
            self.create_track1_course_box(i+1, x + i * (box_width + gap), y)

    # Mapping from track name to course list
    TRACK_COURSE_DATABASES = {
        "Bioelectrical Systems": [
            ("EEE 4215", "Biomedical Optical Spectroscopy & Imaging", "F","3hrs"),
            ("EEE 4260C", "Bioelectricity", "F","3hrs"),
            ("EEE 4271", "Bioelectronics", "S","3hrs"),
            ("EEE 4410", "System on a Chip", "Last Sem. S 2021","3hrs"),
            ("EEE 4506", "Biomedical Image Processing", "Last Sem. S 2021","3hrs"),
            ("EEL 3116L", "Laboratory II", "F, S","1hr"),
        ],
        "Communication Systems": [
            ("EEE 4423", "Quantum Computing & Communications", "S","3hrs"),
            ("EEE 4746", "Wireless Mobile Computing & Security", "F","3hrs"),
            ("EEL 4423C", "Wireless Circuits & Systems Design Laboratory", "F, S","3hrs"),
            ("EEL 4540", "Radar Systems", "F","3hrs"),
            ("EEL 4595", "Mobile and Personal Communication", "Last Sem. F 2021","3hrs"),
            ("EEL 4727C", "Dig. Sig. Process. w/ Field Programmable", "S","3hrs"),
            ("EEL 4756", "Digital Signal Processing", "F","3hrs"),
            ("EEL 4936L", "Wireless Communications Lab", "S","3hrs"),
            ("EEL 4743L", "Microprocessor Laboratory", "F","1hr"),
        ],
        "Energy, Power, & Sustainability": [
            ("EEL 4212", "Energy Delivery Systems", "S", "3hrs"),
            ("EEL 4214", "Electric (Utility) Distribution Systems", "Not Offered", "3hrs"),
            ("EEL 4224", "Electric Machines & Drives", "F", "3hrs"),
            ("EEL 4241", "Power Electronics", "S", "3hrs"),
            ("EEL 4251", "Power System Analysis", "F", "3hrs"),
            ("EEL 4252", "Power Systems II", "Last Sem. S 2021", "3hrs"),
            ("EEL 4271", "Power System Protection", "F", "3hrs"),
            ("EEL 4283", "Sustainable Energy", "Last Sem. F 2021", "3hrs"),
            ("EEL 4206L", "Electromechanical Energy System Lab", "F, S", "1hr"),
        ],
        "Mechatronics, Robotics, & Embedded Systems": [
            ("EEL 3100", "Network Analysis and Design", "Last Sem. F 2022", "3hrs"),
            ("EEL 4663", "Applied Robotics", "F", "3hrs"),
            ("EEL 4680", "Applied Mechatronics", "S", "3hrs"),
            ("EEL 4740", "Embedded Systems", "S", "3hrs"),
            ("EEL 4744", "Microprocessor Principles & Applications", "F", "3hrs"),
            ("EEL 4657L", "Linear Controls Laboratory", "F, S", "1hr"),
            ("EEL 4743L", "Microprocessor Laboratory", "F", "1hr"),
        ],
        "Micro & Nano-scale Systems": [
            ("EEE 3302", "Electronics I", "F, S","3hrs"),
            ("EEE 4359", "Analog CMOS/VLSI Design", "S","3hrs"),
            ("EEL 4567", "Electro-Optics", "Last Sem. S 2022","3hrs"),
            ("EEL 3116L", "Laboratory II", "F, S","1hr"),
        ],
        "Wireless Circuits and Systems": [
            ("EEL 4420", "Radio Freq Microwave Measurement", "F","3hrs"),
            ("EEL 4421", "RF/Microwave Circuits I", "F","3hrs"),
            ("EEL 4422", "RF/Microwave Circuits II", "S","3hrs"),
            ("EEL 4461", "Antenna Theory", "S","3hrs"),
            ("EEL 4540", "Radar Systems", "F","3hrs"),
        ],
        "Systems and Security": [
            ("EEE 4746", "Wireless Mobile Computing & Security", "F","3hrs"),
            ("EEE 4748", "Cryptography & Data Security", "S","3hrs"),
            ("EEE 4774", "Data Analytics", "S","3hrs"),
            ("EEL 4782", "Data Networks, Systems & Security", "F, S, Sum","3hrs"),
            ("EEL 4872", "AI & Security in Cyber Physical Systems", "F","3hrs"),
            ("EEL 4743L", "Microprocessor Laboratory", "F","1hr"),
        ],
        # Add other tracks here as needed, e.g.:
        # "Communication Systems": [...],
        # "Energy, Power, and Sustainability": [...],
    }

    def open_track_course_selector(self, track_name, box_number, x, y, w, h):
        selector = tk.Toplevel(self)
        selector.title(f"Select {track_name} Course")
        selector.geometry(f"500x400+{int(self.winfo_rootx() + x + w//2)}+{int(self.winfo_rooty() + y + h//2)}")
        selector.grab_set()
        selector.configure(bg='#E6F3FF')

        main_frame = tk.Frame(selector, bg='#E6F3FF')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        title_label = tk.Label(main_frame, 
                             text=f"Choose a {track_name} Course:", 
                             font=("Helvetica", 12, "bold"),
                             bg='#E6F3FF')
        title_label.pack(pady=(0, 10))
        
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True)
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 11), rowheight=30)
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        tree = ttk.Treeview(tree_frame, 
                           columns=("Code", "Name", "Term"),
                           show="headings",
                           height=6,
                           selectmode="browse",
                           yscrollcommand=tree_scroll.set)
        tree.column("Code", width=120, anchor="center")
        tree.column("Name", width=250, anchor="w")
        tree.column("Term", width=100, anchor="center")
        tree.heading("Code", text="Course Code")
        tree.heading("Name", text="Course Name")
        tree.heading("Term", text="Term(s)")
        
        # Use TRACK_COURSE_DATABASES for the selected track
        track_courses = self.TRACK_COURSE_DATABASES[track_name]
        for course in track_courses:
            tree.insert("", "end", values=course)
            
        tree.pack(side='left', fill='both', expand=True)
        tree_scroll.config(command=tree.yview)
        current_course = getattr(self, f'selected_{track_name.lower().replace(" ", "_")}_course_{box_number}', None)
        if current_course:
            for item in tree.get_children():
                if tree.item(item)['values'][0] == current_course:
                    tree.selection_set(item)
                    tree.see(item)
                    break
        button_frame = tk.Frame(main_frame, bg='#E6F3FF')
        button_frame.pack(fill='x', pady=(20, 0))
        def set_course():
            selection = tree.selection()
            if not selection:
                return
            values = tree.item(selection[0])['values']
            if values:
                setattr(self, f'selected_{track_name.lower().replace(" ", "_")}_course_{box_number}', values[0])
                text_widget = getattr(self, f'{track_name.lower().replace(" ", "_")}_text_{box_number}')
                bg_item = getattr(self, f'{track_name.lower().replace(" ", "_")}_bg_{box_number}', None)
                if bg_item:
                    self.canvas.delete(bg_item)
                    setattr(self, f'{track_name.lower().replace(" ", "_")}_bg_{box_number}', None)
                display_text = f"{values[0]}\n{values[1]}\n{values[2]}"
                self.canvas.itemconfig(text_widget, 
                                    text=display_text,
                                    fill='black',
                                    font=("Helvetica", 13))
                self.update_track_buttons(track_name, box_number)
                selector.destroy()
        def cancel():
            selector.destroy()
        ok_button = tk.Button(button_frame,
                            text="Select",
                            command=set_course,
                            font=("Helvetica", 11, "bold"),
                            bg='#006747',
                            fg='white',
                            width=10,
                            relief='flat',
                            activebackground='#004F2D',
                            activeforeground='white')
        ok_button.pack(side='right', padx=5)
        cancel_button = tk.Button(button_frame,
                                text="Cancel",
                                command=cancel,
                                font=("Helvetica", 11),
                                bg='#E6F3FF',
                                width=10)
        cancel_button.pack(side='right', padx=5)
        tree.bind('<Double-1>', lambda e: set_course())
        selector.bind('<Return>', lambda e: set_course())
        selector.bind('<Escape>', lambda e: cancel())
        selector.update_idletasks()
        width = selector.winfo_width()
        height = selector.winfo_height()
        x = (selector.winfo_screenwidth() // 2) - (width // 2)
        y = (selector.winfo_screenheight() // 2) - (height // 2)
        selector.geometry(f'{width}x{height}+{x}+{y}')

    def create_track_course_box(self, track_name, box_number, x, y, course_selected=True):
        box_width = 220
        box_height = 90
        
        # Create main box
        box = self.canvas.create_rectangle(
            x, y, x + box_width, y + box_height,
            outline='black', width=2
        )
        
        # Create background
        bg = self.canvas.create_rectangle(
            x+2, y+2, x+box_width-2, y+box_height-2,
            fill='#006747', outline=''
        )
        self.canvas.tag_lower(bg, box)
        
        # Create text
        text = self.canvas.create_text(
            x + box_width/2, y + box_height/2,
            text="Add Track Course",
            font=("Helvetica", 12, "bold"),
            fill='white',
            width=box_width-16,
            justify='center'
        )
        
        # Store references
        for suffix in ['_box', '_bg', '_text']:
            old = getattr(self, f'{track_name.lower().replace(" ", "_")}{suffix}{box_number}', None)
            if old:
                try:
                    if isinstance(old, int):
                        self.canvas.delete(old)
                    else:
                        old.destroy()
                except Exception:
                    pass
                delattr(self, f'{track_name.lower().replace(" ", "_")}{suffix}{box_number}')
        
        # Update references
        setattr(self, f'{track_name.lower().replace(" ", "_")}_box_{box_number}', box)
        setattr(self, f'{track_name.lower().replace(" ", "_")}_bg_{box_number}', bg)
        setattr(self, f'{track_name.lower().replace(" ", "_")}_text_{box_number}', text)
        
        # Add buttons
        info_btn = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#4FC3F7', fg='white',
                            command=lambda: self.show_selected_track_info(track_name, box_number))
        self.canvas.create_window(x + 2, y + 2, window=info_btn, anchor='nw')
        setattr(self, f'{track_name.lower().replace(" ", "_")}_info_btn_{box_number}', info_btn)
        
        clear_btn = tk.Button(self.canvas, text="×", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#FF0000', fg='white',
                            command=lambda: self.clear_track_selection(track_name, box_number))
        self.canvas.create_window(x + box_width - 25, y + 2, window=clear_btn, anchor='nw')
        setattr(self, f'{track_name.lower().replace(" ", "_")}_clear_btn_{box_number}', clear_btn)
        
        self.update_track_buttons(track_name, box_number)
        if course_selected:
            self.canvas.tag_bind(box, '<Button-1>', 
                lambda e: self.open_track_course_selector(track_name, box_number, x, y, box_width, box_height))
            self.canvas.tag_bind(text, '<Button-1>', 
                lambda e: self.open_track_course_selector(track_name, box_number, x, y, box_width, box_height))

    def clear_track_selection(self, track_name, box_number):
        setattr(self, f'selected_{track_name.lower().replace(" ", "_")}_course_{box_number}', None)
        # Get the coordinates for the box
        text_widget = getattr(self, f'{track_name.lower().replace(" ", "_")}_text_{box_number}', None)
        box_coords = self.canvas.coords(text_widget) if text_widget else [0, 0]
        x = box_coords[0] - 110 if box_coords else 0
        y = box_coords[1] - 45 if box_coords else 0
        # Remove all old widgets for this box
        for suffix in ['_bg_', '_box_', '_text_', '_info_btn_', '_clear_btn_']:
            old = getattr(self, f'{track_name.lower().replace(" ", "_")}{suffix}{box_number}', None)
            if old:
                try:
                    if isinstance(old, int):
                        self.canvas.delete(old)
                    else:
                        old.destroy()
                except Exception:
                    pass
                delattr(self, f'{track_name.lower().replace(" ", "_")}{suffix}{box_number}')
        # Recreate the box in the cleared state (green, with text/buttons, but no course)
        self.create_track_course_box(track_name, box_number, x, y, course_selected=True)

    def show_selected_track_info(self, track_name, box_number):
        course = getattr(self, f'selected_{track_name.lower().replace(" ", "_")}_course_{box_number}', None)
        if course:
            # Show a simple info popup for now
            details = course
            win = tk.Toplevel(self)
            win.title(f"Course Info: {course}")
            win.geometry("400x200")
            win.configure(bg='#E6F3FF')
            frame = tk.Frame(win, bg='#E6F3FF')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            text = tk.Label(frame, text=details, font=("Helvetica", 13), bg='#E6F3FF', fg='#006747', justify='left')
            text.pack(fill='both', expand=True, padx=10, pady=10)
            btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
            btn.pack(pady=10)

    def update_track_buttons(self, track_name, box_number):
        info_btn = getattr(self, f'{track_name.lower().replace(" ", "_")}_info_btn_{box_number}')
        clear_btn = getattr(self, f'{track_name.lower().replace(" ", "_")}_clear_btn_{box_number}')
        if getattr(self, f'selected_{track_name.lower().replace(" ", "_")}_course_{box_number}', None):
            info_btn.config(state='normal')
            clear_btn.config(state='normal')
        else:
            info_btn.config(state='disabled')
            clear_btn.config(state='disabled')

    def draw_track_course_boxes(self, track_name, x, y):
        box_width = 220
        box_height = 90
        gap = 40
        for i in range(3):
            # Draw a white rectangle to clear any previous content in this box area
            self.canvas.create_rectangle(
                x + i * (box_width + gap), y,
                x + i * (box_width + gap) + box_width, y + box_height,
                fill='white', outline='white')
            self.create_track_course_box(track_name, i+1, x + i * (box_width + gap), y)

    def draw_tech_electives(self):
        # Position for technical electives - moved further right
        tech_start_x = 4400 # Moved 300 pixels right (from 3500)
        tech_start_y = 230   # Keeping same vertical position
        box_width = 220
        box_height = 90
        tech_gap = 40

        # Draw title
        self.canvas.create_text(tech_start_x + box_width/2-22, tech_start_y - 12,
                              text="Technical Electives:", font=("Helvetica", 14, "bold"))

        # Create 8 technical elective boxes (2 rows of 4)
        for i in range(8):
            row = i // 4
            col = i % 4
            x = tech_start_x + col * (box_width + tech_gap)
            y = tech_start_y + row * (box_height + tech_gap)
            self.create_tech_elective_box(i+1, x, y)

        # Draw Design Courses section
        design_start_x = tech_start_x  # Same x as tech electives
        design_start_y = tech_start_y + 2 * (box_height + tech_gap) +  0# Below tech electives with some spacing

        # Draw Design section title
        self.canvas.create_text(design_start_x + box_width/2-35, design_start_y - 12,
                              text="Design Courses:", font=("Helvetica", 14, "bold"))

        # Draw Design 1 box
        design1_box = self.canvas.create_rectangle(
            design_start_x, design_start_y,
            design_start_x + box_width, design_start_y + box_height,
            outline='black', width=2
        )
        self.canvas.create_text(
            design_start_x + box_width/2, design_start_y + box_height/2,
            text="EEL 4906\nSenior Design I\n3 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        # Add info button for Design 1
        info_btn_design1 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#4FC3F7', fg='white',
                            command=lambda: self.show_course_details_box('EEL', '4906'))
        self.canvas.create_window(design_start_x + 2, design_start_y + 2, window=info_btn_design1, anchor='nw')

        # Add status button for Design 1
        self.status_btn_design1 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_design1.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EEL 4906", design1_box, self.status_btn_design1))
        self.canvas.create_window(design_start_x + box_width, design_start_y + box_height, 
                                window=self.status_btn_design1, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EEL 4906", design1_box, self.status_btn_design1)

        # Draw Design 2 box
        design2_x = design_start_x + box_width + tech_gap
        design2_box = self.canvas.create_rectangle(
            design2_x, design_start_y,
            design2_x + box_width, design_start_y + box_height,
            outline='black', width=2
        )
        self.canvas.create_text(
            design2_x + box_width/2, design_start_y + box_height/2,
            text="EEL 4914\nSenior Design II\n3 hrs F, S",
            font=("Helvetica", 13),
            justify='center'
        )
        # Add info button for Design 2
        info_btn_design2 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#4FC3F7', fg='white',
                            command=lambda: self.show_course_details_box('EEL', '4914'))
        self.canvas.create_window(design2_x + 2, design_start_y + 2, window=info_btn_design2, anchor='nw')

        # Add status button for Design 2
        self.status_btn_design2 = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black')
        self.status_btn_design2.bind('<Button-1>', lambda e: self.show_course_status_menu(e, "EEL 4914", design2_box, self.status_btn_design2))
        self.canvas.create_window(design2_x + box_width, design_start_y + box_height, 
                                window=self.status_btn_design2, anchor='se')
        # Set initial "Not Started" state
        self.show_course_status_menu_default("EEL 4914", design2_box, self.status_btn_design2)

        # Draw Credit Hours text - positioned to the right of Design boxes
        credit_x = design2_x + box_width + tech_gap + 40  # Further right of Design 2 box
        credit_y = design_start_y + box_height/2  # Vertically centered with design boxes
        self.canvas.create_text(
            credit_x, credit_y,
            text="Total Elective Hours (has to be 43 or higher):",
            font=("Helvetica", 14, "bold"),
            justify='left',
            anchor='w'
        )

        # Update scroll region to ensure all elements are visible
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def create_tech_elective_box(self, box_number, x, y):
        box_width = 220
        box_height = 90
        
        # Create the box and store its reference
        box = self.canvas.create_rectangle(x, y, x + box_width, y + box_height, outline='black', width=2)
        setattr(self, f'tech_box_{box_number}', box)
        
        # Add green background if no course selected
        bg = self.canvas.create_rectangle(x+2, y+2, x+box_width-2, y+box_height-2, fill='#006747', outline='')
        self.canvas.tag_lower(bg, box)
        setattr(self, f'tech_bg_{box_number}', bg)
        
        # Create text
        text = self.canvas.create_text(
            x + box_width/2,
            y + box_height/2,
            text="Add Technical\nElective",
            font=("Helvetica", 12, "bold"),
            fill='white',
            width=box_width-16,
            justify='center'
        )
        setattr(self, f'tech_text_{box_number}', text)
        
        # Add info button
        info_btn = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#4FC3F7', fg='white',
                            command=lambda: self.show_selected_tech_elective_info(box_number))
        self.canvas.create_window(x + 2, y + 2, window=info_btn, anchor='nw')
        setattr(self, f'tech_info_btn_{box_number}', info_btn)
        
        # Add clear button
        clear_btn = tk.Button(self.canvas, text="×", font=("Helvetica", 8, "bold"), 
                             width=2, height=1, bg='#FF0000', fg='white',
                             command=lambda: self.clear_tech_elective_selection(box_number))
        self.canvas.create_window(x + box_width - 26, y + 2, window=clear_btn, anchor='nw')
        setattr(self, f'tech_clear_btn_{box_number}', clear_btn)

        # Add status button
        status_btn = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black', state='disabled')
        status_btn.bind('<Button-1>', lambda e: self.show_course_status_menu(e, f"Technical Elective {box_number}", box, status_btn))
        self.canvas.create_window(x + box_width, y + box_height, 
                                window=status_btn, anchor='se')
        setattr(self, f'tech_status_btn_{box_number}', status_btn)
        
        # Update button visibility
        self.update_tech_elective_buttons(box_number)
        
        # Bind click events
        self.canvas.tag_bind(box, '<Button-1>', 
                           lambda e: self.open_tech_elective_selector(box_number, x, y, box_width, box_height))
        self.canvas.tag_bind(text, '<Button-1>', 
                           lambda e: self.open_tech_elective_selector(box_number, x, y, box_width, box_height))

    def open_tech_elective_selector(self, box_number, x, y, w, h):
        selector = tk.Toplevel(self)
        selector.title("Select Technical Elective")
        selector.geometry(f"500x400+{int(self.winfo_rootx() + x + w//2)}+{int(self.winfo_rooty() + y + h//2)}")
        selector.grab_set()
        selector.configure(bg='#E6F3FF')

        # Create main frame
        main_frame = tk.Frame(selector, bg='#E6F3FF')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title label
        title_label = tk.Label(main_frame, 
                             text="Choose a Technical Elective:", 
                             font=("Helvetica", 12, "bold"),
                             bg='#E6F3FF')
        title_label.pack(pady=(0, 10))
        
        # Create frame for Treeview
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Create Treeview and scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        # Configure style for Treeview
        style = ttk.Style()
        style.configure("Treeview", 
                       font=("Helvetica", 11),
                       rowheight=30)
        style.configure("Treeview.Heading", 
                       font=("Helvetica", 11, "bold"))
        
        # Create Treeview
        tree = ttk.Treeview(tree_frame, 
                           columns=("Code", "Name", "Credits"),
                           show="headings",
                           height=6,
                           selectmode="browse",
                           yscrollcommand=tree_scroll.set)
        
        # Configure columns
        tree.column("Code", width=120, anchor="center")
        tree.column("Name", width=250, anchor="w")
        tree.column("Credits", width=80, anchor="center")
        
        # Configure headings
        tree.heading("Code", text="Course Code")
        tree.heading("Name", text="Course Name")
        tree.heading("Credits", text="Credits")
        
        # Technical electives data
        tech_electives = [
            ("EEL 3003", "Introduction to Electrical Engineering", "3"),
            ("EEL 3111C", "Circuits I", "4"),
            ("EEL 3112", "Circuits II", "3"),
            ("EEL 3135", "Signals and Systems", "3"),
            ("EEL 3303", "Electronics I", "3"),
            ("EEL 3472", "Electromagnetic Fields", "3"),
            ("EEL 3705", "Digital Logic Design", "3"),
            ("EEL 3705L", "Digital Logic Design Lab", "1"),
            ("EEL 3801", "Engineering Programming", "3"),
            ("EEL 3801L", "Engineering Programming Lab", "1")
        ]
        
        # Insert courses into Treeview
        for course in tech_electives:
            tree.insert("", "end", values=course)
        
        tree.pack(side='left', fill='both', expand=True)
        tree_scroll.config(command=tree.yview)
        
        # Select current course if set
        current_course = getattr(self, f'selected_tech_elective_{box_number}', None)
        if current_course:
            for item in tree.get_children():
                if tree.item(item)['values'][0] == current_course:
                    tree.selection_set(item)
                    tree.see(item)
                    break
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg='#E6F3FF')
        button_frame.pack(fill='x', pady=(20, 0))
        
        def set_course():
            selection = tree.selection()
            if not selection:
                return
            values = tree.item(selection[0])['values']
            if values:
                setattr(self, f'selected_tech_elective_{box_number}', values[0])
                # Update the text and remove green background
                text_widget = getattr(self, f'tech_text_{box_number}')
                bg_item = getattr(self, f'tech_bg_{box_number}', None)
                if bg_item:
                    self.canvas.delete(bg_item)
                    setattr(self, f'tech_bg_{box_number}', None)
                display_text = f"{values[0]}\n{values[1]}\n{values[2]} hrs F, S"
                self.canvas.itemconfig(text_widget, 
                                    text=display_text,
                                    fill='black',
                                    font=("Helvetica", 13))
                self.update_tech_elective_buttons(box_number)
                selector.destroy()
        
        def cancel():
            selector.destroy()
        
        # Create buttons
        ok_button = tk.Button(button_frame,
                            text="Select",
                            command=set_course,
                            font=("Helvetica", 11, "bold"),
                            bg='#006747',
                            fg='white',
                            width=10,
                            relief='flat',
                            activebackground='#004F2D',
                            activeforeground='white')
        ok_button.pack(side='right', padx=5)
        
        cancel_button = tk.Button(button_frame,
                                text="Cancel",
                                command=cancel,
                                font=("Helvetica", 11),
                                bg='#E6F3FF',
                                width=10)
        cancel_button.pack(side='right', padx=5)
        
        # Bind double-click to select
        tree.bind('<Double-1>', lambda e: set_course())
        
        # Bind Return key to select
        selector.bind('<Return>', lambda e: set_course())
        selector.bind('<Escape>', lambda e: cancel())
        
        # Center the window on the screen
        selector.update_idletasks()
        width = selector.winfo_width()
        height = selector.winfo_height()
        x = (selector.winfo_screenwidth() // 2) - (width // 2)
        y = (selector.winfo_screenheight() // 2) - (height // 2)
        selector.geometry(f'{width}x{height}+{x}+{y}')

    def show_selected_tech_elective_info(self, box_number):
        course = getattr(self, f'selected_tech_elective_{box_number}', None)
        if course:
            prefix, number = course.split()
            try:
                from courses import courses
                course_info = courses["University of South Florida"][prefix][number]
                details = (
                    f"Course: {prefix} {number}\n\n"
                    f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
                    f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
                    f"Description: {course_info.get('Description', 'N/A')}\n\n"
                    f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
                    f"Corequisites: {course_info.get('Coreqs', 'N/A')}"
                )
            except (ImportError, KeyError):
                tech_electives = {
                    "EEL 3003": ("Introduction to Electrical Engineering", "3"),
                    "EEL 3111C": ("Circuits I", "4"),
                    "EEL 3112": ("Circuits II", "3"),
                    "EEL 3135": ("Signals and Systems", "3"),
                    "EEL 3303": ("Electronics I", "3"),
                    "EEL 3472": ("Electromagnetic Fields", "3"),
                    "EEL 3705": ("Digital Logic Design", "3"),
                    "EEL 3705L": ("Digital Logic Design Lab", "1"),
                    "EEL 3801": ("Engineering Programming", "3"),
                    "EEL 3801L": ("Engineering Programming Lab", "1")
                }
                name, credits = tech_electives.get(course, ("N/A", "3"))
                details = (
                    f"Course: {course}\n\n"
                    f"Name: {name}\n\n"
                    f"Credits: {credits}\n\n"
                    f"Availability: Fall, Spring"
                )
            win = tk.Toplevel(self)
            win.title(f"Course Info: {course}")
            win.geometry("540x420")
            win.configure(bg='#E6F3FF')
            frame = tk.Frame(win, bg='#E6F3FF')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            text_widget = tk.Text(frame, font=("Helvetica", 13), bg='#E6F3FF', fg='#006747', wrap='word', borderwidth=0, highlightthickness=0)
            text_widget.insert('1.0', details)
            text_widget.config(state='disabled')
            text_widget.pack(fill='both', expand=True, padx=10, pady=10)
            btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
            btn.pack(pady=10)

    def clear_tech_elective_selection(self, box_number):
        setattr(self, f'selected_tech_elective_{box_number}', None)
        text_widget = getattr(self, f'tech_text_{box_number}')
        box = getattr(self, f'tech_box_{box_number}')
        
        # Get the coordinates for the green background
        box_coords = self.canvas.coords(box)
        
        # Delete old background if it exists
        old_bg = getattr(self, f'tech_bg_{box_number}', None)
        if old_bg:
            self.canvas.delete(old_bg)
        
        # Create new green background
        bg = self.canvas.create_rectangle(
            box_coords[0]+2, box_coords[1]+2, 
            box_coords[2]-2, box_coords[3]-2, 
            fill='#006747', outline=''
        )
        self.canvas.tag_lower(bg, box)
        setattr(self, f'tech_bg_{box_number}', bg)
        
        # Update text
        self.canvas.itemconfig(text_widget, 
                             text="Add Technical\nElective",
                             font=("Helvetica", 12, "bold"),
                             fill='white')
        
        # Clear the course status
        if f"Technical Elective {box_number}" in self.course_status:
            del self.course_status[f"Technical Elective {box_number}"]
        
        # Reset box color to white
        if box:
            self.canvas.itemconfig(box, fill='')
        
        self.update_tech_elective_buttons(box_number)

    def update_tech_elective_buttons(self, box_number):
        info_btn = getattr(self, f'tech_info_btn_{box_number}')
        clear_btn = getattr(self, f'tech_clear_btn_{box_number}')
        status_btn = getattr(self, f'tech_status_btn_{box_number}')
        box = getattr(self, f'tech_box_{box_number}')
        
        if getattr(self, f'selected_tech_elective_{box_number}', None):
            info_btn.config(state='normal')
            clear_btn.config(state='normal')
            status_btn.config(state='normal')
            # Set initial "Not Started" state if no status exists
            if f"Technical Elective {box_number}" not in self.course_status:
                self.show_course_status_menu_default(f"Technical Elective {box_number}", box, status_btn)
        else:
            info_btn.config(state='disabled')
            clear_btn.config(state='disabled')
            status_btn.config(state='disabled', text="○", bg='lightgray')

    def draw_sections(self):
        """Redraw all sections of the academic plan"""
        self.canvas.delete('all')  # Clear canvas
        self.draw_general_education_requirements()
        self.draw_required_ee_coursework()
        self.draw_track_selection()
        self.draw_core_electives()
        self.draw_tech_electives()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def open_track_course_selector_old(self, track_name, box_number, x, y, w, h):
        """DEPRECATED: Use open_track_course_selector instead"""
        return self.open_track_course_selector(track_name, box_number, x, y, w, h)

    def show_course_status_menu(self, event, course_code, box_id, button):
        """Show the status menu for course status"""
        # Don't show menu if button is disabled
        if button['state'] == 'disabled':
            return
            
        menu = tk.Menu(self, tearoff=0)
        
        def set_status(status):
            self.course_status[course_code] = status
            # Store current text and font
            text_items = self.canvas.find_overlapping(*self.canvas.coords(box_id))
            text_item = None
            current_text = ""
            current_font = ""
            
            for item in text_items:
                if self.canvas.type(item) == "text":
                    text_item = item
                    break
            
            if text_item:
                current_text = self.canvas.itemcget(text_item, "text")
                current_font = self.canvas.itemcget(text_item, "font")
            
            # Update box appearance based on status
            if status == "Complete":
                self.canvas.itemconfig(box_id, fill="#90EE90")  # Light green
                button.configure(text="✓", bg="#90EE90")
            elif status == "In Progress":
                self.canvas.itemconfig(box_id, fill="#FFD700")  # Gold
                button.configure(text="...", bg="#FFD700")
            else:  # Not Started
                self.canvas.itemconfig(box_id, fill="#FF0000")  # Red
                button.configure(text="○", bg="lightgray")
                
            # Restore text if it was found
            if text_item:
                self.canvas.itemconfig(text_item, text=current_text, font=current_font)
                self.canvas.tag_raise(text_item)

        menu.add_command(label="Complete", command=lambda: set_status("Complete"))
        menu.add_command(label="In Progress", command=lambda: set_status("In Progress"))
        menu.add_command(label="Not Started", command=lambda: set_status("Not Started"))
        
        # Display the menu at button position
        menu.post(event.x_root, event.y_root)

    def create_core_elective_box(self, box_number, x, y):
        box_width = 220
        box_height = 90
        
        # Create the box and store its reference
        box = self.canvas.create_rectangle(x, y, x + box_width, y + box_height, outline='black', width=2)
        setattr(self, f'core_box_{box_number}', box)
        
        # Add green background if no course selected
        bg = self.canvas.create_rectangle(x+2, y+2, x+box_width-2, y+box_height-2, fill='#006747', outline='')
        self.canvas.tag_lower(bg, box)
        setattr(self, f'core_bg_{box_number}', bg)
        
        # Create text
        text = self.canvas.create_text(
            x + box_width/2,
            y + box_height/2,
            text="Add Gateway\nCourse",
            font=("Helvetica", 12, "bold"),
            fill='white',
            width=box_width-16,
            justify='center'
        )
        setattr(self, f'core_text_{box_number}', text)
        
        # Add info button
        info_btn = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#4FC3F7', fg='white',
                            command=lambda: self.show_selected_core_elective_info(box_number))
        self.canvas.create_window(x + 2, y + 2, window=info_btn, anchor='nw')
        setattr(self, f'core_info_btn_{box_number}', info_btn)
        
        # Add clear button
        clear_btn = tk.Button(self.canvas, text="×", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#FF0000', fg='white',
                            command=lambda: self.clear_core_elective_selection(box_number))
        self.canvas.create_window(x + box_width - 25, y + 2, window=clear_btn, anchor='nw')
        setattr(self, f'core_clear_btn_{box_number}', clear_btn)

        # Add status button
        status_btn = tk.Button(self.canvas, text="○", font=("Helvetica", 12, "bold"), 
                              width=2, height=1, bg='lightgray', fg='black', state='disabled')
        status_btn.bind('<Button-1>', lambda e: self.show_course_status_menu(e, f"Gateway Course {box_number}", box, status_btn))
        self.canvas.create_window(x + box_width, y + box_height, 
                                window=status_btn, anchor='se')
        setattr(self, f'core_status_btn_{box_number}', status_btn)
        
        # Update button visibility
        self.update_core_elective_buttons(box_number)
        
        # Bind click events
        self.canvas.tag_bind(box, '<Button-1>', 
            lambda e: self.open_core_elective_selector(box_number, x, y, box_width, box_height))
        self.canvas.tag_bind(text, '<Button-1>', 
            lambda e: self.open_core_elective_selector(box_number, x, y, box_width, box_height))
        self.canvas.tag_bind(bg, '<Button-1>', 
            lambda e: self.open_core_elective_selector(box_number, x, y, box_width, box_height))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Academic Plan")
    page = AcademicPlanPage(root)
    page.pack(fill='both', expand=True)
    root.geometry("1100x900")
    root.mainloop()
