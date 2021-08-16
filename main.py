from PIL import Image, ImageDraw
from flask import send_file, Flask
import logging
import os
import cProfile, pstats

from lib.exporter import Exporter
from lib.stackDrawer import StackDrawer
from lib.mapCreator import MapCreator

app = Flask(__name__)


def tile(img):
    # Opens an image
    bg = Image.open("./img/" + "wave.jpg", "r")

    bg_w, bg_h = bg.size
    w, h = img.size

    for i in range(0, w, bg_w):
        for j in range(0, h, bg_h):
            img.paste(bg, (i, j))

    bg.close()
    return img


def createImage():

    # size of image
    scaleDPI = 4
    canvas = (3508 * scaleDPI, 2480 * scaleDPI)  # A4

    im = Image.new("RGBA", canvas, (255, 255, 255, 255))
    im = tile(im)

    foreground = Image.open("./img/" + "foreground.png", "r")
    # foreground = foreground.resize(canvas)

    stack = StackDrawer()
    stack.merge(MapCreator(canvas).toStack())

    im = stack.drawAll(im, scaleDPI)

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
    createImage()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("cumtime")
    stats.print_stats()


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
