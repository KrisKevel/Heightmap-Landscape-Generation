#!/usr/bin/env python3

import tkinter as tk
import tkinter.filedialog
from tkinter.font import Font
from functools import partial


def create_button(frame, text, command, *args, **kwargs):
    button = tk.Button(frame, text=text, command=partial(command, *args), **kwargs)

    return button


def create_radio(frame):
    radioframe = tk.Frame(frame)
    var = tk.IntVar()
    r1 = tk.Radiobutton(radioframe, text="Üks", variable=var, value=1, command=lambda: print(var.get()))
    r1.pack()
    r2 = tk.Radiobutton(radioframe, text="Kaks", variable=var, value=2, command=lambda: print(var.get()))
    r2.pack()
    r3 = tk.Radiobutton(radioframe, text="Kolm", variable=var, value=3, command=lambda: print(var.get()))
    r3.pack()
    return radioframe


def create_dropdown(frame, default_value, options):
    pointer = tk.IntVar(frame)
    pointer.set(default_value)
    option_menu = tk.OptionMenu(frame, pointer, *options)

    return pointer, option_menu


def create_spinbox(frame, start, stop, step, **kwargs):
    spin = tk.Spinbox(frame, values=[i for i in range(start, stop+step, step)], **kwargs)

    return spin


def save(loc):
    loc = tk.filedialog.asksaveasfilename()
    print(loc)


def write_to_console(dd_val, skr):
    sone = "Menüüs on valitud number " + str(dd_val.get()) +\
           "\nKerijas on valitud number " + str(skr.get())
    print(sone)


if __name__ == '__main__':
    juur = tk.Tk()
    juur.title("Landscape generation parameters")
    frame1 = tk.Frame(juur)
    frame1.pack()

    button1 = create_button(frame1, "Quit", quit, fg="red")
    a = [1, 2, 3]
    # Elemendid lisatakse pakkimise järjekorras
    dropdown_value, dropdown = create_dropdown(frame1, 1, a)
    skroller = create_spinbox(frame1, 1, 10, 1, width=10, font=Font(family='Helvetica', size=12))
    button2 = create_button(frame1, "Hello", write_to_console, dropdown_value, skroller)
    button2.pack()
    dropdown.pack()

    raadio = create_radio(frame1)
    raadio.pack()

    skroller.pack()

    save_loc = None
    browse_button = create_button(frame1, "Browse...", save, save_loc)
    browse_button.pack()

    button1.pack()

    juur.minsize(500, 100)
    juur.mainloop()




