from typing import TypeAlias, Union, overload, ClassVar, TypedDict, Literal, Optional

Shape_T: TypeAlias = "Shape"


class DrawingOptions(TypedDict):
    thickness: Literal["thickness {dim}", "thick", "thin"]
    stroke_color: Literal[
        "invisible", "color {color}"
    ]  # 148 std CSS colors, not case-sensitive or 24-bit int or hex
    fill: Literal["fill {color}"]  # Same as stroke_color. Also None/Off set transparent


TextAttributes: set[str] = {
    "above",
    "aligned",
    "below",
    "big",
    "bold",
    "mono",
    "monospace",
    "center",
    "italic",
    "ljust",
    "rjust",
    "small",
}


class Shape:
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

    def __init__(self) -> None:
        self._shape_md: bytes = b""
        self._md: bytes = self._shape_md

    @property
    def shapemd(self) -> bytes:
        return self._shape_md

    @property
    def md(self) -> bytes:
        return self._md

    @md.setter
    def md(self, value: bytes) -> None:
        self._md = value

    @overload
    def __rshift__(self, right: Shape_T) -> Shape_T: ...
    @overload
    def __rshift__(self, right: bytes) -> Shape_T: ...

    def __rshift__(self, right: Union[Shape_T, bytes]) -> Shape_T:
        if isinstance(right, Shape):
            self._md = self._shape_md + b";" + right.shapemd
            right.md = self._md
        else:
            self._md = self._shape_md + b";" + right
        return self

    @overload
    def __lshift__(self, left: Shape_T) -> Shape_T: ...
    @overload
    def __lshift__(self, left: bytes) -> Shape_T: ...

    def __lshift__(self, left: Union[Shape_T, bytes]) -> Shape_T:
        if isinstance(left, Shape):
            self._md = left.shapemd + b";" + self._shape_md
            left.md = self._md
        else:
            self._md = left + b";" + self._shape_md
        return self


class ShapeWithText(Shape):
    def __init__(self, text: str, shape_type: str) -> None:
        # support `fit`, `width` (wid), `height`
        self._shape_md: bytes = f'{shape_type} "{text}"'.encode()
        self._md: bytes = self._shape_md


class ShapeWithoutText(Shape):
    def __init__(self, shape_type: str) -> None:
        self._shape_md: bytes = f"{shape_type}".encode()
        self._md: bytes = self._shape_md


class Box(ShapeWithText):
    def __init__(self, text: str) -> None:
        super().__init__(text=text, shape_type="box")


class Circle(ShapeWithText):
    def __init__(self, text: str) -> None:
        super().__init__(text=text, shape_type="circle")


class Ellipse(ShapeWithText):
    def __init__(self, text: str) -> None:
        super().__init__(text=text, shape_type="ellipse")


class Oval(ShapeWithText):
    def __init__(self, text: str) -> None:
        super().__init__(text=text, shape_type="oval")


class Cylinder(ShapeWithText):
    def __init__(self, text: str) -> None:
        super().__init__(text=text, shape_type="cylinder")


class File(ShapeWithText):
    def __init__(self, text: str) -> None:
        super().__init__(text=text, shape_type="file")


class Diamond(ShapeWithText):
    def __init__(self, text: str) -> None:
        super().__init__(text=text, shape_type="diamond")


class Line(ShapeWithoutText):
    def __init__(self) -> None:
        super().__init__(shape_type="line")


class Arrow(ShapeWithoutText):
    def __init__(self) -> None:
        super().__init__(shape_type="arrow")


class Spline(ShapeWithoutText):
    def __init__(self) -> None:
        super().__init__(shape_type="spline")


class Dot(ShapeWithoutText):
    def __init__(self) -> None:
        super().__init__(shape_type="dot")


class Arc(ShapeWithoutText):
    def __init__(self) -> None:
        super().__init__(shape_type="arc")
