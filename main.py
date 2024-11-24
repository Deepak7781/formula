import sqlite3
from tkinter import *
from tkinter.font import Font

root = Tk()
root.tk.call('tk', 'scaling', 1.3)  

root.title("Formula")
root.config(bg="skyblue") 
root.state("zoomed")  

# Styling
header_font = Font(family="Helvetica", size=24, weight="bold", slant="italic")
section_title_font = Font(family="Helvetica", size=18, weight="bold")
content_font = Font(family="Arial", size=12, weight = "normal")

def get_formula():
    field = clicked.get()  
    formula_desc = desc_field_entry.get() 
    
    table_map = {
        "General Physics": "classicalPhysics",
        "Thermodynamics": "thermodynamics",
        "Solid Mechanics": "solidMechanics",
        "Fluid Mechanics": "fluidMechanics"
    }
    
    table_name = table_map.get(field)

    if table_name:
        connection = sqlite3.connect("formula.db")
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT formula, terms FROM {table_name} WHERE name = ?",
            (formula_desc,)
        )
        result = cursor.fetchall()
        connection.close()

        if result:
            print(result)
            formula, terms = result[0] 
            print(terms)
            formula_display.config(text=f"{formula}")
            explanation_display.config(text=f"{terms}")  
        else:
            formula_display.config(text="No formula found for the given query.")  
            explanation_display.config(text="") 




root.grid_rowconfigure(0, weight=0)  # Fixed height for the header
root.grid_rowconfigure(1, weight=1)  # Expandable content area
root.grid_columnconfigure(0, weight=1)  # Left column
root.grid_columnconfigure(1, weight=1)  # Right column

# Header
header = Label(
    root,
    text="Formula",
    font=header_font,
    fg="blue",
    bg="white",
    padx=10,
    pady=10
)
header.grid(row=0, column=0, columnspan=2, sticky="ew")

# Left Section: Introduction and Dropdown Menu
left_frame = Frame(root, bg="skyblue")  # Set background to black
left_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

intro_title = Label(
    left_frame,
    text="Welcome to the Formula Selector App!",
    font=section_title_font,
    anchor="w",
    bg="skyblue",
    fg="white"
)
intro_title.pack(anchor="nw", pady=10)

intro_content = Label(
    left_frame,
    text=(
        "This application is designed to simplify your exploration of essential formulas across various\n\n"
        "scientific fields. Whether you're delving into General Physics, Thermodynamics, Solid Mechanics,\n\n"
        "or Fluid Mechanics, this app provides an intuitive interface to quickly access the formulas you need."
    ),
    font=content_font,
    justify="left",
    anchor="nw",
    bg="skyblue",
    fg="#4F4F4F"
)
intro_content.pack(anchor="nw", pady=5)

field_title = Label(
    left_frame,
    text="Select a field:",
    font=("Arial", 14),
    anchor="w",
    bg="skyblue",
    fg="white"
)
field_title.pack(anchor="nw", pady=10)

clicked = StringVar()
clicked.set("General Physics")
dropdown = OptionMenu(left_frame, clicked, "General Physics", "Thermodynamics", "Solid Mechanics", "Fluid Mechanics")
dropdown.config(width=20, font=("Arial", 12), bg="white", fg="black")  # Keep dropdown default background
dropdown.pack(anchor="nw", pady=10)

desc_field_label = Label(
    left_frame,
    text="Name/Description of the formula:",
    font=("Arial", 14),
    bg="skyblue",
    fg="white",
    anchor="w"
)
desc_field_label.pack(anchor="nw", pady=10)

# Add a text box for user input
desc_field_entry = Entry(
    left_frame,
    font=("Arial", 12),
    width=40,
    bg="white",
    fg="black"
)
desc_field_entry.pack(anchor="nw", pady=5)

search_button = Button(
    left_frame,
    text="Search Formula",
    command=get_formula,
    font=("Arial", 12),
    bg="blue",
    fg="white",
    padx=10,
    pady=5
)
search_button.pack(anchor="nw", pady=10)

# Right Section
right_frame = Frame(root, bg="skyblue")
right_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)

formula_display_title = Label(
    left_frame,
    text="Formula",
    font=section_title_font,
    fg="white",
    bg="skyblue"
)
formula_display_title.pack(anchor="nw", pady=10)

formula_display = Label(
    left_frame,
    text="Enter a field and formula description to see the formula here.",
    font=content_font,
    justify="left",
    anchor="nw",
    bg="skyblue",
    fg="#4F4F4F",
    wraplength=400
)
formula_display.pack(anchor="nw", pady=5)

explanation_display_title = Label(
    left_frame,
    text="Explanation",
    font=section_title_font,
    fg="white",
    bg="skyblue"
)
explanation_display_title.pack(anchor="nw", pady=10)

explanation_display = Label(
    left_frame,
    text="Explanation will be shown here.",
    font=content_font,
    justify="left",
    anchor="nw",
    bg="skyblue",
    fg="#4F4F4F",
    wraplength=400
)
explanation_display.pack(anchor="nw", pady=5)

# Right Section: Quotes, Constants, and Formulas
right_frame = Frame(root, bg="skyblue")  # Set background to black
right_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)

quote_title = Label(
    right_frame,
    text="Quote of the Day",
    font=section_title_font,
    fg="white",
    bg="skyblue"
)
quote_title.pack(anchor="nw", pady=10)

quote = Label(
    right_frame,
    text='"The important thing is to never stop questioning." - Albert Einstein',
    font=("Arial", 12, "italic"),
    fg="#4F4F4F",
    bg="skyblue",
    wraplength=400,
    justify="left"
)
quote.pack(anchor="nw", pady=5)

constants_title = Label(
    right_frame,
    text="Fundamental Constants",
    font=section_title_font,
    fg="white",
    bg="skyblue"
)
constants_title.pack(anchor="nw", pady=10)

constants = Label(
    right_frame,
    text=(
        "1. Speed of Light (c): 299,792,458 m/s\n\n"
        "2. Gravitational Constant (G): 6.674 × 10⁻¹¹ N·m²/kg²\n\n"
        "3. Planck's Constant (h): 6.626 × 10⁻³⁴ J·s\n\n"
        "4. Elementary Charge (e): 1.602 × 10⁻¹⁹ C\n\n"
        "5. Avogadro's Number (NA): 6.022 × 10²³ mol⁻¹"
    ),
    font=content_font,
    justify="left",
    anchor="nw",
    bg="skyblue",
    fg="#4F4F4F"
)
constants.pack(anchor="nw", pady=5)

formulas_title = Label(
    right_frame,
    text="Sample Formulas",
    font=section_title_font,
    fg="white",
    bg="skyblue"
)
formulas_title.pack(anchor="nw", pady=10)

formulas = Label(
    right_frame,
    text=(
        "1. Newton's Second Law: F = m × a\n\n"
        "2. Kinetic Energy: KE = ½ × m × v²\n\n"
        "3. Ideal Gas Law: PV = nRT\n\n"
        "4. Ohm's Law: V = I × R\n\n"
        "5. Wave Equation: v = f × λ"
    ),
    font=content_font,
    justify="left",
    anchor="nw",
    bg="skyblue",
    fg="#4F4F4F"
)
formulas.pack(anchor="nw", pady=5)

root.mainloop()
