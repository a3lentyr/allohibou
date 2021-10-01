from PIL import Image, ImageDraw, ImageFilter, ImageOps
from flask import Flask, send_from_directory
import os
import cProfile, pstats
import pyximport
import json

pyximport.install()

from lib.exporter import Exporter
from lib.stackDrawer import StackDrawer
from lib.mapCreator import MapCreator
from pyx.landGenerator import LandGenerator
from lib.mountains import Mountains
from lib.missionCreator import MissionCreator

app = Flask(__name__)

BG_COLOR = (232, 205, 160, 255)


def createTerrain(canvas, scaleDPI):
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


def createImage():

    # size of image
    scaleDPI = 1
    canvas = (2480 * scaleDPI, 3508 * scaleDPI)  # A4
    layout = (2480 * scaleDPI * 2, 3508 * scaleDPI)  # A4

    imLayout = Image.new("RGBA", layout, BG_COLOR)
    # imLayout.paste(createTerrain(canvas, scaleDPI), (0, 0))
    imLayout.paste(
        MissionCreator(BG_COLOR).createMissionSheet(canvas, scaleDPI), (canvas[0], 0)
    )

    return imLayout


@app.route("/", defaults={"nameid": ""})
@app.route("/<nameid>")
def generate(nameid=""):
    im = createImage()
    return Exporter.export(im)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "img/rond-port.png",
        mimetype="image/vnd.microsoft.icon",
    )


def profile():

    profiler = cProfile.Profile()
    profiler.enable()

    im = createImage()
    # im.save("test.png")

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("cumtime")
    stats.print_stats()


if __name__ == "__main__":
    # profile()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
