"""Classes and utilities for holding a full pikchr diagram."""

__all__ = ["Diagram", "Direction"]
__author__ = "Gabriel Dorlhiac"

from enum import Enum
from typing import Optional

from pypikchr.diagram.shapes import Shape_T
from pypikchr.util.pikchr import create_pikchr, PikchrException


class PikchrFlags(int, Enum):
    PLAINTEXT_ERRORS = 0x0001
    DARK_MODE = 0x0002


class Direction(str, Enum):
    right = "right"
    down = "down"
    left = "left"
    up = "up"


class Diagram:
    def __init__(
        self,
        direction: Direction = Direction.right,
        shape: Optional[Shape_T] = None,
        flags: int = 0,
    ) -> None:
        """Diagrams hold the entirety of a Pikchr markdown drawing.

        Args:
            direction (Direction): Starting orientation of the diagram.
                Default: "right".

            shape (Optional[Shape]): Provide an initial shape.

            flags (int): Pass additional flags to pikchr. Currently supported
                flags are:
                    - 0x0001 = Plain-text errors instead of HTML-formatted errors.
                    - 0x0002 = Use dark-mode.
                Multiple flag bits can be passed together.
        """
        self._direction = direction

        self._diagram: Optional[Shape_T] = shape
        if flags > (PikchrFlags.PLAINTEXT_ERRORS | PikchrFlags.DARK_MODE):
            raise PikchrException(
                "Valid flag bits are:\n"
                "- PLAINTEXT_ERRORS: 0x0001\n"
                "- DARK_MODE: 0x0002"
            )
        self._flags: int = flags

    def __str__(self) -> str:
        if self._diagram is not None:
            return create_pikchr(self._diagram.md, "", self._flags, 0, 0)
        else:
            return ""
