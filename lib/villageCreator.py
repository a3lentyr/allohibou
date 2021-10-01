import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random

from lib.util import pasteCenter


def createVillageMission(imMission, canvas, offset, scaleDPI, bonus_list, short):

    number_width = 6
    if short:
        number_width = 4

    for x in range(0, number_width):
        x_coord = (canvas[0] * (x + 1)) // 7

        y_coord_list = [
            (128 + 64) * scaleDPI,
            (canvas[1]) // 6,
            (canvas[1]) // 3 - (128 + 64) * scaleDPI,
        ]
        for index_y, y_coord in enumerate(y_coord_list):
            if x != 0:
                if index_y != 1:
                    pasteCenter(
                        imMission,
                        "right-arrow",
                        x_coord,
                        y_coord,
                        offset,
                        scaleDPI,
                        0.5,
                    )
                else:
                    pasteCenter(
                        imMission,
                        "left-arrow",
                        x_coord,
                        y_coord,
                        offset,
                        scaleDPI,
                        0.5,
                    )

            bonus = bonus_list.pop()
            pasteCenter(
                imMission,
                bonus,
                x_coord + canvas[0] // 14,
                y_coord,
                offset,
                scaleDPI,
                0.6,
            )

    pasteCenter(
        imMission,
        "down-arrow",
        int(floor(canvas[0] * (number_width + 0.5))) // 7,
        canvas[1] // 9,
        offset,
        scaleDPI,
        0.5,
    )

    pasteCenter(
        imMission,
        "down-arrow",
        int(floor(canvas[0] * 1.5)) // 7,
        (canvas[1] * 2) // 9,
        offset,
        scaleDPI,
        0.5,
    )
