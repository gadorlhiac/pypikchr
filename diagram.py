from enum import Enum
from typing import Optional

from shapes import Shape_T
from pypikchr import create_pikchr


class Direction(bytes, Enum):
    right = b"right"
    down = b"down"
    left = b"left"
    up = b"up"


class Diagram:
    def __init__(self, direction: Direction = Direction.right) -> None:
        self._direction = direction

        self._diagram: Optional[Shape_T] = None

    def __str__(self) -> str:
        if self._diagram is not None:
            return str(create_pikchr(self._diagram.md, b"", 0, 0, 0))
        else:
            return ""
