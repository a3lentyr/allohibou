import tempfile
import itertools as IT
import os
import random
import math
from math import sqrt
from lib import fbd, links

from noise import pnoise2,snoise2

# random.seed(45)


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


def load_svg(name):
    name_file = open("img/" + name + ".svg", 'r')
    name_text = name_file.read()
    name_file.close()

    return name_text


def draw_places():
    # forming list of places
    form_list = ["triangle", "carre", "rond", "losange"]
    color_list = ["violet", "orange", "green"]

    places_list = []
    for form in form_list:
        for color in color_list:
            places_list.append(form + "-" + color)

    data_dict = {}

    for name in places_list:
        data_dict[name] = load_svg(name)

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

    content_text = ""
    for i, name in enumerate(places_list):
        x = trans_places[i][0]
        y = trans_places[i][1]
        content_text += '<g transform="translate(' + str(x) + ',' + str(y) + ')">'  # placing it
        content_text += data_dict[name] + '</g>'  # content

    return content_text, trans_places, d


def draw_marchandise(road_places_list):
    # forming list of marchandise
    form_list_m = ["triangle", "triangle", "triangle", "carre", "rond", "losange", "losange"]
    color_list = ["violet", "orange", "green"]
    m_list = []
    for form in form_list_m:
        for color in color_list:
            m_list.append(form + "-" + color + "-m")
    random.shuffle(form_list_m)

    data_dictm = {}

    for name in m_list:
        data_dictm[name] = load_svg(name)

    m_index = 0
    content_text = ""
    for road in road_places_list:
        if m_index < len(m_list):
            xm = road[0]
            ym = road[1]
            content_text += '<g transform="translate(' + str(xm) + ',' + str(ym) + ')">'
            content_text += data_dictm[m_list[m_index]] + '</g>'  # m content
            m_index += 1

    return content_text


def draw_roads(trans_places, d):
    # forming list of road
    road_list = ["blue", "red", "yellow"]
    data_dictr = {}

    for name in road_list:
        data_dictr[name] = load_svg(name)

    # adding path
    shortened_list = []
    road_places_list = []
    march_places_list = []

    content_text = ""

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

                    content_text += '<g transform="translate(' + str(xrm) + ',' + str(yrm) + ') rotate(' + str(
                        rotate_factor) + ') ">'
                    content_text += data_dictr[road_list[int((target - 0.3) * 100)]] + '</g>'  # m content

    return content_text, road_places_list, march_places_list


def draw_cluster(forbid_places, name, scale_min=0.05, scale_max=0.1, num_min=1, num_max=3, cluster_min=1, cluster_max=2, offset_x=20,
                 offset_y=20, offset_height=40, offset_width=20):
    stones_text = load_svg(name)
    trans_places = []

    rand_num = random.randint(0, num_max) + num_min  # number of stone cluster
    content_text = ""
    for stone_index in range(0, rand_num):
        # check for collision
        is_under = True
        while is_under:
            x = random.random() * 300
            y = random.random() * 250
            is_under = False
            for p in forbid_places:
                if sqrt((p[0] - x + offset_x) ** 2 + (p[1] - y + offset_y) ** 2) < (10+max(offset_width,offset_height)):
                    is_under = True
                    break

        rand_num_small = random.randint(0, cluster_max) + cluster_min

        perlin_list=[]
        for y in range(0,offset_width,10):
            for x in range(0,offset_height,10):
                perlin_list.append((x,y,snoise2(x / 16.0, y / 16.0, 1)))
        perlin_list.sort(key=lambda tup: tup[2])

        for stone_indexes in perlin_list[0:rand_num_small]:
            xs = x - offset_height / 2 + stone_indexes[0]
            ys = y - offset_width / 2 + stone_indexes[1]
            trans_places.append([xs, ys])

    # filter places from front to back
    trans_places.sort(key=lambda tup: tup[1])
    for p in trans_places:
        xs = p[0]+ 2 * random.random()
        ys = p[1]+ 2 * random.random()
        scale = random.uniform(scale_min,scale_max)
        content_text += '<g transform="translate(' + str(xs - offset_x) + ',' + str(
            ys - offset_y) + ')  scale(' + str(scale) + ',' + str(
            scale) + ')">' + stones_text + '</g>'

    return content_text, trans_places


def draw_trees(trans_places, road_places_list):
    tree_text = load_svg("tree")

    content_text=""
    for x_index in range(-10, 300, 5):
        for y_index in range(270, -10, -5):
            x = x_index + 4 * random.random()
            y = y_index - 4 * random.random()
            rand_tree = random.random()
            if rand_tree > 0.6:
                # should not be placed under places nor roads
                is_under = False
                for p in trans_places:
                    if sqrt((p[0] - x - 10) ** 2 + (p[1] - y - 10) ** 2) < 25:
                        is_under = True
                        break

                if not is_under:
                    for p in road_places_list:
                        if sqrt((p[0] - x - 10) ** 2 + (p[1] - y - 10) ** 2) < 10:
                            is_under = True
                            break

                if not is_under:
                    content_text = '<g transform="translate(' + str(x) + ',' + str(
                        y) + ')  scale(0.03,0.03)" fill="rgb(50,' + str(
                        50 + random.random() * 50) + ',50)">' + tree_text + '</g>' + content_text
    return content_text


def main():
    places_text, trans_places, d = draw_places()
    roads_text, road_places_list, march_places_list = draw_roads(trans_places, d)
    march_text = draw_marchandise(march_places_list)

    # Adding background
    stones_text, trans_places_cluster = draw_cluster(road_places_list, "stones")
    trans_places += trans_places_cluster
    stadium_text, trans_places_cluster = draw_cluster(road_places_list, "stadium", 0.05, 0.0, 1, 1, 0, 0)
    trans_places += trans_places_cluster
    castle_text, trans_places_cluster = draw_cluster(road_places_list, "castle", 0.05, 0.0, 1, 1, 0, 0, 20, 20)
    trans_places += trans_places_cluster

    # Minor background
    hut_text, trans_places_cluster = draw_cluster(road_places_list, "hut", 0.03, 0.03, 1, 1, 0, 20, 10,10,70,70)
    road_places_list += trans_places_cluster
    cow_text, trans_places_cluster = draw_cluster(road_places_list, "cow", 0.03, 0.0, 1, 1, 1, 5, 20, 20, 20, 20)
    road_places_list += trans_places_cluster

    tree_text = draw_trees(trans_places, road_places_list)

    # Creating file
    new_path = uniquify('file.svg')
    new_file = open(new_path, 'w')

    header = load_svg("header")
    footer = load_svg("footer")
    title = header + stones_text + roads_text +  stadium_text + hut_text + castle_text + cow_text + tree_text + places_text + march_text + footer
    new_file.write(title)

    new_file.close()
    print(new_path)


if __name__ == "__main__":
    main()
