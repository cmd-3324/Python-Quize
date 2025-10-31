from tkinter import *
from time import *
from tkinter.ttk import *
def Progress():
   prograssbar["value"] += 30
    # window.update_idletasks()
window = Tk()
downloadubtn = Button(window, text="Download Me",command=Progress).pack()
prograssbar = Progressbar(window,orient=HORIZONTAL,length=300).pack(pady=30)

window.mainloop()
