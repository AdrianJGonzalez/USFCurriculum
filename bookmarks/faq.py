import tkinter as tk
from tkinter import ttk
import webbrowser

class FAQPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg='#dcdad5')

        # Canvas and scrollbar
        self.canvas = tk.Canvas(self, bg='#dcdad5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame inside the canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg='#dcdad5')
        self.scroll_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Header
        header = tk.Label(self.scrollable_frame, text="FREQUENTLY ASKED QUESTIONS", font=("Helvetica", 20, "bold"),
                          fg="#006747", bg="#dcdad5")
        header.pack(pady=20)

        # Centered content frame
        self.centered_frame = tk.Frame(self.scrollable_frame, bg="#dcdad5")
        self.centered_frame.pack(anchor="center", padx=20)

        # Add categories with prioritized questions
        self.add_category("About the App", [
            ("What does this app do?", "This app helps students understand and manage their USF course registration process."),
            ("Is this app mobile-friendly?", "As of now, the app is responsive only on computers.The Academic Programer manager will be mobile-friendly soon :)"),
            ("Can I register for classes through this app?", "No, this app is for planning only. Official registration must be done through OASIS."),
            ("In the app, what is the difference between the Semester Plan tab and the Academic Plan tab?", "The Semester Plan tab allows you to plan out your semesters, while the Academc Plan allows for overall degree progress tracking."),
            ("Can I save my schedule?", "Yes, your schedule can be saved for future access."),
            ("Does this app show real-time seat availability?", "No, seat availability is shown as of the last sync. Always confirm in OASIS."),
            ("Is there a dark mode?", "Not currently, but accessibility improvements are under consideration.")
        ])

        self.add_category("Registration", [
            ("How do I register for courses?", "Go to myUSF > My Resources tab > Student Self-Service (OASIS)."),
            ("How do I get a registration time?", "Times are assigned based on earned credit hours. Check OASIS about a month before registration opens."),
            ("What is 'Plan Ahead'?", "It lets you pre-build schedules in OASIS for quicker registration."),
            ("I got a 'Student Attribute Restriction' error. What does that mean?", "It usually means your academic program doesn't match course requirements. Contact your advisor."),
            ("Can I register without meeting prerequisites?", "No. Courses with prerequisites require prior approval or completion."),
            ("How do I change my major to access restricted courses?", "Contact your academic advisor and submit a Change of Major request through OASIS."),
            ("The course is full. Can I still register?", "You’ll need instructor permission. Even then, space limitations might block registration.")
        ])

        self.add_category("Transcript", [
            ("How do I request an official transcript?", "Go to myUSF > Student Self-Service > Transcript Request."),
            ("Can I access an unofficial transcript?", "Yes, you can access it through FloridaShines.org if enrolled within the last year."),
            ("I can’t log into FloridaShines. What should I do?", "Request an official transcript or contact support."),
            ("How much does an official transcript cost?", "For an official transcript, there is a $10 fee plus an additional processing fee for each transcript ordered. Active students are able to access an unofficial transcript at no cost. Former students may only access official transcripts."),
            ("What should I do if there's an error on my transcript?", "Email USFtranscript@usf.edu with full details."),
            ("How long does it take to process a transcript?", "Typically 1–3 business days, depending on demand.")
        ])

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self.scroll_window, width=event.width)

    def add_category(self, title, faq_list):
        section_title = tk.Label(self.centered_frame, text=title.upper(), font=("Helvetica", 16, "bold"),
                                 fg="#006747", bg="#dcdad5")
        section_title.pack(pady=(20, 10))

        for question, answer in faq_list:
            self.create_faq_item(question, answer)

    def create_faq_item(self, question, answer):
        container = tk.Frame(self.centered_frame, bg="#dcdad5")
        container.pack(pady=5, fill="x", padx=40)

        answer_frame = tk.Frame(container, bg="#dcdad5")
        answer_frame.pack_forget()

        # Handle special case for USFtranscript email
        if "USFtranscript@usf.edu" in answer:
            before, email, after = answer.partition("USFtranscript@usf.edu")

            answer_line = tk.Frame(answer_frame, bg="#dcdad5")
            answer_line.pack(pady=(0, 10))

            tk.Label(answer_line, text=before, font=("Helvetica", 12),
                     fg="#006747", bg="#dcdad5", wraplength=700, justify="center").pack(side="left")

            email_label = tk.Label(answer_line, text=email, font=("Helvetica", 12, "underline"),
                                   fg="blue", bg="#dcdad5", cursor="hand2", wraplength=700, justify="center")
            email_label.pack(side="left")

            tk.Label(answer_line, text=after, font=("Helvetica", 12),
                     fg="#006747", bg="#dcdad5", wraplength=700, justify="center").pack(side="left")

            def open_email(event):
                webbrowser.open(f"mailto:{email}")

            email_label.bind("<Button-1>", open_email)

        else:
            tk.Label(answer_frame, text=answer, font=("Helvetica", 12),
                     fg="#006747", bg="#dcdad5", wraplength=700, justify="center").pack(pady=(0, 10))

        def toggle_answer():
            if answer_frame.winfo_ismapped():
                answer_frame.pack_forget()
                question_btn.config(text="➕ " + question)
            else:
                answer_frame.pack(fill="x")
                question_btn.config(text="➖ " + question)

            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        question_btn = tk.Button(container, text="➕ " + question,
                                 font=("Helvetica", 12, "bold"),
                                 relief="flat", fg="#006747", bg="#dcdad5",
                                 wraplength=700, justify="center",
                                 command=toggle_answer, cursor="hand2")
        question_btn.pack(fill="x", padx=10)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    root.title("FAQ Page - USF Course Registration")
    root.geometry("850x700")
    root.configure(bg='#dcdad5')
    FAQPage(root).pack(fill="both", expand=True)
    root.mainloop()
