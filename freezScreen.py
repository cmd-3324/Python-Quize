import tkinter as tk
import threading
import time
import ctypes
import sys


# Function to block input using Windows API
def block_input():
    ctypes.windll.user32.BlockInput(True)


def unblock_input():
    ctypes.windll.user32.BlockInput(False)


# Function to close the window and unblock input
def close_window(root):
    unblock_input()
    root.destroy()


# Main function to create the fullscreen transparent window
def freeze_screen():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.3)  # Semi-transparent
    root.configure(bg="black")

    # Block input in a separate thread
    threading.Thread(target=block_input).start()

    # Schedule window to close after 60 seconds
    threading.Timer(10, lambda: close_window(root)).start()

    root.mainloop()


if __name__ == "__main__":
    freeze_screen()
