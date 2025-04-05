import os
import pygame
import importlib
from utils import draw_multiline_text, get_multiline_text_height

# List of departments (add more entries as needed)
departments = [
    {
        "name": "Electrical Engineering",
        "module": "pages.advising.Departments.electrical_engineering_adv"
    }
    ,
    {
        "name": "Mechanical Engineering",
        "module": "pages.advising.Departments.mechanical_engineering_adv"
    }
]


# Global state for the advisors page
selected_department = None  # When None, grid mode is active (with search)
grid_offset = 0             # Vertical scroll offset for the department grid
content_offset = 0          # Vertical scroll offset for department content

# Flags to register single clicks
grid_click_registered = False
content_click_registered = False
search_click_registered = False

# Global search state
search_query = ""
search_active = False

def process_search_event(event):
    """
    Call this from your main event loop (for KEYDOWN events)
    to update the search query when the search box is active.
    Pressing Enter deactivates the search field.
    """
    global search_query, search_active
    if search_active and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            search_active = False
        elif event.key == pygame.K_BACKSPACE:
            search_query = search_query[:-1]
        else:
            if event.unicode.isprintable():
                search_query += event.unicode

def render(surface, area_rect, font, BLACK, BLUE, scroll_offset):
    global selected_department, grid_offset, content_offset
    global grid_click_registered, content_click_registered, search_click_registered, search_active, search_query

    # Update scroll offsets
    if selected_department is None:
        grid_offset += scroll_offset
    else:
        content_offset += scroll_offset

    if selected_department is None:
        # ----- GRID MODE: Show Department Grid with Search Column -----
        # Divide the area into left and right columns.
        left_ratio = 0.65  # Left column for grid (65%)
        left_area_width = int(area_rect.width * left_ratio)
        left_area_rect = pygame.Rect(area_rect.x, area_rect.y, left_area_width, area_rect.height)
        right_area_rect = pygame.Rect(area_rect.x + left_area_width, area_rect.y,
                                      area_rect.width - left_area_width, area_rect.height)

        # Draw the search feature in the right column
        pygame.draw.rect(surface, (240, 240, 240), right_area_rect)  # light gray background
        pygame.draw.rect(surface, BLACK, right_area_rect, 2)
        search_box_height = 40
        search_box_rect = pygame.Rect(right_area_rect.x + 10, right_area_rect.y + 10,
                                      right_area_rect.width - 20, search_box_height)
        # Show blue border when active
        border_color = (0, 0, 255) if search_active else (0, 0, 0)
        pygame.draw.rect(surface, (255, 255, 255), search_box_rect)  # white background for search box
        pygame.draw.rect(surface, border_color, search_box_rect, 2)
        display_text = search_query if search_query else "Search..."
        search_text_display = font.render(display_text, True, BLACK)
        surface.blit(search_text_display, (search_box_rect.x + 5,
                                           search_box_rect.y + (search_box_rect.height - font.get_height()) // 2))
        # Activate search on click
        if pygame.mouse.get_pressed()[0]:
            if search_box_rect.collidepoint(pygame.mouse.get_pos()) and not search_click_registered:
                search_active = True
                search_click_registered = True
        else:
            search_click_registered = False

        # Filter and draw the department grid in the left column
        filtered_departments = ([dept for dept in departments if search_query.lower() in dept["name"].lower()]
                                if search_query else departments)
        margin = 10
        button_height = 60
        button_width = (left_area_rect.width - 3 * margin) // 2
        num_departments = len(filtered_departments)
        num_rows = (num_departments + 1) // 2  # round up
        grid_total_height = num_rows * (button_height + margin) + margin
        max_scroll = max(0, grid_total_height - left_area_rect.height)
        grid_offset = max(0, min(grid_offset, max_scroll))
        if num_departments == 0:
            no_match_text = font.render("No matching departments found.", True, BLACK)
            surface.blit(no_match_text, (left_area_rect.x + margin, left_area_rect.y + margin))
        else:
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            for i, dept in enumerate(filtered_departments):
                row = i // 2
                col = i % 2
                x = left_area_rect.x + margin + col * (button_width + margin)
                y = left_area_rect.y + margin + row * (button_height + margin) - grid_offset
                rect = pygame.Rect(x, y, button_width, button_height)
                pygame.draw.rect(surface, (220, 220, 220), rect)
                pygame.draw.rect(surface, BLACK, rect, 2)
                text_surface = font.render(dept["name"], True, BLACK)
                text_rect = text_surface.get_rect(center=rect.center)
                surface.blit(text_surface, text_rect)
                if mouse_buttons[0] and rect.collidepoint(mouse_pos) and not grid_click_registered:
                    selected_department = dept
                    content_offset = 0
                    grid_click_registered = True
            if not mouse_buttons[0]:
                grid_click_registered = False

    else:
        # ----- DEPARTMENT MODE: Show the Department Advisor's Page Without the Search Column -----
        # Draw a "Back" button at the top left
        back_button_width = 80
        back_button_height = 30
        back_button_rect = pygame.Rect(area_rect.x + 10, area_rect.y + 10,
                                       back_button_width, back_button_height)
        pygame.draw.rect(surface, (200, 200, 200), back_button_rect)
        pygame.draw.rect(surface, BLACK, back_button_rect, 2)
        back_text = font.render("< Back", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        surface.blit(back_text, back_text_rect)
        # Check for back button click: clear search state and return to grid mode
        if pygame.mouse.get_pressed()[0]:
            if back_button_rect.collidepoint(pygame.mouse.get_pos()) and not content_click_registered:
                search_query = ""
                search_active = False
                selected_department = None
                grid_offset = 0
                content_click_registered = True
                return
        else:
            content_click_registered = False

        # Use the entire area (minus back button area) for the department content
        content_y = back_button_rect.bottom + 10
        content_area_rect = pygame.Rect(area_rect.x, content_y,
                                        area_rect.width, area_rect.height - (content_y - area_rect.y))
        # Import and render the selected department module dynamically
        dept_module_path = selected_department["module"]
        try:
            dept_module = importlib.import_module(dept_module_path)
        except Exception as e:
            error_text = font.render("Error importing module: " + dept_module_path, True, (255, 0, 0))
            surface.blit(error_text, (content_area_rect.x + 10, content_area_rect.y + 10))
            return
        if hasattr(dept_module, "render"):
            dept_module.render(surface, content_area_rect, font, BLACK, BLUE, content_offset)
        else:
            error_text = font.render("No render() function in " + dept_module_path, True, (255, 0, 0))
            surface.blit(error_text, (content_area_rect.x + 10, content_area_rect.y + 10))