#!/usr/bin/env python3

# pip install pypng
# pip install noise
# pip install numpy
import numpy as np
import png
import random
import math
from noise import pnoise2
from itertools import chain
from copy import deepcopy


def generate_heightmap(height=2017, width=2017, greyscale=True, bitdepth=16, algorithm="perlin",
                       thhighpoints=300, thdotsize=30, thsmoothing=40, save_loc="heightmap.png",
                       scale=400, octaves=30, lacunarity=2, persistence=0.2, seed=None):
    # max value of pixel
    maxval = pow(2, bitdepth) - 1
    image = [[0 for i in range(height)] for j in range(width)]

    if algorithm == "thousand needles":
        image = thousandNeedles(image, height, width, thhighpoints, thdotsize, thsmoothing, maxval)
    elif algorithm == "perlin":
        image = perlin(image, height, width, maxval, scale, octaves, persistence, lacunarity, seed)
    elif algorithm == "diamondsquare":
        image = diamond_square(height, bitdepth)

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


# Code was inspired by and based on the blog post https://engineeredjoy.com/blog/perlin-noise/
def perlin(image, height, width, maxval=pow(2, 16) - 1, scale=400, octaves=30, persistence=0.2, lacunarity=2,
           seed=None):
    if seed is None:
        seed = np.random.randint(0, 100)
        print("creating Perlin Noise heightmap, seed was {}".format(seed))
    image = [[pnoise2(i / scale,
                      j / scale,
                      octaves=octaves,
                      persistence=persistence,
                      lacunarity=lacunarity,
                      repeatx=1024,
                      repeaty=1024,
                      base=seed)
              for j in range(width)]
              for i in range(height)]

    image = [[abs(math.floor(image[i][j] * maxval))
              for j in range(len(image[0]))]#width
              for i in range(len(image))]   #height

    return image


def diamond(heightmap, magnitude, max_val):
    size = len(heightmap)
    new_heightmap = deepcopy(heightmap)
    for p1_y in range(size):
        for p1_x in range(size):
            if heightmap[p1_y][p1_x] != "_____":
                for p2_x in range(p1_x+2, size):
                    if heightmap[p1_y][p2_x] != "_____":
                        side = p2_x-p1_x
                        if p1_y + side <= size:
                            new_heightmap[int(p1_y+side/2)][int(p1_x+side/2)] = round(max(min(((heightmap[p1_y][p1_x]
                                                                                                + heightmap[p1_y][p2_x]
                                                                                                + heightmap[p1_y + side][p1_x]
                                                                                                + heightmap[p1_y + side][p2_x])
                                                                                               / 4
                                                                                               + random.uniform(0, magnitude)),
                                                                                              max_val), 0))
                        break
    return new_heightmap


def square(heightmap, magnitude, max_val):
    size = len(heightmap)
    new_heightmap = deepcopy(heightmap)
    for p1_y in range(size):
        for x in range(size):
            if heightmap[p1_y][x] != "_____":
                node_unhandled = True
                for p2_y in range(p1_y+2, size):
                    if heightmap[p2_y][x] != "_____":
                        radius = int((p2_y - p1_y) / 2)
                        underflow_x = x - radius
                        overflow_x = x + radius
                        if underflow_x < 0:
                            underflow_x -= 1
                        if overflow_x > size-1:
                            overflow_x -= size-1
                        new_heightmap[p1_y + radius][x] = round(max(min(((heightmap[p1_y][x]
                                                                          + heightmap[p2_y][x]
                                                                          + heightmap[p1_y+radius][underflow_x]
                                                                          + heightmap[p1_y+radius][overflow_x])
                                                                         / 4
                                                                        + random.uniform(0, magnitude)), max_val), 0))
                        node_unhandled = False
                        break
                if node_unhandled and p1_y < size-1:
                    radius = size-1 - p1_y
                    underflow_x = x - radius
                    if underflow_x < 0:
                        underflow_x -= 1
                    overflow_x = x + radius
                    if overflow_x > size - 1:
                        overflow_x -= size - 1
                    underflow_y = size-1
                    overflow_y = 0
                    new_val = round(max(min(((heightmap[p1_y][x] * 2
                                              + heightmap[overflow_y][underflow_x]
                                              + heightmap[overflow_y][overflow_x])
                                             / 4
                                             + random.uniform(-magnitude, magnitude)), max_val), 0))
                    new_heightmap[overflow_y][x] = new_val
                    new_heightmap[underflow_y][x] = new_val
    return new_heightmap


# Arbitrary positive integer size, seeds between 0 and 1
def diamond_square(size, bitdepth, seed_min=0.17, seed_max=0.83, magnitude=0.2, magnitude_reduction=0.6):
    max_val = 2**bitdepth - 1

    # Data preprocessing
    dimension = 1 + (1 << (size - 1).bit_length())
    seed1 = round(random.uniform(seed_min * max_val, seed_max * max_val))
    seed2 = round(random.uniform(seed_min * max_val, seed_max * max_val))
    seed3 = round(random.uniform(seed_min * max_val, seed_max * max_val))
    seed4 = round(random.uniform(seed_min * max_val, seed_max * max_val))

    # Heightmap generation
    heightmap = [["_____" for i in range(dimension)] for j in range(dimension)]
    heightmap[0][0] = seed1
    heightmap[0][dimension-1] = seed2
    heightmap[dimension-1][0] = seed3
    heightmap[dimension-1][dimension-1] = seed4

    state_is_diamond = True
    magnitude = magnitude * max_val
    while "_____" in chain(*heightmap):
        if state_is_diamond:
            heightmap = diamond(heightmap, magnitude, max_val)
        else:
            heightmap = square(heightmap, magnitude, max_val)
        state_is_diamond = not state_is_diamond
        magnitude = magnitude * magnitude_reduction

    # Padding removal
    heightmap = [i[0:size] for i in heightmap[0:size]]

    return heightmap
