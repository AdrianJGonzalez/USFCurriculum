import tkinter as tk
import webbrowser

class FAQPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label_title = tk.Label(self, text="Frequently Asked Questions", font=("Helvetica", 16, "bold"))
        label_title.pack(pady=(20, 10))

        # Q1
        q1 = tk.Label(self, text="Q: How can I book an advising appointment?", font=("Helvetica", 12, "bold"), anchor='w', justify='left')
        q1.pack(anchor='w')
        a1 = tk.Label(self, text="A: Once your ULDP form is processed, you can either book an online appointment or visit us during walk-in hours.", font=("Helvetica", 12), wraplength=700, anchor='w', justify='left')
        a1.pack(anchor='w', padx=(20,0))

        # Space
        tk.Label(self, text="").pack()

        # Q2
        q2 = tk.Label(self, text="Q: What are the Walk-in Advising Hours?", font=("Helvetica", 12, "bold"), anchor='w', justify='left')
        q2.pack(anchor='w')
        a2 = tk.Label(self, text="A: Walk-in Advising is available on Tuesdays and Thursdays from 10 AM to 4 PM at ENB 379.", font=("Helvetica", 12), wraplength=700, anchor='w', justify='left')
        a2.pack(anchor='w', padx=(20,0))

        # Space
        tk.Label(self, text="").pack()

        # Q3
        q3 = tk.Label(self, text="Q: How do I contact you for additional questions?", font=("Helvetica", 12, "bold"), anchor='w', justify='left')
        q3.pack(anchor='w')
        a3 = tk.Label(self, text="A: For further inquiries, please email us at ENG-EEAdvising@usf.edu.", font=("Helvetica", 12), wraplength=700, anchor='w', justify='left')
        a3.pack(anchor='w', padx=(20,0))

        # Space
        tk.Label(self, text="").pack()

        # Q4
        q4 = tk.Label(self, text="Q: Where can I find more information?", font=("Helvetica", 12, "bold"), anchor='w', justify='left')
        q4.pack(anchor='w')
        # Only the link is clickable
        def open_link(event):
            webbrowser.open_new("https://www.usf.edu/engineering/ee/undergraduate/ugadvising.aspx")
        a4_frame = tk.Frame(self)
        a4_frame.pack(anchor='w', padx=(20,0))
        a4_text = tk.Label(a4_frame, text="A: You can visit our official advising website at: ", font=("Helvetica", 12))
        a4_text.pack(side="left")
        link = tk.Label(a4_frame, text="https://www.usf.edu/engineering/ee/undergraduate/ugadvising.aspx", fg="blue", cursor="hand2", font=("Helvetica", 12, "underline"))
        link.pack(side="left")
        link.bind("<Button-1>", open_link)

        # Space
        tk.Label(self, text="").pack()

        # Q5
        q5 = tk.Label(self, text="Q: What is a Co/Prerequisite?", font=("Helvetica", 12, "bold"), anchor='w', justify='left')
        q5.pack(anchor='w')
        a5 = tk.Label(self, text="A: A co/prerequisite is a course you can either take before or alongside a desired class.", font=("Helvetica", 12), wraplength=700, anchor='w', justify='left')
        a5.pack(anchor='w', padx=(20,0))
