import os
import pygame
from utils import draw_multiline_text, get_multiline_text_height

# Determine the base directory for the advising folder
CURRENT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
IMAGES_DIR = os.path.join(BASE_DIR, "advisor_images", "Electrical_Engineering")

# Build absolute paths to the images
image1_path = os.path.join(IMAGES_DIR, "uysal.png")
image2_path = os.path.join(IMAGES_DIR, "amy.png")

# Load advisor images
try:
    advisor_image1 = pygame.image.load(image1_path)
    advisor_image2 = pygame.image.load(image2_path)
except Exception as e:
    advisor_image1 = pygame.Surface((100, 100))
    advisor_image1.fill((150, 150, 150))
    advisor_image2 = pygame.Surface((100, 100))
    advisor_image2.fill((100, 150, 150))

# Scale images
advisor_image1 = pygame.transform.scale(advisor_image1, (100, 125))
advisor_image2 = pygame.transform.scale(advisor_image2, (100, 125))

# Advisor details - split name and title for better formatting
advisor1_name = "Dr. Ismail Uysal"
advisor1_title = "Undergraduate Program Director"
advisor1_link = "https://calendly.com/iuysal/advising"

advisor2_name = "Amy Lyn Medicielo"
advisor2_title = "Undergraduate Program Specialist"
advisor2_link = "https://calendly.com/iuysal/advising"

# Original text, formatted for better readability
advisors_text = """Dear students,

If you have submitted your ULDP (Upper-Level) form, it has been processed & accepted, and you would like to book an advising appointment - you've come to the right place. You have multiple options available to you for booking your appointment.

WALK-IN HOURS (Updated for Spring 2025):
• Location: Main EE office (ENB 379)
• Time: 10AM - 4PM on Mondays and Wednesdays
• First-come-first-serve basis
• Walk-in hours begin Monday, Jan 28th

*** IMPORTANT: These days are updated for Spring - they used to be Tuesday/Thursday - please note the new days! ***

ONLINE APPOINTMENTS:
• Book using the Calendly links below
• If you don't see available slots, use walk-in hours
• After booking, you'll receive a Microsoft Teams meeting invitation
• Choose ONE slot only

Remember: Once confirmed, you will receive a calendar invitation for your Teams meeting on or before your scheduled appointment."""

# Add state variable to track which page we're on
show_text_page = False

def render(surface, area_rect, font, BLACK, BLUE, scroll_offset):
    """
    Draws the Electrical Engineering advisors page in the given area.
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
        text_pos = (area_rect.x + padding, area_rect.y + padding + 50)
        draw_multiline_text(surface, advisors_text, text_pos, font, BLACK, text_area_width)

        # Handle back button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if mouse_clicked and back_button_rect.collidepoint(mouse_pos):
            show_text_page = False

        return 0

    # Main page layout
    current_y = area_rect.y + padding

    # Position advisors side by side
    advisor1_x = area_rect.x + padding
    advisor2_x = area_rect.centerx + padding

    # Draw first advisor block (left side)
    name1_surface = font.render(advisor1_name, True, BLACK)
    surface.blit(name1_surface, (advisor1_x, current_y))
    
    title1_y = current_y + font.get_linesize()
    title1_surface = font.render(advisor1_title, True, BLACK)
    surface.blit(title1_surface, (advisor1_x, title1_y))
    
    image1_y = title1_y + font.get_linesize() + 5
    surface.blit(advisor_image1, (advisor1_x, image1_y))
    
    link1_y = image1_y + advisor_image1.get_height() + 5
    link1_surface = font.render(advisor1_link, True, BLUE)
    surface.blit(link1_surface, (advisor1_x, link1_y))

    # Draw second advisor block (right side)
    name2_surface = font.render(advisor2_name, True, BLACK)
    surface.blit(name2_surface, (advisor2_x, current_y))
    
    title2_surface = font.render(advisor2_title, True, BLACK)
    surface.blit(title2_surface, (advisor2_x, title1_y))
    
    surface.blit(advisor_image2, (advisor2_x, image1_y))
    
    link2_surface = font.render(advisor2_link, True, BLUE)
    surface.blit(link2_surface, (advisor2_x, link1_y))

    # Calculate where advisor section ends
    advisor_section_bottom = link1_y + font.get_linesize() + 20

    # Draw separator line
    pygame.draw.line(surface, BLACK, 
                    (area_rect.x + padding, advisor_section_bottom),
                    (area_rect.right - padding, advisor_section_bottom),
                    1)

    # Calculate available height for text
    available_height = area_rect.bottom - advisor_section_bottom - padding
    
    # Calculate if text will fit
    text_height = get_multiline_text_height(advisors_text, font, text_area_width)
    
    if text_height > available_height:
        # Text won't fit, show preview and "See More" button
        preview_text = advisors_text.split('\n\n')[0] + "\n\n..."  # Show first paragraph
        draw_multiline_text(surface, preview_text, 
                          (area_rect.x + padding, advisor_section_bottom + 20),
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
        draw_multiline_text(surface, advisors_text,
                          (area_rect.x + padding, advisor_section_bottom + 20),
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