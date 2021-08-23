import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random

# attribution : https://crossheadstudios.com/


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

        common_bonus = [
            "bomb",
            "parrot",
            "pirate-patch",
            "jolly-roger",
        ]

        rare_bonus = [
            "diamond",
            "palm-tree",
            "pirate-ship",
            "rond-village-2-bonus",
        ]

        unique_bonus = [
            "rond-village-1-bonus",
            "rond-village-3-bonus",
        ]

        bonus_list = 6 * common_bonus + 3 * rare_bonus + unique_bonus  # 12+8+8 = 28

        random.shuffle(bonus_list)

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
            if missions[i]["type"] == "port":
                self.createPortMission(imMission, canvas, offset, scaleDPI, bonus_list)

            if missions[i]["type"] == "village":
                self.createVillageMission(
                    imMission, canvas, offset, scaleDPI, bonus_list
                )
            if missions[i]["type"] == "market":
                self.createMarketMission(
                    imMission, canvas, offset, scaleDPI, bonus_list
                )

        return imMission

    def createVillageMission(self, imMission, canvas, offset, scaleDPI, bonus_list):
        for x in range(0, 6):
            MissionCreator.pasteCenter(
                imMission,
                "right-arrow",
                (canvas[0] * (x + 1)) // 7,
                canvas[1] // 9,
                offset,
                scaleDPI,
                0.5,
            )

            bonus = bonus_list.pop()
            MissionCreator.pasteCenter(
                imMission,
                bonus,
                int(floor(canvas[0] * (x + 1.5))) // 7,
                canvas[1] // 9,
                offset,
                scaleDPI,
                0.6,
            )

            if x != 0:
                MissionCreator.pasteCenter(
                    imMission,
                    "left-arrow",
                    (canvas[0] * (x + 1)) // 7,
                    (canvas[1] * 2) // 9,
                    offset,
                    scaleDPI,
                    0.5,
                )

            bonus = bonus_list.pop()
            MissionCreator.pasteCenter(
                imMission,
                bonus,
                int(floor(canvas[0] * (x + 1.5))) // 7,
                (canvas[1] * 2) // 9,
                offset,
                scaleDPI,
                0.6,
            )

        MissionCreator.pasteCenter(
            imMission,
            "down-arrow",
            int(floor(canvas[0] * 6.5)) // 7,
            canvas[1] // 6,
            offset,
            scaleDPI,
            0.5,
        )

    def createPortMission(self, imMission, canvas, offset, scaleDPI, bonus_list):
        # Add port

        coinsList = []
        for _ in range(0, 8):
            coinsList.append(random.randint(1, 4))

        for box, n_coin in enumerate(sorted(coinsList)):

            MissionCreator.pasteCenter(
                imMission,
                "fullbox",
                (canvas[0] * (box + 2)) // 10,
                canvas[1] // 6,
                offset,
                scaleDPI,
                1,
            )

            for h in range(0, n_coin):

                MissionCreator.pasteCenter(
                    imMission,
                    "coin",
                    (canvas[0] * (box + 2)) // 10,
                    canvas[1] // 6 + (64 - h * 128) * scaleDPI,
                    offset,
                    scaleDPI,
                    0.4,
                )

            bonus = bonus_list.pop()
            MissionCreator.pasteCenter(
                imMission,
                bonus,
                (canvas[0] * (box + 2)) // 10,
                canvas[1] // 3 - (128 + 64) * scaleDPI,
                offset,
                scaleDPI,
                0.6,
            )

    def createMarketMission(self, imMission, canvas, offset, scaleDPI, bonus_list):

        market = ["rond-village-2", "rond-village-1", "rond-village-3"]

        for m, m_name in enumerate(market):
            x_coord = (canvas[0] * (m + 1)) // 4 + 64 * m * scaleDPI

            MissionCreator.pasteCenter(
                imMission,
                m_name,
                x_coord,
                128 * scaleDPI,
                offset,
                scaleDPI,
                1.4,
            )

            for x in range(0, 4):
                y_coord = (canvas[1] * (x + 1)) // 14 + 64 * scaleDPI

                MissionCreator.pasteCenter(
                    imMission,
                    "case",
                    x_coord - 128 * scaleDPI,
                    y_coord,
                    offset,
                    scaleDPI,
                    1,
                )
                MissionCreator.pasteCenter(
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
                MissionCreator.pasteCenter(
                    imMission,
                    bonus,
                    (canvas[0] * (2 * m + 1)) // 8 + 64 * (2 * m - 1) // 2 * scaleDPI,
                    y_coord,
                    offset,
                    scaleDPI,
                    0.6,
                )
