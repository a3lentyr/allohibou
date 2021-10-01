import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random

from lib.util import pasteCenter


def createBankMission(imMission, canvas, offset, scaleDPI, bonus_list, short):
    # Add bank

    coinsList = []
    number_width = 6
    if short:
        number_width = 5
    for _ in range(0, number_width):
        coinsList.append(random.randint(1, 2))

    for box, n_coin in enumerate(sorted(coinsList)):
        x_pos = (canvas[0] * (box + 2)) // 8
        pasteCenter(
            imMission,
            "loan",
            x_pos,
            canvas[1] // 6,
            offset,
            scaleDPI,
            1,
        )

        for n in range(n_coin):
            bonus = bonus_list.pop()
            pasteCenter(
                imMission,
                bonus,
                x_pos - 64,
                (148 * (n + 1) + 64) * scaleDPI,
                offset,
                scaleDPI,
                0.5,
            )
