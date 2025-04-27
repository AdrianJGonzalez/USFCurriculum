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
        # Position to the right of the existing layout
        start_x = 3000
        start_y = 230
        box_width = 400
        box_height = 50
        gap = 10

        # Draw Core Electives boxes first (to the left of track selection)
        core_box_width = 220
        core_box_height = 90
        core_gap = 40
        core_start_x = start_x-400
        core_start_y = start_y

        for i in range(4):
            y = core_start_y + i * (core_box_height + core_gap)
            self.draw_box(core_start_x, y, core_box_width, core_box_height, "Core Electives")

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
            "Track 3: Energy, Power, and Sustainability",
            "Track 4: Mechatronics, Robotics, & Embedded Systems",
            "Track 5: Micro and Nano-scale Systems",
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
            self.canvas.create_window(start_x + 20, y + box_height/2, window=checkbutton, anchor='w')
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

        # Get selected tracks
        selected_tracks = [self.tracks[i] for i, var in enumerate(self.track_vars) if var.get()]
        selected_names = [t.split(': ', 1)[1] for t in selected_tracks]
        n = len(selected_names)

        # Always show first two rows (6 boxes)
        box_w = 220
        box_h = 90
        h_gap = 40
        v_gap = 40
        x0 = self.track_boxes_start_x  # Use the calculated position
        y0 = self.track_boxes_start_y
        for row in range(2):
            # Label above row: show track name if selected, else blank
            label = selected_names[row] if row < n else ""
            label_id = self.canvas.create_text(x0 + box_w + h_gap, y0 + row * (box_h + v_gap) - 30, text=label, font=("Helvetica", 16))
            self.dynamic_track_items.append(label_id)
            # Draw 3 boxes in this row
            for col in range(3):
                x = x0 + col * (box_w + h_gap)
                y = y0 + row * (box_h + v_gap)
                box_id = self.canvas.create_rectangle(x, y, x + box_w, y + box_h, outline='black', width=2)
                self.dynamic_track_items.append(box_id)
        # Only show third row if 3 tracks are selected
        if n == 3:
            label = selected_names[2]
            row = 2
            label_id = self.canvas.create_text(x0 + box_w + h_gap, y0 + row * (box_h + v_gap) - 30, text=label, font=("Helvetica", 16))
            self.dynamic_track_items.append(label_id)
            for col in range(3):
                x = x0 + col * (box_w + h_gap)
                y = y0 + row * (box_h + v_gap)
                box_id = self.canvas.create_rectangle(x, y, x + box_w, y + box_h, outline='black', width=2)
                self.dynamic_track_items.append(box_id)

        # --- Add Tech Electives, Total Elective Hours, and Capstone Courses section ---
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
            x0, y0, x1, y1 = bbox
            self.canvas.config(scrollregion=(x0, y0, x1 + 400, y1))
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
        self.canvas.tag_bind(enc1101_box, '<Double-Button-1>', lambda e: self.show_course_details_box('ENC', '1101'))
        self.canvas.tag_bind(enc1101_text, '<Double-Button-1>', lambda e: self.show_course_details_box('ENC', '1101'))

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
        self.canvas.tag_bind(enc1102_box, '<Double-Button-1>', lambda e: self.show_course_details_box('ENC', '1102'))
        self.canvas.tag_bind(enc1102_text, '<Double-Button-1>', lambda e: self.show_course_details_box('ENC', '1102'))

        # GenEd Core Humanities (course selector)
        hum_y = enc1102_y + box_height + box_gap
        self.selected_humanities_course = getattr(self, 'selected_humanities_course', None) or None
        self.hum_box = self.canvas.create_rectangle(left_margin, hum_y, left_margin + box_width, hum_y + box_height, outline='black', width=2, tags=('course_box', 'hum_selector_box'))
        # Prepare display text
        display_text = self.get_humanities_display_text(self.selected_humanities_course)
        self.hum_text = self.canvas.create_text(
            left_margin + box_width/2,
            hum_y + box_height/2,
            text=display_text,
            font=("Helvetica", 13),
            justify='center'
        )
        self.canvas.tag_bind(self.hum_box, '<Button-1>', lambda e: self.open_humanities_selector(left_margin, hum_y, box_width, box_height))
        self.canvas.tag_bind(self.hum_text, '<Button-1>', lambda e: self.open_humanities_selector(left_margin, hum_y, box_width, box_height))

        # GenEd Core Social Sciences
        soc_y = hum_y + box_height + box_gap
        self.draw_box(left_margin, soc_y, box_width, box_height, "GenEd Core Social Sciences")

        # EGN 3000 (below GenEd Core Social Sciences)
        egn3000_y = soc_y + box_height + box_gap
        self.draw_box(left_margin, egn3000_y, box_width, box_height, "EGN 3000")

        # EGN 3000L (below EGN 3000)
        egn3000l_y = egn3000_y + box_height + box_gap
        self.draw_box(left_margin, egn3000l_y, box_width, box_height, "EGN 3000L")

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

        # Draw the large enclosing box for first three columns
        enclosure_width = 6 * (box_width + h_gap) - h_gap/2
        enclosure_height = 6 * (box_height + v_gap) - v_gap/2
        self.canvas.create_rectangle(
            left - 20, top - 20,
            left + enclosure_width + 20, top + enclosure_height + 20,
            width=2
        )

        # Define box positions in exact grid layout matching the image
        # Only include boxes that have text, empty spaces are skipped
        positions = {
            # Row 1 (top)
            'Mod Analysis/Diff EQ': (left + (box_width + h_gap), top),
            'EE Systems 1': (left + 2*(box_width + h_gap), top),
            'Lab 1': (left + 5*(box_width + h_gap), top),

            # Row 2
            'Calc 1': (left, top + (box_height + v_gap)),
            'Calc 2': (left + (box_width + h_gap), top + (box_height + v_gap)),
            'Calc 3': (left + 2*(box_width + h_gap), top + (box_height + v_gap)),
            'EE Science 2': (left + 4*(box_width + h_gap), top + (box_height + v_gap)),
            'Electrical Systems 2': (left + 5*(box_width + h_gap), top + (box_height + v_gap)),

            # Row 3
            'Phy 1': (left, top + 2*(box_height + v_gap)),
            'EE Science 1': (left + 2*(box_width + h_gap), top + 2*(box_height + v_gap)),

            # Row 4
            'Phy 1 Lab': (left, top + 3*(box_height + v_gap)),
            'Chem Lab': (left + (box_width + h_gap), top + 3*(box_height + v_gap)),
            'Chem': (left + 2*(box_width + h_gap), top + 3*(box_height + v_gap)),
            'Engineering Analysis': (left + 3*(box_width + h_gap), top + 3*(box_height + v_gap)),
            'Signals and Systems': (left + 5*(box_width + h_gap), top + 3*(box_height + v_gap)),

            # Row 5
            'Fund. of Digital Circuits': (left, top + 4*(box_height + v_gap)),
            'EGN Communication': (left + (box_width + h_gap), top + 4*(box_height + v_gap)),
            'ENG Econ': (left + 2*(box_width + h_gap), top + 4*(box_height + v_gap)),
            'Comp Tools': (left + 5*(box_width + h_gap), top + 4*(box_height + v_gap)),

            # Row 6 (bottom)
            'Logic Design Lab\nDigital Circuits Lab': (left, top + 5*(box_height + v_gap)),
            'PFE 1': (left + (box_width + h_gap), top + 5*(box_height + v_gap)),
            'PFE 2': (left + 2*(box_width + h_gap), top + 5*(box_height + v_gap)),
            'PFE 3': (left + 3*(box_width + h_gap), top + 5*(box_height + v_gap)),
            'Programming with C\nEE Comp. Methods': (left + 4*(box_width + h_gap), top + 5*(box_height + v_gap)),
            'Programming Design': (left + 5*(box_width + h_gap), top + 5*(box_height + v_gap))
        }

        # Draw all boxes
        for name, (x, y) in positions.items():
            self.draw_box(x, y, box_width, box_height, name)

        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def draw_box(self, x, y, w, h, text):
        self.canvas.create_rectangle(x, y, x + w, y + h, outline='black', width=2)
        self.canvas.create_text(x + w/2, y + h/2, text=text, font=("Helvetica", 13), justify='center')
        return (x, y, x + w, y + h)

    def draw_arrow(self, x1, y1, x2, y2, double_headed=False, dashed=False):
        if dashed:
            self.canvas.create_line(x1, y1, x2, y2, arrow='both' if double_headed else 'last', width=2, dash=(6, 4))
        else:
            self.canvas.create_line(x1, y1, x2, y2, arrow='both' if double_headed else 'last', width=2)

    def show_course_details_box(self, prefix, number):
        try:
            from courses import courses
        except ImportError:
            messagebox.showerror("Error", "Course catalog not available.")
            return
        # Try to get course info from catalog
        course_info = None
        if prefix in courses["University of South Florida"] and number in courses["University of South Florida"][prefix]:
            course_info = courses["University of South Florida"][prefix][number]
        if course_info:
            # Format details with spacing and bold labels
            details = (
                f"Course: {prefix} {number}\n\n"
                f"Name: {course_info.get('Class Full Name', 'N/A')}\n\n"
                f"Credits: {course_info.get('Credit Hours', 'N/A')}\n\n"
                f"Description:\n{course_info.get('Description', 'N/A')}\n\n"
                f"Prerequisites: {course_info.get('Prereqs', 'N/A')}\n\n"
                f"Corequisites: {course_info.get('Coreqs', 'N/A')}\n"
            )
            win = tk.Toplevel(self)
            win.title(f"Course Info: {prefix} {number}")
            win.geometry("540x420")
            win.configure(bg='#E6F3FF')  # USF mint green

            # Frame for padding and background
            frame = tk.Frame(win, bg='#E6F3FF')
            frame.pack(fill='both', expand=True, padx=10, pady=10)

            # Add a Text widget with a scrollbar
            text_frame = tk.Frame(frame, bg='#E6F3FF')
            text_frame.pack(fill='both', expand=True)
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side='right', fill='y')
            text = tk.Text(
                text_frame,
                font=("Helvetica", 12),
                wrap='word',
                bg='#E6F3FF',
                fg='#006747',  # USF dark green
                yscrollcommand=scrollbar.set,
                borderwidth=0,
                highlightthickness=0
            )
            text.insert('1.0', details)
            text.config(state='disabled')
            text.pack(fill='both', expand=True, padx=10, pady=10)
            scrollbar.config(command=text.yview)

            # Styled close button
            btn = tk.Button(frame, text="Close", command=win.destroy, bg='#006747', fg='white', font=("Helvetica", 11, 'bold'), relief='flat', activebackground='#004F2D', activeforeground='white')
            btn.pack(pady=10)
        else:
            messagebox.showinfo("Course Info", f"No details found for {prefix} {number}.")

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
            selector.destroy()
        btn = tk.Button(selector, text="OK", command=set_course, font=("Helvetica", 11, 'bold'), bg='#006747', fg='white', relief='flat', activebackground='#004F2D', activeforeground='white')
        btn.pack(pady=10)
        selector.bind('<Return>', lambda e: set_course())

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Academic Plan")
    page = AcademicPlanPage(root)
    page.pack(fill='both', expand=True)
    root.geometry("1100x900")
    root.mainloop()
