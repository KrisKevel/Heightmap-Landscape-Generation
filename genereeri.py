#!/usr/bin/env python3

import random
import tkinter as tk
import tkinter.filedialog
from tkinter.messagebox import showerror
from tkinter.font import Font
from functools import partial
from heightmap_generator import generate_heightmap
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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


def create_dropdown(frame, default_value, options):
    pointer = tk.StringVar(frame)
    pointer.set(default_value)
    option_menu = tk.OptionMenu(frame, pointer, *options)

    return pointer, option_menu


def create_spinbox(frame, start, stop, step, **kwargs):
    spin = tk.Spinbox(frame, values=[i for i in range(start, stop+step, step)], **kwargs)

    return spin


def create_heightmap(width_src, height_src, file_loc, algorithm,
                     thhighpoints_src=None, thdotsize_src=None, thsmoothing_src=None,
                     scale_src=None, octaves_src=None, lacunarity_src=None, persistence_src=None, seed_src=None, secondstr_src=None,
                     seed_min_src=None, seed_max_src=None, magnitude_src=None, magnitude_reduction_src=None):
    if file_loc.get() != "":
        if algorithm == "thousand needles":
            generate_heightmap(height=height_src.get(), width=width_src.get(), algorithm="thousand needles",
                               save_loc=file_loc.get(),
                               thhighpoints=thhighpoints_src.get(),
                               thdotsize=thdotsize_src.get(),
                               thsmoothing=thsmoothing_src.get(),)
        elif algorithm == "perlin":
            generate_heightmap(height=height_src.get(), width=width_src.get(), algorithm="perlin",
                               save_loc=file_loc.get(),
                               scale=scale_src.get(),
                               octaves=octaves_src.get(),
                               lacunarity=lacunarity_src.get()/100,
                               persistence=persistence_src.get()/100,
                               seed=seed_src.get(),
                               secondstrength=secondstr_src.get())
        elif algorithm == "diamondsquare":
            generate_heightmap(height=height_src.get(), width=width_src.get(), algorithm=algorithm,
                               save_loc=file_loc.get(),
                               seed_min=seed_min_src.get()/100,
                               seed_max=seed_max_src.get()/100,
                               magnitude=magnitude_src.get()/100,
                               magnitude_reduction=magnitude_reduction_src.get()/100)

        img = mpimg.imread(file_loc.get())
        imgplot = plt.imshow(img, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
        plt.show()
    else:
        showerror("Error creating heightmap", "Please select output file name and location!")


def turn_page_2(frame_to_remove, img_width, img_height, algorithm_src, thousand_needles_data, perlin_data, ds_data):
    if algorithm_src.get() == "thousand needles":
        turn_tn_page(frame_to_remove, img_width, img_height, thousand_needles_data)
    elif algorithm_src.get() == "perlin":
        turn_perl_page(frame_to_remove, img_width, img_height, perlin_data)
    elif algorithm_src.get() == "diamond-square":
        turn_perl_page(frame_to_remove, img_width, img_height, ds_data)


def turn_tn_page(frame_to_remove, img_width, img_height, tn_data):
    tn_data["thhp_scroll"].config(values=[i for i in range(1, 1, img_width.get() * img_height.get()+1)])
    tn_data["thhp"].set(int(img_width.get() * img_height.get()/2))
    tn_data["thds_scroll"].config(values=[i for i in range(1, int(min(img_width.get()/2, img_height.get()/2))+1, 1)])
    tn_data["thds"].set(int(min(img_width.get()/2, img_height.get()/2)/2))
    turn_page(frame_to_remove, tn_data["page"])


def turn_perl_page(frame_to_remove, img_width, img_height, perlin_data):
    turn_page(frame_to_remove, perlin_data["page"])


def turn_ds_page(frame_to_remove, img_width, img_height, ds_data):
    turn_page(frame_to_remove, ds_data["page"])
    

def turn_page(frame_to_remove, frame_to_add):
    frame_to_remove.pack_forget()
    frame_to_add.pack()


def save(loc, button):
    savloc = tk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG-file", "*.png"),))
    button.config(fg="green", activeforeground="green", text=savloc.split("/")[-1])
    loc.set(savloc)


def create_thousand_needles_page(root):
    thousand_needles_page = tk.Frame(root)

    algorithm = "thousand needles"
    algorithm_label = tk.Label(thousand_needles_page, text="Algorithm: " + algorithm)
    algorithm_label.pack()

    parameter_grid_frame = tk.Frame(thousand_needles_page)
    parameter_grid_frame.pack()
    setup_buttons = tk.Frame(thousand_needles_page)
    setup_buttons.pack()
    button_frame2 = tk.Frame(thousand_needles_page)
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
                                  lambda: create_heightmap(width, height, save_loc, algorithm,
                                                           thhighpoints_src=thhighpoints,
                                                           thdotsize_src=thdotsize,
                                                           thsmoothing_src=thsmoothing))
    finish_button.pack(side=tk.LEFT)

    prev_page_button = create_button(button_frame2, "Back", lambda: turn_page(thousand_needles_page, page1))
    prev_page_button.pack(side=tk.LEFT)
    quit_button = create_button(button_frame2, "Quit", quit, fg="red")
    quit_button.pack(side=tk.RIGHT)

    data = {"page": thousand_needles_page,
            "thhp_scroll": thhighpoints_skroller, "thhp": thhighpoints,
            "thds_scroll": thdotsize_skroller, "thds": thdotsize}

    return data


