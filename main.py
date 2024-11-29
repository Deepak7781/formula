from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import showerror, showinfo
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
import sqlite3
import random
import re

#setup

root = Tk()
root.tk.call('tk', 'scaling', 1.5)
root.title("Formula")
root.config(bg="skyblue")
root.state("zoomed")

# Styling
header_font = Font(family="Helvetica", size=24, weight="bold", slant="italic")
section_title_font = Font(family="Helvetica", size=18, weight="bold")
content_font = Font(family="Arial", size=12, weight="normal")

# Random quotes
QUOTES = [
    '"The important thing is to never stop questioning." - Albert Einstein',
    '"Imagination is more important than knowledge." - Albert Einstein',
    '"Science is the poetry of reality." - Richard Dawkins',
    '"Not everything that counts can be counted." - William Bruce Cameron',
    '"E = mc²: Energy equals mass times the speed of light squared." - Einstein'
]

def clean_text(text):
    """Cleans the input text by removing unwanted characters."""
    return re.sub(r'[^\x20-\x7E\n\t\u0370-\u03FFu2080-\u208E\u2090-\u209C]', '', text)

def get_formula():
    """Fetches formulas based on user selection."""
    field = clicked.get()
    formula_desc = desc_field_entry.get().strip()
    
    table_map = {
        "General Physics": "classicalPhysics",
        "Thermodynamics": "thermodynamics",
        "Solid Mechanics": "solidMechanics",
        "Fluid Mechanics": "fluidMechanics"
    }
    
    table_name = table_map.get(field)

    if table_name:
        try:
            connection = sqlite3.connect("formula.db")
            cursor = connection.cursor()
            
            if formula_desc.lower() == "all":  # Fetch all formulas
                cursor.execute(f"SELECT name, formula, terms FROM {table_name}")
                results = cursor.fetchall()
                
                if results:
                    display_text = "\n\n".join([f"Name: {row[0]}\nFormula: {row[1]}\nTerms: {row[2]}" for row in results])
                    formula_display_text.set("All formulas fetched. Ready for export.")
                    explanation_display_text.set(display_text)
                else:
                    formula_display_text.set("No formulas found in this table.")
                    explanation_display_text.set("")
            else:  # Fetch specific formula
                cursor.execute(
                    f"SELECT formula, terms FROM {table_name} WHERE name = ?",
                    (formula_desc,)
                )
                result = cursor.fetchone()
                if result:
                    formula, terms = result
                    formula_display_text.set(formula)
                    explanation_display_text.set(terms)
                else:
                    formula_display_text.set("No formula found for the given query.")
                    explanation_display_text.set("")
            
            connection.close()
        except Exception as e:
            showerror("Database Error", f"An error occurred: {e}")
    else:
        showerror("Field Error", "Please select a valid field.")

pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))

def export_formula_to_pdf():
    formula = clean_text(formula_display_text.get().strip())
    explanation = clean_text(explanation_display_text.get().strip())

    if formula and "All formulas fetched" in formula:
        try:
            c = pdf_canvas.Canvas("all_formulas_export.pdf", pagesize=letter)
            c.setFont("DejaVuSans", 12)
            c.drawString(30, 750, "All Formulas Export")

            y_position = 730
            formulas = explanation.split("\n\n")

            for item in formulas:
                for line in item.split("\n"):
                    c.drawString(30, y_position, line)
                    y_position -= 15
                    if y_position < 50:
                        c.showPage()
                        c.setFont("DejaVuSans", 12)
                        y_position = 750

            c.save()
            showinfo("Export Success", "All formulas exported to all_formulas_export.pdf!")
        except Exception as e:
            showerror("Export Error", f"An error occurred: {e}")
    elif formula:
        try:
            c = canvas.Canvas("exported_formula.pdf", pagesize=letter)
            c.setFont("DejaVuSans", 12)
            c.drawString(30, 750, "Formula Export")
            c.drawString(30, 730, "Formula:")
            c.drawString(30, 710, formula)
            c.drawString(30, 690, "Explanation:")

            explanation_lines = explanation.split("\n")
            y_position = 670
            for line in explanation_lines:
                c.drawString(30, y_position, line)
                y_position -= 15
                if y_position < 50:
                    c.showPage()
                    c.setFont("DejaVuSans", 12)
                    y_position = 750

            c.save()
            showinfo("Export Success", "Formula exported to exported_formula.pdf!")
        except Exception as e:
            showerror("Export Error", f"An error occurred: {e}")
    else:
        showerror("Export Error", "No valid formula to export. Please search for a formula first.")

