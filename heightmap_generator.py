#!/usr/bin/env python3

# pip install pypng
# pip install noise
# pip install numpy
import numpy as np
import png
import random
import math
from noise import pnoise2


def generate_heightmap(height=2017, width=2017, greyscale=True, bitdepth=16, algorithm="thousand needles",
                       thhighpoints=300, thdotsize=30, thsmoothing=40, save_loc="heightmap.png"):
    # max value of pixel
    maxval = pow(2, 16) - 1
    image = [[0 for i in range(height)] for j in range(width)]

    if algorithm == "thousand needles":
        image = thousandNeedles(image, height, width, thhighpoints, thdotsize, thsmoothing, maxval)
    elif algorithm == "perlin":
        image = perlin(image, height, width, maxval)

    with open(save_loc, "wb") as file:
        w = png.Writer(height=height, width=width, greyscale=greyscale, bitdepth=bitdepth)
        w.write(file, image)


def thousandNeedles(image, height, width, thhighpoints=300, thdotsize=30, thsmoothing=40, maxval=pow(2, 16) - 1):
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

#Code was inspired by and based on the blog post https://engineeredjoy.com/blog/perlin-noise/
def perlin(image, height, width, maxval=pow(2, 16) - 1, scale=400, octaves=30, persistence=0.2, lacunarity=2,
           seed=None):
    if not seed:
        seed = np.random.randint(0, 100)
        print("creating Perlin Noise heightmap, seed was {}".format(seed))
    for i in range(height):
        for j in range(width):
            image[i][j] = pnoise2(i / scale,
                                  j / scale,
                                  octaves=octaves,
                                  persistence=persistence,
                                  lacunarity=lacunarity,
                                  repeatx=1024,
                                  repeaty=1024,
                                  base=seed)
    max_arr = np.max(image)
    min_arr = np.min(image)

    for i in range(len(image)):
        for j in range(len(image[0])):
            image[i][j] = abs(math.floor(image[i][j] * maxval))
    return image