def create_perlin_page(root):
    perlin_page = tk.Frame(root)

    algorithm = "perlin"
    algorithm_label = tk.Label(perlin_page, text="Algorithm: " + algorithm)
    algorithm_label.pack()

    parameter_grid_frame = tk.Frame(perlin_page)
    parameter_grid_frame.pack()
    setup_buttons = tk.Frame(perlin_page)
    setup_buttons.pack()
    button_frame2 = tk.Frame(perlin_page)
    button_frame2.pack()

    scale_label = tk.Label(parameter_grid_frame, text="Scale:")
    scale_label.grid(row=0, column=0, sticky='S', ipady=2)
    scale = tk.IntVar()
    scale_skroller = create_spinbox(parameter_grid_frame, 1, 5000, 1, width=10,
                                    font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                    justify=tk.RIGHT, textvariable=scale)
    scale_skroller.grid(row=0, column=1)
    scale.set(400)

    octaves_label = tk.Label(parameter_grid_frame, text="octaves:")
    octaves_label.grid(row=1, column=0, sticky='S', ipady=2)
    octaves = tk.IntVar()
    octaves_skroller = create_spinbox(parameter_grid_frame, 1, 10, 1, width=10,
                                      font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                      justify=tk.RIGHT, textvariable=octaves)
    octaves_skroller.grid(row=1, column=1)
    octaves.set(3)

    lacunarity_label = tk.Label(parameter_grid_frame, text="lacunarity:")
    lacunarity_label.grid(row=2, column=0, sticky='S', ipady=2)
    lacunarity = tk.IntVar()
    lacunarity_skroller = create_spinbox(parameter_grid_frame, 1, 100, 1, width=10,
                                         font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                         justify=tk.RIGHT, textvariable=lacunarity)
    lacunarity_skroller.grid(row=2, column=1)
    lacunarity.set(20)

    persistence_label = tk.Label(parameter_grid_frame, text="persistence:")
    persistence_label.grid(row=3, column=0, sticky='S', ipady=2)
    persistence = tk.IntVar()
    persistence_skroller = create_spinbox(parameter_grid_frame, 1, 100, 1, width=10,
                                          font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                          justify=tk.RIGHT, textvariable=persistence)
    persistence_skroller.grid(row=3, column=1)
    persistence.set(2)

    seed_label = tk.Label(parameter_grid_frame, text="seed:")
    seed_label.grid(row=4, column=0, sticky='S', ipady=2)
    seed = tk.IntVar()
    seed_skroller = create_spinbox(parameter_grid_frame, 0, 1000, 1, width=10,
                                   font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                   justify=tk.RIGHT, textvariable=seed)
    seed_skroller.grid(row=4, column=1)
    seed.set(random.randint(0, 1000))

    secondstr_label = tk.Label(parameter_grid_frame, text="secondstr:")
    secondstr_label.grid(row=5, column=0, sticky='S', ipady=2)
    secondstr = tk.IntVar()
    secondstr_skroller = create_spinbox(parameter_grid_frame, 0, 65535, 1, width=10,
                                        font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                        justify=tk.RIGHT, textvariable=secondstr)
    secondstr_skroller.grid(row=5, column=1)
    secondstr.set(60)

    save_loc = SaveLoc("")
    browse_button = create_button(setup_buttons, "Browse...", print, fg="red", activeforeground="red")
    browse_button.config(command=lambda: save(save_loc, browse_button))
    browse_button.pack(side=tk.LEFT)

    finish_button = create_button(setup_buttons, "Create image",
                                  lambda: create_heightmap(width, height, save_loc, algorithm,
                                                           scale_src=scale,
                                                           octaves_src=octaves,
                                                           lacunarity_src=lacunarity,
                                                           persistence_src=persistence,
                                                           seed_src=seed,
                                                           secondstr_src=secondstr))
    finish_button.pack(side=tk.LEFT)

    prev_page_button = create_button(button_frame2, "Back", lambda: turn_page(perlin_page, page1))
    prev_page_button.pack(side=tk.LEFT)
    quit_button = create_button(button_frame2, "Quit", quit, fg="red")
    quit_button.pack(side=tk.RIGHT)

    data = {"page": perlin_page}
    return data


