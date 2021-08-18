import random
import noise
import numpy as np
import math
import time
from PIL import Image

import multiprocessing
import functools
from itertools import product

cimport numpy


def apply_gradient_noise(
    i,
    j,
    mapSize,
    x_starting_pos,
    y_starting_pos,
    scale,
    random_nr,
    octaves,
    persistance,
    lacunarity,
    max_grad,
):

    center_x, center_y = mapSize[1] // 2, mapSize[0] // 2

    noiseValue = noise.pnoise3(
        (i + y_starting_pos) / scale,
        (j + x_starting_pos) / scale,
        random_nr,
        octaves=octaves,
        persistence=persistance,
        lacunarity=lacunarity,
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
        octaves=6,
        persistance=0.6,
        lacunarity=2.0,
        x_starting_pos=0,
        y_starting_pos=0,
    ):
        self.scale = scale
        self.octaves = octaves
        self.persistance = persistance
        self.lacunarity = lacunarity

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

    def generate_map(self):
        random_nr = random.randint(0, self.mapSize[0])

        max_grad = (
            math.sqrt(
                self.mapSize[0] * self.mapSize[0] + self.mapSize[1] * self.mapSize[1]
            )
            / 2
        )

        partialapply_gradient_noise = functools.partial(
            apply_gradient_noise,
            mapSize=self.mapSize,
            x_starting_pos=self.x_starting_pos,
            y_starting_pos=self.y_starting_pos,
            scale=self.scale,
            random_nr=random_nr,
            octaves=self.octaves,
            persistance=self.persistance,
            lacunarity=self.lacunarity,
            max_grad=max_grad,
        )
        coord = [(i, j) for i in range(self.mapSize[0]) for j in range(self.mapSize[1])]

        with multiprocessing.Pool(processes=16) as pool:
            gradient = np.reshape(
                pool.starmap(partialapply_gradient_noise, coord), self.mapSize
            )

        # get it between 0 and 1
        max_grad = np.max(gradient)
        gradient = gradient / max_grad

        print("monochrome map created")
        im = Image.fromarray(np.uint8(gradient)).convert("RGB")

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

        t1 = time.time()

        w, h = img.size

        land, mask, coastalPlaces, mountainsPlaces = self.generate(
            (img.size[1], img.size[0])
        )
        img.paste(land, (0, 0))

        # filling with water
        fullwater = self.tile(img, "wave.jpg", BG_COLOR)

        img.paste(fullwater, (0, 0), mask)
        fullwater.close()

        t2 = time.time()
        t = t2 - t1
        print("%.20f" % t)

        return img, coastalPlaces, mountainsPlaces
