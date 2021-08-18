from math import dist, sqrt, floor
import random
from typing import List, Tuple

from lib.stackDrawer import StackDrawer
from lib import commonMath
from lib.road import Road
from lib.mountains import Mountains


class Obstacle:
    _coord: Tuple[int, int]
    _type: str
    _sepia: bool

    def __init__(self, coord: Tuple[int, int], sepia: bool = False):
        self._coord = coord
        self._type = "cross"
        self._sepia = sepia

    def toStack(self) -> StackDrawer:
        stack = StackDrawer()
        stack.add(self._type, self._coord, 0, sepia=self._sepia)
        return stack


class City:
    _coord: Tuple[int, int]
    _type: str

    def __init__(self, coord: Tuple[int, int]):
        self._coord = coord
        self._type = "rond-port"

    def toStack(self) -> StackDrawer:
        stack = StackDrawer()
        stack.add(self._type, self._coord, 3)
        return stack


class MapCreator:

    _citiesPlaces: List[City]
    _roads: List[Road]
    _obstacles: List[Obstacle]
    _mountains: List[Mountains]
    _canvasSize: Tuple[int, int]
    _canvasOffset: Tuple[int, int]
    _cityMargin: int
    _obstacleMargin: int
    _mapMargin: int
    _coastalPlaces: List[Tuple[int, int]]
    _mountainsPlaces: List[Tuple[int, int]]

    def __init__(
        self,
        canvasSize: Tuple[int, int],
        coastalPlaces: List[Tuple[int, int]],
        mountainsPlaces: List[Tuple[int, int]],
        canvasOffset: Tuple[int, int] = (0, 0),
        nCities=12,
        nRoads=21,
    ):
        self._citiesPlaces = []
        self._roads = []
        self._mountains = []
        self._obstacles = []
        self._canvasSize = canvasSize
        self._canvasOffset = canvasOffset
        self._cityMargin = floor(max(canvasSize[0], canvasSize[1]) * 0.15)
        self._obstacleMargin = floor(max(canvasSize[0], canvasSize[1]) * 0.07)
        self._mapMargin = floor(max(canvasSize[0], canvasSize[1]) * 0.07)
        self._coastalPlaces = coastalPlaces
        self._mountainsPlaces = mountainsPlaces

        self.addCross()
        self.placeMountains()

        self.placeCities(nCities)
        self.placeRoads(nRoads)

        self.allocateCities()
        self.allocateRoads()

    def placeMountains(self):

        random.shuffle(self._mountainsPlaces)

        n_mountains = random.randint(2, 6)
        for i in range(0, n_mountains):
            if len(self._mountainsPlaces) == 0:
                break

            coord = self._mountainsPlaces.pop(1)
            land = Mountains(coord)
            land._type = "Mountains" + str(random.randint(1, 3))

            self._mountains.append(land)

    def addCross(self):
        margin = floor(self._mapMargin) * 2
        possiblecoord = [
            (
                self._canvasOffset[0] + margin,
                self._canvasOffset[1] + margin,
            ),
            (
                self._canvasOffset[0] + self._canvasSize[0] - margin,
                self._canvasOffset[1] + self._canvasSize[1] - margin,
            ),
            (
                self._canvasOffset[0] + margin,
                self._canvasOffset[1] + self._canvasSize[1] - margin,
            ),
            (
                self._canvasOffset[0] + self._canvasSize[0] - margin,
                self._canvasOffset[1] + margin,
            ),
        ]
        coord = random.choice(possiblecoord)
        bestdistance = 0
        # find place furthest from coast
        for candidatX, candidatY in possiblecoord:
            distance = 0
            for x, y in random.sample(self._coastalPlaces, 100):
                distance += (candidatX - x) ** 2 + (candidatY - y) ** 2
            if distance > bestdistance:
                bestdistance = distance
                coord = (candidatX, candidatY)

        self._obstacles.append(Obstacle(coord))

    def placeCities(self, nCities):
        random.shuffle(self._coastalPlaces)
        currentNumberOfCities = 0

        for _ in range(nCities * 1000):
            if currentNumberOfCities >= nCities:
                break

            coord = self.getNonIntersectRandomCoordinates()

            inter = False
            for otherCity in self._citiesPlaces:
                dist = sqrt(
                    (coord[0] - otherCity._coord[0]) ** 2
                    + (coord[1] - otherCity._coord[1]) ** 2
                )
                inter = inter or dist < self._cityMargin

            for otherCity in self._obstacles:
                dist = sqrt(
                    (coord[0] - otherCity._coord[0]) ** 2
                    + (coord[1] - otherCity._coord[1]) ** 2
                )
                inter = inter or dist < self._obstacleMargin

            if not inter:
                self._citiesPlaces.append(City(coord))
                currentNumberOfCities += 1

    def placeRoads(self, nRoads):
        possibleRoads = []

        for cityIndex, cityStart in enumerate(self._citiesPlaces[:-1]):
            for cityEnd in self._citiesPlaces[cityIndex + 1 :]:
                possibleRoads.append((cityStart._coord, cityEnd._coord))

        random.shuffle(possibleRoads)

        currentNumberOfRoads = 0
        for start, end in possibleRoads:
            if currentNumberOfRoads >= nRoads:
                break

            inter = False
            # roads cannot intersect each other
            for seg2 in self._roads:
                inter = inter or commonMath.intersectLines(
                    start, end, seg2._start, seg2._end
                )

            # roads cannot intersect existing cities
            for otherCity in self._citiesPlaces:
                if otherCity._coord == start or otherCity._coord == end:
                    continue
                x, y = otherCity._coord
                inter = inter or commonMath.intersectLines(
                    start,
                    end,
                    (x - self._cityMargin / 2, y),
                    (x + self._cityMargin / 2, y),
                )
                inter = inter or commonMath.intersectLines(
                    start,
                    end,
                    (x, y - self._cityMargin / 2),
                    (x, y + self._cityMargin / 2),
                )

            # roads cannot intersect existing obstacles
            for otherCity in self._obstacles:
                if otherCity._coord == start or otherCity._coord == end:
                    continue
                x, y = otherCity._coord
                inter = inter or commonMath.intersectLines(
                    start,
                    end,
                    (x - self._obstacleMargin / 2, y),
                    (x + self._obstacleMargin / 2, y),
                )
                inter = inter or commonMath.intersectLines(
                    start,
                    end,
                    (x, y - self._obstacleMargin / 2),
                    (x, y + self._obstacleMargin / 2),
                )

            if not inter:
                self._roads.append(Road(start, end))
                currentNumberOfRoads += 1

    def allocateCities(self):

        possibleCities = [
            "rond-port",
            "rond-village-1",
            "rond-village-2",
            "rond-village-3",
            "rond-village",
        ]
        random.shuffle(possibleCities)

        for city_id, city in enumerate(self._citiesPlaces):
            city._type = possibleCities[city_id % len(possibleCities)]

    def allocateRoads(self):
        possibleRoads = [
            ("blue", "resource-ship-blue"),
            ("red", "resource-ship-red"),
            ("yellow", "resource-ship-yellow"),
        ]
        random.shuffle(possibleRoads)
        for road_id, road in enumerate(self._roads):
            road._type = possibleRoads[road_id % len(possibleRoads)][0]
            road._boatType = possibleRoads[road_id % len(possibleRoads)][1]

    def toStack(self) -> StackDrawer:
        stack = StackDrawer()

        for mountains in self._mountains:
            stack.merge(mountains.toStack())

        for obstacle in self._obstacles:
            stack.merge(obstacle.toStack())

        for city in self._citiesPlaces:
            stack.merge(city.toStack())

        for road in self._roads:
            stack.merge(road.toStack(stack))
        return stack

    def getNonIntersectRandomCoordinates(self) -> Tuple[int, int]:
        while len(self._coastalPlaces) > 0:
            x, y = self._coastalPlaces.pop(1)
            if (
                x > (self._canvasOffset[0] + floor(self._mapMargin))
                and x
                < (self._canvasOffset[0] + self._canvasSize[0] - floor(self._mapMargin))
                and y > (self._canvasOffset[1] + floor(self._mapMargin))
                and y
                < (self._canvasOffset[1] + self._canvasSize[1] - floor(self._mapMargin))
            ):
                return (x, y)

        # Else we return a random number
        x = random.randint(
            self._canvasOffset[0] + floor(self._mapMargin),
            self._canvasOffset[0] + self._canvasSize[0] - floor(self._mapMargin),
        )
        y = random.randint(
            self._canvasOffset[1] + floor(self._mapMargin),
            self._canvasOffset[1] + self._canvasSize[1] - floor(self._mapMargin),
        )
        return (x, y)
