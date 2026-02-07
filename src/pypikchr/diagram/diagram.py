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

from __future__ import annotations

"""Classes and utilities for holding a full pikchr diagram."""

import re
from enum import Enum
from typing import Iterable, List, Optional, Union

from pypikchr.diagram.shapes import Box, Shape
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

    def auto_size_boxes(self, padding: float = 0.2) -> "Diagram":
        """Scale all boxes in the diagram to the width of the longest label.

        Args:
            padding (float): Extra width to add to the calculated maximum.

        Returns:
            self (Diagram): Scaled version of self.
        """
        max_len = 0
        boxes: List[Box] = []
        for s in self._shapes:
            if isinstance(s, Box) and s._text:
                boxes.append(s)
                max_len = max(max_len, len(s._text))

        if not boxes:
            return self

        # Heuristic for width: ~0.1 inches per character
        # Standard pikchr box width is often 0.75 or 1.0 depending on text
        # If we use fit, it does it automatically, but this provides some bit of
        # normalization.
        for b in boxes:
            b.width(max_len * 0.1 + padding)

        return self

    @property
    def md(self) -> str:
        """Return the pikchr markdown.

        Returns:
            md (str): Pikchr markdown for the diagram.
        """
        return self._get_md(include_markers=False)

    def _get_md(self, include_markers: bool = False) -> str:
        md_parts = []
        if self._direction != Direction.right:
            md_parts.append(self._direction.value)

        for shape in self._shapes:
            if isinstance(shape, Shape):
                md_parts.append(shape.get_md(include_markers=include_markers))
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
        svg: str = create_pikchr(
            self._get_md(include_markers=True), "", self._flags, 0, 0
        )

        # Post-process for URLs and grouping
        if "[[pypikchr-id:" in svg:
            lines: List[str] = svg.splitlines()
            processed_lines: List[str] = []

            i: int = 0
            while i < len(lines):
                line: str = lines[i]
                marker_match: Optional[re.Match] = re.search(
                    r"\[\[pypikchr-id:(\d+)(?::url:(.*?))?\]\]", line
                )
                if marker_match:
                    # id_num = marker_match.group(1)
                    url = marker_match.group(2)

                    # Remove the marker from the text
                    line = re.sub(r"\s*\[\[pypikchr-id:.*?\]\]", "", line)

                    # Look back for associated shape elements
                    back_idx: int = len(processed_lines) - 1
                    elements_to_wrap: List[str] = []
                    while back_idx >= 0:
                        prev_line = processed_lines[back_idx]
                        # Stop if we hit a previous wrapper or the start
                        if any(stop in prev_line for stop in ["</a>", "</g>", "<svg"]):
                            break
                        # Collect SVG elements that belong to this shape
                        if any(
                            tag in prev_line
                            for tag in [
                                "<path",
                                "<polygon",
                                "<rect",
                                "<circle",
                                "<ellipse",
                                "<text",
                            ]
                        ):
                            elements_to_wrap.insert(0, processed_lines.pop(back_idx))
                        back_idx -= 1

                    if url:
                        processed_lines.append(f'<a href="{url}">')
                    else:
                        processed_lines.append("<g>")

                    processed_lines.extend(elements_to_wrap)
                    # Don't add empty text lines (if marker was the only content)
                    if not re.match(r"^\s*<text[^>]*>\s*</text>\s*$", line):
                        processed_lines.append(line)

                    if url:
                        processed_lines.append("</a>")
                    else:
                        processed_lines.append("</g>")
                else:
                    processed_lines.append(line)
                i += 1
            svg = "\n".join(processed_lines)

        return svg
