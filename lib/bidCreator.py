import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random

from lib.util import pasteCenter


def createBidMission(imMission, canvas, offset, scaleDPI, bonus_list, short):

    market = ["", "rond-village-4", "rond-village-1", "rond-village-3"]

    column_num = 12
    if short:
        column_num = 9

    y_coord_list = [
        (128 + 64) * scaleDPI,
        (canvas[1]) // 6,
        (canvas[1] * 2) // 9,
        (canvas[1]) // 3 - (128 + 64) * scaleDPI,
    ]
    x_offset = canvas[0] // 17 + canvas[0] // 15

    random_distrib = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 6, 1, 1]

    for ym, m_name in enumerate(market):

        y_coord = y_coord_list[ym]
        if ym > 0:
            pasteCenter(
                imMission,
                m_name,
                x_offset,
                y_coord,
                offset,
                scaleDPI,
                1,
            )

        for x in range(column_num):

            x_coord = (canvas[0] * (x + 1)) // 15 + x_offset

            random_case = "invest" + str(random.choice(random_distrib[: -(ym + 1)]))

            scale = 1
            if ym == 0:
                random_case = bonus_list.pop()
                scale = 0.6

            pasteCenter(
                imMission,
                random_case,
                x_coord,
                y_coord,
                offset,
                scaleDPI,
                scale,
            )
