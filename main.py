import pygame
import sys

from utils import draw_multiline_text, get_multiline_text_height
from pages.advising import advisors
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
    "advisors": pygame.Rect(10, 10 + 2 * (button_height + button_margin), LEFT_COLUMN_WIDTH - 20, button_height),
    "transcript": pygame.Rect(10, 10 + 3 * (button_height + button_margin), LEFT_COLUMN_WIDTH - 20, button_height),
    "about": pygame.Rect(10, 10 + 4 * (button_height + button_margin), LEFT_COLUMN_WIDTH - 20, button_height),
    "faq": pygame.Rect(10, 10 + 5 * (button_height + button_margin), LEFT_COLUMN_WIDTH - 20, button_height),
}

active_page = "welcome"
scroll_offset = 0

clock = pygame.time.Clock()
running = True

while running:
    # Reset scroll offset at the start of each loop if needed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            WINDOW_WIDTH, WINDOW_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

        # If the advisors page is active, pass KEYDOWN events for search input
        elif event.type == pygame.KEYDOWN:
            if active_page == "advisors":
                advisors.process_search_event(event)

        elif event.type == pygame.MOUSEWHEEL:
            if active_page == "advisors":
                scroll_offset -= event.y * 30  # Adjust scroll speed

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # wheel up
                if active_page == "advisors":
                    scroll_offset -= 30
                continue
            elif event.button == 5:  # wheel down
                if active_page == "advisors":
                    scroll_offset += 30
                continue
            else:
                mouse_pos = pygame.mouse.get_pos()
                for key in buttons:
                    if buttons[key].collidepoint(mouse_pos):
                        active_page = key
                        scroll_offset = 0
                        break

    # Clear screen and draw left sidebar
    screen.fill(WHITE)
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, LEFT_COLUMN_WIDTH, WINDOW_HEIGHT))
    for key, rect in buttons.items():
        pygame.draw.rect(screen, GRAY if key == active_page else WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        button_labels = {
            "welcome": "Welcome",
            "curriculum": "Curriculum Flowchart Creator",
            "advisors": "Advisors",
            "transcript": "Upload an official Transcript",
            "about": "About this Application",
            "faq": "Frequently Asked Questions"
        }
        text_surface = font.render(button_labels[key], True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    # Draw the right content area
    right_area_rect = pygame.Rect(LEFT_COLUMN_WIDTH, 0, WINDOW_WIDTH - LEFT_COLUMN_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, WHITE, right_area_rect)
    pygame.draw.rect(screen, BLACK, right_area_rect, 2)

    # Render active page content. The advisors page now handles its own search functionality.
    render_functions = {
        "welcome": welcome.render,
        "curriculum": curriculum.render,
        "advisors": lambda s, r, f, b, bl: advisors.render(s, r, f, b, bl, scroll_offset),
        "transcript": transcript.render,
        "about": about.render,
        "faq": faq.render
    }
    render_functions[active_page](screen, right_area_rect, font, BLACK, BLUE)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
