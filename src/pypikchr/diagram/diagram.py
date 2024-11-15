"""Classes and utilities for holding a full pikchr diagram."""

__all__ = ["Diagram", "Direction"]
__author__ = "Gabriel Dorlhiac"

from enum import Enum
from typing import Optional

from pypikchr.diagram.shapes import Shape_T
from pypikchr.util.pikchr import create_pikchr


class Direction(str, Enum):
    right = "right"
    down = "down"
    left = "left"
    up = "up"


class Diagram:
    def __init__(self, direction: Direction = Direction.right, shape: Optional[Shape_T] = None) -> None:
        self._direction = direction

        self._diagram: Optional[Shape_T] = shape

    def __str__(self) -> str:
        if self._diagram is not None:
            return create_pikchr(self._diagram.md, "", 0, 0, 0)
        else:
            return ""
