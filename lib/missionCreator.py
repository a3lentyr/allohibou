import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random

from lib.portCreator import createPortMission
from lib.villageCreator import createVillageMission
from lib.marketCreator import createMarketMission
from lib.bankCreator import createBankMission
from lib.util import pasteCenter

# attribution : https://crossheadstudios.com/


class MissionCreator:
    def __init__(self, BG_COLOR):
        self.BG_COLOR = BG_COLOR

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
            missions = random.sample(json.load(f)["missions"], 3)

        for i in range(0, 3):
            short = i == 0

            offset = i * (canvas[1] // 3)

            square = Image.open(
                "./img/" + missions[i]["missionBackground"] + ".png", "r"
            )
            imMission.paste(square, (0, offset), square)

            pasteCenter(
                imMission,
                missions[i]["icon"],
                (128 + 64) * scaleDPI,
                (128 + 64) * scaleDPI,
                offset,
                scaleDPI,
            )

            if "forceIcon" in missions[i]:
                pasteCenter(
                    imMission,
                    missions[i]["forceScale"],
                    100 * scaleDPI,
                    canvas[1] // 3 - (420 + 64) * scaleDPI,
                    offset,
                    scaleDPI,
                    1,
                )

                pasteCenter(
                    imMission,
                    missions[i]["forceIcon"],
                    100 * scaleDPI,
                    canvas[1] // 3 - (128 + 64) * scaleDPI,
                    offset,
                    scaleDPI,
                    0.7,
                )
            if missions[i]["type"] == "port":
                createPortMission(
                    imMission, canvas, offset, scaleDPI, bonus_list, short
                )

            if missions[i]["type"] == "bank":
                createBankMission(
                    imMission, canvas, offset, scaleDPI, bonus_list, short
                )

            if missions[i]["type"] == "village":
                createVillageMission(
                    imMission, canvas, offset, scaleDPI, bonus_list, short
                )
            if missions[i]["type"] == "market":
                createMarketMission(
                    imMission, canvas, offset, scaleDPI, bonus_list, short
                )

            # add objectives
            objective = random.choice(missions[i]["objectives"])
            pasteCenter(
                imMission,
                objective,
                canvas[0] - (128 + 60) * scaleDPI,
                (canvas[1] * i) // 12 + (256) * scaleDPI,
                0,
                scaleDPI,
                1,
            )

        return imMission
