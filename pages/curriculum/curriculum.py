#This is in development and is not currently implemented to the larger application.
#Things that remain to be done on this test
#1. Add some vertical scrolling so that the user can read further down with more courses - Have a Temp Solution 
#2. Make the boxes everso smaller in height
#3. Add the Prereqs and Coreq Arrows to the courses. (Make sure the arrows don't touch!)
#4. Give error window when adding duplicate classes
#5. Add scrolling into the Department filter in the course selection
#6. Add some "bar end" indicators on the scroll bars and typing indicators on the search boxes
#7. Add # of Credit Hours to the course box
#8. Center the indicator icons (X and !)
#9. Make the Semester indicator be the width of the column or centered
#10. Maybe add a scroll bar in course selector - DONE
#11. Add features that do not allow courses to be but in subsequent semesters if the prereq is not completed.
#Actually add an option to override.
#12. Integrate into the main program by adding it to main and by adding an "auto fill" feature from the transcript upload.
#13. Make it look a bit better visually and more inviting.
#14 Choose Better Colors (Maybe USF colors) for windows, buttons, ect.

import pygame
import sys
from pygame.locals import *
from .courses import courses
import json
import os

pygame.init()

WIDTH, HEIGHT = 1200, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont('arial', 18)
BIG_FONT = pygame.font.SysFont('arial', 24)
pygame.display.set_caption("Course Flowchart")

WHITE, GRAY, LIGHT_GRAY, BLACK, BLUE, RED, GREEN = (255, 255, 255), (200, 200, 200), (220, 220, 220), (0, 0, 0), (100, 149, 237), (255, 0, 0), (0, 200, 0)

COLUMN_HEIGHT = 700
SCROLL_X = 0
SCROLL_SPEED = 20
SCROLL_BAR_HEIGHT = 20

is_dragging_scroll = False
scroll_drag_offset = 0

