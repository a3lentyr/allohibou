from PIL import Image, ImageDraw, ImageEnhance
from typing import Tuple, List


class DrawingElement:
    def __init__(
        self,
        name: str,
        center: Tuple[int, int],
        depth: int,
        rotate: float,
        sepia: bool = True,
    ):
        self._name = name
        self._center = center
        self._depth = depth
        self._rotate = rotate
        self._sepia = sepia

    def draw(self, im, imgPasted):
        bg_x, bg_y = self._center

        img = imgPasted.rotate(self._rotate, Image.NEAREST, expand=1)
        img_w, img_h = img.size

        offset = (bg_x - (img_w) // 2, bg_y - (img_h) // 2)
        im.paste(img, offset, img)

        return im


class StackDrawer:

    _stack: List[DrawingElement]

    def __init__(self):
        self._stack = []

    def add(
        self,
        name: str,
        center: Tuple[int, int],
        depth: int = 0,
        rotate: float = 0,
        sepia: bool = True,
    ):
        self._stack.append(DrawingElement(name, center, depth, rotate, sepia))

    def merge(self, stack):
        for element in stack._stack:
            self._stack.append(element)

    def drawAll(self, im, scale):

        # Preload all images
        image_list = list(
            set(
                [
                    (drawingElement._name, drawingElement._sepia)
                    for drawingElement in self._stack
                ]
            )
        )
        image_dict = {}
        for image_name, sepia in image_list:
            image_target = Image.open("./img/" + image_name + ".png", "r")
            if sepia:
                # image_target = self.sepia(image_target)

                converter = ImageEnhance.Color(image_target)
                image_target = converter.enhance(0.5)

            img_w, img_h = image_target.size
            newsize = (img_w * scale, img_h * scale)
            image_target = image_target.resize(newsize)

            image_dict[image_name] = image_target

        # sort
        self._stack = sorted(
            self._stack, key=lambda x: x._depth * 100000 + x._center[1]
        )

        # draw
        for drawingElement in self._stack:

            img = image_dict[drawingElement._name]
            im = drawingElement.draw(im, img)

        for _, img in image_dict.items():
            img.close()

        return im

    def sepia(self, img) -> Image:
        width, height = img.size

        pixels = img.load()  # create the pixel map

        for py in range(height):
            for px in range(width):
                r, g, b, a = img.getpixel((px, py))

                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                if tr > 255:
                    tr = 255

                if tg > 255:
                    tg = 255

                if tb > 255:
                    tb = 255

                pixels[px, py] = (tr, tg, tb, a)

        return img
