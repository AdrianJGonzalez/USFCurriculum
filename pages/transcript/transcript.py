import fitz
import re
import json
import pygame
from pages.curriculum.courses import courses

# Read text from the PDF
def read_pdf_text(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text
    except Exception as e:
        print(f"Couldn't read the PDF file: {e}")
        return ""

# Extract completed course codes from the transcript
def find_completed_courses(text):
    usf_courses = courses.get("University of South Florida", {})
    matched_courses = set()
    pattern = re.compile(r"\b([A-Z]{2,4})\s+(\d{4}[A-Z]?)\b")

    for match in pattern.finditer(text):
        dept, code = match.groups()
        dept = dept.upper()
        code = code.upper()

        try:
            numeric_code = int(re.match(r"\d{4}", code).group())
            if numeric_code < 3000:
                continue
        except:
            continue

        if dept in usf_courses and code in usf_courses[dept]:
            name = usf_courses[dept][code].get("Class Full Name", "Unknown Course")
            matched_courses.add(f"{dept} {code} - {name}")

    return sorted(list(matched_courses))

# Save list to file (optional)
def save_courses_to_file(courses, filename="completed_courses.json"):
    try:
        with open(filename, "w") as f:
            json.dump(courses, f, indent=2)
    except Exception as e:
        print(f"Couldn't save courses: {e}")

# Launch file dialog (using tkinter silently)
def get_pdf_path():
    import tkinter as tk
    from tkinter import filedialog
    tk.Tk().withdraw()
    return filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

# --- Pygame Integration ---
completed_courses = []
status_message = "Upload a transcript to see completed courses."
upload_button = pygame.Rect(0, 0, 0, 0)  # Dummy placeholder

def render(screen, area, font, text_color, accent_color):
    global completed_courses, status_message, upload_button

    # Place button relative to content area
    upload_button_local = pygame.Rect(area.left + 20, area.top + 20, 200, 40)

    pygame.draw.rect(screen, (180, 180, 255), upload_button_local)
    pygame.draw.rect(screen, (0, 0, 0), upload_button_local, 2)
    button_text = font.render("Upload Transcript", True, (0, 0, 0))
    screen.blit(button_text, button_text.get_rect(center=upload_button_local.center))

    # Display results
    y_offset = upload_button_local.bottom + 20
    lines = [status_message] if not completed_courses else ["Completed Courses:"] + [f"- {c}" for c in completed_courses]

    for line in lines:
        rendered = font.render(line, True, text_color)
        screen.blit(rendered, (area.left + 20, y_offset))
        y_offset += rendered.get_height() + 5

    # Update button for event handling
    upload_button = upload_button_local

def handle_event(event):
    global completed_courses, status_message

    if event.type == pygame.MOUSEBUTTONDOWN and upload_button.collidepoint(event.pos):
        file_path = get_pdf_path()
        if file_path:
            text = read_pdf_text(file_path)
            if not text:
                status_message = "Failed to read PDF."
                return

            completed_courses = find_completed_courses(text)
            save_courses_to_file(completed_courses)
            status_message = "Transcript processed." if completed_courses else "No valid courses found."