def create_diamond_square_page(root):
    ds_page = tk.Frame(root)

    algorithm = "diamondsquare"
    algorithm_label = tk.Label(ds_page, text="Algorithm: " + algorithm)
    algorithm_label.pack()

    parameter_grid_frame = tk.Frame(ds_page)
    parameter_grid_frame.pack()
    setup_buttons = tk.Frame(ds_page)
    setup_buttons.pack()
    button_frame2 = tk.Frame(ds_page)
    button_frame2.pack()

    # minimum seed value
    seed_min_label = tk.Label(parameter_grid_frame, text="seed_min:")
    seed_min_label.grid(row=0, column=0, sticky='S', ipady=2)
    seed_min = tk.IntVar()
    seed_min_skroller = create_spinbox(parameter_grid_frame, 1, 100, 1, width=10,
                                       font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                       justify=tk.RIGHT, textvariable=seed_min)
    seed_min_skroller.grid(row=0, column=1)
    seed_min.set(17)

    # maximum seed value
    seed_max_label = tk.Label(parameter_grid_frame, text="seed_max:")
    seed_max_label.grid(row=1, column=0, sticky='S', ipady=2)
    seed_max = tk.IntVar()
    seed_max_skroller = create_spinbox(parameter_grid_frame, 1, 100, 1, width=10,
                                       font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                       justify=tk.RIGHT, textvariable=seed_max)
    seed_max_skroller.grid(row=1, column=1)
    seed_max.set(83)

    # magnitude of change
    magnitude_label = tk.Label(parameter_grid_frame, text="magnitude:")
    magnitude_label.grid(row=2, column=0, sticky='S', ipady=2)
    magnitude = tk.IntVar()
    magnitude_skroller = create_spinbox(parameter_grid_frame, 1, 100, 5, width=10,
                                        font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                        justify=tk.RIGHT, textvariable=magnitude)
    magnitude_skroller.grid(row=2, column=1)
    magnitude.set(20)

    # level of magnitude reduction
    magnitude_reduction_label = tk.Label(parameter_grid_frame, text="magnitude_reduction:")
    magnitude_reduction_label.grid(row=3, column=0, sticky='S', ipady=2)
    magnitude_reduction = tk.IntVar()
    magnitude_reduction_skroller = create_spinbox(parameter_grid_frame, 1, 100, 5, width=10,
                                                  font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                                  justify=tk.RIGHT, textvariable=magnitude_reduction)
    magnitude_reduction_skroller.grid(row=3, column=1)
    magnitude_reduction.set(60)

    save_loc = SaveLoc("")
    browse_button = create_button(setup_buttons, "Browse...", print, fg="red", activeforeground="red")
    browse_button.config(command=lambda: save(save_loc, browse_button))
    browse_button.pack(side=tk.LEFT)

    finish_button = create_button(setup_buttons, "Create image",
                                  lambda: create_heightmap(width, height, save_loc, algorithm,
                                                           seed_min_src=seed_min,
                                                           seed_max_src=seed_max,
                                                           magnitude_src=magnitude,
                                                           magnitude_reduction_src=magnitude_reduction))
    finish_button.pack(side=tk.LEFT)

    prev_page_button = create_button(button_frame2, "Back", lambda: turn_page(ds_page, page1))
    prev_page_button.pack(side=tk.LEFT)
    quit_button = create_button(button_frame2, "Quit", quit, fg="red")
    quit_button.pack(side=tk.RIGHT)

    data = {"page": ds_page}
    return data


