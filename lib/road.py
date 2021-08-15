
from math import sqrt, floor
from typing import Tuple

from lib.stackDrawer import StackDrawer
from lib import commonMath

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


    def toStack(self,obstaclesList) -> StackDrawer:
        stack = StackDrawer()

        x1,y1 = self._start
        x2,y2 = self._end
        x = (x1 + x2)//2
        y = (y1 + y2)//2

        bestDistance = 0
        best_road = ()

        for road_test_index in range(0,10):
            tc = (-100 + 20 * road_test_index)*self._scale
            center, roadList, distance = self.compute_road_position(tc,obstaclesList)
            if road_test_index==0 or distance>bestDistance:
                best_road = center, roadList
                bestDistance = distance

        center, roadList = best_road
        stack.add(self._boatType, center, 2)

        for roadCenter in roadList:
            stack.add(self._type, roadCenter[:2], 1, rotate=roadCenter[2])


        return stack


    def compute_road_position(self, tc, obstaclesList):
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
        distance_num = 0

        for road_index in range(road_num):
            t = (road_index * 1.0) / road_num
            xrm, yrm = Road.bezier(x1, y1, xc, yc, x2, y2, t)

            xrmp, yrmp = Road.bezier(x1, y1, xc, yc, x2, y2, t - 1.0 / road_num)
            xrmn, yrmn = Road.bezier(x1, y1, xc, yc, x2, y2, t + 1.0 / road_num)

            rotate_factor = commonMath.ang([[xrmp, yrmp], [xrmn, yrmn]], [[0, 0], [1, 0]])
            if yrmp > yrmn:
                rotate_factor = commonMath.ang([[xrmp, yrmp], [xrmn, yrmn]], [[0, 0], [-1, 0]])

            road_return.append([floor(xrm), floor(yrm),- rotate_factor])

        # We try to maximize the distance to obstacles and other roads
        for other_road in obstaclesList._stack:
            dist = -1/(1+sqrt((other_road._center[0] - xrm)**2 + (other_road._center[1] - yrm)**2))
            distance_num += dist

        return (floor(xm), floor(ym)), road_return, distance_num

    @staticmethod
    def bezier(x1, y1, xc, yc, x2, y2, t):
        x = (1-t)*((1-t)*x1+t*xc)+t*((1-t)*xc+t*x2)
        y = (1-t)*((1-t)*y1+t*yc)+t*((1-t)*yc+t*y2)
        return x, y
