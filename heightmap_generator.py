#!/usr/bin/env python3

# pip install pypng
import png
import random


def generate_heightmap(height=2017, width=2017, greyscale=True, bitdepth=16, algorithm="thousand needles",
                       thhighpoints=300, thdotsize=30, thsmoothing=40, save_loc="heightmap.png"):
    # max value of pixel
    maxval = pow(2, 16) - 1
    image = [[0 for i in range(height)] for j in range(width)]

    if algorithm == "thousand needles":
        image = thousandNeedles(image, height, width, thhighpoints, thdotsize, thsmoothing, maxval)

    with open(save_loc, "wb") as file:
        w = png.Writer(height=height, width=width, greyscale=greyscale, bitdepth=bitdepth)
        w.write(file, image)

def thousandNeedles(image, height, width, thhighpoints, thdotsize, thsmoothing, maxval):
    print("creating Thousand Needles Heightmap")

    for i in range(thhighpoints):
        rndheight = random.randint(0 + thdotsize, height - 1 - thdotsize)
        rndwidth = random.randint(0 + thdotsize, width - 1 - thdotsize)
        rndint = random.randint(0, maxval)
        image[rndheight][rndwidth] = maxval
        for j in range(-thdotsize, thdotsize):
            for k in range(-thdotsize, thdotsize):
                image[rndheight + j][rndwidth + k] = maxval
        # print(image[rndheight][rndwidth])

    for step in range(thsmoothing):
        for i in range(height):
            for j in range(width):
                image[i][j] = (int)(
                    (image[max(0, i - 1)][j] + image[i][max(0, j - 1)] + image[min(height - 1, i + 1)][j] +
                     image[i][min(width - 1, j + 1)] + image[i][j]) / 5)
        # print(image[rndheight][rndwidth])
        print("progress at ", step + 1, " out of ", thsmoothing)

    return image