#This is in development and is not currently implemented to the larger application.
#Things that remain to be done on this test
#1. Add some vertical scrolling so that the user can read further down with more courses
#2. Make the boxes everso smaller in height
#3. Add the Prereqs and Coreq Arrows to the courses. (Make sure the arrows don't touch!)
#4. Give error window when adding duplicate classes
#5. Add scrolling into the Department filter in the course selection
#6. Add some "bar end" indicators on the scroll bars and typing indicators on the search boxes
#7. Add # of Credit Hours to the course box
#8. Center the indicator icons (X and !)
#9. Make the Semester indicator be the width of the column or centered
#10. Maybe add a scroll bar in course selector
#11. Add features that do not allow courses to be but in subsequent semesters if the prereq is not completed.
#Actually add an option to override.
#12. Integrate into the main program by adding it to main and by adding an "auto fill" feature from the transcript upload.
#13. Make it look a bit better visually and more inviting.
#14 Choose Better Colors (Maybe USF colors) for windows, buttons, ect.

import pygame
import sys
from pygame.locals import *
from courses import courses

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
        self.rect = pygame.Rect(x, y, width, 30)
        self.options = options
        self.selected = selected if selected else options[0]
        self.expanded = False

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)  # Added border
        text_surface = FONT.render(self.selected, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*30, self.rect.width, 30)
                pygame.draw.rect(screen, LIGHT_GRAY, option_rect)
                pygame.draw.rect(screen, BLACK, option_rect, 1)  # Border for each option
                screen.blit(FONT.render(option, True, BLACK), (option_rect.x + 5, option_rect.y + 5))

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Only handle left click
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                return True
            elif self.expanded:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*30, self.rect.width, 30)
                    if option_rect.collidepoint(event.pos):
                        self.selected = option
                        self.expanded = False
                        return True
                self.expanded = False
        return False


class Column:
    def __init__(self, x, semester="Fall", year="2025"):
        self.base_x = x
        self.semester_dropdown = Dropdown(x + 10, 10, ["Fall", "Spring", "Summer"])
        self.year_input = ""
        self.boxes = [Box()]
        self.year_rect = pygame.Rect(x + 110, 10, 60, 30)

    def draw(self, screen, offset):
        self.x = self.base_x - offset
        self.semester_dropdown.rect.x = self.x + 10
        self.year_rect.x = self.x + 110
        self.semester_dropdown.draw(screen)
        pygame.draw.rect(screen, WHITE, self.year_rect)
        pygame.draw.rect(screen, BLACK, self.year_rect, 1)
        screen.blit(FONT.render(self.year_input, True, BLACK), (self.year_rect.x+5, self.year_rect.y+5))

        for i, box in enumerate(self.boxes):
            y = 60 + i * 120  # 110 height + 10px padding
            if y + 80 < COLUMN_HEIGHT:
                box.draw(screen, self.x + 10, y)

    def handle_event(self, event):
        if self.semester_dropdown.handle_event(event):
            return
        if event.type == MOUSEBUTTONDOWN and self.year_rect.collidepoint(event.pos):
            self.active = True
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.year_input = self.year_input[:-1]
            elif event.unicode.isdigit() and len(self.year_input) < 4:
                self.year_input += event.unicode

        for box in self.boxes:
            box.handle_event(event)

        self.boxes = [box for box in self.boxes if box.course or box == self.boxes[-1]]
        if not self.boxes or self.boxes[-1].course:
            self.boxes.append(Box())

