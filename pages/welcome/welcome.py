import pygame

def render(surface, area_rect, font, BLACK, BLUE):
    padding = 20
    
    # Render the welcome text
    text = "Welcome to the Flowchart Application!"
    text_surface = font.render(text, True, BLACK)
    surface.blit(text_surface, (area_rect.x + padding, area_rect.y + padding))
    
    # Render the ULDP question text
    question_text = "Have you achieved Upper Level Degree Progression (ULDP) status?"
    question_surface = font.render(question_text, True, BLACK)
    surface.blit(question_surface, (area_rect.x + padding, area_rect.y + padding + 40))
    
    # Define button properties
    button_width = 100
    button_height = 50
    button_color = pygame.Color("#006747")
    font_color = pygame.Color("#cfc493")
    
    # Create YES button
    yes_button_rect = pygame.Rect(area_rect.x + padding, area_rect.y + padding + 100, button_width, button_height)
    pygame.draw.rect(surface, button_color, yes_button_rect)
    yes_text_surface = font.render("YES", True, font_color)
    yes_text_rect = yes_text_surface.get_rect(center=yes_button_rect.center)
    surface.blit(yes_text_surface, yes_text_rect)
    
    # Create NO button
    no_button_rect = pygame.Rect(area_rect.x + padding + 150, area_rect.y + padding + 100, button_width, button_height)
    pygame.draw.rect(surface, button_color, no_button_rect)
    no_text_surface = font.render("NO", True, font_color)
    no_text_rect = no_text_surface.get_rect(center=no_button_rect.center)
    surface.blit(no_text_surface, no_text_rect)
