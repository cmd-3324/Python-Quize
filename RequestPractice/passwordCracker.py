import time as  tm
import requests as rq
import bs4 as beatifulSoup
# password = input("Enter your password : ")
# gueses = []
# start = tm.time()
# chars = "abcdefghijkhlmnopqrstuvwxyz"
# nums = "1234567890"
# for val in range(5):
#     a = [i for i in chars]
#     for y in range(val):
#         a = [x + i +s for i in chars for x in a for s in nums]
#         gueses +=a
#     if password in gueses:
#         break
# end =  tm.time()
# clock = str(end - start)
# print("Your passcode is : " , password)
# print("Time taken : ", clock)

class InputExtraction:
    def __init__(self,url):
        self.url = url
        # self.tagname = tagname
    def accessTag(self):
        respones = rq.get(self.url)
        html = beatifulSoup.BeautifulSoup(respones.text, "html.parser")
        #at least we can add 7 ids to check tags , hold on method to see for a few secodns
        x = html.find_all("a",string="", class_="gb1")
        s = 0
        for times in x:
             s +=1
             #len is also can be used here for iterration prevnetion
        print(x,"\n","Times is :",s ,end=" ")
test = InputExtraction("https://google.com")
test.accessTag()

# from fpdf import FPDF

# # Create a Unicode-safe PDF (fpdf2 supports UTF-8)
# pdf = FPDF()
# pdf.set_auto_page_break(auto=True, margin=10)

# # Register a Unicode font (DejaVu is built into most systems)
# # If it fails, download and place DejaVuSans.ttf in the same folder.
# pdf.add_font("DejaVu", "", "C:/Windows/Fonts/DejaVuSans.ttf", uni=True)
# pdf.set_font("DejaVu", "", 12)


# def add_code_block(pdf, code):
#     pdf.set_font("DejaVu", "", 10)
#     pdf.set_fill_color(245, 245, 245)
#     pdf.multi_cell(0, 6, code)
#     pdf.ln(3)


# def add_tip(pdf, number, title, description, examples):
#     pdf.set_font("DejaVu", "B", 14)
#     pdf.cell(0, 8, f"{number}. {title}", ln=True)
#     pdf.set_font("DejaVu", "", 12)
#     pdf.multi_cell(0, 6, description)
#     pdf.ln(3)
#     for ex in examples:
#         add_code_block(pdf, ex)


# # Add Title Page
# pdf.add_page()
# pdf.set_font("DejaVu", "B", 20)
# pdf.cell(0, 12, "🐍 Python One-Liner Mastery", ln=True, align="C")
# pdf.ln(8)
# pdf.set_font("DejaVu", "", 13)
# pdf.multi_cell(
#     0,
#     8,
#     "Master the art of Python one-liners — from transformations and filtering to nested comprehensions and functional tricks. Each section comes with examples you can run instantly.",
# )
# pdf.ln(10)

