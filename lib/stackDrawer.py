from PIL import Image, ImageDraw
from typing import Tuple, List


class DrawingElement:
    def __init__(self, name: str, center: Tuple[int, int], depth: int):
        self._name = name
        self._center = center
        self.depth = depth

    def draw(self, im, scale):
        bg_x, bg_y = self._center

        img = Image.open("./img/" + self._name + ".png", "r")
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

    def add(self, name: str, center: Tuple[int, int], depth: int = 0):
        self._stack.append(DrawingElement(name, center, depth))

    def drawAll(self, im, scale):
        for drawingElement in self._stack:
            im = drawingElement.draw(im, scale)

        return im
