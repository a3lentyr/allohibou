import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random

from lib.util import pasteCenter


def createMarketMission(imMission, canvas, offset, scaleDPI, bonus_list, short):

    market = ["rond-village-2", "rond-village-1", "rond-village-3"]

    column_list = [2, 2, 1]
    if short:
        column_list = [1.5, 1.5, 1]
    column_offset = 0

    for m, m_name in enumerate(market):
        x_coord = int(
            floor(
                (canvas[0] * (column_offset + 1)) // 6
                + (32 * column_offset + 128 + 64) * scaleDPI
            )
        )

        if column_list[m] == 2:
            pasteCenter(
                imMission,
                m_name,
                x_coord,
                (128 + 64) * scaleDPI,
                offset,
                scaleDPI,
                1.4,
            )
        else:
            pasteCenter(
                imMission,
                m_name,
                x_coord - 128 * scaleDPI,
                (128 + 64) * scaleDPI,
                offset,
                scaleDPI,
                1.4,
            )

        for x in range(0, 4):
            y_coord = (canvas[1] * (x + 2)) // 20 + 64 * scaleDPI

            pasteCenter(
                imMission,
                "case",
                x_coord - 128 * scaleDPI,
                y_coord,
                offset,
                scaleDPI,
                1,
            )

            if column_list[m] == 2:
                pasteCenter(
                    imMission,
                    "case",
                    x_coord + 128 * scaleDPI,
                    y_coord,
                    offset,
                    scaleDPI,
                    1,
                )

            if m == 0:
                continue

            bonus = bonus_list.pop()
            pasteCenter(
                imMission,
                bonus,
                int(
                    floor(
                        (canvas[0] * column_offset) // 6
                        + 64 * (column_offset - 1) // 2 * scaleDPI
                        + (128 + 64) * scaleDPI
                    )
                ),
                y_coord,
                offset,
                scaleDPI,
                0.6,
            )
        column_offset += column_list[m]
