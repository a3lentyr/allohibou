import tempfile
import itertools as IT
import os
import random
import math
from math import sqrt
import fbd


def get_ordered_list(points, x_list, i):
    x = x_list[i][0]
    y = x_list[i][0]
    points.sort(key=lambda p: sqrt((x_list[p][0] - x) ** 2 + (x_list[p][1] - y) ** 2))
    return points


def create_multiple_link(nrows, x, i, d, segment, num_max=3):
    next_list = list(range(nrows))
    random.shuffle(next_list)
    next_list = get_ordered_list(next_list, x, i)

    # finding links that can be allocated
    d, segment = create_single_link(d, segment, x, next_list, i, num_max)

    return d, segment


def create_single_link(d, segment, x, next_list, i, num_max=3):
    found_list = []
    links_count = sum(d[i]) / 0.3
    if links_count >= num_max:
        return d, segment

    # finding links that can be allocated
    for j in next_list:
        links_next = sum(d[j]) / 0.3
        if i != j and links_next < num_max and d[i][j] <= 0:
            inter = False
            for seg2 in segment:
                inter = inter or intersect(x[i], x[j], seg2[0], seg2[1])

            if not inter:
                found_list.append(j)

    # selecting closest link
    found_sorted = get_ordered_list(found_list, x, i)

    if len(found_sorted) > 0:
        j = found_sorted[0]

        col = [0, 0, 0]
        for colindex in range(3):
            col[colindex] = sum([1 for c in d[i] if c == (0.3 + colindex * 0.01)]) + sum(
                [1 for c in d[j] if c == (0.3 + colindex * 0.01)])

        indices = [colenum for colenum, colindex in enumerate(col) if colindex == min(col)]
        random.shuffle(indices)
        color = indices[0] * 0.01

        d[i][j] = .3 + color  # passing color info within d
        d[j][i] = d[i][j]
        segment.append([x[i], x[j]])
        next_list = get_ordered_list(next_list, x, j)
        d, segment = create_single_link(d, segment, x, next_list, j, num_max)

    return d, segment


# link creation and adjustment
def create_random_links(x, m):
    d = []
    nrows = m
    ncols = m
    for i in range(nrows):
        dr = []
        for j in range(ncols):
            dr.append(.0)
        d.append(dr)

    segment = []

    # first we create a cycle
    cycle_list = list(range(nrows))
    random.shuffle(cycle_list)

    for i in cycle_list:
        d, segment = create_multiple_link(nrows, x, i, d, segment, 2)
    cycle_list = list(reversed(cycle_list))

    # Then we complete the links
    for i in cycle_list:
        d, segment = create_multiple_link(nrows, x, i, d, segment, 4)

    return d


def on_segment(p, q, r):
    if max(p[0], r[0]) >= q[0] >= min(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
        return True

    return False


def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0:
        return 0

    if val > 0:
        return 1
    return 2


def intersect(p1, q1, p2, q2):
    if p1 == p2 or p1 == q2 or q1 == p2 or q1 == q2:
        return False

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        # print("intersect")
        return True

    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    if o3 == 0 and on_segment(p2, p1, q2):
        return True

    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False;


def get_places_coordinates(m):
    x = []
    v = []

    # we generate a grid 4*4
    grid = []

    for i in range(4):
        for j in range(4):
            grid.append([i / 4.0, j / 4.0])

    # count the number of links
    count_links = 0
    count_single = 0
    while count_links < 20.9 or count_links > 22.2 or count_single > 0:

        random.shuffle(grid)

        x = []
        v = []

        for i in range(m):
            xi = grid[i]
            x.append(xi)
            v.append([0.0, 0.0])

        best_d = create_random_links(x, m)
        count_links = sum([sum(d) for d in best_d]) / 0.6
        count_single = sum([1 for d in best_d if sum(d) / 0.3 <= 1])

    # finish with a simple Forced based drawing

    for i in range(0, 1000):
        x, v = fbd.forcedrawing(x, v, best_d)

    # check for deviation
    deviation=False
    for place in x:
        if place[0]<-10 or place[0]>10 or place[1]<-10 or place[1]>10:
            deviation = True
            break

    if deviation :
        #print("deviation")
        return get_places_coordinates(m)

    return x, best_d

def dot(vA, vB):
    return vA[0] * vB[0] + vA[1] * vB[1]


def ang(line_a, line_b):
    # Get nicer vector form
    v_a = [(line_a[0][0] - line_a[1][0]), (line_a[0][1] - line_a[1][1])]
    v_b = [(line_b[0][0] - line_b[1][0]), (line_b[0][1] - line_b[1][1])]
    # Get dot prod
    dot_prod = dot(v_a, v_b)
    # Get magnitudes
    mag_a = dot(v_a, v_a) ** 0.5
    mag_b = dot(v_b, v_b) ** 0.5
    # Get cosine value
    if mag_a == 0:
        return 90.0
    if mag_b == 0:
        return 90.0

    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod / mag_b / mag_a)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle) % 360
    if ang_deg - 180 >= 0:
        # As in if statement
        return 360 - ang_deg
    else:

        return ang_deg