class Box:
    def __init__(self):
        self.course = None
        self.rect = pygame.Rect(0, 0, 180, 110)  # Increased height
        self.add_btn = pygame.Rect(0, 0, 180, 110)
        self.delete_btn = pygame.Rect(0, 0, 25, 25)
        self.info_btn = pygame.Rect(0, 0, 25, 25)

    def draw(self, screen, x, y):
        self.rect.topleft = (x, y)
        self.add_btn.topleft = (x, y)
        self.delete_btn.topleft = (x + 5, y + self.rect.height - 30)
        self.info_btn.topleft = (x + 150, y + self.rect.height - 30)

        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        if self.course:
            # Split into code and name
            course_code, course_name = self.course.split(":", 1)
            course_code = course_code.strip()
            course_name = course_name.strip()

            # Fonts
            code_font = FONT
            name_font = pygame.font.SysFont('arial', 14)

            # Render and center course code
            code_surface = code_font.render(course_code, True, BLACK)
            code_rect = code_surface.get_rect(center=(x + self.rect.width // 2, y + 12))
            screen.blit(code_surface, code_rect)

            # Word-wrap course name
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

            name_lines = wrap_text(course_name, name_font, self.rect.width - 10)
            for i, line in enumerate(name_lines[:3]):  # Limit to 3 lines
                line_surface = name_font.render(line, True, BLACK)
                line_rect = line_surface.get_rect(center=(x + self.rect.width // 2, y + 34 + i * 16))
                screen.blit(line_surface, line_rect)

            # Draw buttons
            pygame.draw.rect(screen, RED, self.delete_btn)
            pygame.draw.rect(screen, BLACK, self.delete_btn, 1)
            screen.blit(FONT.render("X", True, WHITE), (self.delete_btn.x + 6, self.delete_btn.y + 3))

            pygame.draw.rect(screen, BLUE, self.info_btn)
            pygame.draw.rect(screen, BLACK, self.info_btn, 1)
            screen.blit(FONT.render("!", True, WHITE), (self.info_btn.x + 8, self.info_btn.y + 3))

        else:
            # Empty box: "+ Add Course"
            add_text = FONT.render("+ Add Course", True, GRAY)
            text_rect = add_text.get_rect(center=self.rect.center)
            screen.blit(add_text, text_rect)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.course:
                if self.delete_btn.collidepoint(event.pos):
                    self.course = None
                elif self.info_btn.collidepoint(event.pos):
                    show_course_info(self.course)
            elif self.add_btn.collidepoint(event.pos):
                open_course_selector(self)


def open_course_selector(box):
    search_text = ""
    running = True
    scroll_offset = 0

    departments = sorted({dept for school in courses.values() for dept in school})
    dept_dropdown = Dropdown(220, 120, ["All"] + departments, width=120, selected="All")

    close_btn = pygame.Rect(950, 110, 40, 30)

    while running:
        SCREEN.fill(WHITE)
        pygame.draw.rect(SCREEN, LIGHT_GRAY, (200, 100, 800, 600))
        pygame.draw.rect(SCREEN, BLACK, (200, 100, 800, 600), 2)

        pygame.draw.rect(SCREEN, RED, close_btn)
        SCREEN.blit(FONT.render("X", True, WHITE), (close_btn.x + 12, close_btn.y + 6))

        # Draw dropdown collapsed view
        pygame.draw.rect(SCREEN, GRAY, dept_dropdown.rect)
        pygame.draw.rect(SCREEN, BLACK, dept_dropdown.rect, 1)
        text_surface = FONT.render(dept_dropdown.selected, True, BLACK)
        text_rect = text_surface.get_rect(center=dept_dropdown.rect.center)
        SCREEN.blit(text_surface, text_rect)

        # Draw search box
        search_box = pygame.Rect(360, 120, 580, 30)
        pygame.draw.rect(SCREEN, WHITE, search_box)
        pygame.draw.rect(SCREEN, BLACK, search_box, 1)
        SCREEN.blit(FONT.render(search_text or "Search courses...", True, GRAY if not search_text else BLACK), (search_box.x + 5, search_box.y + 5))

        # Filter course list
        full_course_list = [
            f"{dept} {code}: {data['Class Full Name']}"
            for school in courses.values()
            for dept, dept_data in school.items()
            for code, data in dept_data.items()
        ]

        filtered = [
            c for c in full_course_list
            if (dept_dropdown.selected == "All" or c.startswith(dept_dropdown.selected))
            and search_text.lower() in c.lower()
        ]

        visible_courses = filtered[scroll_offset:scroll_offset + 18]

        course_rects = []
        for i, course in enumerate(visible_courses):
            y = 170 + i * 30
            if y + 25 > 700:
                break
            course_rect = pygame.Rect(220, y, 760, 25)
            pygame.draw.rect(SCREEN, WHITE, course_rect)
            pygame.draw.rect(SCREEN, BLACK, course_rect, 1)
            SCREEN.blit(FONT.render(course, True, BLACK), (course_rect.x + 5, course_rect.y + 5))
            course_rects.append((course_rect, course))

        # Draw dropdown options on top (if expanded)
        if dept_dropdown.expanded:
            dept_dropdown.draw(SCREEN)

        pygame.display.flip()

        for event in pygame.event.get():  # <-- Make sure this is at root level of `while running`
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEWHEEL:
                scroll_offset -= event.y
                scroll_offset = max(0, min(scroll_offset, max(0, len(filtered) - 18)))
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if close_btn.collidepoint(event.pos):
                    running = False
                elif dept_dropdown.handle_event(event):
                    continue
                else:
                    for rect, course in course_rects:
                        if rect.collidepoint(event.pos):
                            box.course = course
                            running = False
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
    close_btn = pygame.Rect(950, 110, 40, 30)
    while running:
        SCREEN.fill(WHITE)
        pygame.draw.rect(SCREEN, LIGHT_GRAY, (200, 100, 800, 600))
        pygame.draw.rect(SCREEN, BLACK, (200, 100, 800, 600), 2)

        pygame.draw.rect(SCREEN, RED, close_btn)
        SCREEN.blit(FONT.render("X", True, WHITE), (close_btn.x + 12, close_btn.y + 6))

        SCREEN.blit(BIG_FONT.render(course_name, True, BLACK), (220, 130))
        y_offset = 180
        for key, val in data.items():
            info = f"{key}: {val}"
            SCREEN.blit(FONT.render(info, True, BLACK), (220, y_offset))
            y_offset += 30

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and close_btn.collidepoint(event.pos):
                running = False

columns = [Column(20)]
add_column_btn = pygame.Rect(20 + len(columns) * 440, 10, 140, 40)
scroll_bar_rect = pygame.Rect(0, HEIGHT - 40, WIDTH, SCROLL_BAR_HEIGHT)
scroll_handle_rect = pygame.Rect(0, HEIGHT - 40, 100, SCROLL_BAR_HEIGHT)

def add_column():
    x = 20 + len(columns) * 440
    columns.append(Column(x))
    global add_column_btn
    add_column_btn = pygame.Rect(20 + len(columns) * 440, 10, 140, 40)

def update_scroll_handle():
    total_width = len(columns) * 440 + 180
    view_ratio = WIDTH / total_width if total_width > WIDTH else 1
    scroll_handle_rect.width = max(60, int(WIDTH * view_ratio))
    scroll_handle_rect.x = int(SCROLL_X / total_width * WIDTH) if total_width > WIDTH else 0

def main():
    global SCROLL_X, is_dragging_scroll, scroll_drag_offset
    clock = pygame.time.Clock()
    while True:
        SCREEN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if add_column_btn.collidepoint(event.pos):
                    add_column()
                if scroll_handle_rect.collidepoint(event.pos):
                    is_dragging_scroll = True
                    scroll_drag_offset = event.pos[0] - scroll_handle_rect.x
                elif scroll_bar_rect.collidepoint(event.pos):
                    mouse_x = event.pos[0]
                    total_width = len(columns) * 440 + 180
                    SCROLL_X = int((mouse_x / WIDTH) * total_width) - WIDTH // 2
                    SCROLL_X = max(0, min(SCROLL_X, total_width - WIDTH))
            if event.type == MOUSEBUTTONUP:
                is_dragging_scroll = False
            if event.type == MOUSEMOTION and is_dragging_scroll:
                total_width = len(columns) * 440 + 180
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
            for col in columns:
                col.handle_event(event)

        for col in columns:
            col.draw(SCREEN, SCROLL_X)

        add_column_btn.x = 20 + len(columns) * 440 - SCROLL_X
        pygame.draw.rect(SCREEN, GREEN, add_column_btn)
        pygame.draw.rect(SCREEN, BLACK, add_column_btn, 2)
        SCREEN.blit(FONT.render("+ Add Column", True, BLACK), (add_column_btn.x + 10, add_column_btn.y + 10))

        update_scroll_handle()
        pygame.draw.rect(SCREEN, LIGHT_GRAY, scroll_bar_rect)
        pygame.draw.rect(SCREEN, GRAY, scroll_handle_rect)

        for col in columns:
            if col.semester_dropdown.expanded:
                col.semester_dropdown.draw(SCREEN)

        pygame.display.flip()
        clock.tick(60)

main()

