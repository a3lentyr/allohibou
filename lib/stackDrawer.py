from PIL import Image, ImageDraw
from typing import Tuple, List


class DrawingElement:
    def __init__(self, name: str, center: Tuple[int, int], depth: int, rotate: float):
        self._name = name
        self._center = center
        self._depth = depth
        self._rotate = rotate

    def draw(self, im, imgPasted, scale):
        bg_x, bg_y = self._center

        img = imgPasted.rotate(self._rotate, Image.NEAREST, expand = 1)
        img_w, img_h = img.size

        newsize = (img_w * scale, img_h * scale)
        img = img.resize(newsize)

        offset = (
            bg_x - (img_w * scale) // 2,
            bg_y - (img_h * scale) // 2,
            bg_x + (img_w * scale) // 2,
            bg_y + (img_h * scale) // 2,
        )
        im.paste(img, offset, img)

        return im


class StackDrawer:

    _stack: List[DrawingElement]

    def __init__(self):
        self._stack = []

    def add(self, name: str, center: Tuple[int, int], depth: int = 0, rotate: float = 0):
        self._stack.append(DrawingElement(name, center, depth, rotate))

    def merge(self, stack):
        for element in stack._stack:
            self._stack.append(element)

    def drawAll(self, im, scale):

        # Preload all images
        image_list = list(set([drawingElement._name for drawingElement in self._stack ]))
        image_dict = {}
        for image_name in image_list:
            image_dict[image_name] = Image.open("./img/" + image_name + ".png", "r")

        # sort
        self._stack = sorted(self._stack, key = lambda x: x._depth*100000 + x._center[1])

        # draw
        for drawingElement in self._stack:

            img = image_dict[drawingElement._name]
            im = drawingElement.draw(im,img, scale)

        return im

