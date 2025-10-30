from tkinter import *
from tkinter import messagebox

# from math import sqrt
# print(sqrt(-1))
sampleFIlePath = "C:\\Users\\Rayan_Svc\\E:"
based_iconPath = "C:\\Users\\Rayan_Svc\\Pictures\\"
mywindow = Tk()
mywindow.geometry("400x400")
mywindow.title("Test BKAB")
mylabelIcon = PhotoImage(file=f"{based_iconPath}123.ico", format="png")
mytestIcon = PhotoImage(file=f"{based_iconPath}rubik.png",format="png")
firstlabel = Label(mywindow,text="First lable", font=("IRRoya", 25, "bold"), fg="red" ,bg="black"
                   ,relief=SUNKEN, bd=20, padx=20, pady=30, compound="bottom")
# mybutton = Button(
#     mywindow,
#     text="Mybutton",
#     fg="red",
#     bg="brown",
#     command=[print("rer") for x in range(14)],
# )

times = 0
def clickme():
    global times
    times +=1 
    # print(f"YOu clicked {times}") 
    print("Hi,you clicked")
def onclose():

    print("You have clicked :",times)
    with open(
        f"{sampleFIlePath}recordsOfclick.txt",
        "a+",
    ) as mn:
        mn.write(f"{times},record\n")
    if messagebox.askokcancel("Quit", f"Are u sure to leave , you records will be removed?"):
        mywindow.destroy()
mywindow.protocol("WM_DELETE_WINDOW", onclose)
secondmbtn = Button(mywindow, text="Mysecond btn",command=clickme, activebackground="gray", 
                )
# "state" is a param in Button to sepcify is button as disabled or enabled
secondmbtn.place(x=700, y=300)
# mybutton.pack()
secondLabel = Label(mywindow, text="Second LAbel with place ", font="IRRoya")
secondLabel.place(x=200,y=130)
firstlabel.pack()
mywindow.config(background="blue")
mywindow.iconphoto(True,mytestIcon)
mywindow.mainloop()
