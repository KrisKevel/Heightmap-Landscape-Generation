#!/usr/bin/env python3

import tkinter as tk
import tkinter.filedialog
from tkinter.messagebox import showerror, showinfo
from tkinter.font import Font
from functools import partial
from heightmap_generator import generate_heightmap


class SaveLoc:
    def __init__(self, save_location):
        self.save_loc = save_location

    def set(self, save_location):
        self.save_loc = save_location

    def get(self):
        return self.save_loc


def create_button(frame, text, command, *args, **kwargs):
    button = tk.Button(frame, text=text, command=partial(command, *args), **kwargs)

    return button


def create_radio(frame):
    radioframe = tk.Frame(frame)
    var = tk.IntVar()
    r1 = tk.Radiobutton(radioframe, text="Üks", variable=var, value=1, command=lambda: one(var))
    r1.pack()
    r2 = tk.Radiobutton(radioframe, text="Kaks", variable=var, value=2, command=lambda: two(var))
    r2.pack()
    r3 = tk.Radiobutton(radioframe, text="Kolm", variable=var, value=3, command=lambda: three(var))
    r3.pack()
    return radioframe

def one(var):
    print(var.get())

def two(var):
    print(var.get())

def three(var):
    print(var.get())

def create_dropdown(frame, default_value, options):
    pointer = tk.IntVar(frame)
    pointer.set(default_value)
    option_menu = tk.OptionMenu(frame, pointer, *options)

    return pointer, option_menu


def create_spinbox(frame, start, stop, step, **kwargs):
    spin = tk.Spinbox(frame, values=[i for i in range(start, stop+step, step)], **kwargs)

    return spin


def create_heightmap(width_source, height_source, thhighpoints_source, thdotsize_source, thsmoothing_source, file_loc):
    if file_loc.get() != "":
        dialog_string = "width: " + str(width_source.get()) + "\nheight: " + str(height_source.get())\
                        + "\nthhighpoints: " + str(thhighpoints_source.get()) + "\nthdotsize: "\
                        + str(thdotsize_source.get()) + "\nthsmoothing: " + str(thsmoothing_source.get())\
                        + "\nsave location: " + file_loc.get()
        showinfo("Creating heightmap", dialog_string)
        generate_heightmap(height=height_source.get(), width=width_source.get(), thhighpoints=thhighpoints_source.get(),
                           thdotsize=thdotsize_source.get(), thsmoothing=thsmoothing_source.get(),
                           save_loc=file_loc.get())
    else:
        showerror("Error creating heightmap", "Please select output file name and location!")


def turn_page_2(frame_to_remove, page_2_frame, width, height, thhighpoints_source, thhighpoints_var, thdotsize_source,
                thdotsize_var):
    thhighpoints_source.config(values=[i for i in range(1, 1, width.get() * height.get()+1)])
    thhighpoints_var.set(int(width.get() * height.get()/2))
    thdotsize_source.config(values=[i for i in range(1, int(min(width.get()/2, height.get()/2))+1, 1)])
    thdotsize_var.set(int(min(width.get()/2, height.get()/2)/2))
    turn_page(frame_to_remove, page_2_frame)


def turn_page(frame_to_remove, frame_to_add):
    frame_to_remove.pack_forget()
    frame_to_add.pack()


def save(loc, button):
    savloc = tk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG-file", "*.png"),))
    button.config(fg="green", activeforeground="green", text=savloc.split("/")[-1])
    loc.set(savloc)


