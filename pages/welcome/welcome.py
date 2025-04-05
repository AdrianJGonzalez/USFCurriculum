import pygame

def render(surface, area_rect, font, BLACK, BLUE):
    padding = 20
    
    # Render the welcome text
    text = "Welcome to the Flowchart Application! Below is work in progress. Buttons don't work yet."
    text_surface = font.render(text, True, BLACK)
    surface.blit(text_surface, (area_rect.x + padding, area_rect.y + padding))
    
    # Render the tracks question text
    tracks_question_text = "What tracks would you like to pursue?"
    tracks_question_surface = font.render(tracks_question_text, True, BLACK)
    surface.blit(tracks_question_surface, (area_rect.x + padding, area_rect.y + padding + 40))
    
    # Define button properties
    button_width = 300
    button_height = 100
    button_color = pygame.Color("#006747")
    font_color = pygame.Color("#cfc493")

    # Define button labels
    button_labels = [
        "Bioelectrical\nSystems", "Communications\nSystems", "Energy, Power, &\nSustainability", 
        "Mechatronic, Robotic &\nEmbedded Systems", "Micro and\nNano-scale Systems", 
        "Wireless Circuits and\nSystems", "Systems and\nSecurity"
    ]

    # Define button positions
    button_positions = [
        (area_rect.x + padding + (i % 3) * (button_width + 20), area_rect.y + padding + 100 + (i // 3) * (button_height + 20))
        for i in range(6)
    ]
    # Add the position for the last button
    button_positions.append((area_rect.x + padding + button_width + 20, area_rect.y + padding + 100 + 2 * (button_height + 20)))

    # Create and render buttons for tracks
    for i, (x, y) in enumerate(button_positions):
        button_rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(surface, button_color, button_rect)
        for j, line in enumerate(button_labels[i].split('\n')):
            button_text_surface = font.render(line, True, font_color)
            button_text_rect = button_text_surface.get_rect(center=(button_rect.centerx, button_rect.y + (j + 1) * (button_height // (len(button_labels[i].split('\n')) + 1))))
            surface.blit(button_text_surface, button_text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1400, 600))
    pygame.display.set_caption('Flowchart Application')
    font = pygame.font.Font(None, 36)
    BLACK = pygame.Color('black')
    BLUE = pygame.Color('blue')
    area_rect = pygame.Rect(50, 50, 1300, 500)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        render(screen, area_rect, font, BLACK, BLUE)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
