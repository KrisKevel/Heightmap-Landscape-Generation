#!/usr/bin/env python3

import png
import random


def generate_heightmap(height=2017, width=2017, greyscale=True, bitdepth=16):
    # max value of pixel
    maxval = pow(2, 16) - 1
    image = [[0 for i in range(height)] for j in range(width)]
    highpoints = 1000
    dotsize = 12

    for i in range(highpoints):
        rndheight = random.randint(0 + dotsize, height - 1 - dotsize)
        rndwidth = random.randint(0 + dotsize, width - 1 - dotsize)
        rndint = random.randint(0, maxval)
        image[rndheight][rndwidth] = maxval
        for j in range(-dotsize, dotsize):
            for k in range(-dotsize, dotsize):
                image[rndheight+j][rndwidth+k] = maxval
        #print(image[rndheight][rndwidth])

    smoothing = 40

    for step in range(smoothing):
        for i in range(height):
            for j in range(width):
                image[i][j] = (int)(
                    (image[max(0, i - 1)][j] + image[i][max(0, j - 1)] + image[min(height - 1, i + 1)][j] +
                     image[i][min(width - 1, j + 1)] + image[i][j])/5)
        # print(image[rndheight][rndwidth])
        print("progress at ", step + 1, " out of ", smoothing)

    # print(len(image), "...", len(image[0]))

    with open("heightmap.png", "wb") as file:
        w = png.Writer(height=height, width=width, greyscale=greyscale, bitdepth=bitdepth)
        w.write(file, image)


generate_heightmap()
