import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random

from lib.util import pasteCenter


def createLibraryMission(imMission, canvas, offset, scaleDPI, bonus_list, short):
    # Add bank
    base_x = (750 + 256 + 128 + 80) * scaleDPI
    base_y = (500 + 64) * scaleDPI
    num_bonus = 6
    x_offset = 0.5

    if short:

        pasteCenter(
            imMission,
            "libraryshort",
            base_x,
            base_y,
            offset,
            scaleDPI,
            1,
        )
    else:

        base_x = (750 + 256 + 128 + 167) * scaleDPI
        base_y = (500 + 64) * scaleDPI
        num_bonus = 7
        x_offset = 0

        pasteCenter(
            imMission,
            "library",
            base_x,
            base_y,
            offset,
            scaleDPI,
            1,
        )

    for y in range(2):
        y_pos = base_y - (500 - 80) * scaleDPI + (860) * y * scaleDPI

        for x in range(num_bonus):
            x_range_offset = 0
            if x == 3:
                continue
            if x > 3:
                x_range_offset = 65

            x_pos = int(
                floor(
                    base_x
                    - (780 - x_range_offset) * scaleDPI
                    + (270) * (x + x_offset) * scaleDPI
                )
            )

            bonus = bonus_list.pop()
            pasteCenter(
                imMission,
                bonus,
                x_pos - 64,
                y_pos,
                offset,
                scaleDPI,
                0.5,
            )
