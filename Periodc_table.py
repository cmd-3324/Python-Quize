# from docx import Document
# from docx.shared import Inches, Cm
# from docx.oxml import parse_xml
# from docx.oxml.ns import nsdecls

# # === Output path ===
# output_path = r"E:\EmptyPeriodic.docx"

# # === Create document ===
# doc = Document()

# # Set narrow margins (≈2 px ≈ 0.07 cm)
# sections = doc.sections
# for section in sections:
#     section.top_margin = Cm(0.07)
#     section.bottom_margin = Cm(0.07)
#     section.left_margin = Cm(0.07)
#     section.right_margin = Cm(0.07)
#     section.page_height = Cm(29.7)  # A4
#     section.page_width = Cm(21.0)

# # === Create table: 4 rows × 13 columns ===
# rows, cols = 4, 13
# table = doc.add_table(rows=rows, cols=cols)
# table.autofit = False

# # === Set uniform cell sizes ===
# cell_width = Cm(21.0 / cols)  # fit width
# cell_height = Cm(29.7 / (rows + 1))  # fit height roughly

# for row in table.rows:
#     for cell in row.cells:
#         cell.width = cell_width
#         # set height via paragraph spacing trick
#         cell.paragraphs[0].space_before = Cm(0)
#         cell.paragraphs[0].space_after = Cm(0)
#         cell.text = ""  # leave empty
#         # center text (just to align if you add later)
#         for p in cell.paragraphs:
#             p.alignment = 1  # center horizontally

# # === Add thick black border ===
# tbl = table._element
# tblBorders = parse_xml(r"""
# <w:tblBorders %s>
# <w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>
# <w:left w:val="single" w:sz="12" w:space="0" w:color="000000"/>
# <w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>
# <w:right w:val="single" w:sz="12" w:space="0" w:color="000000"/>
# <w:insideH w:val="single" w:sz="6" w:space="0" w:color="000000"/>
# <w:insideV w:val="single" w:sz="6" w:space="0" w:color="000000"/>
# </w:tblBorders>
# """ % nsdecls('w'))
# tbl.tblPr.tblBorders = tblBorders

# # === Save file ===
# doc.save(output_path)
# print(f"✅ Periodic table created at: {output_path}")

import os
import random
from time import sleep
elements = [
    {"atomic_number": 1, "symbol": "H", "name": "Hydrogen"},
    {"atomic_number": 2, "symbol": "He", "name": "Helium"},
    {"atomic_number": 3, "symbol": "Li", "name": "Lithium"},
    {"atomic_number": 4, "symbol": "Be", "name": "Beryllium"},
    {"atomic_number": 5, "symbol": "B", "name": "Boron"},
    {"atomic_number": 6, "symbol": "C", "name": "Carbon"},
    {"atomic_number": 7, "symbol": "N", "name": "Nitrogen"},
    {"atomic_number": 8, "symbol": "O", "name": "Oxygen"},
    {"atomic_number": 9, "symbol": "F", "name": "Fluorine"},
    {"atomic_number": 10, "symbol": "Ne", "name": "Neon"},
    {"atomic_number": 11, "symbol": "Na", "name": "Sodium"},
    {"atomic_number": 12, "symbol": "Mg", "name": "Magnesium"},
    {"atomic_number": 13, "symbol": "Al", "name": "Aluminium"},
    {"atomic_number": 14, "symbol": "Si", "name": "Silicon"},
    {"atomic_number": 15, "symbol": "P", "name": "Phosphorus"},
    {"atomic_number": 16, "symbol": "S", "name": "Sulfur"},
    {"atomic_number": 17, "symbol": "Cl", "name": "Chlorine"},
    {"atomic_number": 18, "symbol": "Ar", "name": "Argon"},
    {"atomic_number": 19, "symbol": "K", "name": "Potassium"},
    {"atomic_number": 20, "symbol": "Ca", "name": "Calcium"},
    {"atomic_number": 21, "symbol": "Sc", "name": "Scandium"},
    {"atomic_number": 22, "symbol": "Ti", "name": "Titanium"},
    {"atomic_number": 23, "symbol": "V", "name": "Vanadium"},
    {"atomic_number": 24, "symbol": "Cr", "name": "Chromium"},
    {"atomic_number": 25, "symbol": "Mn", "name": "Manganese"},
    {"atomic_number": 26, "symbol": "Fe", "name": "Iron"},
    {"atomic_number": 27, "symbol": "Co", "name": "Cobalt"},
    {"atomic_number": 28, "symbol": "Ni", "name": "Nickel"},
    {"atomic_number": 29, "symbol": "Cu", "name": "Copper"},
    {"atomic_number": 30, "symbol": "Zn", "name": "Zinc"},
    {"atomic_number": 31, "symbol": "Ga", "name": "Gallium"},
    {"atomic_number": 32, "symbol": "Ge", "name": "Germanium"},
    {"atomic_number": 33, "symbol": "As", "name": "Arsenic"},
    {"atomic_number": 34, "symbol": "Se", "name": "Selenium"},
    {"atomic_number": 35, "symbol": "Br", "name": "Bromine"},
    {"atomic_number": 36, "symbol": "Kr", "name": "Krypton"},
]

