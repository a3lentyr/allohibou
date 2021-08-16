from PIL import Image, ImageDraw
from flask import send_file, Flask
import logging
import os

from lib.exporter import Exporter
from lib.stackDrawer import StackDrawer
from lib.mapCreator import MapCreator

app = Flask(__name__)


@app.route("/", defaults={"nameid": ""})
@app.route("/<nameid>")
def generate(nameid=""):
    # size of image
    scaleDPI = 4
    canvas = (3508 * scaleDPI, 2480 * scaleDPI)  # A4

    im = Image.new("RGBA", canvas, (255, 255, 255, 255))
    background = Image.open("./img/" + "background.jpg", "r")
    background = background.resize(canvas)
    im.paste(background, (0, 0))

    stack = StackDrawer()
    stack.merge(MapCreator(canvas).toStack())

    im = stack.drawAll(im, scaleDPI)

    return Exporter.export(im)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
