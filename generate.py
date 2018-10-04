import tempfile
import itertools as IT
import os
import random
import math
from math import sqrt
from lib import fbd, links

from noise import pnoise2,snoise2
import re
# random.seed(45)


class DrawObject:
    def __init__(self, x_, y_, type_, color_, margin_, size_, rotate_factor_= 0, overlay_=False, opacity_=1):
        self.x = x_
        self.y = y_
        self.type = type_
        self.margin = margin_
        self.color = color_
        self.size = size_
        self.rotate_factor = rotate_factor_
        self.overlay = overlay_
        self.opacity = opacity_


class SvgObject:
    def __init__(self, name, svg_cache):
        if not name in svg_cache:
            svg_cache[name] = load_svg(name)
        self.text = svg_cache[name]


# return a unique file name
def uniquify(path, sep=''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s=sep, n=next(count))

    orig = tempfile._name_sequence
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dir_name, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir=dir_name, prefix=filename, suffix=ext)
        tempfile._name_sequence = orig
    return filename


def load_svg(name,noreplace=False):
    name_file = open("img/" + name + ".svg", 'r')
    name_text = name_file.read()
    if not noreplace:
        name_text = re.sub(r"<\?xml.*</metadata>", "", name_text,flags=re.DOTALL)
        name_text = re.sub(r"</svg>", "", name_text,flags=re.DOTALL)
    name_file.close()

    return name_text


def draw_places(draw_array):
    # forming list of places
    form_list = ["triangle", "carre", "rond", "losange"]
    color_list = ["violet", "orange", "green"]

    places_list = []
    for form in form_list:
        for color in color_list:
            places_list.append(form + "-" + color)


    # placing places
    places_coord, d = links.get_places_coordinates(len(places_list))

    # -- rescale such that everything is in 30:270 and 30:230
    minx = min([x[0] for x in places_coord])
    maxx = max([x[0] for x in places_coord])
    miny = min([y[1] for y in places_coord])
    maxy = max([y[1] for y in places_coord])

    trans_places = []
    for pair_coord in places_coord:
        x = int((pair_coord[0] - minx) * (280 - 25) / (maxx - minx) + 25)
        y = int((pair_coord[1] - miny) * (250 - 25) / (maxy - miny) + 25)
        trans_places.append([x, y])

    # Adding places

    for i, name in enumerate(places_list):
        x = trans_places[i][0]
        y = trans_places[i][1]
        draw_array.append(DrawObject(x, y, name, "", 25, 1, 0, True))

    return trans_places, d


def draw_marchandise(road_places_list, draw_array):
    # forming list of marchandise
    form_list_m = ["triangle", "triangle", "triangle", "carre", "rond", "losange", "losange"]
    color_list = ["violet", "orange", "green"]
    m_list = []
    for form in form_list_m:
        for color in color_list:
            m_list.append(form + "-" + color + "-m")
    random.shuffle(form_list_m)

    m_index = 0
    for road in road_places_list:
        if m_index < len(m_list):
            xm = road[0]
            ym = road[1]
            draw_array.append(DrawObject(xm, ym, m_list[m_index], "", 15, 1, 0, True))
            m_index += 1


def draw_roads(trans_places, d, draw_array):
    # forming list of road
    road_list = ["blue", "red", "yellow"]

    # adding path
    shortened_list = []
    road_places_list = []
    march_places_list = []

    for i, place_list in enumerate(d):
        for j, target in enumerate(place_list):
            if target > 0 and j > i:
                # path between 4 and 4 are only drawn as half
                x1 = trans_places[i][0]
                y1 = trans_places[i][1]
                x2 = trans_places[j][0]
                y2 = trans_places[j][1]
                unique_color = (len([1 for c in d[i] if c == target]) <= 1)  # do not remove unique color
                unique_color = (unique_color or len([1 for c in d[j] if c == target]) <= 1)

                xm = (trans_places[i][0] + trans_places[j][0]) / 2
                ym = (trans_places[i][1] + trans_places[j][1]) / 2

                if sum(place_list) / 0.3 > 3 and sum(
                        d[j]) / 0.3 > 3 and i not in shortened_list and j not in shortened_list and not unique_color:
                    x2 = (x1 + x2) / 2
                    y2 = (y1 + y2) / 2
                    xm = x2
                    ym = y2
                    shortened_list.append(i)
                    shortened_list.append(j)

                march_places_list.append([xm, ym])

                # road graphism
                rotate_factor = links.ang([[x1, y1], [x2, y2]], [[0, 0], [1, 0]])
                if y1 > y2:
                    rotate_factor = links.ang([[x1, y1], [x2, y2]], [[0, 0], [-1, 0]])

                single_width = 14.0  # length of the path in road file
                road_length = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                road_num = int(road_length / single_width) + 1  # how many time it should be pasted

                for road_index in range(road_num):
                    xrm = (x1 * (road_num - road_index - 1.0) + x2 * (road_index + 1.0)) / road_num
                    yrm = (y1 * (road_num - road_index - 1.0) + y2 * (road_index + 1.0)) / road_num

                    road_places_list.append([xrm, yrm])
                    draw_array.append(DrawObject(xrm, yrm, road_list[int((target - 0.3) * 100)], "", 13, 1, rotate_factor))

    return road_places_list, march_places_list


