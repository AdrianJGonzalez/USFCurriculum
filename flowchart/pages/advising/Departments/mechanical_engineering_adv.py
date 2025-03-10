import os
import pygame
from utils import draw_multiline_text, get_multiline_text_height

# Determine the base directory for the advising folder (one level up from Departments)
CURRENT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
# Define the subfolder where the advisor images are stored for Electrical Engineering
IMAGES_DIR = os.path.join(BASE_DIR, "advisor_images", "Electrical_Engineering")

# Build absolute paths to the images inside the advisor_images/Electrical_Engineering folder
image1_path = os.path.join(IMAGES_DIR, "uysal.png")
image2_path = os.path.join(IMAGES_DIR, "amy.png")

# Load advisor images using the absolute paths
try:
    advisor_image1 = pygame.image.load(image1_path)
    advisor_image2 = pygame.image.load(image2_path)
except Exception as e:
    advisor_image1 = pygame.Surface((100, 100))
    advisor_image1.fill((150, 150, 150))
    advisor_image2 = pygame.Surface((100, 100))
    advisor_image2.fill((100, 150, 150))

# Scale images if needed
advisor_image1 = pygame.transform.scale(advisor_image1, (120, 150))
advisor_image2 = pygame.transform.scale(advisor_image2, (120, 150))

# Advisor details
advisor1_name = "Dr.OOOf / Undergraduate Program Director"
advisor1_link = "https://calendly.com/iuysal/advising"

advisor2_name = "Amy Lyn Medicielo / Undergraduate Program Specialist"
advisor2_link = "https://calendly.com/iuysal/advising"

# Text content for the advisors page
advisors_text = """Dear students,

If you have submitted your ULDP (Upper-Level) form, it has been processed & accepted, and you would like to book an advising appointment - you've come to the right place. You have multiple options available to you for booking your appointment.

1) We have walk-in hours in the main EE office (ENB 379) between 10AM and 4PM on Mondays and Wednesdays (UPDATED FOR SPRING 2025). Please note that these are first-come-first-serve which means you may need to wait sometimes especially during the busy periods throughout the semester.

*** Walk-in hours for Spring 2025 will begin once again on Monday Jan 28th - feel free to stop by on Mondays/Wednesdays for any/all questions you may have regarding your progress in the program *** (These days are updated for Spring - they used to be Tuesday/Thursday - so please note the new days!)

2) You can book online appointments with our advisors. When you click the links below, you will be redirected to a page where you can select an available time slot for the advisor. If you do not see or cannot click on an option, it means it is already booked. You can still do a walk-in on between 10AM-4PM on Tuesdays and Thursdays as described above.

Remember that you can only choose ONE slot. Once confirmed, you will receive a calendar invitation for a Microsoft Teams meeting on or before the day of your scheduled appointment with us.
"""

def render(surface, area_rect, font, BLACK, BLUE, scroll_offset):
    """
    Draws the Electrical Engineering advisors page in the given area.
    """
    padding = 20
    text_area_width = area_rect.width - 2 * padding

    # Calculate text height and position advisors blocks after the text
    text_height = get_multiline_text_height(advisors_text, font, text_area_width)
    advisor1_top = padding + text_height + 20
    advisor1_block_height = (
        advisor_image1.get_height() +
        5 +  # gap before name
        font.get_linesize() +
        5 +  # gap before link
        font.get_linesize()
    )
    advisor1_bottom = advisor1_top + advisor1_block_height
    advisor2_top = advisor1_bottom + 40
    advisor2_block_height = (
        advisor_image2.get_height() +
        5 +
        font.get_linesize() +
        5 +
        font.get_linesize()
    )

    # Determine overall content height and clamp scroll_offset
    content_bottom = max(advisor1_bottom, advisor2_top + advisor2_block_height) + padding
    max_scroll = max(0, content_bottom - area_rect.height)
    scroll_offset = max(0, min(scroll_offset, max_scroll))

    # Draw the multiline text
    draw_multiline_text(
        surface,
        advisors_text,
        (area_rect.x + padding, area_rect.y + padding - scroll_offset),
        font,
        BLACK,
        text_area_width
    )

    # Draw first advisor block
    image1_x = area_rect.x + padding
    surface.blit(advisor_image1, (image1_x, advisor1_top - scroll_offset))
    name1_y = advisor1_top + advisor_image1.get_height() + 5
    name1_surface = font.render(advisor1_name, True, BLACK)
    surface.blit(name1_surface, (image1_x, name1_y - scroll_offset))
    link1_y = name1_y + font.get_linesize() + 5
    link1_surface = font.render(advisor1_link, True, BLUE)
    surface.blit(link1_surface, (image1_x, link1_y - scroll_offset))

    # Draw second advisor block
    surface.blit(advisor_image2, (image1_x, advisor2_top - scroll_offset))
    name2_y = advisor2_top + advisor_image2.get_height() + 5
    name2_surface = font.render(advisor2_name, True, BLACK)
    surface.blit(name2_surface, (image1_x, name2_y - scroll_offset))
    link2_y = name2_y + font.get_linesize() + 5
    link2_surface = font.render(advisor2_link, True, BLUE)
    surface.blit(link2_surface, (image1_x, link2_y - scroll_offset))

