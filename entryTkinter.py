from tkinter import *
import time


# Entry widget = textbox that accepts a single line of user input
def submit():
    username = entry.get()
    print("Hello " + username)


def delete():
    entry.delete(0, END)


def backspace():
    entry.delete(len(entry.get()) - 1,END)


def DBbackspace():
    username = entry.get()
    entry.delete(len(username) - 2, END)


# Timer variables
timer_running = False
start_time = 0
elapsed_time = 0


def start():
    global timer_running, start_time
    if not timer_running:
        start_time = time.time() - elapsed_time  # continue from last elapsed
        timer_running = True
        update_timer()
        print("Timer started")


def stop():
    global timer_running, elapsed_time
    if timer_running:
        timer_running = False
        elapsed_time = time.time() - start_time
        print(f"Timer stopped at {elapsed_time:.2f} seconds")


def restart():
    global timer_running, start_time, elapsed_time
    timer_running = False
    start_time = time.time()
    elapsed_time = 0
    timer_label.config(text="0.00 s")
    start()  # automatically starts timer
    print("Timer restarted")


def update_timer():
    if timer_running:
        current_time = time.time() - start_time
        timer_label.config(text=f"{current_time:.5f} s")
        window.after(1,update_timer)  # update every 100 ms


# GUI setup
window = Tk()
window.title("Timer Example")

entry = Entry(window, font=("Arial", 50), fg="#00ff00", bg="black")
entry.insert(0, "Spongebob")
entry.pack(side=LEFT)

submit_button = Button(window, text="submit", command=submit)
submit_button.pack(side=RIGHT)

delete_button = Button(window, text="delete", command=delete)
delete_button.pack(side=RIGHT)

backspace_button = Button(window, text="backspace", command=backspace)
backspace_button.pack(side=RIGHT)

backspaceBtnTwice = Button(window, text="Doubl-Backspace", command=DBbackspace)
backspaceBtnTwice.pack(side=RIGHT)

# Timer label
timer_label = Label(window, text="0.00 s", font=("Arial", 30))
timer_label.pack()

# Timer buttons
start_btn = Button(
    window, text="Start", font="Arial", fg="green", bg="black", command=start
)
start_btn.pack()
stop_btn = Button(window, text="Stop", font="Arial", fg="red", bg="black", command=stop)
stop_btn.pack()
restart_btn = Button(
    window, text="Restart", font="Arial", fg="blue", bg="black", command=restart
)
restart_btn.pack()

window.mainloop()
