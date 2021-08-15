
from math import sqrt, floor
import random
from typing import List,Tuple

from lib.stackDrawer import StackDrawer
from lib import commonMath


class City:
    _coord:Tuple[int,int]
    _type:str

    def __init__(self, coord : Tuple[int,int]):
        self._coord = coord
        self._type = "rond-port"

    def toStack(self)  -> StackDrawer:
        stack = StackDrawer()
        stack.add(self._type, self._coord, 3)
        return stack

class Road:
    _start: Tuple[int,int]
    _end: Tuple[int,int]
    _type:str
    _boatType:str
    _scale:int = 2 * 4

    def __init__(self, start: Tuple[int, int], end: Tuple[int,int]):
        self._start = start
        self._end = end
        self._type = "blue"
        self._boatType = "resource-ship-blue"


    def toStack(self) -> StackDrawer:
        stack = StackDrawer()

        x1,y1 = self._start
        x2,y2 = self._end
        x = (x1 + x2)//2
        y = (y1 + y2)//2

        road_test_index = 0
        tc = (-100 + 20 * road_test_index)*self._scale
        center, roadList = self.compute_road_position(tc)

        stack.add(self._boatType, center, 2)

        for roadCenter in roadList:
            stack.add(self._type, roadCenter[:2], 1, rotate=roadCenter[2])


        return stack


    def compute_road_position(self, tc):
        x1,y1 = self._start
        x2,y2 = self._end

        ax = 10000
        if y2 != y1:
            ax = (x2 - x1) / (y2 - y1)
        ay = 10000
        if x2 != x1:
            ay = (y2 - y1) / (x2 - x1)

        xc = (x1 + x2) / 2 + tc * ay / (ax + ay)
        yc = (y1 + y2) / 2 + tc * ax / (ax + ay)

        xm, ym = Road.bezier(x1, y1, xc, yc, x2, y2, 0.5)


        # road graphism
        single_width = 42.0 * self._scale  # length of the path in road file
        road_length = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        control_length = sqrt((xc - x1) ** 2 + (yc - y1) ** 2) + sqrt((x2 - xc) ** 2 + (y2 - yc) ** 2)

        road_num = int((road_length + control_length) / (2 * single_width)) + 1
        # how many time it should be pasted, average between curve and control

        road_return = []

        for road_index in range(road_num):
            t = (road_index * 1.0) / road_num
            xrm, yrm = Road.bezier(x1, y1, xc, yc, x2, y2, t)

            xrmp, yrmp = Road.bezier(x1, y1, xc, yc, x2, y2, t - 1.0 / road_num)
            xrmn, yrmn = Road.bezier(x1, y1, xc, yc, x2, y2, t + 1.0 / road_num)

            rotate_factor = commonMath.ang([[xrmp, yrmp], [xrmn, yrmn]], [[0, 0], [1, 0]])
            if yrmp > yrmn:
                rotate_factor = commonMath.ang([[xrmp, yrmp], [xrmn, yrmn]], [[0, 0], [-1, 0]])

            road_return.append([floor(xrm), floor(yrm),- rotate_factor])

        return (floor(xm), floor(ym)), road_return

    @staticmethod
    def bezier(x1, y1, xc, yc, x2, y2, t):
        x = (1-t)*((1-t)*x1+t*xc)+t*((1-t)*xc+t*x2)
        y = (1-t)*((1-t)*y1+t*yc)+t*((1-t)*yc+t*y2)
        return x, y

class MapCreator:


    _citiesPlaces : List[City]
    _roads : List[Road]
    _canvasSize : Tuple[int,int]
    _canvasOffset : Tuple[int,int]

    def __init__(self, canvasSize:Tuple[int,int], canvasOffset:Tuple[int,int] = (0,0), nCities=8, nRoads = 21 ):
        self._citiesPlaces = []
        self._roads = []
        self._canvasSize = canvasSize
        self._canvasOffset = canvasOffset

        self.placeCities(nCities)
        self.placeRoads(nRoads)


    def placeCities(self, nCities=8):
        for _ in range(nCities):
            coord = self.getNonIntersectRandomCoordinates()
            self._citiesPlaces.append(City(coord))


    def placeRoads(self, nRoads = 21 ):
        possibleRoads = []

        for cityIndex,cityStart in enumerate(self._citiesPlaces[:-1]):
            for cityEnd in self._citiesPlaces[cityIndex+1:]:
                possibleRoads.append((cityStart._coord,cityEnd._coord))

        random.shuffle(possibleRoads)

        currentNumberOfRoads = 0
        for start, end in possibleRoads:
            if currentNumberOfRoads >= nRoads:
                break

            inter = False
            # roads cannot intersect each other
            for seg2 in self._roads:
                inter = inter or commonMath.intersectLines(start,end, seg2._start, seg2._end)

            if not inter:
                self._roads.append(Road(start,end))
                currentNumberOfRoads += 1



    def toStack(self) -> StackDrawer:
        stack = StackDrawer()

        for city in self._citiesPlaces:
            stack.merge(city.toStack())

        for road in self._roads:
            stack.merge(road.toStack())
        return stack


    def getNonIntersectRandomCoordinates(self) -> Tuple[int,int]:
        x = random.randint(self._canvasOffset[0],self._canvasOffset[0]+ self._canvasSize[0])
        y = random.randint(self._canvasOffset[1],self._canvasOffset[1]+ self._canvasSize[1])
        return (x, y)