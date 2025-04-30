import tkinter as tk
from tkinter import ttk
import webbrowser

class FAQPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F4F4F4")

        # Scrollable canvas setup
        self.canvas = tk.Canvas(self, bg="#F4F4F4", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(self.canvas, bg="#F4F4F4")
        self.scroll_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Page header
        tk.Label(self.scrollable_frame, text="FREQUENTLY ASKED QUESTIONS", font=("Helvetica", 22, "bold"),
                 fg="#006747", bg="#F4F4F4").pack(pady=(30, 20))

        # Centered content container
        self.centered_frame = tk.Frame(self.scrollable_frame, bg="#F4F4F4")
        self.centered_frame.pack(anchor="n", padx=40, fill="x")

        # FAQ Categories
        self.add_category("About the App", [
            ("What does this app do?", "This app helps students understand and manage their USF course registration process."),
            ("Is this app mobile-friendly?", "Currently optimized for desktop. A mobile-friendly version is planned."),
            ("Can I register for classes through this app?", "No. This app is for planning. Use OASIS for registration."),
            ("Semester Plan vs. Academic Plan?", "Semester Plan = per-term view. Academic Plan = overall degree path."),
            ("Can I save my schedule?", "Yes, your schedule is saved locally."),
            ("Real-time seat availability?", "No. Check OASIS for live seat info."),
            ("Is there a dark mode?", "Not yet, but it's on the roadmap.")
        ])

        self.add_category("Registration", [
            ("How do I register?", "Go to myUSF > My Resources > OASIS."),
            ("How is registration time assigned?", "Based on credit hours earned. Check OASIS."),
            ("What's 'Plan Ahead'?", "OASIS feature to pre-build schedules."),
            ("Student Attribute Restriction?", "Your program doesn't match course restrictions. Contact advisor."),
            ("Register without prerequisites?", "No. You must meet or get approval for prerequisites."),
            ("Change my major?", "Submit request through OASIS with advisor guidance."),
            ("Class full. Now what?", "You need instructor permission. Availability not guaranteed.")
        ])

        self.add_category("Transcript", [
            ("Request official transcript?", "Use myUSF > Student Self-Service > Transcript Request."),
            ("Unofficial transcript?", "Available via FloridaShines.org if recently enrolled."),
            ("Can't access FloridaShines?", "Request official transcript or contact support."),
            ("Transcript cost?", "Official: $10 + fees. Unofficial: free for current students."),
            ("Error on transcript?", "Email USFtranscript@usf.edu with details."),
            ("Processing time?", "1–3 business days typically.")
        ])

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self.scroll_window, width=event.width)

    def add_category(self, title, faq_list):
        tk.Label(self.centered_frame, text=title.upper(), font=("Helvetica", 16, "bold"),
                 fg="#006747", bg="#F4F4F4").pack(pady=(20, 10), anchor="w")
        for question, answer in faq_list:
            self.create_faq_item(question, answer)

    def create_faq_item(self, question, answer):
        container = tk.Frame(self.centered_frame, bg="#FFFFFF", bd=1, relief="solid")
        container.pack(pady=8, fill="x")

        answer_frame = tk.Frame(container, bg="#FFFFFF")
        answer_frame.pack_forget()

        if "USFtranscript@usf.edu" in answer:
            before, email, after = answer.partition("USFtranscript@usf.edu")
            line = tk.Frame(answer_frame, bg="#FFFFFF")
            line.pack(pady=(0, 10))
            tk.Label(line, text=before, font=("Helvetica", 11), fg="#333", bg="#FFFFFF").pack(side="left")
            email_label = tk.Label(line, text=email, font=("Helvetica", 11, "underline"), fg="blue", bg="#FFFFFF", cursor="hand2")
            email_label.pack(side="left")
            tk.Label(line, text=after, font=("Helvetica", 11), fg="#333", bg="#FFFFFF").pack(side="left")
            email_label.bind("<Button-1>", lambda e: webbrowser.open(f"mailto:{email}"))
        else:
            tk.Label(answer_frame, text=answer, font=("Helvetica", 11), fg="#333",
                     bg="#FFFFFF", wraplength=700, justify="left").pack(pady=(0, 10), padx=10)

        def toggle_answer():
            if answer_frame.winfo_ismapped():
                answer_frame.pack_forget()
                question_btn.config(text="➕ " + question)
            else:
                answer_frame.pack(fill="x", padx=10, pady=(0, 10))
                question_btn.config(text="➖ " + question)
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        question_btn = tk.Button(container, text="➕ " + question, font=("Helvetica", 12, "bold"),
                                 relief="flat", fg="#006747", bg="#FFFFFF",
                                 activebackground="#E6F3F2", anchor="w", justify="left",
                                 command=toggle_answer, cursor="hand2")
        question_btn.pack(fill="x", padx=10, pady=8)

# Test runner
if __name__ == "__main__":
    root = tk.Tk()
    root.title("FAQ Page - USF Course Registration")
    root.geometry("900x750")
    root.configure(bg="#F4F4F4")
    FAQPage(root).pack(fill="both", expand=True)
    root.mainloop()