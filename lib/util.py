import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random


def pasteCenter(imMission, name, bg_x, bg_y, offset, scaleDPI, scale=2):

    missionIcon = Image.open("./img/" + name + ".png", "r")

    img_w, img_h = missionIcon.size
    missionIcon = missionIcon.resize(
        (int(floor(img_w * scale * scaleDPI)), int(floor(img_h * scale * scaleDPI)))
    )
    img_w, img_h = missionIcon.size

    inner_offset = (bg_x - (img_w) // 2, bg_y + offset - (img_h) // 2)

    imMission.paste(missionIcon, inner_offset, missionIcon)
