from threading import Thread
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo


def loading_start(time):
    # root window
    root = tk.Tk()
    root.geometry('300x120')
    root.title('loading')
    root.after(time * 5000, root.destroy)

    # progressbar
    pb = ttk.Progressbar(
        root,
        orient='horizontal',
        mode='determinate',
        length=280
    )
    pb.start()
    # place the progressbar
    pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

    # label
    value_label = ttk.Label(root, text=f"Loading machines")
    value_label.grid(column=0, row=1, columnspan=2)
    root.mainloop()
    del root