# # ==================== TIPS ====================
# tips = [
#     (
#         1,
#         "Basic Transformation",
#         "Apply a transformation to each element in a list.\nSyntax: [expression for item in iterable]",
#         [
#             "numbers = [1,2,3,4,5]\nsquared = [n**2 for n in numbers]",
#             'words = ["hello", "world"]\nupper_words = [w.upper() for w in words]',
#             'lines = [" hello ", " world "]\ncleaned = [line.strip() for line in lines]',
#             "celsius = [0, 20, 30]\nfahrenheit = [(c*9/5)+32 for c in celsius]",
#             'names = ["Alice", "Bob", "Charlie"]\ninitials = [name[0] for name in names]',
#         ],
#     ),
#     (
#         2,
#         "Filtering Items",
#         "Select only items that meet a condition.\nSyntax: [expression for item in iterable if condition]",
#         [
#             "numbers = [1,2,3,4,5]\neven = [n for n in numbers if n % 2 == 0]",
#             'words = ["hi","hello","ok","Python"]\nlong_words = [w for w in words if len(w)>3]',
#             'lines = ["", "hello", " ", "world"]\ncleaned = [l for l in lines if l.strip()]',
#             "nums = [4,15,8,23,7]\nbig = [n for n in nums if n>10]",
#             'files = ["data.csv","notes.txt","image.png","log.txt"]\ntxt_files = [f for f in files if f.endswith(".txt")]',
#         ],
#     ),
#     (
#         3,
#         "Nested Loops",
#         "Combine multiple loops in one line.\nSyntax: [expression for item1 in iterable1 for item2 in iterable2]",
#         [
#             "pairs = [(i,j) for i in range(3) for j in range(3)]",
#             "pairs_exclude = [(i,j) for i in range(3) for j in range(3) if i!=j]",
#             "matrix = [[1,2],[3,4],[5,6]]\nflat = [num for row in matrix for num in row]",
#             'letters = ["a","b"]\nnumbers = [1,2]\ncomb = [(l,n) for l in letters for n in numbers]',
#         ],
#     ),
#     (
#         4,
#         "Conditional Expressions",
#         "Use if…else expressions inside a comprehension.\nSyntax: [expr_if_true if condition else expr_if_false for item in iterable]",
#         [
#             'numbers = [1,2,3,4,5]\nlabels = ["even" if n%2==0 else "odd" for n in numbers]',
#             'scores = [45,85,72]\ngrades = ["Fail" if s<50 else "Pass" for s in scores]',
#             'products = [{"name":"Pen","stock":0},{"name":"Notebook","stock":5}]\nstatus = ["In Stock" if p["stock"]>0 else "Out of Stock" for p in products]',
#             'nums = [1,2,3]\nformatted = [f"Number {n}" if n%2==1 else f"Even {n}" for n in nums]',
#         ],
#     ),
#     (
#         5,
#         "Flattening Lists",
#         "Flatten nested lists.\nSyntax: [item for sublist in nested_list for item in sublist]",
#         [
#             "matrix = [[1,2],[3,4],[5,6]]\nflat = [num for row in matrix for num in row]",
#             "matrix3d = [[[1],[2]],[[3],[4]]]\nflat3d = [num for plane in matrix3d for row in plane for num in row]",
#             'data = [{"vals":[1,2]},{"vals":[3,4]}]\nall_vals = [v for d in data for v in d["vals"]]',
#         ],
#     ),
#     (
#         6,
#         "Extracting Data",
#         "Extract attributes or values from HTML/JSON in one line.",
#         [
#             'hrefs = [link.get("href") for link in html.find_all("a") if link.get("href")]',
#             'srcs = [img.get("src") for img in html.find_all("img") if img.get("src")]',
#             'names = [d["name"] for d in [{"name":"Alice"},{"name":"Bob"}]]',
#             'passed = [d["name"] for d in [{"name":"Alice","score":80},{"name":"Bob","score":45}] if d["score"]>=50]',
#         ],
#     ),
#     (
#         7,
#         "Applying Functions",
#         "Apply functions to elements in a comprehension.",
#         [
#             'words = ["python","java","c++"]\nlengths = [len(w) for w in words]',
#             'words = ["apple","banana"]\nupper_words = [w.upper() for w in words]',
#             "import math\nnums = [1,4,9]\nroots = [math.sqrt(n) for n in nums]",
#             "def double(x): return x*2\ndoubled = [double(n) for n in [1,2,3]]",
#         ],
#     ),
#     (
#         8,
#         "Removing Empty Items",
#         "Remove empty or whitespace elements from lists.",
#         [
#             'lines = ["hello",""," ","world"]\ncleaned = [l.strip() for l in lines if l.strip()]',
#             "data = [{},{'a':1},{},{'b':2}]\nnon_empty = [d for d in data if d]",
#             "vals = [1,None,2,None,3]\ncleaned = [v for v in vals if v is not None]",
#         ],
#     ),
#     (
#         9,
#         "Dictionary Comprehension",
#         "Create dictionaries using comprehensions.",
#         [
#             "squares = {n:n**2 for n in range(5)}",
#             'names = ["Alice","Bob"]\ninitials = {name:name[0] for name in names}',
#             'scores = {"Alice":45,"Bob":80}\npassed = {k:v for k,v in scores.items() if v>=50}',
#         ],
#     ),
#     (
#         10,
#         "Set Comprehension",
#         "Create sets of unique items using set comprehension.",
#         [
#             "nums = [1,2,2,3,3,3]\nunique_squares = {n**2 for n in nums}",
#             'text = "banana"\nunique_letters = {ch for ch in text}',
#             'words = ["hi","hello","hey","hello"]\nunique_long = {w for w in words if len(w)>3}',
#         ],
#     ),
# ]

# # Add all tips
# for tip in tips:
#     add_tip(pdf, *tip)

# # Save the file
# output_path = "Python_One_Liner_Mastery_Full.pdf"
# pdf.output(output_path)
# print(f"✅ PDF generated successfully: {output_path}")
