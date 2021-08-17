from typing import List, Tuple

from lib.stackDrawer import StackDrawer


class Mountains:
    _coord: Tuple[int, int]
    _type: str

    def __init__(self, coord: Tuple[int, int]):
        self._coord = coord
        self._type = "Mountains1"

    def toStack(self) -> StackDrawer:
        stack = StackDrawer()
        stack.add(self._type, self._coord, 0)
        return stack
