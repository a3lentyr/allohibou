import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor


class MissionCreator:
    def __init__(self, BG_COLOR):
        self.BG_COLOR = BG_COLOR

    @staticmethod
    def pasteCenter(imMission, name, bg_x, bg_y, offset, scaleDPI, scale=2):

        missionIcon = Image.open("./img/" + name + ".png", "r")

        img_w, img_h = missionIcon.size
        missionIcon = missionIcon.resize(
            (int(floor(img_w * scale * scaleDPI)), int(floor(img_h * scale * scaleDPI)))
        )
        img_w, img_h = missionIcon.size

        inner_offset = (bg_x - (img_w) // 2, bg_y + offset - (img_h) // 2)

        imMission.paste(missionIcon, inner_offset, missionIcon)

    def createMissionSheet(self, canvas, scaleDPI):
        # mission sheet
        imMission = Image.new("RGBA", canvas, self.BG_COLOR)
        bomb = Image.open("./img/" + "bomb.png", "r")

        with open("missionDescriptor.json") as f:
            missions = json.load(f)["missions"]

        for i in range(0, 3):
            offset = i * (canvas[1] // 3)

            square = Image.open(
                "./img/" + missions[i]["missionBackground"] + ".png", "r"
            )
            imMission.paste(square, (0, offset), square)

            MissionCreator.pasteCenter(
                imMission,
                missions[i]["icon"],
                (128 + 64) * scaleDPI,
                (128 + 64) * scaleDPI,
                offset,
                scaleDPI,
            )

            if "forceIcon" in missions[i]:
                MissionCreator.pasteCenter(
                    imMission,
                    missions[i]["forceScale"],
                    100 * scaleDPI,
                    canvas[1] // 3 - (420 + 64) * scaleDPI,
                    offset,
                    scaleDPI,
                    1,
                )

                MissionCreator.pasteCenter(
                    imMission,
                    missions[i]["forceIcon"],
                    100 * scaleDPI,
                    canvas[1] // 3 - (128 + 64) * scaleDPI,
                    offset,
                    scaleDPI,
                    0.7,
                )

            # Add port

            for box in range(0, 12):

                MissionCreator.pasteCenter(
                    imMission,
                    "fullbox",
                    (canvas[0] * (box + 2)) // 16,
                    canvas[1] // 6,
                    offset,
                    scaleDPI,
                    1,
                )

        return imMission
