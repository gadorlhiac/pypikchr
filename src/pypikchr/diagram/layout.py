from __future__ import annotations

from typing import List, Union, Optional

from pypikchr.diagram.shapes import Shape, Shape_T


class Group(Shape):
    def __init__(self) -> None:
        super().__init__("group")
        self._shapes: List[Union[Shape, str]] = []

    def add(self, item: Union[Shape, str]) -> Group:
        self._shapes.append(item)
        return self

    @property
    def md(self) -> str:
        content = []
        for s in self._shapes:
            if isinstance(s, Shape):
                content.append(s.md)
            else:
                content.append(s)

        inner_md = ";\n  ".join(content)
        return f"[\n  {inner_md}\n]"


class Stack(Group):
    def __init__(
        self, direction: str = "down", spacing: Optional[float] = None
    ) -> None:
        super().__init__()
        self._direction = direction
        self._spacing = spacing

    def add(self, item: Union[Shape, str]) -> Stack:
        if isinstance(item, Shape) and self._shapes:
            # Position relative to previous shape if it's the first in stack
            # Actually, inside a [ ] grouping, the direction is set.
            pass
        super().add(item)
        return self

    @property
    def md(self) -> str:
        content = [self._direction]
        if self._spacing:
            content.append(f"dist {self._spacing}")

        for s in self._shapes:
            if isinstance(s, Shape):
                content.append(s.md)
            else:
                content.append(s)

        inner_md = ";\n  ".join(content)
        return f"[\n  {inner_md}\n]"
