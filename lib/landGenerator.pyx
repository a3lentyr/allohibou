import random
import noise
import numpy as np
import math
import time
from PIL import Image
import logging
logging.basicConfig(level=logging.INFO)

import multiprocessing
import functools
from itertools import product

cimport numpy
cimport cython
from cython.parallel import prange


@cython.boundscheck(False)
@cython.wraparound(False)
cdef double apply_gradient_noise(
    int i,
    int j,
    int center_x,
    int center_y,
    double random_nr,
    double max_grad
):
    cdef double noiseValue, distx, disty, dist, value, returnValue

    cdef int x_starting_pos = 0
    cdef int y_starting_pos = 0
    cdef double scale = 350*4

    noiseValue = noise.pnoise3(
        (i + y_starting_pos) / scale,
        (j + x_starting_pos) / scale,
        random_nr,
        octaves=6,
        persistence=0.6,
        lacunarity=2.0,
        repeatx=10000000,
        repeaty=10000000,
        base=0,
    )

    distx = abs(j - center_x)
    disty = abs(i - center_y)
    dist = math.sqrt(distx * distx + disty * disty)

    value = -(dist / max_grad - 0.5) * 2.0 / 20
    if value > 0:
        value *= 20

    returnValue = noiseValue * value / 20
    if returnValue > 0:
        returnValue *= 20

    return returnValue


class GenerateMap:
    def __init__(
        self,
        size=(50, 50),
        color_range=10,
        color_perlin_scale=0.025,
        scale=350 * 4,
        x_starting_pos=0,
        y_starting_pos=0,
    ):
        self.scale = scale

        self.x_starting_pos = x_starting_pos
        self.y_starting_pos = y_starting_pos

        self.mapSize = size  # size in pixels
        self.mapCenter = (self.mapSize[0] / 2, self.mapSize[1] / 2)

        self.randomColorRange = color_range
        self.colorPerlinScale = color_perlin_scale

        self.blue = [209, 167, 127]
        self.green = [104, 67, 51]
        self.land = [232, 205, 160]

        self.threshold = -0.01

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def generate_map(self):

        cdef int random_nr, i, j, center_x, center_y, width, height
        cdef double max_grad, value
        cdef numpy.ndarray[numpy.double_t, ndim=2]  gradient

        width = self.mapSize[0]
        height = self.mapSize[1]

        random_nr = random.randint(0, width)

        max_grad = (
            math.sqrt(
                width * width + height* height
            )
            / 2
        )

        gradient = np.zeros((width, height), dtype=np.double)

        center_x = height // 2
        center_y = width // 2

        for i in range(width):
            for j in range(height):
                value = apply_gradient_noise( i,j,center_x,center_y,random_nr,max_grad)
                gradient[i][j] = value


        # get it between 0 and 1
        max_grad = np.max(gradient)
        gradient = gradient / max_grad

        print("monochrome map created")


        color_map, mask, coastalPlaces, mountainsPlaces = self.add_color(gradient)


        return color_map, mask, coastalPlaces, mountainsPlaces

    def add_color(self, world):

        color_world = np.zeros(world.shape + (3,))

        mask = np.zeros((self.mapSize[0], self.mapSize[1]))
        coastalPlaces = []
        mountainsPlaces = []

        # print(color_world)
        for i in range(self.mapSize[0]):
            for j in range(self.mapSize[1]):
                if world[i][j] < self.threshold + 0.02:
                    mask[i][j] = 1
                elif world[i][j] < self.threshold + 0.03:
                    color_world[i][j] = self.blue
                    coastalPlaces.append((j, i))
                elif world[i][j] < self.threshold + 0.05:
                    color_world[i][j] = self.green
                elif world[i][j] > self.threshold + 0.5:
                    mountainsPlaces.append((j, i))
                    color_world[i][j] = self.land
                else:
                    color_world[i][j] = self.land

        print("color map created")
        return color_world, mask, coastalPlaces, mountainsPlaces


class LandGenerator:
    def generate(self, canvas):
        map_data = GenerateMap(canvas, x_starting_pos=0, y_starting_pos=0)

        mono_map, mask, coastalPlaces, mountainsPlaces = map_data.generate_map()
        im = Image.fromarray(np.uint8(mono_map)).convert("RGB")
        watermask = Image.fromarray((mask * 255).astype("uint8"), mode="L")
        return im, watermask, coastalPlaces, mountainsPlaces

    def tile(self, original, name, BG_COLOR):
        img = Image.new("RGBA", original.size, BG_COLOR)

        # Opens an image
        bg = Image.open("./img/" + name, "r")

        bg_w, bg_h = bg.size
        w, h = img.size

        for i in range(0, w, bg_w):
            for j in range(0, h, bg_h):
                img.paste(bg, (i, j))

        bg.close()
        return img

    def drawLand(self, img, BG_COLOR):


        w, h = img.size

        land, mask, coastalPlaces, mountainsPlaces = self.generate(
            (img.size[1], img.size[0])
        )
        img.paste(land, (0, 0))

        # filling with water
        fullwater = self.tile(img, "wave.jpg", BG_COLOR)

        img.paste(fullwater, (0, 0), mask)
        fullwater.close()


        return img, coastalPlaces, mountainsPlaces
