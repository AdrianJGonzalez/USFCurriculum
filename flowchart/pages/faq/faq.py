import pygame

def render(surface, area_rect, font, BLACK, BLUE):
    padding = 20
    text = "Frequently Asked Questions page coming soon."
    text_surface = font.render(text, True, BLACK)
    surface.blit(text_surface, (area_rect.x + padding, area_rect.y + padding))
