import tkinter as tk
from tkinter import ttk
from bookmarks.welcome import WelcomePage
from bookmarks.course_catalog import CourseCatalogPage
from bookmarks.flowchart import FlowchartPage
from bookmarks.track_selector import TrackSelector
from bookmarks.upload_transcript import TranscriptPage
from bookmarks.advising import AdvisingPage
from bookmarks.faq import FAQPage  # <-- Add this import

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Academic Planner")
        self.geometry("800x600")
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create frames for each tab
        self.welcome_frame = WelcomePage(self.notebook)
        self.course_catalog_frame = CourseCatalogPage(self.notebook)
        self.flowchart_frame = FlowchartPage(self.notebook)
        self.track_selector_frame = TrackSelector(self.notebook)
        self.transcript_frame = TranscriptPage(self.notebook)
        self.advising_frame = AdvisingPage(self.notebook)
        self.faq_frame = FAQPage(self.notebook)  # <-- Add this line
        
        # Connect transcript page to flowchart
        self.transcript_frame.set_flowchart(self.flowchart_frame)
        
        # Add frames to notebook
        self.notebook.add(self.welcome_frame, text="Welcome")
        self.notebook.add(self.course_catalog_frame, text="Course Catalog")
        self.notebook.add(self.flowchart_frame, text="Flowchart")
        self.notebook.add(self.track_selector_frame, text="Track Selector")
        self.notebook.add(self.transcript_frame, text="Upload Transcript")
        self.notebook.add(self.advising_frame, text="Advising")
        self.notebook.add(self.faq_frame, text="FAQ")  # <-- Add this line

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

