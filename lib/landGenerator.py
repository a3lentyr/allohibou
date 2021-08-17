import random
import noise
import numpy as np
import math
from PIL import Image


class Color:

    # 0 -> 255

    r = 0.0
    g = 0.0
    b = 0.0
    a = 1.0

    def __init__(self, r=0.0, g=0.0, b=0.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = 1

    def GetTuple(self):
        return int(self.r), int(self.g), int(self.b)

    def SetColor(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def Copy(self, color):
        self.r = color.r
        self.g = color.g
        self.b = color.b

    def SetWhite(self):
        self.SetColor(1, 1, 1)

    def SetBlack(self):
        self.SetColor(0, 0, 0)

    def SetColorFromGrayscale(self, f=0.0):
        self.SetColor(f, f, f)


class GenerateMap:
    def __init__(
        self,
        size=(50, 50),
        color_range=10,
        color_perlin_scale=0.025,
        scale=3500,
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

        self.heightMap = np.zeros(self.mapSize)
        # self.colorMap = [[Color() for j in range(self.mapSize)] for i in range(self.mapSize)]

        self.randomColorRange = color_range
        self.colorPerlinScale = color_perlin_scale

        self.lightblue = [255, 0, 0]  # not used
        self.blue = [209, 167, 127]
        self.darkblue = [0, 0, 0]
        self.green = [232, 205, 160]
        self.darkgreen = [201, 174, 127]
        self.sandy = [172, 136, 78]
        self.beach = [238, 214, 175]
        self.snow = [104, 67, 51]
        self.mountain = [176, 138, 91]

        self.threshold = -0.01

    def generate_map(self, map_type=""):
        random_nr = random.randint(0, self.mapSize[0])
        # random_nr = 3
        for i in range(self.mapSize[0]):
            for j in range(self.mapSize[1]):

                new_i = i + self.y_starting_pos
                new_j = j + self.x_starting_pos

                self.heightMap[i][j] = noise.pnoise3(
                    new_i / self.scale,
                    new_j / self.scale,
                    random_nr,
                    octaves=self.octaves,
                    persistence=self.persistance,
                    lacunarity=self.lacunarity,
                    repeatx=10000000,
                    repeaty=10000000,
                    base=0,
                )
        print("monochrome map created")
        gradient = self.create_circular_gradient(self.heightMap)
        color_map = self.add_color(gradient)
        return color_map

    def add_color(self, world):
        color_world = np.zeros(world.shape + (3,))
        # print(color_world)
        for i in range(self.mapSize[0]):
            for j in range(self.mapSize[1]):
                if world[i][j] < self.threshold + 0.02:
                    color_world[i][j] = self.darkblue
                elif world[i][j] < self.threshold + 0.03:
                    color_world[i][j] = self.blue
                elif world[i][j] < self.threshold + 0.058:
                    color_world[i][j] = self.sandy
                elif world[i][j] < self.threshold + 0.1:
                    color_world[i][j] = self.beach
                elif world[i][j] < self.threshold + 0.25:
                    color_world[i][j] = self.green
                elif world[i][j] < self.threshold + 0.6:
                    color_world[i][j] = self.darkgreen
                elif world[i][j] < self.threshold + 0.7:
                    color_world[i][j] = self.mountain
                else:  # elif world[i][j] < self.threshold + 1.0:
                    color_world[i][j] = self.snow
        print("color map created")
        return color_world

    def create_circular_gradient(self, world):
        center_x, center_y = self.mapSize[1] // 2, self.mapSize[0] // 2
        circle_grad = np.zeros_like(world)

        for y in range(world.shape[0]):
            for x in range(world.shape[1]):
                distx = abs(x - center_x)
                disty = abs(y - center_y)
                dist = math.sqrt(distx * distx + disty * disty)
                circle_grad[y][x] = dist

        # get it between -1 and 1
        max_grad = np.max(circle_grad)
        circle_grad = circle_grad / max_grad
        circle_grad -= 0.5
        circle_grad *= 2.0
        circle_grad = -circle_grad

        # shrink gradient
        for y in range(world.shape[0]):
            for x in range(world.shape[1]):
                if circle_grad[y][x] > 0:
                    circle_grad[y][x] *= 20

        # get it between 0 and 1
        max_grad = np.max(circle_grad)
        circle_grad = circle_grad / max_grad
        grad_world = self.apply_gradient_noise(world, circle_grad)
        return grad_world

    def apply_gradient_noise(self, world, c_grad):
        world_noise = np.zeros_like(world)

        for i in range(self.mapSize[0]):
            for j in range(self.mapSize[1]):
                world_noise[i][j] = world[i][j] * c_grad[i][j]
                if world_noise[i][j] > 0:
                    world_noise[i][j] *= 20

        # get it between 0 and 1
        max_grad = np.max(world_noise)
        world_noise = world_noise / max_grad
        return world_noise


class LandGenerator:
    def generate(self, canvas):
        map_data = GenerateMap(canvas, x_starting_pos=0, y_starting_pos=0)
        mono_map = map_data.generate_map("island")
        im = Image.fromarray(np.uint8(mono_map)).convert("RGB")

        mask = np.zeros((map_data.mapSize[0], map_data.mapSize[1]))

        for i in range(map_data.mapSize[0]):
            for j in range(map_data.mapSize[1]):
                if (mono_map[i][j] == map_data.darkblue).all():
                    mask[i][j] = 1

        watermask = Image.fromarray((mask * 255).astype("uint8"), mode="L")
        return im, watermask
