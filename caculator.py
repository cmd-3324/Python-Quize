import tkinter as tk
import math
import time

# --- Main window ---
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("370x520")
root.config(bg="#1e1e1e")

# --- Display ---
entry = tk.Entry(
    root,
    width=25,
    borderwidth=5,
    font=("Consolas", 22),
    justify="right",
    state="readonly",
    bg="#2e2e2e",
    fg="#00ffcc",
)
entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

expression = ""
last_expression = ""


# --- Update display ---
def update_display():
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, expression)
    entry.config(state="readonly")


# --- Button actions ---
def button_click(value):
    global expression
    expression += str(value)
    update_display()


def button_clear():
    global expression
    expression = ""
    update_display()


def button_equal():
    global expression, last_expression
    try:
        exp = expression
        # Replace custom symbols with valid Python code
        exp = exp.replace("√(", "math.sqrt(")
        exp = exp.replace("³√(", "(")  # we'll append **(1/3) manually
        exp = exp.replace("^", "**")

        # Handle cube roots: find all ³√(expr) and convert to (expr)**(1/3)
        while "³√(" in expression:
            start = exp.find("(")  # first open after ³√
            count = 1
            i = start + 1
            while i < len(exp) and count > 0:
                if exp[i] == "(":
                    count += 1
                elif exp[i] == ")":
                    count -= 1
                i += 1
            # Replace the inner expr with (expr)**(1/3)
            inner = exp[start:i]
            exp = exp.replace(inner, f"{inner}**(1/3)", 1)

        # Evaluate trig functions in degrees
        exp = exp.replace("sin(", "math.sin(math.radians(")
        exp = exp.replace("cos(", "math.cos(math.radians(")
        exp = exp.replace("tan(", "math.tan(math.radians(")

        result = eval(exp)
        last_expression = expression
        expression = str(result)
        update_display()
    except Exception:
        expression = "Error"
        update_display()
        expression = ""


# --- Shortcut buttons ---
def button_square():
    button_click("**2")


def button_cube():
    button_click("**3")


def button_sqrt():
    button_click("√(")


def button_cuberoot():
    button_click("³√(")


def button_trig(func):
    button_click(f"{func}(")


# --- Smart AutoPlay ---
def autoplay():
    global last_expression, expression
    if last_expression:
        expression = last_expression
        update_display()
        root.update()
        time.sleep(0.3)
        button_equal()


# --- Button layout ---
buttons = [
    ("7", 1, 0),
    ("8", 1, 1),
    ("9", 1, 2),
    ("/", 1, 3),
    ("C", 1, 4),
    ("4", 2, 0),
    ("5", 2, 1),
    ("6", 2, 2),
    ("*", 2, 3),
    ("√", 2, 4),
    ("1", 3, 0),
    ("2", 3, 1),
    ("3", 3, 2),
    ("-", 3, 3),
    ("³√", 3, 4),
    ("0", 4, 0),
    (".", 4, 1),
    ("+", 4, 2),
    ("^", 4, 3),
    ("=", 4, 4),
    ("x²", 5, 0),
    ("x³", 5, 1),
    ("sin", 5, 2),
    ("cos", 5, 3),
    ("tan", 5, 4),
    ("(", 6, 0),
    (")", 6, 1),
    ("AutoPlay", 6, 2, 3),
]

# --- Create buttons ---
for btn in buttons:
    text = btn[0]
    row = btn[1]
    col = btn[2]
    colspan = btn[3] if len(btn) > 3 else 1

    if text == "=":
        cmd = button_equal
        color = "#00cc66"
    elif text == "C":
        cmd = button_clear
        color = "#ff4444"
    elif text == "x²":
        cmd = button_square
        color = "#6666ff"
    elif text == "x³":
        cmd = button_cube
        color = "#6666ff"
    elif text == "√":
        cmd = button_sqrt
        color = "#ffaa00"
    elif text == "³√":
        cmd = button_cuberoot
        color = "#ffaa00"
    elif text in ("sin", "cos", "tan"):
        cmd = lambda t=text: button_trig(t)
        color = "#ff99ff"
    elif text == "AutoPlay":
        cmd = autoplay
        color = "#00ccff"
    else:
        cmd = lambda t=text: button_click(t)
        color = "#444444"

    tk.Button(
        root,
        text=text,
        padx=20,
        pady=20,
        font=("Arial", 12, "bold"),
        bg=color,
        fg="white",
        activebackground="#333333",
        command=cmd,
    ).grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=1, pady=1)

# --- Make grid responsive ---
for i in range(7):
    root.rowconfigure(i, weight=1)
for j in range(5):
    root.columnconfigure(j, weight=1)

root.mainloop()
