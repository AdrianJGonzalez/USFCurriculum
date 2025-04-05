import pygame
import sys
import os

from utils import draw_multiline_text, get_multiline_text_height
from pages.advising import advising_main
from pages.welcome import welcome
from pages.curriculum import curriculum
from pages.transcript import transcript
from pages.faq import faq
from pages import about

pygame.init()

# Initial window dimensions and left sidebar width
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
LEFT_COLUMN_WIDTH = 250

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Flowchart Application")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE = (0, 0, 255)

# Font
font = pygame.font.SysFont(None, 24)

# Button setup (left sidebar)
button_height = 40
button_margin = 10
buttons = {
    "welcome": pygame.Rect(10, 10, LEFT_COLUMN_WIDTH - 20, button_height),
    "curriculum": pygame.Rect(10, 10 + (button_height + button_margin), LEFT_COLUMN_WIDTH - 20, button_height),
    "advising_main": pygame.Rect(10, 10 + 2 * (button_height + button_margin), LEFT_COLUMN_WIDTH - 20, button_height),
    "transcript": pygame.Rect(10, 10 + 3 * (button_height + button_margin), LEFT_COLUMN_WIDTH - 20, button_height),
    "about": pygame.Rect(10, 10 + 4 * (button_height + button_margin), LEFT_COLUMN_WIDTH - 20, button_height),
    "faq": pygame.Rect(10, 10 + 5 * (button_height + button_margin), LEFT_COLUMN_WIDTH - 20, button_height),
}

# Right content area
right_area_rect = pygame.Rect(LEFT_COLUMN_WIDTH, 0, WINDOW_WIDTH - LEFT_COLUMN_WIDTH, WINDOW_HEIGHT)

active_page = "welcome"
scroll_offset = 0

clock = pygame.time.Clock()
running = True

# Determine the base directory for the advising folder (one level up from Departments)
CURRENT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
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

# Define scroll constants
SCROLL_AREA_HEIGHT = 500
SCROLL_BAR_WIDTH = 10
SCROLL_HANDLE_HEIGHT = 60

# Initialize scroll variables
scroll_offset = 0
is_dragging_scrollbar = False
scroll_drag_offset_y = 0

def draw_scrollbar(surface, x, y, total_height, visible_height):
    global scroll_offset

    # Calculate scrollbar dimensions
    max_offset = max(0, total_height - visible_height)
    scroll_ratio = scroll_offset / max_offset if max_offset > 0 else 0
    handle_height = max(40, int(SCROLL_AREA_HEIGHT * min(1, visible_height / total_height)))
    handle_y = y + int((SCROLL_AREA_HEIGHT - handle_height) * scroll_ratio)

    # Draw scrollbar
    scrollbar_rect = pygame.Rect(x, y, SCROLL_BAR_WIDTH, SCROLL_AREA_HEIGHT)
    pygame.draw.rect(surface, pygame.Color('lightgray'), scrollbar_rect)
    pygame.draw.rect(surface, pygame.Color('black'), scrollbar_rect, 1)

    # Draw scroll handle
    scroll_handle_rect = pygame.Rect(x, handle_y, SCROLL_BAR_WIDTH, handle_height)
    pygame.draw.rect(surface, pygame.Color('gray'), scroll_handle_rect)
    pygame.draw.rect(surface, pygame.Color('black'), scroll_handle_rect, 1)

def handle_scroll_events(event, total_height, visible_height):
    global scroll_offset, is_dragging_scrollbar, scroll_drag_offset_y

    max_offset = max(0, total_height - visible_height)

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if scroll_handle_rect.collidepoint(event.pos):
            is_dragging_scrollbar = True
            scroll_drag_offset_y = event.pos[1] - scroll_handle_rect.y
    elif event.type == pygame.MOUSEBUTTONUP:
        is_dragging_scrollbar = False
    elif event.type == pygame.MOUSEMOTION and is_dragging_scrollbar:
        mouse_y = event.pos[1]
        new_handle_y = mouse_y - scroll_drag_offset_y
        new_handle_y = max(SCROLL_BAR_Y, min(SCROLL_BAR_Y + SCROLL_AREA_HEIGHT - handle_height, new_handle_y))
        scroll_ratio = (new_handle_y - SCROLL_BAR_Y) / (SCROLL_AREA_HEIGHT - handle_height)
        scroll_offset = int(scroll_ratio * max_offset)
    elif event.type == pygame.MOUSEWHEEL:
        scroll_offset -= event.y * 10  # Adjust scroll speed
        scroll_offset = max(0, min(scroll_offset, max_offset))

def render(surface, area_rect, font, BLACK, BLUE):
    """
    Draws the Mechanical Engineering advisors page in the given area.
    """
    global scroll_offset  # Use the global scroll_offset

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

    # Draw scrollbar
    draw_scrollbar(surface, area_rect.right - SCROLL_BAR_WIDTH, area_rect.y, content_bottom, area_rect.height)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            WINDOW_WIDTH, WINDOW_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
            # Update right area rect when window is resized
            right_area_rect.width = WINDOW_WIDTH - LEFT_COLUMN_WIDTH
            right_area_rect.height = WINDOW_HEIGHT

        elif event.type == pygame.KEYDOWN:
            if active_page == "advising_main":
                advising_main.process_search_event(event)
            elif active_page == "curriculum":
                curriculum.handle_event(event, right_area_rect)

        elif event.type == pygame.MOUSEWHEEL:
            if active_page == "advising_main":
                scroll_offset -= event.y * 30  # Adjust scroll speed
            elif active_page == "curriculum":
                curriculum.handle_event(event, right_area_rect)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                if active_page == "advising_main":
                    scroll_offset -= 30
                continue
            elif event.button == 5:  # Scroll down
                if active_page == "advising_main":
                    scroll_offset += 30
                continue
            else:
                mouse_pos = pygame.mouse.get_pos()

                # Handle transcript button inside main area
                if active_page == "transcript":
                    transcript.handle_event(event)
                # Handle curriculum events
                elif active_page == "curriculum":
                    curriculum.handle_event(event, right_area_rect)

                # Sidebar buttons
                for key in buttons:
                    if buttons[key].collidepoint(mouse_pos):
                        active_page = key
                        scroll_offset = 0
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if active_page == "curriculum":
                curriculum.handle_event(event, right_area_rect)

        elif event.type == pygame.MOUSEMOTION:
            if active_page == "curriculum":
                curriculum.handle_event(event, right_area_rect)

    # Clear screen and draw left sidebar
    screen.fill(WHITE)
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, LEFT_COLUMN_WIDTH, WINDOW_HEIGHT))
    for key, rect in buttons.items():
        pygame.draw.rect(screen, GRAY if key == active_page else WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        button_labels = {
            "welcome": "Welcome",
            "curriculum": "Curriculum Flowchart Creator",
            "advising_main": "Advising",
            "transcript": "Upload an official Transcript",
            "about": "About this Application",
            "faq": "Frequently Asked Questions"
        }
        text_surface = font.render(button_labels[key], True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    # Draw the right content area
    pygame.draw.rect(screen, WHITE, right_area_rect)
    pygame.draw.rect(screen, BLACK, right_area_rect, 2)

    # Render active page content
    render_functions = {
        "welcome": welcome.render,
        "curriculum": curriculum.render,
        "advising_main": lambda s, r, f, b, bl: advising_main.render(s, r, f, b, bl, scroll_offset),
        "transcript": transcript.render,
        "about": about.render,
        "faq": faq.render
    }
    render_functions[active_page](screen, right_area_rect, font, BLACK, BLUE)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