class PeriodicTableQuiz:
    def __init__(self, elements):
        self.elements = elements
        self.counter = 0
        self.correctNum = 0
        self.falseNum = 0
        self.TrueRate = 0

    def get_random_options(self, correct_element, key, num_options=5):
        options = set()
        options.add(correct_element[key])
        while len(options) < num_options:
            element = random.choice(self.elements)
            options.add(element[key])
        options = list(options)
        random.shuffle(options)
        return options
    def clearscreen(self):
        sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')

    def ask_question_type1(self):
        element = random.choice(self.elements)
        symbol = element["symbol"]
        correct_name = element["name"]
        options = self.get_random_options(element, "name")

        print(f"\nWhat is the name of the element with symbol '{symbol}'?")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        answer = input("Enter option number: ").strip()

        if not answer.isdigit() or int(answer) < 1 or int(answer) > len(options):
            print("Invalid input. Moving to next question.")
            return False

        chosen_name = options[int(answer) - 1]
        if chosen_name == correct_name:
            self.correctNum += 1
            print("Correct!")
           
        else:
            self.falseNum += 1
            print(f"Wrong! The correct answer is: {correct_name}")
          
        return True

    def ask_question_type2(self):
        element = random.choice(self.elements)
        name = element["name"]
        correct_symbol = element["symbol"]
        options = self.get_random_options(element, "symbol")

        print(f"\nWhat is the symbol of the element named '{name}'?")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        answer = input("Enter option number: ").strip()

        if not answer.isdigit() or int(answer) < 1 or int(answer) > len(options):
            print("Invalid input. Moving to next question.")
            return False

        chosen_symbol = options[int(answer) - 1]
        if chosen_symbol == correct_symbol:
            self.correctNum += 1
            print("Correct!")
     
        else:
            self.falseNum += 1
            print(f"Wrong! The correct answer is: {correct_symbol}")
  
        return True

    def ask_question_type3(self):
        element = random.choice(self.elements)
        atomic_number = element["atomic_number"]
        correct_name = element["name"]
        options = self.get_random_options(element, "name")

        print(f"\nWhat is the name of the element with atomic number '{atomic_number}'?")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        answer = input("Enter option number: ").strip()

        if not answer.isdigit() or int(answer) < 1 or int(answer) > len(options):
            print("Invalid input. Moving to next question.")
            return False

        chosen_name = options[int(answer) - 1]
        if chosen_name == correct_name:
            self.correctNum += 1
            print("Correct!")
            
        else:
            self.falseNum += 1
            print(f"Wrong! The correct answer is: {correct_name}")
           
        return True

    def run(self):
        print("Periodic Table Quiz - First 36 Elements")
        print("Choose question type:")
        print("1: Given symbol, select name")
        print("2: Given name, select symbol")
        print("3: Given atomic number, select name")

        while True:
            q_type = input("\nEnter question type (1/2/3) or 'exit' to quit: ").strip().lower()
            TrueRate = self.TrueRate = (self.correctNum / self.counter) * 100 if self.counter > 0 else 0

            if q_type == "exit":
                print(f"\nYou've played {self.counter} questions, got {self.correctNum} correct, and {self.falseNum} wrong. \n {TrueRate} ")
                print("Thanks for playing!")
                break

            if q_type not in ("1", "2", "3"):
                
                self.clearscreen()
                print("Invalid question type. Try again.")
                continue

            if q_type == "1":
                if self.ask_question_type1():
                    self.counter += 1
                    self.clearscreen()
            elif q_type == "2":
                if self.ask_question_type2():
                    self.counter += 1
                    self.clearscreen()
            else:
                if self.ask_question_type3():
                    self.counter += 1
                    self.clearscreen()

if __name__ == "__main__":
    quiz = PeriodicTableQuiz(elements)
    quiz.run()

