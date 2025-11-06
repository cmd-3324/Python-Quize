from tkinter import *
from time import sleep


def show_window():
    window = Tk()
    window.attributes("-topmost", True)
    
    window.resizable(True, False)

    canvas = Canvas(window, width=500, height=500)
    canvas.pack()

    canvas.create_line(0, 0, 500, 500, fill="red", width=5)
    canvas.create_arc(
        0, 0, 500, 500, style=PIESLICE, start=180, extent=180, outline="gray", width=4
    )
    canvas.create_rectangle(14, 300, 300, 14, fill="orange", width=1.5)

    # Schedule the window to close
    window.after(5000, lambda: close_and_repeat(window))
    window.mainloop()


def close_and_repeat(win):
    win.destroy()  # Close current window
    # Wait 1 second, then reopen
    sleep(3)
    show_window()


# Start the loop
show_window()