def draw_cluster(draw_array, name, scale_min=0.05, scale_max=0.1, num_min=1, num_max=3, cluster_min=1, cluster_max=2, offset_height=40, offset_width=20):

    trans_places = []

    rand_num = random.randint(0, num_max-num_min) + num_min  # number of stone cluster
    content_text = ""
    for stone_index in range(0, rand_num):
        # check for collision
        is_under = True
        x = 0
        y = 0
        while is_under:
            y = random.random() * 250
            x = random.random() * 300
            is_under = False
            for p in draw_array:
                if sqrt((p.x - x ) ** 2 + (p.y - y ) ** 2) < p.margin+10: # own margin
                    is_under = True
                    break

        rand_num_small = random.randint(0, cluster_max-cluster_min) + cluster_min

        perlin_list=[]
        for y_off in range(0, offset_width, 10):
            for x_off in range(0, offset_height, 10):
                perlin_list.append((x_off, y_off, snoise2(x_off / 16.0, y_off / 16.0, 1)))
        perlin_list.sort(key=lambda tup: tup[2])

        for stone_indexes in perlin_list[0:rand_num_small]:
            xs = x - offset_height / 2 + stone_indexes[0]
            ys = y - offset_width / 2 + stone_indexes[1]
            trans_places.append([xs, ys])

    # filter places from front to back
    trans_places.sort(key=lambda tup: tup[1])
    for p in trans_places:
        xs = p[0] + 2 * random.random()
        ys = p[1] + 2 * random.random()
        scale = random.uniform(scale_min, scale_max)
        draw_array.append(DrawObject(xs, ys, name, "", 10, scale))

    return content_text, trans_places


def place_trees(draw_array):

    for x_index in range(-10, 310, 5):
        for y_index in range(270, -10, -5):
            x = x_index + 4 * random.random()
            y = y_index - 4 * random.random()
            if random.random() > 0.4:
                is_under = False
                for p in draw_array:
                    if sqrt((p.x - x) ** 2 + (p.y - y) ** 2) < p.margin:
                        is_under = True
                        break
                if not is_under:
                    color = "rgb(50," + str(50 + random.random() * 50) + ",50)"
                    size = random.uniform(0.02, 0.03)
                    draw_array.append(DrawObject(x, y, "tree", color, 0, size))


def draw(draw_array, svg_cache):
    content_text=""
    overlay_text=""
    for d in draw_array:
        text = SvgObject(d.type, svg_cache).text
        data_text = '<g transform="translate(' + str(d.x) + ',' + str(
            d.y) + ')  scale(' + str(d.size) + ',' + str(d.size)+') rotate(' + str(
                        d.rotate_factor) + ')" fill="' + d.color + '" style="opacity:' + str(d.opacity)+';">' + text + '</g>'
        if d.overlay:
            overlay_text += data_text
        else:
            content_text += data_text

    return content_text, overlay_text


def main():
    draw_array = []
    svg_cache = {}
    trans_places, d = draw_places(draw_array)
    road_places_list, march_places_list = draw_roads(trans_places, d, draw_array)
    draw_marchandise(march_places_list,draw_array)


    # Adding background
    draw_cluster(draw_array, "stones")

    # Adding unique feature
    feature = [("stadium", 0.03, 0.05), ("castle", 0.03, 0.05), ("moais", 0.02, 0.03), ("dragon", 0.01, 0.02),
               ("columns", 0.02, 0.03), ("grave", 0.01, 0.02), ("treasure", 0.01, 0.02), ("tower", 0.02, 0.03),
               ("emblem", 0.01, 0.02)]
    for f in feature:
        draw_cluster(draw_array, f[0], f[1], f[2], 1, 1, 1, 1)

    # Minor background
    draw_cluster(draw_array, "hut", 0.02, 0.03, 1, 3, 1, 10, 50, 50)
    draw_cluster(draw_array, "cow", 0.01, 0.02, 1, 2, 1, 5, 20, 20)

    place_trees(draw_array)
    draw_array.sort(key=lambda p: p.y)
    tree_text, overlay_text = draw(draw_array, svg_cache)

    # Creating file
    new_path = uniquify('file.svg')
    new_file = open(new_path, 'w')

    header = load_svg("header", True)
    footer = load_svg("footer", True)
    title = header + tree_text + overlay_text + footer
    new_file.write(title)

    new_file.close()
    print(new_path)


if __name__ == "__main__":
    main()
