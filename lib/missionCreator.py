import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from math import floor
import random

from lib.portCreator import createPortMission
from lib.villageCreator import createVillageMission
from lib.marketCreator import createMarketMission
from lib.bankCreator import createBankMission
from lib.castleCreator import createCastleMission
from lib.libraryCreator import createLibraryMission
from lib.bidCreator import createBidMission
from lib.caveCreator import createCaveMission
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
            "jolly-roger",
        ]

        rare_bonus = [
            "pirate-ship",
        ]

        unique_bonus = []

        missionIcon = []

        with open("missionDescriptor.json") as f:
            missions = random.sample(json.load(f)["missions"], 3)

        for m in missions:
            common_bonus.extend(m["bonus"])
            rare_bonus.extend(m["rare_bonus"])
            unique_bonus.extend(m["unique_bonus"])
            missionIcon.extend(m["mapIcon"])

        bonus_list = (
            10 * common_bonus + 5 * rare_bonus + 2 * unique_bonus
        )  # 12+8+8 = 28

        random.shuffle(bonus_list)

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
            if missions[i]["type"] == "castle":
                createCastleMission(
                    imMission, canvas, offset, scaleDPI, bonus_list, short
                )
            if missions[i]["type"] == "library":
                createLibraryMission(
                    imMission, canvas, offset, scaleDPI, bonus_list, short
                )
            if missions[i]["type"] == "bid":
                createBidMission(imMission, canvas, offset, scaleDPI, bonus_list, short)
            if missions[i]["type"] == "cave":
                createCaveMission(
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

        return imMission, missionIcon
