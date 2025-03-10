import pygame

def draw_multiline_text(surface, text, pos, font, color, max_width, line_spacing=5):
    """
    Draws the text at the given pos, wrapping words to fit max_width.
    Returns the final y-coordinate after drawing.
    """
    x, y = pos
    paragraphs = text.split("\n")
    for paragraph in paragraphs:
        if paragraph.strip() == "":
            y += font.get_linesize()
            continue

        words = paragraph.split(" ")
        line = ""
        for word in words:
            test_line = line + (" " if line else "") + word
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                line_surface = font.render(line, True, color)
                surface.blit(line_surface, (x, y))
                y += font.get_linesize() + line_spacing
                line = word
        if line:
            line_surface = font.render(line, True, color)
            surface.blit(line_surface, (x, y))
            y += font.get_linesize() + line_spacing
    return y

def get_multiline_text_height(text, font, max_width, line_spacing=5):
    """
    Computes the height of a block of multiline text with word wrapping.
    """
    height = 0
    paragraphs = text.split("\n")
    for paragraph in paragraphs:
        if paragraph.strip() == "":
            height += font.get_linesize()
            continue
        words = paragraph.split(" ")
        line = ""
        for word in words:
            test_line = line + (" " if line else "") + word
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                height += font.get_linesize() + line_spacing
                line = word
        if line:
            height += font.get_linesize() + line_spacing
    return height
