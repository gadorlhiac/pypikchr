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

"""Classes and utilities for basic pikchr components."""

__author__ = "Gabriel Dorlhiac"

import warnings
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    TypeAlias,
    TypedDict,
    Union,
    overload,
)

Shape_T: TypeAlias = "Shape"


class Shape:
    """Base class for all Pikchr shapes."""

    anchor_points: ClassVar[set[str]] = {
        "nw",
        "n",
        "ne",
        "e",
        "se",
        "s",
        "sw",
        "w",
        "c",
    }

    def __init__(self, shape_type: str, text: Optional[str] = None) -> None:
        self._shape_type = shape_type
        self._text = text
        self._label: Optional[str] = None
        self._attributes: dict[str, Any] = {}
        self._md_prefix: str = ""
        self._md_suffix: str = ""

    @property
    def name(self) -> str:
        return self._label if self._label else self._shape_type

    def label(self, label: str) -> Shape_T:
        """Set a label for the shape.

        Labels are annotations within the pikchr markup language that can be used
        to refer to the shape later. This allows for construction of dependencies
        even when there are many intervening objects. The label is NOT displayed
        as text in the generated image.
        """
        upper_case: str = label.upper()
        for char in label:
            if char.islower():
                warnings.warn(
                    "Lower case letters cannot be used in labels!\n"
                    f"Label {label} will be converted to {upper_case}!",
                    category=RuntimeWarning,
                )
                break  # Only need to warn once
        self._label = upper_case
        return self

    def width(self, val: Union[float, str]) -> Shape_T:
        self._attributes["width"] = val
        return self

    def height(self, val: Union[float, str]) -> Shape_T:
        self._attributes["height"] = val
        return self

    def radius(self, val: Union[float, str]) -> Shape_T:
        self._attributes["radius"] = val
        return self

    def diameter(self, val: Union[float, str]) -> Shape_T:
        self._attributes["diameter"] = val
        return self

    def thick(self) -> Shape_T:
        self._attributes["thick"] = True
        return self

    def thin(self) -> Shape_T:
        self._attributes["thin"] = True
        return self

    def fill(self, color: str) -> Shape_T:
        self._attributes["fill"] = color
        return self

    def color(self, color: str) -> Shape_T:
        self._attributes["color"] = color
        return self

    def at(self, pos: Union[str, Shape_T]) -> Shape_T:
        if isinstance(pos, Shape):
            self._attributes["at"] = pos.name
        else:
            self._attributes["at"] = pos
        return self

    def right_of(self, other: Shape_T, offset: Optional[float] = None) -> Shape_T:
        """Position this shape to the right of another shape."""
        pos = f"{other.name}.e"
        if offset is not None:
            pos += f" + ({offset}, 0)"
        self._attributes["at"] = pos
        return self

    def left_of(self, other: Shape_T, offset: Optional[float] = None) -> Shape_T:
        """Position this shape to the left of another shape."""
        pos = f"{other.name}.w"
        if offset is not None:
            pos += f" - ({offset}, 0)"
        self._attributes["at"] = pos
        return self

    def above(self, other: Shape_T, offset: Optional[float] = None) -> Shape_T:
        """Position this shape above another shape."""
        pos = f"{other.name}.n"
        if offset is not None:
            pos += f" + (0, {offset})"
        self._attributes["at"] = pos
        return self

    def below(self, other: Shape_T, offset: Optional[float] = None) -> Shape_T:
        """Position this shape below another shape."""
        pos = f"{other.name}.s"
        if offset is not None:
            pos += f" - (0, {offset})"
        self._attributes["at"] = pos
        return self

    def from_pos(self, pos: Union[str, Shape_T]) -> Shape_T:
        if isinstance(pos, Shape):
            self._attributes["from"] = pos.name
        else:
            self._attributes["from"] = pos
        return self

    def to_pos(self, pos: Union[str, Shape_T]) -> Shape_T:
        if isinstance(pos, Shape):
            self._attributes["to"] = pos.name
        else:
            self._attributes["to"] = pos
        return self

    def dotted(self) -> Shape_T:
        self._attributes["dotted"] = True
        return self

    def dashed(self) -> Shape_T:
        self._attributes["dashed"] = True
        return self

    def up(self, val: Optional[float] = None) -> Shape_T:
        self._attributes["up"] = val if val is not None else True
        return self

    def down(self, val: Optional[float] = None) -> Shape_T:
        self._attributes["down"] = val if val is not None else True
        return self

    def left(self, val: Optional[float] = None) -> Shape_T:
        self._attributes["left"] = val if val is not None else True
        return self

    def right(self, val: Optional[float] = None) -> Shape_T:
        self._attributes["right"] = val if val is not None else True
        return self

    def fit(self) -> Shape_T:
        self._attributes["fit"] = True
        return self

    @property
    def n(self) -> str:
        return f"{self.name}.n"

    @property
    def s(self) -> str:
        return f"{self.name}.s"

    @property
    def e(self) -> str:
        return f"{self.name}.e"

    @property
    def w(self) -> str:
        return f"{self.name}.w"

    @property
    def nw(self) -> str:
        return f"{self.name}.nw"

    @property
    def ne(self) -> str:
        return f"{self.name}.ne"

    @property
    def sw(self) -> str:
        return f"{self.name}.sw"

    @property
    def se(self) -> str:
        return f"{self.name}.se"

    @property
    def c(self) -> str:
        return f"{self.name}.c"

    @property
    def md(self) -> str:
        parts = []
        if self._label:
            parts.append(f"{self._label}:")
        parts.append(self._shape_type)
        if self._text:
            parts.append(f'"{self._text}"')

        for k, v in self._attributes.items():
            if v is True:
                parts.append(k)
            else:
                parts.append(f"{k} {v}")

        content = " ".join(parts)
        return f"{self._md_prefix}{content}{self._md_suffix}"

    def __rshift__(self, other: Union[Shape_T, str]) -> Shape_T:
        """The >> operator can be used to chain shapes."""
        if isinstance(other, Shape):
            other._md_prefix = self.md + "; "
            return other
        self._md_suffix += f"; {other}"
        return self

    def __lshift__(self, other: Union[Shape_T, str]) -> Shape_T:
        if isinstance(other, Shape):
            self._md_prefix = other.md + "; "
            return self
        self._md_prefix = f"{other}; " + self._md_prefix
        return self


class Box(Shape):
    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__("box", text)


class Circle(Shape):
    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__("circle", text)


class Ellipse(Shape):
    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__("ellipse", text)


class Oval(Shape):
    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__("oval", text)


class Cylinder(Shape):
    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__("cylinder", text)


class File(Shape):
    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__("file", text)


class Diamond(Shape):
    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__("diamond", text)


class Line(Shape):
    def __init__(self) -> None:
        super().__init__("line")


class Arrow(Shape):
    def __init__(self, text: Optional[str] = None) -> None:
        super().__init__("arrow", text)


class Spline(Shape):
    def __init__(self) -> None:
        super().__init__("spline")


class Dot(Shape):
    def __init__(self) -> None:
        super().__init__("dot")


class Arc(Shape):
    def __init__(self) -> None:
        super().__init__("arc")


class Text(Shape):
    def __init__(self, text: str) -> None:
        super().__init__("text", text)
