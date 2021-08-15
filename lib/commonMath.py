import math


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


def intersectLines(p1, q1, p2, q2):
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

    return False