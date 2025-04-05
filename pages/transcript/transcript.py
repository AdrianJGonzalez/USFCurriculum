import fitz
import re
import json
import pygame
import PyPDF2
import tkinter as tk
from tkinter import filedialog
from pages.curriculum.courses import courses

# Read text from the PDF
def read_pdf_text(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        print(f"\nReading PDF: {file_path}")
        print(f"Number of pages: {len(doc)}")
        
        for page_num, page in enumerate(doc):
            print(f"\nExtracting text from page {page_num + 1}")
            page_text = page.get_text("text")
            print(f"Characters extracted from page: {len(page_text)}")
            text += page_text + "\n"
        
        print("\nTotal text extracted:", len(text), "characters")
        return text
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return ""

# Extract completed course codes from the transcript
def find_completed_courses(text):
    print("\n=== DEBUG: Starting course search ===")
    print("\nRaw text from PDF:")
    print("-" * 50)
    print(text)
    print("-" * 50)

    matched_courses = []
    current_term = None
    current_year = None
    
    # Split into lines and process each line
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        print(f"\nProcessing line: {line}")
        
        # Look for term headers (very simple pattern)
        if any(term in line for term in ['Spring', 'Fall', 'Summer']):
            if any(str(year) in line for year in range(2020, 2025)):  # Look for recent years
                print(f"Possible term line found: {line}")
        
        # Look for course codes (very simple pattern)
        words = line.split()
        for i in range(len(words)-1):
            # Look for pattern: 2-4 letters followed by 4 digits
            if (len(words[i]) in [2,3,4] and words[i].isalpha() and 
                len(words[i+1]) >= 4 and words[i+1][:4].isdigit()):
                print(f"Possible course found: {words[i]} {words[i+1]}")
                
                # Look for grade in the same line
                for word in words:
                    if re.match(r'^[ABCDF][+-]?$', word):
                        print(f"Grade found: {word}")

    print("\n=== DEBUG: Search complete ===")
    return matched_courses

# Save list to file (optional)
def save_courses_to_file(courses, filename="completed_courses.json"):
    try:
        with open(filename, "w") as f:
            json.dump(courses, f, indent=2)
    except Exception as e:
        print(f"Couldn't save courses: {e}")

# Launch file dialog (using tkinter silently)
def get_pdf_path():
    tk.Tk().withdraw()
    return filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

# --- Pygame Integration ---
completed_courses = []
status_message = "Upload a transcript to see completed courses."
upload_button = pygame.Rect(0, 0, 0, 0)  # Dummy placeholder
current_page = 0
COURSES_PER_PAGE = 10  # Adjust this number based on your screen size
next_page_button = pygame.Rect(0, 0, 0, 0)
prev_page_button = pygame.Rect(0, 0, 0, 0)

def render(screen, area, font, text_color, accent_color):
    global completed_courses, status_message, upload_button, current_page
    global next_page_button, prev_page_button

    # Place buttons relative to content area
    upload_button_local = pygame.Rect(area.left + 20, area.top + 20, 200, 40)
    
    # Add navigation buttons
    button_width = 100
    button_height = 40
    button_spacing = 20
    
    prev_button_local = pygame.Rect(
        area.left + 20,
        area.bottom - button_height - 20,
        button_width,
        button_height
    )
    
    next_button_local = pygame.Rect(
        prev_button_local.right + button_spacing,
        area.bottom - button_height - 20,
        button_width,
        button_height
    )

    # Draw upload button
    pygame.draw.rect(screen, (180, 180, 255), upload_button_local)
    pygame.draw.rect(screen, (0, 0, 0), upload_button_local, 2)
    button_text = font.render("Upload Transcript", True, (0, 0, 0))
    screen.blit(button_text, button_text.get_rect(center=upload_button_local.center))

    # Display results
    y_offset = upload_button_local.bottom + 20
    
    if not completed_courses:
        lines = [status_message]
    else:
        # Calculate pagination
        total_pages = (len(completed_courses) - 1) // COURSES_PER_PAGE + 1
        start_idx = current_page * COURSES_PER_PAGE
        end_idx = min(start_idx + COURSES_PER_PAGE, len(completed_courses))
        
        lines = [f"Completed Courses (Page {current_page + 1} of {total_pages}):"]
        
        # Display only courses for current page
        for course in completed_courses[start_idx:end_idx]:
            course_text = f"- {course['course_code']} - {course['course_name']} ({course['semester']} {course['year']}) - Grade: {course['grade']}"
            lines.append(course_text)
        
        # Draw navigation buttons if needed
        if total_pages > 1:
            # Previous page button
            if current_page > 0:
                pygame.draw.rect(screen, (180, 180, 255), prev_button_local)
                pygame.draw.rect(screen, (0, 0, 0), prev_button_local, 2)
                prev_text = font.render("Previous", True, (0, 0, 0))
                screen.blit(prev_text, prev_text.get_rect(center=prev_button_local.center))
            
            # Next page button
            if current_page < total_pages - 1:
                pygame.draw.rect(screen, (180, 180, 255), next_button_local)
                pygame.draw.rect(screen, (0, 0, 0), next_button_local, 2)
                next_text = font.render("Next", True, (0, 0, 0))
                screen.blit(next_text, next_text.get_rect(center=next_button_local.center))

    # Render course lines
    for line in lines:
        rendered = font.render(line, True, text_color)
        screen.blit(rendered, (area.left + 20, y_offset))
        y_offset += rendered.get_height() + 5

    # Update button rectangles for event handling
    upload_button = upload_button_local
    next_page_button = next_button_local
    prev_page_button = prev_button_local

def handle_event(event):
    global completed_courses, status_message, current_page

    if event.type == pygame.MOUSEBUTTONDOWN:
        if upload_button.collidepoint(event.pos):
            file_path = get_pdf_path()
            if file_path:
                try:
                    completed_courses = extract_courses(file_path)
                    save_courses_to_file(completed_courses)
                    current_page = 0  # Reset to first page
                    status_message = "Transcript processed." if completed_courses else "No valid courses found."
                except Exception as e:
                    status_message = f"Error processing transcript: {str(e)}"
        
        # Handle pagination buttons
        elif next_page_button.collidepoint(event.pos):
            total_pages = (len(completed_courses) - 1) // COURSES_PER_PAGE + 1
            if current_page < total_pages - 1:
                current_page += 1
        
        elif prev_page_button.collidepoint(event.pos):
            if current_page > 0:
                current_page -= 1

def extract_courses(pdf_path):
    courses = []
    current_college = None
    current_semester = None
    current_year = None

    # Regex patterns
    date_range_semester_regex = re.compile(
        r'^(Fall|Spring|Summer)\s+(\d{4})\s+(\d{2}/\d{2}/\d{4})\s*-\s*(\d{2}/\d{2}/\d{4})$',
        re.IGNORECASE
    )
    no_range_semester_regex = re.compile(
        r'^(Fall|Spring|Summer)\s+(\d{4})$',
        re.IGNORECASE
    )
    dept_num_regex = re.compile(r'^([A-Za-z]+)(\d{3,4}[A-Za-z]?)$')

    valid_grades = {
        "A","A+","A-","B","B+","B-","C","C+","C-","D","D+","D-","F","IP","S"
    }

    def detect_college_name(line: str) -> str or None:
        text = line.strip().lower()
        if "hillsborough cc" in text:
            return "Hillsborough CC"
        return None

    def parse_course_line(line: str):
        tokens = line.split()
        if len(tokens) < 4:
            return None

        m = dept_num_regex.match(tokens[0])
        if not m:
            return None

        dept = m.group(1)
        course_num = m.group(2)

        remainder = [tok for tok in tokens[1:] if tok != 'T']

        grade_index = None
        for i in reversed(range(len(remainder))):
            if remainder[i] in valid_grades:
                grade_index = i
                break
        if grade_index is None:
            return None

        grade = remainder[grade_index]
        if grade_index + 1 >= len(remainder):
            return None

        try:
            credit_hours = int(remainder[grade_index + 1])
        except ValueError:
            return None

        course_name = " ".join(remainder[:grade_index])

        return {
            "Department": dept,
            "Course Number": course_num,
            "Course Name": course_name,
            "Grade": grade,
            "Credit Hours": credit_hours
        }

    # Read PDF text lines
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        lines = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            lines.extend(page_text.splitlines())

    # Process lines
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        # Check for semester patterns
        m = date_range_semester_regex.match(line)
        if m:
            current_semester = m.group(1).capitalize()
            current_year = m.group(2)
            continue

        m = no_range_semester_regex.match(line)
        if m:
            current_semester = m.group(1).capitalize()
            current_year = m.group(2)
            continue

        # Check for college name
        c = detect_college_name(line)
        if c:
            current_college = c
            continue

        # Parse course line
        result = parse_course_line(line)
        if result and current_semester and current_year:
            if not current_college or current_college.lower() == "the university of south florida":
                continue

            cleaned_course = {
                "course_code": f"{result['Department']} {result['Course Number']}",
                "course_name": result['Course Name'],
                "semester": current_semester,
                "year": current_year,
                "grade": result['Grade'],
                "credits": result['Credit Hours'],
                "institution": current_college
            }
            courses.append(cleaned_course)

    return courses
