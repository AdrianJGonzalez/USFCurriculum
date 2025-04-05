import pygame
from utils import draw_multiline_text, get_multiline_text_height

# Add state variables for page navigation
current_page = 0
button_clicked = False  # Add state to track button clicks

def render(surface, area_rect, font, BLACK, BLUE, scroll_offset=0):
    global current_page, button_clicked
    padding = 20
    bottom_padding = 50
    text_area_width = area_rect.width - 2 * padding
    current_y = area_rect.y + padding - scroll_offset

    # Define pages content
    pages = [
        # Page 1: Overview and Key Features
        [
            ("Overview", 
             "This application is a comprehensive academic planning and advising tool designed specifically for Electrical Engineering students at the University of South Florida. It serves as a central hub for curriculum planning, academic advising, and degree progress tracking."),
            
            ("Key Features", """
• Curriculum Flowchart Creator: Visualize and plan your academic journey through the EE program
• Interactive Advising Portal: Connect with academic advisors and access important advising resources
• Transcript Analysis: Upload and analyze your academic transcript to track degree progress
• FAQ Section: Quick access to common questions about advising and curriculum
• Department Information: Direct access to EE department resources and contacts"""),
        ],
        # Page 2: Advising and Curriculum
        [
            ("Advising Resources", """
The application provides direct access to EE academic advisors:
• Schedule appointments with advisors
• View walk-in advising hours (Tuesdays and Thursdays, 10 AM - 4 PM at ENB 379)
• Contact advisors via email at ENG-EEAdvising@usf.edu
• Access the official USF EE advising website"""),
            
            ("Curriculum Planning", """
The curriculum planning features help you:
• Visualize course prerequisites and co-requisites
• Plan future semester schedules
• Track completed courses
• Identify remaining degree requirements"""),
        ],
        # Page 3: Development and Usage
        [
            ("Development", """
This application was developed for the USF Electrical Engineering Department to streamline the academic planning and advising process. It combines modern technology with user-friendly interfaces to enhance the student experience in academic planning and progression tracking."""),
            
            ("How to Use", """
1. Use the navigation menu on the left to access different sections
2. Visit the Curriculum section to plan your courses
3. Check the Advising section to connect with academic advisors
4. Upload your transcript to track your progress
5. Consult the FAQ section for quick answers to common questions""")
        ]
    ]

    # Title
    title_font = pygame.font.Font(None, 36)
    title = f"About This Application (Page {current_page + 1} of {len(pages)})"
    title_surface = title_font.render(title, True, BLACK)
    surface.blit(title_surface, (area_rect.x + padding, current_y))
    current_y += title_surface.get_height() + 30

    # Render current page content
    for title, content in pages[current_page]:
        # Section title
        section_title_font = pygame.font.Font(None, 28)
        section_title_surface = section_title_font.render(title, True, BLACK)
        surface.blit(section_title_surface, (area_rect.x + padding, current_y))
        current_y += section_title_surface.get_height() + 10

        # Section content
        content_height = get_multiline_text_height(content, font, text_area_width - 20)
        draw_multiline_text(
            surface,
            content,
            (area_rect.x + padding + 10, current_y),
            font,
            BLACK,
            text_area_width - 20
        )
        current_y += content_height + 30

    # Navigation buttons
    button_width = 100
    button_height = 30
    button_y = area_rect.bottom - button_height - padding
    
    # Get mouse state
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    # Reset button_clicked if mouse is not pressed
    if not mouse_clicked:
        button_clicked = False

    # Previous button (if not on first page)
    if current_page > 0:
        prev_button_rect = pygame.Rect(
            area_rect.x + padding,
            button_y,
            button_width,
            button_height
        )
        pygame.draw.rect(surface, (200, 200, 200), prev_button_rect)
        pygame.draw.rect(surface, BLACK, prev_button_rect, 2)
        prev_text = font.render("Previous", True, BLACK)
        prev_text_rect = prev_text.get_rect(center=prev_button_rect.center)
        surface.blit(prev_text, prev_text_rect)

        # Handle previous button click
        if mouse_clicked and prev_button_rect.collidepoint(mouse_pos) and not button_clicked:
            current_page = max(0, current_page - 1)
            button_clicked = True

    # Next button (if not on last page)
    if current_page < len(pages) - 1:
        next_button_rect = pygame.Rect(
            area_rect.right - button_width - padding,
            button_y,
            button_width,
            button_height
        )
        pygame.draw.rect(surface, (200, 200, 200), next_button_rect)
        pygame.draw.rect(surface, BLACK, next_button_rect, 2)
        next_text = font.render("Next", True, BLACK)
        next_text_rect = next_text.get_rect(center=next_button_rect.center)
        surface.blit(next_text, next_text_rect)

        # Handle next button click
        if mouse_clicked and next_button_rect.collidepoint(mouse_pos) and not button_clicked:
            current_page = min(len(pages) - 1, current_page + 1)
            button_clicked = True

    # Calculate total content height for scrolling
    total_content_height = current_y + bottom_padding
    
    # Ensure scroll offset stays within bounds
    max_scroll = max(0, total_content_height - area_rect.height)
    return max(0, min(scroll_offset, max_scroll))

def handle_event(event):
    """
    Handle any cleanup when switching pages
    """
    global current_page
    if event.type == pygame.MOUSEBUTTONDOWN:
        return
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            current_page = max(0, current_page - 1)
        elif event.key == pygame.K_RIGHT:
            current_page = min(2, current_page + 1)
