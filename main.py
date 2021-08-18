from PIL import Image, ImageDraw, ImageFilter, ImageOps
from flask import Flask
import os
import random
import cProfile, pstats
import pyximport

pyximport.install()

from lib.exporter import Exporter
from lib.stackDrawer import StackDrawer
from lib.mapCreator import MapCreator
from lib.landGenerator import LandGenerator
from lib.mountains import Mountains

app = Flask(__name__)

BG_COLOR = (232, 205, 160, 255)


def createImage():

    # size of image
    scaleDPI = 1
    canvas = (3508 * scaleDPI, 2480 * scaleDPI)  # A4

    # creating terrain

    im = Image.new("RGBA", canvas, BG_COLOR)

    generator = LandGenerator()
    im, coastalPlaces, mountainsPlaces = generator.drawLand(im, BG_COLOR)

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
    im.save("test.png")

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("cumtime")
    stats.print_stats()


if __name__ == "__main__":
    # profile()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
