import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random

from lib.util import pasteCenter


def createCaveMission(imMission, canvas, offset, scaleDPI, bonus_list, short):

    column_num = 8
    if short:
        column_num = 6

    top = (128 + 64) * scaleDPI
    bottom = (canvas[1]) // 3 - (128 + 64) * scaleDPI

    y_coord_list = [
        top,
        top + (bottom - top) // 3,
        top + 2 * (bottom - top) // 3,
        bottom,
    ]
    x_offset = canvas[0] // 12 + canvas[0] // 10

    for ym, y_coord in enumerate(y_coord_list):

        for x in range(column_num):

            x_coord = (canvas[0] * (x)) // 10 + x_offset

            if ym == 0 and x == 0:
                pasteCenter(
                    imMission,
                    "rond-cave",
                    x_coord,
                    y_coord,
                    offset,
                    scaleDPI,
                    1,
                )
            else:
                if random.randint(0, 3) == 0:
                    pasteCenter(
                        imMission,
                        "diamond",
                        x_coord,
                        y_coord,
                        offset,
                        scaleDPI,
                        0.6,
                    )
                else:
                    bonus = bonus_list.pop()
                    pasteCenter(
                        imMission,
                        bonus,
                        x_coord,
                        y_coord,
                        offset,
                        scaleDPI,
                        0.6,
                    )
            if random.randint(0, 4) == 0 and x > 0:
                pasteCenter(
                    imMission,
                    "lineh",
                    x_coord - (canvas[0]) // 20,
                    y_coord,
                    offset,
                    scaleDPI,
                    1,
                )

            if random.randint(0, 4) == 0 and ym > 0:
                pasteCenter(
                    imMission,
                    "linev",
                    x_coord,
                    y_coord - (bottom - top) // 6,
                    offset,
                    scaleDPI,
                    1,
                )
