import tkinter as tk
from tkinter import ttk, messagebox

class AcademicPlanPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg='white', height=900, width=8000)
        self.h_scroll = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set)
        self.canvas.pack(side='top', fill='both', expand=True)
        self.h_scroll.pack(side='bottom', fill='x')
        
        # Bind mouse wheel to horizontal scrolling
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)
        self.canvas.bind('<Shift-MouseWheel>', self.on_mousewheel)  # For some systems
        # For Linux and Mac
        self.canvas.bind('<Button-4>', self.on_mousewheel)
        self.canvas.bind('<Button-5>', self.on_mousewheel)
        
        # Track selection variables
        self.track_vars = []
        self.track_checkbuttons = []
        
        self.draw_general_education_requirements()
        self.draw_required_ee_coursework()
        self.draw_track_selection()

    def on_mousewheel(self, event):
        # Handle different event types for different systems
        if event.num == 4:  # Linux scroll up
            self.canvas.xview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas.xview_scroll(1, "units")
        else:  # Windows and macOS
            # Convert vertical scroll to horizontal
            # Adjust the multiplier (-1 or 1) based on your preferred scroll direction
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def draw_track_selection(self):
        # Position to the right of the core electives
        start_x = 3000
        start_y = 230
        box_width = 450
        box_height = 50
        gap = 10

        # Draw Core Electives first
        self.draw_core_electives()

        # Draw title box with gray background
        title_box_height = 60
        self.canvas.create_rectangle(start_x, start_y, start_x + box_width, start_y + title_box_height, 
                                   fill='lightgray', outline='black', width=2)
        self.canvas.create_text(start_x + box_width/2, start_y + title_box_height/2,
                              text="Select Your Track", font=("Helvetica", 14, "bold"))

        # Track options
        self.tracks = [
            "Track 1: Bioelectrical Systems",
            "Track 2: Communication Systems",
            "Track 3: Energy, Power, & Sustainability",
            "Track 4: Mechatronics, Robotics, & Embedded Systems",
            "Track 5: Micro & Nano-scale Systems",
            "Track 6: Wireless Circuits and Systems",
            "Track 7: Systems and Security"
        ]

        # Clear track_vars before creating new checkbuttons
        self.track_vars = []
        self.track_checkbuttons = []
        for i, track in enumerate(self.tracks):
            y = start_y + title_box_height + gap + i * (box_height + gap)
            var = tk.BooleanVar()
            self.track_vars.append(var)
            checkbutton = tk.Checkbutton(
                self.canvas,
                text=track,
                variable=var,
                bg='white',
                font=("Helvetica", 11),
                command=self.on_track_selection
            )
            self.canvas.create_rectangle(start_x, y, start_x + box_width, y + box_height, outline='black', width=2)
            self.canvas.create_window(start_x, y + box_height/2, window=checkbutton, anchor='w')
            self.track_checkbuttons.append(checkbutton)

        # Set up coordinates for dynamic track boxes (just to the right of track selection)
        self.track_boxes_start_x = start_x + box_width + 100
        self.track_boxes_start_y = start_y

        # Ensure the canvas scroll region includes the track selection
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        # Draw dynamic track boxes based on current selection
        self.draw_dynamic_track_boxes()

    def draw_dynamic_track_boxes(self):
        # Remove any previous dynamic widgets (only those we created)
        if not hasattr(self, 'dynamic_track_items'):
            self.dynamic_track_items = []
        for item in self.dynamic_track_items:
            self.canvas.delete(item)
        self.dynamic_track_items = []

        # Remove any previous track course box widgets/items
        if not hasattr(self, 'track_course_box_items'):
            self.track_course_box_items = []
        for item in self.track_course_box_items:
            try:
                if isinstance(item, int):
                    self.canvas.delete(item)
                else:
                    item.destroy()
            except Exception:
                pass
        self.track_course_box_items = []

        # --- Clear state for all possible tracks/boxes (so boxes reset when deselected) ---
        for track in self.TRACK_COURSE_DATABASES.keys():
            for i in range(1, 4):  # Assuming 3 boxes per track
                attr = f'selected_{track}_course_{i}'
                if hasattr(self, attr):
                    setattr(self, attr, None)
                # Also clear text/bg/info_btn/clear_btn attributes if they exist
                for suffix in ['_text_', '_bg_', '_info_btn_', '_clear_btn_']:
                    attr2 = f'{track}{suffix}{i}'
                    if hasattr(self, attr2):
                        delattr(self, attr2)

        # Always show three rows of boxes and labels, updating them based on selected tracks
        box_w = 220
        box_h = 90
        h_gap = 40
        v_gap = 40
        x0 = self.track_boxes_start_x
        y0 = self.track_boxes_start_y

        # Get selected tracks
        selected_tracks = [self.tracks[i] for i, var in enumerate(self.track_vars) if var.get()]
        selected_names = [t.split(': ', 1)[1] for t in selected_tracks]
        n = len(selected_names)

        # If no tracks are selected, clear all possible track course box content
        if n == 0:
            for track in self.TRACK_COURSE_DATABASES.keys():
                for i in range(1, 4):
                    for suffix in ['_bg_', '_text_', '_info_btn_', '_clear_btn_']:
                        attr = f'{track}{suffix}{i}'
                        item = getattr(self, attr, None)
                        if item:
                            if isinstance(item, int):
                                self.canvas.delete(item)
                            elif hasattr(item, 'destroy'):
                                item.destroy()
                            delattr(self, attr)

        # Always show 3 rows
        for row in range(3):
            label = selected_names[row] if row < n else ""
            label_id = self.canvas.create_text(x0 + box_w + h_gap + 100, y0 + row * (box_h + v_gap) - 15, text=label, font=("Helvetica", 16))
            self.dynamic_track_items.append(label_id)
            for col in range(3):
                x = x0 + col * (box_w + h_gap)
                y = y0 + row * (box_h + v_gap)
                box_id = self.canvas.create_rectangle(x, y, x + box_w, y + box_h, outline='black', width=2)
                self.dynamic_track_items.append(box_id)
        # Draw the course selection boxes for each selected track in the corresponding row
        # First, build a set of track names that are currently selected and their row assignments
        selected_track_set = set(selected_names)
        for row in range(3):
            if row < n:
                track_name = selected_names[row]
                y_offset = y0 + 120 - 120 + row * 130  # match previous y logic
                x_offset = x0
                self.draw_track_course_boxes(track_name, x_offset, y_offset)
            else:
                # Only clear content for tracks that are NOT currently selected
                for i in range(3):
                    for suffix in ['_bg_', '_text_', '_info_btn_', '_clear_btn_']:
                        for track in self.TRACK_COURSE_DATABASES.keys():
                            if track in selected_track_set:
                                continue  # Don't clear content for selected tracks
                            attr = f'{track}{suffix}{i+1}'
                            item = getattr(self, attr, None)
                            if item:
                                if isinstance(item, int):
                                    self.canvas.delete(item)
                                elif hasattr(item, 'destroy'):
                                    item.destroy()
                                delattr(self, attr)

        # --- Restore Tech Electives, Total Elective Hours, and Capstone Courses section ---
        section_x = x0 + 3 * (box_w + h_gap) + 200  # Space to the right of track boxes
        section_y = y0

        # Tech Electives label
        tech_label = self.canvas.create_text(section_x + 2 * (box_w + h_gap), section_y, text="Tech Electives", font=("Helvetica", 16))
        self.dynamic_track_items.append(tech_label)
        tech_y_start = section_y + 30
        # Draw 2 rows of 4 boxes
        for row in range(2):
            for col in range(4):
                x = section_x + col * (box_w + h_gap)
                y = tech_y_start + row * (box_h + v_gap)
                # First box in first column: ENC 1101 with course_box tag and click event
                if row == 0 and col == 0:
                    box_id = self.canvas.create_rectangle(x, y, x + box_w, y + box_h, outline='black', width=2, tags=('course_box', 'enc_1101_box'))
                    text_id = self.canvas.create_text(x + box_w/2, y + box_h/2, text='', font=("Helvetica", 13))
                    self.canvas.tag_bind(box_id, '<Button-1>', lambda e: self.show_course_details_box('ENC', '1101'))
                    self.canvas.tag_bind(text_id, '<Button-1>', lambda e: self.show_course_details_box('ENC', '1101'))
                    self.dynamic_track_items.extend([box_id, text_id])
                else:
                    box_id = self.canvas.create_rectangle(x, y, x + box_w, y + box_h, outline='black', width=2)
                    self.dynamic_track_items.append(box_id)
        # Total Elective Hours label
        total_label_y = tech_y_start + 2 * (box_h + v_gap) + 40
        total_label = self.canvas.create_text(section_x + 2 * (box_w + h_gap), total_label_y, text="Total Elective Hours:", font=("Helvetica", 16))
        self.dynamic_track_items.append(total_label)
        # If you need to take Programming Design...
        info_text = "If you need to take Programming Design the Total Hours need are: 40\nIf not: 43"
        info_label = self.canvas.create_text(section_x + 2 * (box_w + h_gap), total_label_y + 40, text=info_text, font=("Helvetica", 14), justify='center')
        self.dynamic_track_items.append(info_label)
        # Capstone Courses label
        capstone_y = total_label_y + 120
        capstone_label = self.canvas.create_text(section_x + 2 * (box_w + h_gap), capstone_y, text="Capstone Courses", font=("Helvetica", 16))
        self.dynamic_track_items.append(capstone_label)
        # Draw 2 capstone boxes
        cap_box_y = capstone_y + 30
        for i, name in enumerate(["Design 1", "Design 2"]):
            x = section_x + i * (box_w + h_gap) + box_w + h_gap//2
            y = cap_box_y
            box_id = self.canvas.create_rectangle(x, y, x + box_w, y + box_h, outline='black', width=2)
            self.dynamic_track_items.append(box_id)
            text_id = self.canvas.create_text(x + box_w/2, y + box_h/2, text=name, font=("Helvetica", 14))
            self.dynamic_track_items.append(text_id)
        # Update scrollregion with extra gap to the right
        bbox = self.canvas.bbox('all')
        if bbox:
            x0b, y0b, x1b, y1b = bbox
            self.canvas.config(scrollregion=(x0b, y0b, x1b + 400, y1b))
        else:
            self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def on_track_selection(self):
        # Limit to 3 tracks
        selected = [i for i, var in enumerate(self.track_vars) if var.get()]
        if len(selected) > 3:
            # Uncheck the last one
            self.track_vars[selected[-1]].set(False)
            return
        self.draw_dynamic_track_boxes()

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
        enc1101_box = self.canvas.create_rectangle(left_margin, enc1101_y, left_margin + box_width, enc1101_y + box_height, outline='black', width=2, tags=('course_box', 'enc_1101_box'))
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

        # ENC 1102 (below ENC 1101, interactive)
        enc1102_y = enc1101_y + box_height + box_gap
        enc1102_box = self.canvas.create_rectangle(left_margin, enc1102_y, left_margin + box_width, enc1102_y + box_height, outline='black', width=2, tags=('course_box', 'enc_1102_box'))
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
        # Update button visibility
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

        # Row 2: MAC 2282 / MAC 2312
        mac2_box = self.canvas.create_rectangle(col3_left, col3_y + col3_gap, col3_left + box_width, col3_y + col3_gap + box_height, outline='black', width=2)
        mac2_text = self.canvas.create_text(
            col3_left + box_width/2,
            col3_y + col3_gap + box_height/2,
            text="MAC 2282\nOr MAC 2312\nCalculus II",
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

        # Row 4: CHS 2440L / CHM 2045L
        chs_box = self.canvas.create_rectangle(col3_left, col3_y + 3*col3_gap, col3_left + box_width, col3_y + 3*col3_gap + box_height, outline='black', width=2)
        chs_text = self.canvas.create_text(
            col3_left + box_width/2,
            col3_y + 3*col3_gap + box_height/2,
            text="CHS 2440L\nOr CHM 2045L\nChemistry Lab",
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

        # Row 5: ENC 3246
        enc_box = self.canvas.create_rectangle(col3_left, col3_y + 4*col3_gap, col3_left + box_width, col3_y + 4*col3_gap + box_height, outline='black', width=2)
        enc_text = self.canvas.create_text(
            col3_left + box_width/2,
            col3_y + 4*col3_gap + box_height/2,
            text="ENC 3246\nCommunication\nfor Engineers",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_enc = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('ENC', '3246'))
        self.canvas.create_window(col3_left + 2, col3_y + 4*col3_gap + 2, window=info_btn_enc, anchor='nw')

        # Row 6: EGS 2070
        egs_box = self.canvas.create_rectangle(col3_left, col3_y + 5*col3_gap, col3_left + box_width, col3_y + 5*col3_gap + box_height, outline='black', width=2)
        egs_text = self.canvas.create_text(
            col3_left + box_width/2,
            col3_y + 5*col3_gap + box_height/2,
            text="EGS 2070\nProf. Formation\nof Eng. I",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egs = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGS', '2070'))
        self.canvas.create_window(col3_left + 2, col3_y + 5*col3_gap + 2, window=info_btn_egs, anchor='nw')

        # Start of fourth column
        col4_left = col3_left + box_width + h_gap
        col4_y = top
        col4_gap = box_height + v_gap

        # Row 1: EGN 3373
        egn_box = self.canvas.create_rectangle(col4_left, col4_y, col4_left + box_width, col4_y + box_height, outline='black', width=2)
        egn_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + box_height/2,
            text="EGN 3373\nElectrical\nSystems I",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egn = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGN', '3373'))
        self.canvas.create_window(col4_left + 2, col4_y + 2, window=info_btn_egn, anchor='nw')

        # Row 2: MAC 2283 / MAC 2313
        mac3_box = self.canvas.create_rectangle(col4_left, col4_y + col4_gap, col4_left + box_width, col4_y + col4_gap + box_height, outline='black', width=2)
        mac3_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + col4_gap + box_height/2,
            text="MAC 2283\nOr MAC 2313\nCalculus III",
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

        # Row 3: EEE 3394
        eee_box = self.canvas.create_rectangle(col4_left, col4_y + 2*col4_gap, col4_left + box_width, col4_y + 2*col4_gap + box_height, outline='black', width=2)
        eee_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + 2*col4_gap + box_height/2,
            text="EEE 3394\nEE Science I\nElec Mtrls",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_eee = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEE', '3394'))
        self.canvas.create_window(col4_left + 2, col4_y + 2*col4_gap + 2, window=info_btn_eee, anchor='nw')

        # Row 4: CHS 2440 / CHM 2045
        chs_chem_box = self.canvas.create_rectangle(col4_left, col4_y + 3*col4_gap, col4_left + box_width, col4_y + 3*col4_gap + box_height, outline='black', width=2)
        chs_chem_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + 3*col4_gap + box_height/2,
            text="CHS 2440\nOr CHM 2045\nChemistry",
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

        # Row 5: EGN 3615
        egn_econ_box = self.canvas.create_rectangle(col4_left, col4_y + 4*col4_gap, col4_left + box_width, col4_y + 4*col4_gap + box_height, outline='black', width=2)
        egn_econ_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + 4*col4_gap + box_height/2,
            text="EGN 3615\nEng Economics",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egn_econ = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGN', '3615'))
        self.canvas.create_window(col4_left + 2, col4_y + 4*col4_gap + 2, window=info_btn_egn_econ, anchor='nw')

        # Row 6: EGS 3071
        egs_box = self.canvas.create_rectangle(col4_left, col4_y + 5*col4_gap, col4_left + box_width, col4_y + 5*col4_gap + box_height, outline='black', width=2)
        egs_text = self.canvas.create_text(
            col4_left + box_width/2,
            col4_y + 5*col4_gap + box_height/2,
            text="EGS 3071\nProf. Formation\nof Eng. II",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egs = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGS', '3071'))
        self.canvas.create_window(col4_left + 2, col4_y + 5*col4_gap + 2, window=info_btn_egs, anchor='nw')

        # Start of fifth column
        col5_left = col4_left + box_width + h_gap
        col5_y = top
        col5_gap = box_height + v_gap

        # Row 4: EGN 3420
        egn_analysis_box = self.canvas.create_rectangle(col5_left, col5_y + 3*col5_gap, col5_left + box_width, col5_y + 3*col5_gap + box_height, outline='black', width=2)
        egn_analysis_text = self.canvas.create_text(
            col5_left + box_width/2,
            col5_y + 3*col5_gap + box_height/2,
            text="EGN 3420\nEngineering\nAnalysis",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egn_analysis = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGN', '3420'))
        self.canvas.create_window(col5_left + 2, col5_y + 3*col5_gap + 2, window=info_btn_egn_analysis, anchor='nw')

        # Row 6: EGS 3072
        egs_box = self.canvas.create_rectangle(col5_left, col5_y + 5*col5_gap, col5_left + box_width, col5_y + 5*col5_gap + box_height, outline='black', width=2)
        egs_text = self.canvas.create_text(
            col5_left + box_width/2,
            col5_y + 5*col5_gap + box_height/2,
            text="EGS 3072\nProf. Formation\nof Eng. III",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egs = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGS', '3072'))
        self.canvas.create_window(col5_left + 2, col5_y + 5*col5_gap + 2, window=info_btn_egs, anchor='nw')

        # Start of sixth column
        col6_left = col5_left + box_width + h_gap
        col6_y = top
        col6_gap = box_height + v_gap

        # Row 2: EEL 3472C
        eel_science_box = self.canvas.create_rectangle(col6_left, col6_y + col6_gap, col6_left + box_width, col6_y + col6_gap + box_height, outline='black', width=2)
        eel_science_text = self.canvas.create_text(
            col6_left + box_width/2,
            col6_y + col6_gap + box_height/2,
            text="EEL 3472C\nEE Science II -\nElectroMag",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_eel_science = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '3472C'))
        self.canvas.create_window(col6_left + 2, col6_y + col6_gap + 2, window=info_btn_eel_science, anchor='nw')

        # Row 6: EEL 2161
        eel_comp_box = self.canvas.create_rectangle(col6_left, col6_y + 5*col6_gap, col6_left + box_width, col6_y + 5*col6_gap + box_height, outline='black', width=2)
        eel_comp_text = self.canvas.create_text(
            col6_left + box_width/2,
            col6_y + 5*col6_gap + box_height/2,
            text="EEL 2161\nEE Comp.\nMethods",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_eel_comp = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '2161'))
        self.canvas.create_window(col6_left + 2, col6_y + 5*col6_gap + 2, window=info_btn_eel_comp, anchor='nw')

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

        # Row 2: EGN 3374
        egn_sys2_box = self.canvas.create_rectangle(col7_left, col7_y + col7_gap, col7_left + box_width, col7_y + col7_gap + box_height, outline='black', width=2)
        egn_sys2_text = self.canvas.create_text(
            col7_left + box_width/2,
            col7_y + col7_gap + box_height/2,
            text="EGN 3374\nElectrical\nSystems II",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_egn_sys2 = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EGN', '3374'))
        self.canvas.create_window(col7_left + 2, col7_y + col7_gap + 2, window=info_btn_egn_sys2, anchor='nw')

        # Row 4: EEL 4102
        signals_box = self.canvas.create_rectangle(col7_left, col7_y + 3*col7_gap, col7_left + box_width, col7_y + 3*col7_gap + box_height, outline='black', width=2)
        signals_text = self.canvas.create_text(
            col7_left + box_width/2,
            col7_y + 3*col7_gap + box_height/2,
            text="EEL 4102\nSignals &\nSystems",
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

        # Row 6: EEL 4835
        prog_design_box = self.canvas.create_rectangle(col7_left, col7_y + 5*col7_gap, col7_left + box_width, col7_y + 5*col7_gap + box_height, outline='black', width=2)
        prog_design_text = self.canvas.create_text(
            col7_left + box_width/2,
            col7_y + 5*col7_gap + box_height/2,
            text="EEL 4835\nProgramming\nDesign",
            font=("Helvetica", 13),
            justify='center'
        )
        info_btn_prog_design = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                                width=2, height=1, bg='#4FC3F7', fg='white',
                                command=lambda: self.show_course_details_box('EEL', '4835'))
        self.canvas.create_window(col7_left + 2, col7_y + 5*col7_gap + 2, window=info_btn_prog_design, anchor='nw')

        # Shift the rest of the grid to the right
        left = left + box_width + h_gap

        self.canvas.config(scrollregion=self.canvas.bbox('all'))

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
        selector.geometry(f"500x400+{self.winfo_rootx() + x + w//2}+{self.winfo_rooty() + y + h//2}")
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
            ("EEE 3302", "Electronics I", "3"),
            ("EEL 4512C", "Communication Systems", "3"),
            ("EGN 3375", "Electromechanical Systems", "3"),
            ("EEL 4657", "Linear Control Systems", "3"),
            ("EEE 4351C", "Semiconductor Devices", "3"),
            ("EEL 4423C", "RF & Microwave Circuits", "3")
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
                # Update the text and remove green background
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

    def create_core_elective_box(self, box_number, x, y):
        box_width = 220
        box_height = 90
        
        # Create the box
        box = self.canvas.create_rectangle(x, y, x + box_width, y + box_height, outline='black', width=2)
        
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
        
        # Update button visibility
        self.update_core_elective_buttons(box_number)
        
        # Bind click events
        self.canvas.tag_bind(box, '<Button-1>', 
            lambda e: self.open_core_elective_selector(box_number, x, y, box_width, box_height))
        self.canvas.tag_bind(text, '<Button-1>', 
            lambda e: self.open_core_elective_selector(box_number, x, y, box_width, box_height))
        self.canvas.tag_bind(bg, '<Button-1>', 
            lambda e: self.open_core_elective_selector(box_number, x, y, box_width, box_height))

    def clear_core_elective_selection(self, box_number):
        setattr(self, f'selected_core_elective_{box_number}', None)
        text_widget = getattr(self, f'core_text_{box_number}')
        
        # Recreate green background
        box_coords = self.canvas.coords(text_widget)
        x = box_coords[0] - 110  # Approximate the original x position
        y = box_coords[1] - 45   # Approximate the original y position
        bg = self.canvas.create_rectangle(x+2, y+2, x+218, y+88, fill='#006747', outline='')
        self.canvas.tag_lower(bg)
        setattr(self, f'core_bg_{box_number}', bg)
        
        # Update text
        self.canvas.itemconfig(text_widget, 
                             text="Add Gateway\nCourse",
                             font=("Helvetica", 12, "bold"),
                             fill='white')
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
        if getattr(self, f'selected_core_elective_{box_number}', None):
            info_btn.config(state='normal')
            clear_btn.config(state='normal')
        else:
            info_btn.config(state='disabled')
            clear_btn.config(state='disabled')

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

    def open_humanities_selector(self, x, y, w, h):
        selector = tk.Toplevel(self)
        selector.title("Select Humanities Course")
        selector.geometry(f"500x400+{self.winfo_rootx() + x + w//2}+{self.winfo_rooty() + y + h//2}")
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
            selector.destroy()
        btn = tk.Button(selector, text="OK", command=set_course, font=("Helvetica", 11, 'bold'), bg='#006747', fg='white', relief='flat', activebackground='#004F2D', activeforeground='white')
        btn.pack(pady=10)
        selector.bind('<Return>', lambda e: set_course())

    def open_social_selector(self, x, y, w, h):
        selector = tk.Toplevel(self)
        selector.title("Select Social Studies Course")
        selector.geometry(f"500x400+{self.winfo_rootx() + x + w//2}+{self.winfo_rooty() + y + h//2}")
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
            selector.destroy()
        btn = tk.Button(selector, text="OK", command=set_course, font=("Helvetica", 11, 'bold'), bg='#006747', fg='white', relief='flat', activebackground='#004F2D', activeforeground='white')
        btn.pack(pady=10)
        selector.bind('<Return>', lambda e: set_course())

    def update_humanities_buttons(self):
        if self.selected_humanities_course:
            self.hum_info_btn.config(state='normal')
            self.hum_clear_btn.config(state='normal')
        else:
            self.hum_info_btn.config(state='disabled')
            self.hum_clear_btn.config(state='disabled')

    def update_social_buttons(self):
        if self.selected_social_course:
            self.soc_info_btn.config(state='normal')
            self.soc_clear_btn.config(state='normal')
        else:
            self.soc_info_btn.config(state='disabled')
            self.soc_clear_btn.config(state='disabled')

    def clear_humanities_selection(self):
        self.selected_humanities_course = None
        self.canvas.itemconfig(self.hum_text, text="Add GenEd Core Humanities")
        self.update_humanities_buttons()

    def clear_social_selection(self):
        self.selected_social_course = None
        self.canvas.itemconfig(self.soc_text, text="Add GenEd Core Social Studies")
        self.update_social_buttons()

    def show_selected_humanities_info(self):
        if self.selected_humanities_course:
            prefix, number = self.selected_humanities_course.split()
            self.show_course_details_box(prefix, number)

    def show_selected_social_info(self):
        if self.selected_social_course:
            prefix, number = self.selected_social_course.split()
            self.show_course_details_box(prefix, number)

    def show_course_details_box(self, prefix, number):
        try:
            from courses import courses
        except ImportError:
            messagebox.showerror("Error", "Course catalog not available.")
            return
        course_info = None
        if prefix in courses["University of South Florida"] and number in courses["University of South Florida"][prefix]:
            course_info = courses["University of South Florida"][prefix][number]
        if not course_info:
            messagebox.showinfo("Course Info", f"No details found for {prefix} {number}.")
            return
        win = tk.Toplevel(self)
        win.title(f"Course Info: {prefix} {number}")
        win.geometry("540x420")
        win.configure(bg='#E6F3FF')
        frame = tk.Frame(win, bg='#E6F3FF')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        details = (
            f"Course: {prefix} {number}\n\n"
            f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
            f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
            f"Description: {course_info.get('Description', 'N/A')}\n\n"
            f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
            f"Corequisites: {course_info.get('Coreqs', 'N/A')}"
        )
        text_widget = tk.Text(frame, font=("Helvetica", 13), bg='#E6F3FF', fg='#006747', wrap='word', borderwidth=0, highlightthickness=0)
        text_widget.insert('1.0', details)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
        btn.pack(pady=10)

    def open_track1_course_selector(self, box_number, x, y, w, h):
        selector = tk.Toplevel(self)
        selector.title("Select Bioelectrical Systems Course")
        selector.geometry(f"500x400+{self.winfo_rootx() + x + w//2}+{self.winfo_rooty() + y + h//2}")
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
        track1_courses = [
            ("EEE 4215", "Biomedical Optical Spectroscopy & Imaging", "F"),
            ("EEE 4260C", "Bioelectricity", "F"),
            ("EEE 4271", "Bioelectronics", "S"),
            ("EEE 4410", "System on a Chip", "Last Sem. S 2021"),
            ("EEE 4506", "Biomedical Image Processing", "Last Sem. S 2021"),
            ("EEL 3116L", "Laboratory II", "F, S"),
        ]
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
            ("EEE 4215", "Biomedical Optical Spectroscopy & Imaging", "F"),
            ("EEE 4260C", "Bioelectricity", "F"),
            ("EEE 4271", "Bioelectronics", "S"),
            ("EEE 4410", "System on a Chip", "Last Sem. S 2021"),
            ("EEE 4506", "Biomedical Image Processing", "Last Sem. S 2021"),
            ("EEL 3116L", "Laboratory II", "F, S"),
        ],
        "Communication Systems": [
            ("EEE 4423", "Quantum Computing & Communications", "S"),
            ("EEE 4746", "Wireless Mobile Computing & Security", "F"),
            ("EEL 4423C", "Wireless Circuits & Systems Design Laboratory", "F, S"),
            ("EEL 4540", "Radar Systems", "F"),
            ("EEL 4595", "Mobile and Personal Communication", "Last Sem. F 2021"),
            ("EEL 4727C", "Dig. Sig. Process. w/ Field Programmable", "S"),
            ("EEL 4756", "Digital Signal Processing", "F"),
            ("EEL 4513L", "Wireless Communication Systems Lab", "Not Offered"),
            ("EEL 4743L", "Microprocessor Laboratory", "F"),
        ],
        "Energy, Power, & Sustainability": [
            ("EEL 4212", "Energy Delivery Systems", "S"),
            ("EEL 4214", "Electric (Utility) Distribution Systems", "Not Offered"),
            ("EEL 4224", "Electric Machines & Drives", "F"),
            ("EEL 4241", "Power Electronics", "S"),
            ("EEL 4251", "Power System Analysis", "F"),
            ("EEL 4252", "Power Systems II", "Last Sem. S 2021"),
            ("EEL 4271", "Power System Protection", "F"),
            ("EEL 4283", "Sustainable Energy", "Last Sem. F 2021"),
            ("EEL 4206L", "Electromechanical Energy System Lab", "F, S"),
        ],
        "Mechatronics, Robotics, & Embedded Systems": [
            ("EEL 3100", "Network Analysis and Design", "Last Sem. F 2022"),
            ("EEL 4663", "Applied Robotics", "F"),
            ("EEL 4680", "Applied Mechatronics", "S"),
            ("EEL 4740", "Embedded Systems", "S"),
            ("EEL 4744", "Microprocessor Principles & Applications", "F"),
            ("EEL 4657L", "Linear Controls Laboratory", "F, S"),
            ("EEL 4743L", "Microprocessor Laboratory", "F"),
        ],
        "Micro and Nano-scale Systems": [
            ("EEE 3302", "Electronics I EEE 4274", "F, S"),
            ("EEE 4359", "Analog CMOS/VLSI Design", "S"),
            ("EEL 4567", "Electro-Optics", "Last Sem. S 2022"),
            ("EEL 3116L", "Laboratory II", "F, S"),
        ],
        "Wireless Circuits and Systems": [
            ("EEL 4420", "Radio Freq Microwave Measurement", "F"),
            ("EEL 4421", "RF/Microwave Circuits I", "F"),
            ("EEL 4422", "RF/Microwave Circuits II", "S"),
            ("EEL 4461", "Antenna Theory", "S"),
            ("EEL 4540", "Radar Systems", "4540"),
            ("EEL 4513L", "Wireless Communication Systems Lab", "Not Offered"),
        ],
        "Systems and Security": [
            ("EEE 4746", "Wireless Mobile Computing & Security", "F"),
            ("EEE 4748", "Cryptography & Data Security", "S"),
            ("EEE 4774", "Data Analytics", "S"),
            ("EEL 4782", "Data Networks, Systems & Security", "F"),
            ("EEL 4872", "AI & Security in Cyber Physical Systems", "F"),
            ("EEL 4743L", "Microprocessor Laboratory", "F"),
        ],
        # Add other tracks here as needed, e.g.:
        # "Communication Systems": [...],
        # "Energy, Power, and Sustainability": [...],
    }

    def open_track_course_selector(self, track_name, box_number, x, y, w, h):
        selector = tk.Toplevel(self)
        selector.title(f"Select {track_name} Course")
        selector.geometry(f"500x400+{self.winfo_rootx() + x + w//2}+{self.winfo_rooty() + y + h//2}")
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
        course_list = self.TRACK_COURSE_DATABASES.get(track_name, [])
        for course in course_list:
            tree.insert("", "end", values=course)
        tree.pack(side='left', fill='both', expand=True)
        tree_scroll.config(command=tree.yview)
        current_course = getattr(self, f'selected_{track_name}_course_{box_number}', None)
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
                setattr(self, f'selected_{track_name}_course_{box_number}', values[0])
                text_widget = getattr(self, f'{track_name}_text_{box_number}')
                bg_item = getattr(self, f'{track_name}_bg_{box_number}', None)
                if bg_item:
                    self.canvas.delete(bg_item)
                    setattr(self, f'{track_name}_bg_{box_number}', None)
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
                                bg='#E6F3F7',
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

    def create_track_course_box(self, track_name, box_number, x, y):
        box_width = 220
        box_height = 90
        box = self.canvas.create_rectangle(x, y, x + box_width, y + box_height, outline='black', width=2)
        bg = self.canvas.create_rectangle(x+2, y+2, x+box_width-2, y+box_height-2, fill='#006747', outline='')
        self.canvas.tag_lower(bg, box)
        setattr(self, f'{track_name}_bg_{box_number}', bg)
        text = self.canvas.create_text(
            x + box_width/2,
            y + box_height/2,
            text=f"Add {track_name}\nCourse",
            font=("Helvetica", 12, "bold"),
            fill='white',
            width=box_width-16,
            justify='center'
        )
        setattr(self, f'{track_name}_text_{box_number}', text)
        info_btn = tk.Button(self.canvas, text="i", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#4FC3F7', fg='white',
                            command=lambda: self.show_selected_track_info(track_name, box_number))
        self.canvas.create_window(x + 2, y + 2, window=info_btn, anchor='nw')
        setattr(self, f'{track_name}_info_btn_{box_number}', info_btn)
        clear_btn = tk.Button(self.canvas, text="×", font=("Helvetica", 8, "bold"), 
                            width=2, height=1, bg='#FF0000', fg='white',
                            command=lambda: self.clear_track_selection(track_name, box_number))
        self.canvas.create_window(x + box_width - 25, y + 2, window=clear_btn, anchor='nw')
        setattr(self, f'{track_name}_clear_btn_{box_number}', clear_btn)
        self.update_track_buttons(track_name, box_number)
        self.canvas.tag_bind(box, '<Button-1>', 
            lambda e: self.open_track_course_selector(track_name, box_number, x, y, box_width, box_height))
        self.canvas.tag_bind(text, '<Button-1>', 
            lambda e: self.open_track_course_selector(track_name, box_number, x, y, box_width, box_height))
        self.canvas.tag_bind(bg, '<Button-1>', 
            lambda e: self.open_track_course_selector(track_name, box_number, x, y, box_width, box_height))

    def clear_track_selection(self, track_name, box_number):
        setattr(self, f'selected_{track_name}_course_{box_number}', None)
        text_widget = getattr(self, f'{track_name}_text_{box_number}')
        box_coords = self.canvas.coords(text_widget)
        x = box_coords[0] - 110
        y = box_coords[1] - 45
        bg = self.canvas.create_rectangle(x+2, y+2, x+218, y+88, fill='#006747', outline='')
        self.canvas.tag_lower(bg)
        setattr(self, f'{track_name}_bg_{box_number}', bg)
        self.canvas.itemconfig(text_widget, 
                             text=f"Add {track_name}\nCourse",
                             font=("Helvetica", 12, "bold"),
                             fill='white')
        self.update_track_buttons(track_name, box_number)

    def show_selected_track_info(self, track_name, box_number):
        course_code = getattr(self, f'selected_{track_name}_course_{box_number}', None)
        if course_code:
            prefix, number = course_code.split()
            try:
                from courses import courses
                course_info = courses["University of South Florida"].get(prefix, {}).get(number, None)
                if course_info:
                    details = (
                        f"Course: {prefix} {number}\n\n"
                        f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
                        f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
                        f"Description: {course_info.get('Description', 'N/A')}\n\n"
                        f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
                        f"Corequisites: {course_info.get('Coreqs', 'N/A')}"
                    )
                else:
                    raise KeyError
            except (ImportError, KeyError):
                # Fallback to TRACK_COURSE_DATABASES
                course_list = self.TRACK_COURSE_DATABASES.get(track_name, [])
                course_info = next((c for c in course_list if c[0] == course_code), None)
                if course_info:
                    details = (
                        f"Course: {course_info[0]}\n\n"
                        f"Name: {course_info[1]}\n\n"
                        f"Term(s): {course_info[2]}"
                    )
                else:
                    details = f"Course: {course_code}\n(No further details found.)"
            win = tk.Toplevel(self)
            win.title(f"Course Info: {course_code}")
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

    def update_track_buttons(self, track_name, box_number):
        info_btn = getattr(self, f'{track_name}_info_btn_{box_number}')
        clear_btn = getattr(self, f'{track_name}_clear_btn_{box_number}')
        if getattr(self, f'selected_{track_name}_course_{box_number}', None):
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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Academic Plan")
    page = AcademicPlanPage(root)
    page.pack(fill='both', expand=True)
    root.geometry("1100x900")
    root.mainloop()
