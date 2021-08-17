from PIL import Image, ImageDraw, ImageFilter, ImageOps
from flask import Flask
import os
import random
import cProfile, pstats

from lib.exporter import Exporter
from lib.stackDrawer import StackDrawer
from lib.mapCreator import MapCreator
from lib.landGenerator import LandGenerator
from lib.mountains import Mountains

app = Flask(__name__)

BG_COLOR = (232, 205, 160, 255)


def tile(original, name):
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


def drawLand(img):

    w, h = img.size

    generator = LandGenerator()
    land, mask, coastalPlaces, mountainsPlaces = generator.generate(
        (img.size[1], img.size[0])
    )
    img.paste(land, (0, 0))

    # filling with water
    fullwater = tile(img, "wave.jpg")

    img.paste(fullwater, (0, 0), mask)
    fullwater.close()

    img.save("test.png")
    return img, coastalPlaces, mountainsPlaces


def createImage():

    # size of image
    scaleDPI = 1
    canvas = (3508 * scaleDPI, 2480 * scaleDPI)  # A4

    # creating terrain

    im = Image.new("RGBA", canvas, BG_COLOR)

    im, coastalPlaces, mountainsPlaces = drawLand(im)

    # find places
    stack = StackDrawer()
    stack.merge(MapCreator(canvas, coastalPlaces, mountainsPlaces).toStack())

    # Drawing

    im = stack.drawAll(im, scaleDPI)

    foreground = Image.open("./img/" + "foreground.png", "r")
    im.paste(foreground, (0, 0), foreground)

    foreground.close()

    return im


@app.route("/", defaults={"nameid": ""})
@app.route("/<nameid>")
def generate(nameid=""):
    im = createImage()
    return Exporter.export(im)


def profile():

    profiler = cProfile.Profile()
    profiler.enable()

    im = createImage()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("cumtime")
    stats.print_stats()


if __name__ == "__main__":
    im = createImage()
    im.save("test.png")
    port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)
