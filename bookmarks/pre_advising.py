import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from fpdf import FPDF
import json
import os
import unicodedata

CHECKLIST_FILE = "pre_advising_progress.json"

def clean_text(text):
    return unicodedata.normalize("NFKD", text).encode("latin-1", "ignore").decode("latin-1")

class PreAdvisingChecklistPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.vars = {}
        self.custom_questions = []
        self.notes_text = None
        self.create_widgets()
        self.load_progress()

    def create_widgets(self):
        self.configure(style="Page.TFrame")
        style = ttk.Style()
        style.configure("Page.TFrame", background="#F4F4F4")
        style.configure("Section.TFrame", background="#F4F4F4", relief="groove", borderwidth=1)
        style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), foreground="#006747", background="#F4F4F4")
        style.configure("Item.TCheckbutton", font=("Helvetica", 11), background="#F4F4F4")
        style.configure("Custom.TEntry", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 10, "bold"))

        canvas = tk.Canvas(self, bg="#F4F4F4", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        container = ttk.Frame(canvas, style="Page.TFrame")

        window_id = canvas.create_window((0, 0), window=container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def resize_canvas(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind("<Configure>", resize_canvas)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        wrapper = ttk.Frame(container, style="Page.TFrame")
        wrapper.pack(anchor="n", pady=20)
        wrapper.configure(width=820)

        content = ttk.Frame(wrapper, style="Page.TFrame", padding=10)
        content.pack(anchor="center", fill="both")

        section_defs = {
            "Self-Reflection": [
                "I reviewed my DegreeWorks.",
                "I know how many credits I've earned.",
                "I’ve looked at my GPA.",
                "I’ve reviewed my academic plan.",
                "I’ve reviewed my holds or registration windows."
            ],
            "Academic Planning": [
                "Am I on track to graduate on time?",
                "What courses do you recommend for next semester?",
                "Can we go over my DegreeWorks together?",
                "Are there electives or certificates that complement my major?",
                "What should I know about summer classes?"
            ],
            "Major & Minor": [
                "Should I change my major or minor?",
                "How do I officially declare a new major or minor?",
                "Does my new major affect my graduation timeline?"
            ],
            "Goals & Opportunities": [
                "What internships or research opportunities are available?",
                "What can I do to improve my academic performance?",
                "What are the next steps for preparing for graduate school?"
            ],
            "Financial Aid & Scholarships": [
                "How do my courses affect my financial aid?",
                "Am I meeting Bright Futures/SAP requirements?",
                "Are there any scholarships specific to my program?"
            ]
        }

        for title, items in section_defs.items():
            self.add_checklist_section(content, title, items)

        self.add_custom_question_section(content)
        self.add_notes_section(content)

        btn_row = ttk.Frame(content, style="Page.TFrame")
        btn_row.pack(pady=20)
        ttk.Button(btn_row, text="💾 Save Progress", command=self.save_progress).pack(side="left", padx=10)
        ttk.Button(btn_row, text="📄 Export to PDF", command=self.export_to_pdf).pack(side="left", padx=10)

    def add_checklist_section(self, parent, title, items):
        section = ttk.Frame(parent, style="Section.TFrame", padding=15)
        section.pack(fill="x", pady=10)

        header = tk.Label(section, text=title, font=("Helvetica", 14, "bold"),
                  fg="#006747", bg="#F4F4F4", anchor="w")

        header.pack(fill="x", padx=5, pady=(0, 10))

        for item in items:
            var = tk.BooleanVar()
            self.vars[item] = var
            chk = ttk.Checkbutton(section, text=item, variable=var, style="Item.TCheckbutton")
            chk.pack(anchor="w", padx=10, pady=2)

    def add_custom_question_section(self, parent):
        frame = ttk.Frame(parent, style="Section.TFrame", padding=15)
        frame.pack(fill="x", pady=10)

        tk.Label(frame, text="Custom Questions", font=("Helvetica", 14, "bold"),
         fg="#006747", bg="#F4F4F4").pack(fill="x", padx=5, pady=(0, 10))

        for _ in range(5):
            var = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=var, width=80, style="Custom.TEntry")
            entry.pack(padx=10, pady=4, fill="x")
            self.custom_questions.append(var)

    def add_notes_section(self, parent):
        frame = ttk.Frame(parent, style="Section.TFrame", padding=15)
        frame.pack(fill="both", expand=True, pady=10)

        tk.Label(frame, text="Notes and Goals", font=("Helvetica", 14, "bold"),
         fg="#006747", bg="#F4F4F4").pack(fill="x", padx=5, pady=(0, 10))
        self.notes_text = tk.Text(frame, height=6, font=("Helvetica", 11), wrap="word")
        self.notes_text.pack(fill="both", expand=True, padx=10, pady=5)

    def save_progress(self):
        data = {
            "checked": {k: v.get() for k, v in self.vars.items()},
            "custom": [v.get() for v in self.custom_questions],
            "notes": self.notes_text.get("1.0", "end").strip()
        }
        with open(CHECKLIST_FILE, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Saved", "Progress saved successfully.")

    def load_progress(self):
        if os.path.exists(CHECKLIST_FILE):
            with open(CHECKLIST_FILE, "r") as f:
                data = json.load(f)
            for k, v in data.get("checked", {}).items():
                if k in self.vars:
                    self.vars[k].set(v)
            for i, v in enumerate(data.get("custom", [])):
                if i < len(self.custom_questions):
                    self.custom_questions[i].set(v)
            self.notes_text.insert("1.0", data.get("notes", ""))

    def export_to_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, clean_text("USF Pre-Advising Checklist"), ln=True)

        def write_section(title, items):
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, clean_text(title), ln=True)
            pdf.set_font("Helvetica", "", 11)
            for text in items:
                check = "[x]" if self.vars.get(text, tk.BooleanVar()).get() else "[ ]"
                pdf.cell(0, 8, clean_text(f"{check} {text}"), ln=True)

        keys = list(self.vars.keys())
        write_section("Self-Reflection", keys[:5])
        write_section("Academic Planning", keys[5:10])
        write_section("Major & Minor", keys[10:13])
        write_section("Goals & Opportunities", keys[13:16])
        write_section("Financial Aid & Scholarships", keys[16:])

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, clean_text("Custom Questions"), ln=True)
        pdf.set_font("Helvetica", "", 11)
        for q in self.custom_questions:
            q_text = q.get()
            if q_text:
                pdf.cell(0, 8, clean_text(f"[ ] {q_text}"), ln=True)

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, clean_text("Notes and Goals"), ln=True)
        pdf.set_font("Helvetica", "", 11)
        for line in self.notes_text.get("1.0", "end").strip().splitlines():
            pdf.multi_cell(0, 8, clean_text(line))

        filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if filepath:
            try:
                pdf.output(filepath)
                messagebox.showinfo("Exported", f"Checklist exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Failed to save PDF: {e}")
        else:
            messagebox.showwarning("Canceled", "Export canceled or invalid file path.")
