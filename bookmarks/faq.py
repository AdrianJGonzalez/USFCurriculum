import tkinter as tk

class FAQPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        faq_content = [
            ("Q: How can I book an advising appointment?",
             "A: Once your ULDP form is processed, you can either book an online appointment or visit us during walk-in hours."),
            ("Q: What are the Walk-in Advising Hours?",
             "A: Walk-in Advising is available on Tuesdays and Thursdays from 10 AM to 4 PM at ENB 379."),
            ("Q: How do I contact you for additional questions?",
             "A: For further inquiries, please email us at ENG-EEAdvising@usf.edu."),
            ("Q: Where can I find more information?",
             "A: You can visit our official advising website at: "),
            ("Q: What is a Co/Prerequisite?",
             "A: A co/prerequisite is a course you can either take before or alongside a desired class.")
        ]
        
        title = tk.Label(self, text="Frequently Asked Questions", font=("Helvetica", 16, "bold"))
        title.pack(pady=(20, 10))

        for i, (q, a) in enumerate(faq_content):
            question = tk.Label(self, text=q, font=("Helvetica", 12, "bold"), anchor="w", justify="left")
            answer = tk.Label(self, text=a, font=("Helvetica", 12), anchor="w", justify="left", wraplength=700)
            question.pack(anchor="w", padx=30)
            answer.pack(anchor="w", padx=50)
            if i < len(faq_content) - 1:
                spacer = tk.Label(self, text="")
                spacer.pack(pady=10)  # Adds two lines of space