# Layout Configuration
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Header
header = Label(root, text="Formula", font=header_font, fg="blue", bg="white", padx=10, pady=10)
header.grid(row=0, column=0, columnspan=2, sticky="ew")

# Left Section
left_frame = Frame(root, bg="skyblue")
left_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

Label(left_frame, text="Welcome to the Formula Selector App!", font=section_title_font, bg="skyblue", fg="white").pack(anchor="nw", pady=10)
Label(left_frame, text=(
    "This application is designed to simplify your exploration of essential formulas across various\n\n"
    "scientific fields. Whether you're delving into General Physics, Thermodynamics, Solid Mechanics,\n\n"
    "or Fluid Mechanics, this app provides an intuitive interface to quickly access the formulas you need."
), font=content_font, bg="skyblue", fg="#4F4F4F", justify="left").pack(anchor="nw", pady=10)

Label(left_frame, text="Select a field:", font=content_font, bg="skyblue", fg="white").pack(anchor="nw", pady=10)
clicked = StringVar(value="General Physics")
dropdown = OptionMenu(left_frame, clicked, *["General Physics", "Thermodynamics", "Solid Mechanics", "Fluid Mechanics"])
dropdown.config(font=("Arial", 12))
dropdown.pack(anchor="nw", pady=5)

desc_field_entry = Entry(left_frame, font=content_font, width=40)
desc_field_entry.pack(anchor="nw", pady=5)

search_button = Button(left_frame, text="Search Formula", command=get_formula, font=content_font, bg="blue", fg="white")
search_button.pack(anchor="nw", pady=10)

export_button = Button(left_frame, text="Export to PDF", command=export_formula_to_pdf, font=content_font, bg="blue", fg="white")
export_button.pack(anchor="nw", pady=5)

# Scrollable Formula and Explanation Display
scrollable_frame = Frame(left_frame)
scrollable_frame.pack(fill=BOTH, expand=True, pady=10)

canvas = Canvas(scrollable_frame, bg="skyblue")
scrollbar = Scrollbar(scrollable_frame, orient=VERTICAL, command=canvas.yview)
scrollable_content = Frame(canvas, bg="skyblue")

scrollable_content.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_content, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

formula_display_text = StringVar(value="Enter a field and formula description to see the formula here.")
formula_display = Label(scrollable_content, textvariable=formula_display_text, font=content_font, bg="skyblue", wraplength=400, justify="left")
formula_display.pack(anchor="nw", pady=5)

explanation_display_text = StringVar(value="Explanation will appear here.")
explanation_display = Label(scrollable_content, textvariable=explanation_display_text, font=content_font, bg="skyblue", wraplength=400, justify="left")
explanation_display.pack(anchor="nw", pady=5)

# Right Section
right_frame = Frame(root, bg="skyblue")
right_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)

Label(right_frame, text="Quote of the Day", font=section_title_font, fg="white", bg="skyblue").pack(anchor="nw", pady=10)
quote = Label(right_frame, text=random.choice(QUOTES), font=("Arial", 12, "italic"), fg="#4F4F4F", bg="skyblue", wraplength=400)
quote.pack(anchor="nw", pady=5)

Label(right_frame, text="Fundamental Constants", font=section_title_font, fg="white", bg="skyblue").pack(anchor="nw", pady=10)
Label(right_frame, text=(
    "1. Speed of Light (c): 299,792,458 m/s\n\n"
    "2. Gravitational Constant (G): 6.674 × 10⁻¹¹ N·m²/kg²\n\n"
    "3. Planck's Constant (h): 6.626 × 10⁻³⁴ J·s\n\n"
    "4. Elementary Charge (e): 1.602 × 10⁻¹⁹ C"
), font=content_font, fg="#4F4F4F", bg="skyblue", justify="left", wraplength=400).pack(anchor="nw")

Label(right_frame, text="Sample Formulas", font=section_title_font, fg="white", bg="skyblue").pack(anchor="nw", pady=10)
Label(right_frame, text=(
    "1. Newton's Second Law: F = m × a\n\n"
    "2. Kinetic Energy: KE = ½ × m × v²\n\n"
    "3. Ideal Gas Law: PV = nRT\n\n"
    "4. Ohm's Law: V = I × R\n\n"
    "5. Wave Equation: v = f × λ"
), font=content_font, fg="#4F4F4F", bg="skyblue", justify="left").pack(anchor="nw", pady=5)



root.mainloop()