if __name__ == '__main__':
    juur = tk.Tk()
    juur.title("Landscape generation parameters")

    # Image size configuration and algorithm selection page generation
    page1 = tk.Frame(juur)
    page1.pack()
    size_grid_frame = tk.Frame(page1)
    size_grid_frame.pack()
    button_frame1 = tk.Frame(page1)
    button_frame1.pack()

    width_label = tk.Label(size_grid_frame, text="Image width:")
    width_label.grid(row=0, column=0, sticky='W', ipady=2)
    width = tk.IntVar()
    width_skroller = create_spinbox(size_grid_frame, 10, 10000, 10, width=10, font=Font(family='Helvetica', size=12),
                                    repeatdelay=60, repeatinterval=40, justify=tk.RIGHT,
                                    textvariable=width)
    width_skroller.grid(row=0, column=1, sticky='E')
    width.set(2020)
    width_px_label = tk.Label(size_grid_frame, text="px")
    width_px_label.grid(row=0, column=2, sticky='S', ipady=2)

    height_label = tk.Label(size_grid_frame, text="Image height:")
    height_label.grid(row=1, column=0, sticky='W', ipady=2)
    height = tk.IntVar()
    height_skroller = create_spinbox(size_grid_frame, 10, 10000, 10, width=10, textvariable=height,
                                     font=Font(family='Helvetica', size=12), repeatdelay=60, repeatinterval=40,
                                     justify=tk.RIGHT)
    height_skroller.grid(row=1, column=1, sticky='E')
    height.set(2020)
    height_px_label = tk.Label(size_grid_frame, text="px")
    height_px_label.grid(row=1, column=2, sticky='S', ipady=2)

    algorithm_selector_label = tk.Label(size_grid_frame, text="Select algorithm:")
    algorithm_selector_label.grid(row=2, column=0, sticky="W")
    algorithm_pointer, algorithm_selector = create_dropdown(size_grid_frame, "perlin", ["thousand needles", "perlin", "diamond-square"])
    algorithm_selector.grid(row=2, column=1, sticky="S")

    tn_data = create_thousand_needles_page(juur)
    perl_data = create_perlin_page(juur)
    ds_data = create_diamond_square_page(juur)

    next_page_button = create_button(button_frame1, "Next", lambda: turn_page_2(page1, width, height,
                                                                                algorithm_pointer,
                                                                                tn_data, perl_data, ds_data))
    next_page_button.pack(side=tk.LEFT)
    quit_button = create_button(button_frame1, "Quit", quit, fg="red")
    quit_button.pack(side=tk.RIGHT)

    # Algorithm parameter and image save location configuration page setup

    # Minimum window size, loop
    juur.minsize(500, 100)
    juur.mainloop()
