import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random

from lib.util import pasteCenter


def createCastleMission(imMission, canvas, offset, scaleDPI, bonus_list, short):
    # Add bank
    base_x = (750 + 256 + 128) * scaleDPI
    base_y = (500 + 64) * scaleDPI
    num_bonus = 5
    x_offset = 0

    if short:

        pasteCenter(
            imMission,
            "reputation",
            base_x,
            base_y,
            offset,
            scaleDPI,
            1,
        )
    else:

        base_x = (750 + 256 + 128 + 167) * scaleDPI
        base_y = (500 + 64) * scaleDPI
        num_bonus = 6
        x_offset = 0.5

        pasteCenter(
            imMission,
            "reputationlong",
            base_x,
            base_y,
            offset,
            scaleDPI,
            1,
        )

    for y in range(3):
        y_pos = base_y - (64) * scaleDPI + (240) * y * scaleDPI

        for x in range(num_bonus):
            if x == 2:
                continue
            if y == 0 and x == 5:
                continue

            x_pos = int(
                floor(
                    base_x
                    - 600 * scaleDPI
                    + (256 + 64 + 12) * (x - x_offset) * scaleDPI
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
