from io import BytesIO

from flask import send_file
from PIL import Image, ImageDraw


class Exporter:
    @staticmethod
    def export(im, scale=5, quality=100):

        # save image
        im = im.convert("RGB")

        img_io = BytesIO()
        im.save(img_io, "JPEG", quality=quality)
        im.close()
        img_io.seek(0)
        return send_file(img_io, mimetype="image/jpeg")
