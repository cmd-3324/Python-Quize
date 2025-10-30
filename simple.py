from tkinter import *

page = Tk()
page.geometry("300x300")
page.config(bg="black")


def method():
    py = python.get()
    jv = java.get()

    if py and jv:
        print("Both")
        exit()
    elif py:
        print("I like Python")
        exit()
    elif jv:
        print("I like Java")
        exit()
    else:
        print("IDK!")
        exit()

java = BooleanVar()
python = BooleanVar()

base_path = "C:\\Users\\Rayan_Svc\\E:\\Simple_Python_Tasks_to_Improve\\All\\eng.ico"

pythonButton = Checkbutton(
    page,
    text="Python",
    fg="green",
    font="Arial",
    compound="right",
    pady=30,
    variable=python,
    command=method,
    activeforeground="red",
    activebackground="orange",
)
pythonButton.pack()

javaButton = Checkbutton(
    page,
    text="Java",
    fg="green",
    font="Arial",
    compound="right",
    pady=40,
    variable=java,
    command=method,
)
javaButton.pack()
page.config(bg="black")
#-----practicing entry 
def showname():
    username = entry_term.get()
    print(f"WElcome {username}")
entry_term = Entry(page, font="Arial", fg="lightgreen", bg="black", activebackground="gray")
showBtn = Button(page,font="Arial", activebackground="yellow", activeforeground="pink" , command=showname)
entry_term.insert(0, "Python")
page.mainloop()
