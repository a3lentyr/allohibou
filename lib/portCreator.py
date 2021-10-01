import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random
from lib.util import pasteCenter


def createPortMission(imMission, canvas, offset, scaleDPI, bonus_list, short):
    # Add port

    coinsList = []
    number_width = 8
    if short:
        number_width = 6
    for _ in range(0, number_width):
        coinsList.append(random.randint(1, 4))

    for box, n_coin in enumerate(sorted(coinsList)):
        x_pos = (canvas[0] * (box + 2)) // 10
        pasteCenter(
            imMission,
            "fullbox",
            x_pos,
            canvas[1] // 6,
            offset,
            scaleDPI,
            1,
        )

        for h in range(0, n_coin):
            y_pos = canvas[1] // 6 + (64 - h * 128) * scaleDPI
            pasteCenter(
                imMission,
                "coin",
                x_pos,
                y_pos,
                offset,
                scaleDPI,
                0.4,
            )

        bonus = bonus_list.pop()
        pasteCenter(
            imMission,
            bonus,
            x_pos,
            canvas[1] // 3 - (128 + 64) * scaleDPI,
            offset,
            scaleDPI,
            0.6,
        )
