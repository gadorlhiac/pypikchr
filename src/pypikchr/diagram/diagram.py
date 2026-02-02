# pypikchr - Small Python wrapper for the Pikchr diagramming language.
#
# Copyright (C) 2026 Gabriel Dorlhiac gabriel@dorlhiac.com
#
# This file is part of pypikchr.
#
# pypikchr is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pypikchr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pypikchr. If not, see <https://www.gnu.org/licenses/>.

"""Classes and utilities for holding a full pikchr diagram."""

from enum import Enum
from typing import List, Optional, Union

from pypikchr.diagram.shapes import Shape
from pypikchr.util.pikchr import PikchrException, create_pikchr


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
        shape: Optional[Shape] = None,
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
                Multiple flag bits can be passed together (bitwise OR).
        """
        self._direction = direction
        self._shapes: List[Union[Shape, str]] = []
        if shape:
            self._shapes.append(shape)

        if flags > (PikchrFlags.PLAINTEXT_ERRORS | PikchrFlags.DARK_MODE):
            raise PikchrException(
                "Valid flag bits are:\n"
                "- PLAINTEXT_ERRORS: 0x0001\n"
                "- DARK_MODE: 0x0002"
            )
        self._flags: int = flags

    def add(self, item: Union[Shape, str]) -> "Diagram":
        """Add a shape or raw pikchr string to the diagram.

        Args:
            item (Shape | str): A pypikchr shape object, or pikchr string.
        """
        self._shapes.append(item)
        return self

    @property
    def md(self) -> str:
        """Return the pikchr markdown.

        Returns:
            md (str): Pikchr markdown for the diagram.
        """
        md_parts = []
        if self._direction != Direction.right:
            md_parts.append(self._direction.value)

        for shape in self._shapes:
            if isinstance(shape, Shape):
                md_parts.append(shape.md)
            else:
                md_parts.append(shape)

        return ";\n".join(md_parts)

    def __str__(self) -> str:
        """Return the generated SVG HTML from the pikchr markdown for the diagram.

        Returns:
            html (str): Generated HTML for the markdown for the diagram.
        """
        if not self._shapes:
            return ""
        return create_pikchr(self.md, "", self._flags, 0, 0)