if __name__ == '__main__':
    juur = tk.Tk()
    juur.title("Landscape generation parameters")

    # Image size configuration (and, one day, algorithm selection) page generation
    page1 = tk.Frame(juur)
    page1.pack()
    size_grid_frame = tk.Frame(page1)
    size_grid_frame.pack()
    button_frame1 = tk.Frame(page1)
    button_frame1.pack()

    width_label = tk.Label(size_grid_frame, text="Image width:")
    width_label.grid(row=0, column=0, sticky='SE', ipady=2)
    width = tk.IntVar()
    width_skroller = create_spinbox(size_grid_frame, 10, 10000, 10, width=10, font=Font(family='Helvetica', size=12),
                                    repeatdelay=60, repeatinterval=40, justify=tk.RIGHT,
                                    textvariable=width)
    width_skroller.grid(row=0, column=1)
    width.set(2020)
    width_px_label = tk.Label(size_grid_frame, text="px")
    width_px_label.grid(row=0, column=2, sticky='S', ipady=2)

    height_label = tk.Label(size_grid_frame, text="Image height:")
    height_label.grid(row=1, column=0, sticky='S', ipady=2)
    height = tk.IntVar()
    height_skroller = create_spinbox(size_grid_frame, 10, 10000, 10, width=10, textvariable=height,
                                     font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                     justify=tk.RIGHT)
    height_skroller.grid(row=1, column=1)
    height.set(2020)
    height_px_label = tk.Label(size_grid_frame, text="px")
    height_px_label.grid(row=1, column=2, sticky='S', ipady=2)

    next_page_button = create_button(button_frame1, "Next", lambda: turn_page_2(page1, page2, width,
                                                                                height, thhighpoints_skroller,
                                                                                thhighpoints,
                                                                                thdotsize_skroller, thdotsize))
    next_page_button.pack(side=tk.LEFT)
    quit_button = create_button(button_frame1, "Quit", quit, fg="red")
    quit_button.pack(side=tk.RIGHT)

    # Algorithm parameter and image save location configuration page setup
    page2 = tk.Frame(juur)

    algorithm = "thousand needles"
    algorithm_label = tk.Label(page2, text="Algorithm: " + algorithm)
    algorithm_label.pack()

    parameter_grid_frame = tk.Frame(page2)
    parameter_grid_frame.pack()
    setup_buttons = tk.Frame(page2)
    setup_buttons.pack()
    button_frame2 = tk.Frame(page2)
    button_frame2.pack()

    # thhighpoints
    thhighpoints_label = tk.Label(parameter_grid_frame, text="thhighpoints:")
    thhighpoints_label.grid(row=0, column=0, sticky='S', ipady=2)
    thhighpoints = tk.IntVar()
    thhighpoints_skroller = create_spinbox(parameter_grid_frame, 10, 10000, 10, width=10,
                                           font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                           justify=tk.RIGHT, textvariable=thhighpoints)
    thhighpoints_skroller.grid(row=0, column=1)
    thhighpoints.set(300)

    # thdotsize
    thdotsize_label = tk.Label(parameter_grid_frame, text="thdotsize:")
    thdotsize_label.grid(row=1, column=0, sticky='S', ipady=2)
    thdotsize = tk.IntVar()
    thdotsize_skroller = create_spinbox(parameter_grid_frame, 10, 10000, 10, width=10,
                                        font=Font(family='Helvetica', size=12), repeatdelay=30, repeatinterval=20,
                                        justify=tk.RIGHT, textvariable=thdotsize)
    thdotsize_skroller.grid(row=1, column=1)
    thhighpoints.set(30)

    # thsmoothing
    thsmoothing_label = tk.Label(parameter_grid_frame, text="thsmoothing:")
    thsmoothing_label.grid(row=2, column=0, sticky='S', ipady=2)
    thsmoothing = tk.IntVar()
    thsmoothing_skroller = create_spinbox(parameter_grid_frame, 10, 5000, 10, width=10,
                                          font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                          justify=tk.RIGHT, textvariable=thsmoothing)
    thsmoothing_skroller.grid(row=2, column=1)
    thsmoothing.set(40)

    save_loc = SaveLoc("")
    browse_button = create_button(setup_buttons, "Browse...", print, fg="red", activeforeground="red")
    browse_button.config(command=lambda: save(save_loc, browse_button))
    browse_button.pack(side=tk.LEFT)

    finish_button = create_button(setup_buttons, "Create image",
                                  lambda: create_heightmap(width, height, thhighpoints,
                                                           thdotsize, thsmoothing, save_loc))
    finish_button.pack(side=tk.LEFT)

    prev_page_button = create_button(button_frame2, "Back", lambda: turn_page(page2, page1))
    prev_page_button.pack(side=tk.LEFT)
    quit_button = create_button(button_frame2, "Quit", quit)
    quit_button.pack(side=tk.RIGHT)

    # Minimum window size, loop
    juur.minsize(500, 100)
    juur.mainloop()




