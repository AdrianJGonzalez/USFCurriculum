import pygame
import webbrowser
from utils import draw_multiline_text, get_multiline_text_height

# Colors for the USF theme
USF_GREEN = (0, 103, 71)  # USF Green
USF_GOLD = (207, 196, 147)  # USF Gold
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FAQ content (questions and answers)
faq_content = [
    ("How can I book an advising appointment?", 
     "Once your ULDP form is processed, you can either book an online appointment or visit us during walk-in hours."),
    ("What are the Walk-in Advising Hours?", 
     "Walk-in Advising is available on Tuesdays and Thursdays from 10 AM to 4 PM at ENB 379."),
    ("How do I contact you for additional questions?", 
     "For further inquiries, please email us at ENG-EEAdvising@usf.edu"),
    ("Where can I find more information?", 
     "You can visit our official advising website at: https://www.usf.edu/engineering/ee/undergraduate/ugadvising.aspx"),
    ("What is a Co/Prerequisite?", 
     "A co/prerequisite is a course you can either take before or alongside a desired class."),
]

def render(surface, area_rect, font, BLACK, BLUE, scroll_offset=0):
    """
    Renders the FAQ page with clickable questions and answers.
    """
    padding = 20
    text_area_width = area_rect.width - 2 * padding
    current_y = area_rect.y + padding - scroll_offset

    # Draw title
    title = "Frequently Asked Questions (FAQ)"
    title_surface = pygame.font.Font(None, 36).render(title, True, BLACK)
    surface.blit(title_surface, (area_rect.x + padding, current_y))
    current_y += title_surface.get_height() + 30

    # Draw FAQ items
    for question, answer in faq_content:
        # Draw question (in bold or different color)
        question_surface = pygame.font.Font(None, 28).render(question, True, USF_GREEN)
        surface.blit(question_surface, (area_rect.x + padding, current_y))
        current_y += question_surface.get_height() + 10

        # Draw answer
        answer_height = get_multiline_text_height(answer, font, text_area_width - 40)
        draw_multiline_text(
            surface,
            answer,
            (area_rect.x + padding + 20, current_y),  # Indent the answer
            font,
            BLACK,
            text_area_width - 40
        )
        current_y += answer_height + 30

        # If the answer contains a link, make it clickable
        if "email" in answer or "website" in answer:
            link_rect = pygame.Rect(
                area_rect.x + padding + 20,
                current_y - font.get_height() - 5,
                text_area_width - 40,
                font.get_height()
            )
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            if link_rect.collidepoint(mouse_pos):
                if "email" in answer and mouse_clicked:
                    webbrowser.open("mailto:ENG-EEAdvising@usf.edu")
                elif "website" in answer and mouse_clicked:
                    webbrowser.open("https://www.usf.edu/engineering/ee/undergraduate/ugadvising.aspx")

    # Calculate total content height for scrolling
    total_content_height = current_y + padding
    
    # Ensure scroll offset stays within bounds
    max_scroll = max(0, total_content_height - area_rect.height)
    return max(0, min(scroll_offset, max_scroll))