class Dropdown:
    def __init__(self, x, y, options, width=100, selected=None):
        # Define standard dimensions
        self.width = width
        self.height = 30
        self.option_height = 30
        self.margin = 5
        self.padding = 5

        # Initialize base rectangle
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.actual_x = x  # Store actual x position without scroll offset
        
        # Store options and selection
        self.options = options
        self.selected = selected if selected else options[0]
        self.expanded = False

        # Create option rectangles (will be positioned in draw)
        self.option_rects = []
        for i in range(len(options)):
            self.option_rects.append(pygame.Rect(x, y + (i+1)*self.option_height, self.width, self.option_height))

    def draw(self, screen):
        # Draw main dropdown box
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)
        
        # Draw selected text centered in box
        text_surface = FONT.render(self.selected, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        # Draw dropdown arrow
        arrow_points = [
            (self.rect.right - 15, self.rect.centery - 3),
            (self.rect.right - 8, self.rect.centery + 4),
            (self.rect.right - 1, self.rect.centery - 3)
        ]
        pygame.draw.polygon(screen, BLACK, arrow_points)

        if self.expanded:
            # Update option rectangles positions
            for i, option_rect in enumerate(self.option_rects):
                option_rect.x = self.rect.x
                option_rect.y = self.rect.y + (i+1)*self.option_height
                
                # Draw option background
                pygame.draw.rect(screen, LIGHT_GRAY, option_rect)
                pygame.draw.rect(screen, BLACK, option_rect, 1)
                
                # Draw option text centered
                option_text = FONT.render(self.options[i], True, BLACK)
                text_rect = option_text.get_rect(center=option_rect.center)
                screen.blit(option_text, text_rect)

    def handle_event(self, event, area_rect):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            # Get current mouse position
            mouse_pos = pygame.mouse.get_pos()
            
            # Calculate the actual position relative to the content area
            adjusted_pos = (
                mouse_pos[0] - area_rect.x,
                mouse_pos[1] - area_rect.y
            )

            # Create click-check rectangle at the actual position
            actual_rect = pygame.Rect(
                self.actual_x - area_rect.x - SCROLL_X,
                self.rect.y,
                self.width,
                self.height
            )

            if actual_rect.collidepoint(adjusted_pos):
                self.expanded = not self.expanded
                return True
            elif self.expanded:
                # Check if click is within any option rectangle
                for i, option_rect in enumerate(self.option_rects):
                    actual_option_rect = pygame.Rect(
                        self.actual_x - area_rect.x - SCROLL_X,
                        option_rect.y,
                        self.width,
                        self.option_height
                    )
                    if actual_option_rect.collidepoint(adjusted_pos):
                        self.selected = self.options[i]
                        self.expanded = False
                        return True
                self.expanded = False
        return False

    def get_total_height(self):
        """Return the total height of the dropdown when expanded"""
        return self.height + (len(self.options) * self.option_height if self.expanded else 0)

    def get_option_rect(self, index):
        """Get the rectangle for a specific option"""
        if 0 <= index < len(self.option_rects):
            return self.option_rects[index]
        return None

class Column:
    def __init__(self, x, semester="Fall", year="2025"):
        self.base_x = x
        self.x = x
        self.actual_x = x  # Store the actual x position without scroll offset
        self.semester_dropdown = Dropdown(x + 10, 10, ["Fall", "Spring", "Summer"])
        self.year_input = ""  # Start with empty year
        self.boxes = [Box()]
        self.year_rect = pygame.Rect(x + 110, 10, 60, 30)
        self.scroll_y = 0
        self.is_scrolling = False
        self.active = False
        self.update_max_visible_boxes()

    def update_max_visible_boxes(self):
        self.max_visible_boxes = (COLUMN_HEIGHT - 60) // 120

    def draw(self, screen, offset):
        # Update max visible boxes based on current column height
        self.update_max_visible_boxes()
        
        # Get the right panel offset
        right_panel_x = 250  # Left column width from main.py
        
        # Update x position relative to right panel
        self.x = right_panel_x + self.base_x - offset
        self.actual_x = right_panel_x + self.base_x  # Store actual x without scroll offset
        
        # Only draw if the column is fully visible (not behind the left panel)
        if self.x >= right_panel_x:
            # Update UI element positions
            self.semester_dropdown.rect.x = self.x + 10
            self.year_rect.x = self.x + 110
            
            # Draw semester dropdown and year input
            self.semester_dropdown.draw(screen)
            
            # Draw year input box with visual feedback when active
            pygame.draw.rect(screen, WHITE if not self.active else LIGHT_GRAY, self.year_rect)
            pygame.draw.rect(screen, BLUE if self.active else BLACK, self.year_rect, 2 if self.active else 1)
            
            # Show dash if empty, otherwise show the year
            display_text = "-" if not self.year_input else self.year_input
            year_text = FONT.render(display_text, True, GRAY if not self.year_input else BLACK)
            text_rect = year_text.get_rect(center=self.year_rect.center)
            screen.blit(year_text, text_rect)

            # Draw scroll indicators if needed
            if self.scroll_y > 0:
                pygame.draw.polygon(screen, BLACK, [
                    (self.x + 90, 50),
                    (self.x + 100, 40),
                    (self.x + 110, 50)
                ])
            
            if (len(self.boxes) - self.scroll_y) > self.max_visible_boxes:
                pygame.draw.polygon(screen, BLACK, [
                    (self.x + 90, COLUMN_HEIGHT - 10),
                    (self.x + 100, COLUMN_HEIGHT),
                    (self.x + 110, COLUMN_HEIGHT - 10)
                ])

            # Draw visible boxes with scroll offset
            visible_boxes = self.boxes[self.scroll_y:self.scroll_y + self.max_visible_boxes]
            for i, box in enumerate(visible_boxes):
                y = 60 + i * 120
                box.draw(screen, self.x + 10, y)

    def handle_event(self, event, area_rect):
        # Get mouse position only for mouse-related events
        if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
            mouse_pos = pygame.mouse.get_pos()
            # Calculate position relative to content area
            adjusted_pos = (
                mouse_pos[0] - area_rect.x,
                mouse_pos[1] - area_rect.y
            )
        else:
            if event.type == KEYDOWN and self.active:
                if event.key == K_BACKSPACE:
                    self.year_input = self.year_input[:-1]
                    return True
                elif event.unicode.isdigit() and len(self.year_input) < 4:
                    self.year_input += event.unicode
                    return True
            return

        # Only handle events if the column is visible
        if self.x >= 250:  # Left panel width
            # Handle semester dropdown click
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Create actual dropdown rect for collision detection
                actual_dropdown_rect = pygame.Rect(
                    self.actual_x - area_rect.x - SCROLL_X + 10,
                    self.semester_dropdown.rect.y,
                    self.semester_dropdown.width,
                    self.semester_dropdown.height
                )
                
                if actual_dropdown_rect.collidepoint(adjusted_pos):
                    self.semester_dropdown.expanded = not self.semester_dropdown.expanded
                    return True
                elif self.semester_dropdown.expanded:
                    # Check if click is within any option rectangle
                    for i, option_rect in enumerate(self.semester_dropdown.option_rects):
                        actual_option_rect = pygame.Rect(
                            self.actual_x - area_rect.x - SCROLL_X + 10,
                            option_rect.y,
                            self.semester_dropdown.width,
                            self.semester_dropdown.option_height
                        )
                        if actual_option_rect.collidepoint(adjusted_pos):
                            self.semester_dropdown.selected = self.semester_dropdown.options[i]
                            self.semester_dropdown.expanded = False
                            return True
                    self.semester_dropdown.expanded = False

                # Handle year input box click
                actual_year_rect = pygame.Rect(
                    self.actual_x - area_rect.x - SCROLL_X + 110,
                    self.year_rect.y,
                    self.year_rect.width,
                    self.year_rect.height
                )
                
                # Check if clicked on year input box
                if actual_year_rect.collidepoint(adjusted_pos):
                    # Deactivate all other columns
                    for col in columns:
                        col.active = False
                    self.active = True
                    return True
                # If clicked outside year input box and this column is active, deactivate it
                elif self.active:
                    self.active = False
                    return True

            if event.type == MOUSEWHEEL:
                # Create actual column bounds for mouse check
                actual_column_rect = pygame.Rect(
                    self.actual_x - SCROLL_X,
                    0,
                    200,
                    COLUMN_HEIGHT
                )
                if actual_column_rect.collidepoint(adjusted_pos):
                    self.is_scrolling = True
                    self.scroll_y = max(0, min(
                        self.scroll_y - event.y,
                        len(self.boxes) - self.max_visible_boxes
                    ))
                    return True

            if event.type == MOUSEBUTTONUP:
                self.is_scrolling = False

            if not self.is_scrolling and event.type == MOUSEBUTTONDOWN and event.button == 1:
                visible_boxes = self.boxes[self.scroll_y:self.scroll_y + self.max_visible_boxes]
                for box in visible_boxes:
                    box.handle_event(event, area_rect)

        self.boxes = [box for box in self.boxes if box.course or box == self.boxes[-1]]
        if not self.boxes or self.boxes[-1].course:
            self.boxes.append(Box())

class Box:
    def __init__(self):
        # Define standard dimensions
        self.width = 180
        self.height = 110
        self.button_size = 25
        self.margin = 5

        # Initialize base rectangle
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        # The add button covers the entire box when there's no course
        self.add_btn = self.rect.copy()
        
        # Small buttons positioned at the bottom
        self.delete_btn = pygame.Rect(0, 0, self.button_size, self.button_size)
        self.info_btn = pygame.Rect(0, 0, self.button_size, self.button_size)
        
        self.course = None
        self.actual_x = 0

    def draw(self, screen, x, y):
        self.actual_x = x
        
        # Update main rectangle position
        self.rect.topleft = (x, y)
        
        # Update all other rectangles based on main rectangle
        self.add_btn.topleft = self.rect.topleft
        self.delete_btn.topleft = (self.rect.x + self.margin, 
                                 self.rect.bottom - self.button_size - self.margin)
        self.info_btn.topleft = (self.rect.right - self.button_size - self.margin,
                                self.rect.bottom - self.button_size - self.margin)

        # Draw main box
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        if self.course:
            # Split into code and name
            course_code, course_name = self.course.split(":", 1)
            course_code = course_code.strip()
            course_name = course_name.strip()

            # Draw course code centered at top
            code_surface = FONT.render(course_code, True, BLACK)
            code_rect = code_surface.get_rect(center=(self.rect.centerx, self.rect.y + 12))
            screen.blit(code_surface, code_rect)

            # Draw course name (wrapped) in middle
            name_font = pygame.font.SysFont('arial', 14)
            name_lines = wrap_text(course_name, name_font, self.width - 2 * self.margin)
            for i, line in enumerate(name_lines[:3]):
                line_surface = name_font.render(line, True, BLACK)
                line_rect = line_surface.get_rect(center=(self.rect.centerx, self.rect.y + 34 + i * 16))
                screen.blit(line_surface, line_rect)

            # Draw control buttons at bottom
            pygame.draw.rect(screen, RED, self.delete_btn)
            pygame.draw.rect(screen, BLACK, self.delete_btn, 1)
            delete_text = FONT.render("X", True, WHITE)
            delete_rect = delete_text.get_rect(center=self.delete_btn.center)
            screen.blit(delete_text, delete_rect)

            pygame.draw.rect(screen, BLUE, self.info_btn)
            pygame.draw.rect(screen, BLACK, self.info_btn, 1)
            info_text = FONT.render("!", True, WHITE)
            info_rect = info_text.get_rect(center=self.info_btn.center)
            screen.blit(info_text, info_rect)
        else:
            # Draw add course text centered in box
            add_text = FONT.render("+ Add Course", True, GRAY)
            add_rect = add_text.get_rect(center=self.rect.center)
            screen.blit(add_text, add_rect)

    def handle_event(self, event, area_rect):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            # Get current mouse position
            mouse_pos = pygame.mouse.get_pos()
            
            # Calculate the actual position relative to the content area
            adjusted_pos = (
                mouse_pos[0] - area_rect.x,
                mouse_pos[1] - area_rect.y
            )

            # Create click-check rectangles at the actual positions
            actual_rect = pygame.Rect(
                self.actual_x - area_rect.x - SCROLL_X,
                self.rect.y,
                self.width,
                self.height
            )
            
            # Only create button rectangles if we have a course
            if self.course:
                actual_delete_btn = pygame.Rect(
                    actual_rect.x + self.margin,
                    actual_rect.bottom - self.button_size - self.margin,
                    self.button_size,
                    self.button_size
                )
                actual_info_btn = pygame.Rect(
                    actual_rect.right - self.button_size - self.margin,
                    actual_rect.bottom - self.button_size - self.margin,
                    self.button_size,
                    self.button_size
                )
                
                if actual_delete_btn.collidepoint(adjusted_pos):
                    self.course = None
                    return True
                elif actual_info_btn.collidepoint(adjusted_pos):
                    show_course_info(self.course)
                    return True
            else:
                # The entire box is clickable for adding a course
                if actual_rect.collidepoint(adjusted_pos):
                    open_course_selector(self)
                    return True
        return False

def open_course_selector(box):
    search_text = ""
    running = True
    scroll_offset = 0

    # Get the main surface and dimensions from the parent window
    surface = pygame.display.get_surface()
    window_width = surface.get_width()
    right_panel_x = 250  # Left column width from main.py
    right_panel_width = window_width - right_panel_x
    
    # Adjust coordinates relative to right panel
    selector_x = right_panel_x + 20
    selector_width = right_panel_width - 40
    
    departments = sorted({dept for school in courses.values() for dept in school})
    dept_dropdown = Dropdown(selector_x + 20, 120, ["All"] + departments, width=120, selected="All")

    close_btn = pygame.Rect(selector_x + selector_width - 60, 110, 40, 30)
    
    # Add scrollbar constants
    SCROLL_AREA_HEIGHT = 500
    SCROLL_BAR_X = selector_x + selector_width - 30
    SCROLL_BAR_Y = 170
    SCROLL_BAR_WIDTH = 10
    SCROLL_HANDLE_HEIGHT = 60

    is_dragging_scrollbar = False
    scroll_drag_offset_y = 0

    while running:
        # Draw selector window in right panel area
        pygame.draw.rect(surface, LIGHT_GRAY, (selector_x, 100, selector_width, 600))
        pygame.draw.rect(surface, BLACK, (selector_x, 100, selector_width, 600), 2)

        pygame.draw.rect(surface, RED, close_btn)
        surface.blit(FONT.render("X", True, WHITE), (close_btn.x + 12, close_btn.y + 6))

        # Draw dropdown
        pygame.draw.rect(surface, GRAY, dept_dropdown.rect)
        pygame.draw.rect(surface, BLACK, dept_dropdown.rect, 1)
        text_surface = FONT.render(dept_dropdown.selected, True, BLACK)
        text_rect = text_surface.get_rect(center=dept_dropdown.rect.center)
        surface.blit(text_surface, text_rect)

        # Draw search box
        search_box = pygame.Rect(selector_x + 160, 120, selector_width - 200, 30)
        pygame.draw.rect(surface, WHITE, search_box)
        pygame.draw.rect(surface, BLACK, search_box, 1)
        surface.blit(FONT.render(search_text or "Search courses...", True, GRAY if not search_text else BLACK), (search_box.x + 5, search_box.y + 5))

        # Filter and display courses
        filtered = [
            c for c in [
                f"{dept} {code}: {data['Class Full Name']}"
                for school in courses.values()
                for dept, dept_data in school.items()
                for code, data in dept_data.items()
            ]
            if (dept_dropdown.selected == "All" or c.startswith(dept_dropdown.selected))
            and search_text.lower() in c.lower()
        ]

        visible_courses = filtered[scroll_offset:scroll_offset + 18]
        course_rects = []
        
        for i, course in enumerate(visible_courses):
            y = 170 + i * 30
            if y + 25 > 700:
                break
            course_rect = pygame.Rect(selector_x + 20, y, selector_width - 60, 25)
            pygame.draw.rect(surface, WHITE, course_rect)
            pygame.draw.rect(surface, BLACK, course_rect, 1)
            surface.blit(FONT.render(course, True, BLACK), (course_rect.x + 5, course_rect.y + 5))
            course_rects.append((course_rect, course))

        # Draw dropdown options on top (if expanded)
        if dept_dropdown.expanded:
            dept_dropdown.draw(surface)

        # Draw scrollbar
        scrollbar_rect = pygame.Rect(SCROLL_BAR_X, SCROLL_BAR_Y, SCROLL_BAR_WIDTH, SCROLL_AREA_HEIGHT)
        pygame.draw.rect(surface, LIGHT_GRAY, scrollbar_rect)
        pygame.draw.rect(surface, BLACK, scrollbar_rect, 1)

        # Calculate and draw scroll handle
        total_courses = len(filtered)
        max_offset = max(0, total_courses - 18)
        scroll_ratio = scroll_offset / max_offset if max_offset > 0 else 0
        handle_height = max(40, int(SCROLL_AREA_HEIGHT * min(1, 18 / total_courses)))
        handle_y = SCROLL_BAR_Y + int((SCROLL_AREA_HEIGHT - handle_height) * scroll_ratio)

        scroll_handle_rect = pygame.Rect(SCROLL_BAR_X, handle_y, SCROLL_BAR_WIDTH, handle_height)
        pygame.draw.rect(surface, GRAY, scroll_handle_rect)
        pygame.draw.rect(surface, BLACK, scroll_handle_rect, 1)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if scroll_handle_rect.collidepoint(event.pos):
                    is_dragging_scrollbar = True
                    scroll_drag_offset_y = event.pos[1] - scroll_handle_rect.y
                elif close_btn.collidepoint(event.pos):
                    running = False
                elif dept_dropdown.handle_event(event, surface.get_rect()):
                    continue
                else:
                    for rect, course in course_rects:
                        if rect.collidepoint(event.pos):
                            box.course = course
                            running = False
            elif event.type == MOUSEBUTTONUP:
                is_dragging_scrollbar = False
            elif event.type == MOUSEMOTION and is_dragging_scrollbar:
                mouse_y = event.pos[1]
                new_handle_y = mouse_y - scroll_drag_offset_y
                new_handle_y = max(SCROLL_BAR_Y, min(SCROLL_BAR_Y + SCROLL_AREA_HEIGHT - handle_height, new_handle_y))
                scroll_ratio = (new_handle_y - SCROLL_BAR_Y) / (SCROLL_AREA_HEIGHT - handle_height)
                scroll_offset = int(scroll_ratio * max_offset)
            elif event.type == MOUSEWHEEL:
                scroll_offset -= event.y
                scroll_offset = max(0, min(scroll_offset, max_offset))
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_BACKSPACE:
                    search_text = search_text[:-1]
                elif event.unicode:
                    search_text += event.unicode

def show_course_info(course_name):
    parts = course_name.split(":")[0].split()
    if len(parts) < 2:
        return
    dept, code = parts[0], parts[1]

    for school in courses.values():
        if dept in school and code in school[dept]:
            data = school[dept][code]
            break
    else:
        return

    running = True
    
    # Get the main surface and dimensions from the parent window
    surface = pygame.display.get_surface()
    window_width = surface.get_width()
    right_panel_x = 250  # Left column width from main.py
    right_panel_width = window_width - right_panel_x
    
    # Adjust coordinates relative to right panel
    info_x = right_panel_x + 20
    info_width = right_panel_width - 40
    close_btn = pygame.Rect(info_x + info_width - 60, 110, 40, 30)
    
    while running:
        # Draw info window in right panel area
        pygame.draw.rect(surface, LIGHT_GRAY, (info_x, 100, info_width, 600))
        pygame.draw.rect(surface, BLACK, (info_x, 100, info_width, 600), 2)

        # Draw close button
        pygame.draw.rect(surface, RED, close_btn)
        surface.blit(FONT.render("X", True, WHITE), (close_btn.x + 12, close_btn.y + 6))

        # Draw course name at the top
        surface.blit(BIG_FONT.render(course_name, True, BLACK), (info_x + 20, 130))
        
        y_offset = 180
        for key, val in data.items():
            # Special handling for Prereqs and Coreqs
            if key in ["Prereqs", "Coreqs"] and isinstance(val, (dict, list)):
                # Render the key
                key_surface = FONT.render(f"{key}:", True, BLACK)
                surface.blit(key_surface, (info_x + 20, y_offset))
                y_offset += 30
                
                # Decode and wrap the requirements
                decoded_reqs = decode_requirement(val, top_level=True)
                wrapped_lines = wrap_text(decoded_reqs, FONT, info_width - 60)
                
                for line in wrapped_lines:
                    surface.blit(FONT.render(line, True, BLACK), (info_x + 40, y_offset))
                    y_offset += 25
                
                y_offset += 15
            else:
                # Regular field rendering
                key_surface = FONT.render(f"{key}:", True, BLACK)
                surface.blit(key_surface, (info_x + 20, y_offset))
                
                wrapped_lines = wrap_text(str(val), FONT, info_width - 60)
                for line in wrapped_lines:
                    y_offset += 30
                    surface.blit(FONT.render(line, True, BLACK), (info_x + 40, y_offset))
            
            y_offset += 40

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and close_btn.collidepoint(event.pos):
                running = False

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def decode_requirement(req, parent_op=None, top_level=False):
    """
    Recursively deciphers a nested prerequisite/corequisite structure.
    """
    if isinstance(req, dict):
        keys = list(req.keys())
        # Check if this dict represents a group with an operator
        if len(keys) == 1 and keys[0] in ["AND", "OR"]:
            op = keys[0]
            children = req[op]
            # Process each child; pass the current operator as parent_op
            sub_strings = [decode_requirement(child, parent_op=op, top_level=False) for child in children]
            # Filter out any empty strings
            sub_strings = [s for s in sub_strings if s]
            # Join using the operator
            joined = f" {op} ".join(sub_strings)
            # Always enclose OR groups in brackets
            # Also, if an AND group is nested inside an OR group, enclose it
            if op == "OR" or (parent_op == "OR" and op == "AND"):
                return f"[{joined}]"
            else:
                return joined
        else:
            # It's a leaf requirement
            dept = req.get("Department", "")
            code = req.get("Course Code", "")
            grade = req.get("Grade", "")
            if dept or code or grade:
                if grade:
                    return f"{dept} {code} (min grade {grade})"
                else:
                    return f"{dept} {code}"
            else:
                return ""
    elif isinstance(req, list):
        # If req is a list, join the items
        sub_strings = [decode_requirement(item, parent_op=parent_op, top_level=top_level) for item in req]
        return " ".join(sub_strings)
    else:
        return str(req)

columns = [Column(20)]
add_column_btn = pygame.Rect(20 + len(columns) * 220, 10, 140, 40)
scroll_bar_rect = pygame.Rect(0, HEIGHT - 40, WIDTH, SCROLL_BAR_HEIGHT)
scroll_handle_rect = pygame.Rect(0, HEIGHT - 40, 100, SCROLL_BAR_HEIGHT)

def add_column():
    x = 20 + len(columns) * 220
    columns.append(Column(x))
    global add_column_btn
    add_column_btn = pygame.Rect(20 + len(columns) * 220, 10, 140, 40)

def update_scroll_handle():
    total_width = len(columns) * 220 + 180
    view_ratio = WIDTH / total_width if total_width > WIDTH else 1
    scroll_handle_rect.width = max(60, int(WIDTH * view_ratio))
    scroll_handle_rect.x = int(SCROLL_X / total_width * WIDTH) if total_width > WIDTH else 0

def init():
    global columns, add_column_btn, scroll_bar_rect, scroll_handle_rect, WIDTH, HEIGHT
    columns = [Column(20)]
    add_column_btn = pygame.Rect(20 + len(columns) * 220, 10, 140, 40)
    scroll_bar_rect = pygame.Rect(0, HEIGHT - 40, WIDTH, SCROLL_BAR_HEIGHT)
    scroll_handle_rect = pygame.Rect(0, HEIGHT - 40, 100, SCROLL_BAR_HEIGHT)

def render(surface, area_rect, font, BLACK, BLUE):
    global SCROLL_X, is_dragging_scroll, scroll_drag_offset, WIDTH, HEIGHT, COLUMN_HEIGHT
    
    # Update dimensions based on the provided area_rect
    WIDTH = area_rect.width
    HEIGHT = area_rect.height
    COLUMN_HEIGHT = HEIGHT - 100  # Adjust column height based on window height
    
    # Clear the content area
    pygame.draw.rect(surface, WHITE, area_rect)
    pygame.draw.rect(surface, BLACK, area_rect, 2)
    
    # Draw the curriculum planner content
    for col in columns:
        col.draw(surface, SCROLL_X)

    # Draw add column button with scaled position
    add_column_btn.x = area_rect.x + 20 + len(columns) * 220 - SCROLL_X
    add_column_btn.y = area_rect.y + 10
    pygame.draw.rect(surface, GREEN, add_column_btn)
    pygame.draw.rect(surface, BLACK, add_column_btn, 2)
    surface.blit(FONT.render("+ Add Column", True, BLACK), (add_column_btn.x + 10, add_column_btn.y + 10))

    # Draw scrollbar at bottom of content area, but only in the right panel
    right_panel_x = 250  # Left column width from main.py
    scroll_bar_rect.width = WIDTH - right_panel_x
    scroll_bar_rect.x = area_rect.x + right_panel_x
    scroll_bar_rect.y = area_rect.y + HEIGHT - 40
    
    # Position scroll handle within the right panel
    scroll_handle_rect.y = area_rect.y + HEIGHT - 40
    update_scroll_handle()
    scroll_handle_rect.x = area_rect.x + right_panel_x + int(SCROLL_X / (len(columns) * 220 + 180) * (WIDTH - right_panel_x))
    
    pygame.draw.rect(surface, LIGHT_GRAY, scroll_bar_rect)
    pygame.draw.rect(surface, GRAY, scroll_handle_rect)

    # Draw expanded dropdowns on top
    for col in columns:
        if col.semester_dropdown.expanded:
            col.semester_dropdown.draw(surface)

def handle_event(event, area_rect):
    global SCROLL_X, is_dragging_scroll, scroll_drag_offset
    
    # Convert mouse position to be relative to the content area for mouse events
    if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
        mouse_pos = pygame.mouse.get_pos()
        adjusted_pos = (
            mouse_pos[0] - area_rect.x,
            mouse_pos[1] - area_rect.y
        )
        
        # Store positions for collision detection
        event.original_pos = mouse_pos
        event.pos = adjusted_pos
    
    if event.type == MOUSEBUTTONDOWN:
        # Create relative rectangles for collision detection
        add_column_relative = pygame.Rect(
            add_column_btn.x - area_rect.x,
            add_column_btn.y - area_rect.y,
            add_column_btn.width,
            add_column_btn.height
        )
        scroll_handle_relative = pygame.Rect(
            scroll_handle_rect.x - area_rect.x,
            scroll_handle_rect.y - area_rect.y,
            scroll_handle_rect.width,
            scroll_handle_rect.height
        )
        scroll_bar_relative = pygame.Rect(
            scroll_bar_rect.x - area_rect.x,
            scroll_bar_rect.y - area_rect.y,
            scroll_bar_rect.width,
            scroll_bar_rect.height
        )

        if add_column_relative.collidepoint(event.pos):
            add_column()
        elif scroll_handle_relative.collidepoint(event.pos):
            is_dragging_scroll = True
            scroll_drag_offset = event.pos[0] - scroll_handle_rect.x
        elif scroll_bar_relative.collidepoint(event.pos):
            mouse_x = event.pos[0]
            total_width = len(columns) * 220 + 180
            SCROLL_X = int((mouse_x / WIDTH) * total_width) - WIDTH // 2
            SCROLL_X = max(0, min(SCROLL_X, total_width - WIDTH))
    
    if event.type == MOUSEBUTTONUP:
        is_dragging_scroll = False
    
    if event.type == MOUSEMOTION and is_dragging_scroll:
        total_width = len(columns) * 220 + 180
        new_x = event.pos[0] - scroll_drag_offset
        scroll_ratio = new_x / WIDTH
        SCROLL_X = int(scroll_ratio * total_width)
        SCROLL_X = max(0, min(SCROLL_X, total_width - WIDTH))

    if event.type == KEYDOWN:
        if event.key == K_RIGHT:
            SCROLL_X += SCROLL_SPEED
        elif event.key == K_LEFT:
            SCROLL_X = max(0, SCROLL_X - SCROLL_SPEED)
        elif event.key == K_a:
            add_column()
    
    # Pass the area_rect to column event handlers
    for col in columns:
        col.handle_event(event, area_rect)

# Initialize when module is imported
init()
