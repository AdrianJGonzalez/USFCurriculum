import tkinter as tk
from tkinter import ttk
from bookmarks.welcome import WelcomePage
from bookmarks.semester_plan import SemesterPlanPage
from bookmarks.course_catalog import CourseCatalogPage
from bookmarks.academic_plan import AcademicPlanPage
from bookmarks.upload_transcript import TranscriptPage
from bookmarks.advising import AdvisingPage
from bookmarks.faq import FAQPage
from bookmarks.course_editor import CourseEditorPage

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Academic Planner")
        self.geometry("800x600")
        
        # Set the background color of the main window aka the outline of the whole tap
        self.configure(bg='#303434')
        
        # Configure custom styles for the notebook
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme which supports custom styling better
        
        # Configure the tab style
        style.configure('Custom.TNotebook', background='#303434') #Back of the tab color
        style.configure('Custom.TNotebook.Tab', 
                       background='#303434',
                       foreground='white',
                       padding=[10, 5],
                       font=('Helvetica', 10))
        
        # Configure the selected tab style
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', '#466069')], #Color of the Selected Tab
                 foreground=[('selected', 'white')]) #Makes the selected tab go down and keep the text
        
        # Create notebook (tabbed interface) with custom style
        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create frames for each tab
        self.welcome_frame = WelcomePage(self.notebook)
        self.course_catalog_frame = CourseCatalogPage(self.notebook)
        self.semester_plan_frame = SemesterPlanPage(self.notebook)
        self.academic_plan_frame = AcademicPlanPage(self.notebook)
        self.transcript_frame = TranscriptPage(self.notebook)
        self.advising_frame = AdvisingPage(self.notebook)
        self.faq_frame = FAQPage(self.notebook)
        
        # Connect transcript page to semester plan
        self.transcript_frame.set_flowchart(self.semester_plan_frame)
        
        # Course Editor
        course_editor = CourseEditorPage(self.notebook)
        
        # Add frames to notebook in desired order
        self.notebook.add(self.welcome_frame, text="Welcome")
        self.notebook.add(self.transcript_frame, text="Upload Transcript")
        self.notebook.add(self.semester_plan_frame, text="Semester Plan")
        self.notebook.add(self.academic_plan_frame, text="Academic Plan")
        self.notebook.add(self.advising_frame, text="Advising")
        self.notebook.add(self.faq_frame, text="FAQ")
        self.notebook.add(self.course_catalog_frame, text="Course Catalog")
        self.notebook.add(course_editor, text="Course Editor")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()