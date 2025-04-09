import os
import pygame
from utils import draw_multiline_text, get_multiline_text_height

# Determine the base directory for the FAQ folder
CURRENT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
IMAGES_DIR = os.path.join(BASE_DIR, "faq_images", "Electrical_Engineering")

# FAQ text content
faq_text = """Frequently Asked Questions - Electrical Engineering

Q: What are the prerequisites for the Electrical Engineering program?
A: Prerequisites include:
• Calculus I, II, and III
• Physics I with lab
• Chemistry for Engineers with lab
• Minimum overall GPA of 3.0 in those classes
• Minimum GPA of 2.75 with Advisor approval 

Q: What specializations are available in Electrical Engineering?
A: Our program offers several focus areas:
• Communications and Signal Processing
• Micro and Nano Eelectronics
• Power and Energy Systems
• Mechatronics and Controls
• Systems and Security
• Wireless and Microwave Communications

Q: What GPA do I need to maintain in the program?
A: Students must maintain:
• Minimum 2.0 GPA overall
• Minimum 2.0 GPA in all engineering courses
• Grade of C- or better in all engineering courses"""

# Additional FAQ content that shows when "See More" is clicked
additional_faq_text = """
Q: Are internships available/required?
A: Internships are strongly encouraged but not required. The department works with many local and national companies to provide internship opportunities. Visit the Career Services office for more information about available positions.

Q: What career paths are available with an EE degree?
A: EE graduates pursue careers in:
• Power and Energy Companies
• Telecommunications
• Aerospace and Defense
• Semiconductor Industry
• Robotics and Automation
• Research and Development
• Graduate Studies

Q: Can I pursue a minor with my EE degree?
A: Yes! Popular minors include:
• Computer Science
• Mathematics
• Physics
• Business
• Biomedical Engineering
Contact your academic advisor to plan your minor coursework.

Q: Are there research opportunities for undergraduates?
A: Yes! Many faculty members welcome undergraduate researchers in their labs. Areas include:
• Power Systems
• Wireless Communications
• Microelectronics
• Machine Learning
• Renewable Energy
Contact individual professors about their research opportunities.

Q: What student organizations are available?
A: Several professional and social organizations are active:
• IEEE Student Branch
• Society of Women Engineers (SWE)
• Engineers Without Borders
• Robotics Club

Q: What computing resources are available?
A: Students have access to:
• Engineering Computer Labs
• Software Licenses (MATLAB, Cadence, etc.)
• High-Performance Computing Cluster
• Virtual Machine Access
• Circuit Simulation Tools"""

# Add state variable to track which page we're on
show_text_page = False

def render(surface, area_rect, font, BLACK, BLUE, scroll_offset):
    """
    Draws the Electrical Engineering FAQ page in the given area.
    """
    global show_text_page
    padding = 20
    text_area_width = area_rect.width - 2 * padding

    # If we're showing the text page
    if show_text_page:
        # Draw back button
        back_button_rect = pygame.Rect(area_rect.x + padding, area_rect.y + padding, 100, 30)
        pygame.draw.rect(surface, (200, 200, 200), back_button_rect)
        pygame.draw.rect(surface, BLACK, back_button_rect, 2)
        back_text = font.render("< Back", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        surface.blit(back_text, back_text_rect)

        # Draw the full text below the back button
        full_text = faq_text + "\n\n" + additional_faq_text
        text_pos = (area_rect.x + padding, area_rect.y + padding + 50)
        draw_multiline_text(surface, full_text, text_pos, font, BLACK, text_area_width)

        # Handle back button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if mouse_clicked and back_button_rect.collidepoint(mouse_pos):
            show_text_page = False

        return 0

    # Main page layout
    current_y = area_rect.y + padding

    # Draw title
    title = "Electrical Engineering Department FAQ"
    title_surface = font.render(title, True, BLACK)
    surface.blit(title_surface, (area_rect.x + padding, current_y))
    
    # Calculate available height for text
    available_height = area_rect.bottom - current_y - padding
    
    # Calculate if text will fit
    text_height = get_multiline_text_height(faq_text + "\n\n" + additional_faq_text, font, text_area_width)
    
    if text_height > available_height:
        # Text won't fit, show preview and "See More" button
        preview_text = faq_text  # Show first part
        draw_multiline_text(surface, preview_text, 
                          (area_rect.x + padding, current_y + font.get_linesize() + 10),
                          font, BLACK, text_area_width)
        
        # Draw "See More" button
        button_width = 120
        button_height = 30
        button_rect = pygame.Rect(
            area_rect.centerx - button_width//2,
            area_rect.bottom - button_height - padding,
            button_width,
            button_height
        )
        pygame.draw.rect(surface, (200, 200, 200), button_rect)
        pygame.draw.rect(surface, BLACK, button_rect, 2)
        button_text = font.render("See More", True, BLACK)
        text_rect = button_text.get_rect(center=button_rect.center)
        surface.blit(button_text, text_rect)
        
        # Handle button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if mouse_clicked and button_rect.collidepoint(mouse_pos):
            show_text_page = True
    else:
        # Text fits, show it all
        full_text = faq_text + "\n\n" + additional_faq_text
        draw_multiline_text(surface, full_text,
                          (area_rect.x + padding, current_y + font.get_linesize() + 10),
                          font, BLACK, text_area_width)

    return 0

def handle_event(event):
    """
    Handle any cleanup when switching pages
    """
    global show_text_page
    if event.type == pygame.MOUSEBUTTONDOWN:
        return
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        show_text_page = False
