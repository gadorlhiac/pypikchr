# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-06

### Added
- **Hyperlink Support**: Added `.url(link)` method to all shapes. This enables embedding hyperlinks in the generated SVG output.
- **Auto-sizing Boxes**: Added `Diagram.auto_size_boxes(padding=0.2)` to scale all boxes in a diagram to match the width of the longest label.
- **Layout Helpers**: Introduced `Group` and `Stack` (Vertical/Horizontal) classes to simplify the construction of groups of elements and shapes.
- **Relative Alignment**: Added `Shape.align_to(other, anchor)` to align a shape's center to a specific anchor on another shape.
- Included a change log.

### Changed
- Refactored SVG generation to use internal markers to enable post-processing. This allows embedding features like URLs, which are not part of the underlying `pikchr` markup language.
- Ensure the public `.md` property remains free of the above internal markers.

## [0.1.0] - 2026-02-02
- Initial release with basic `pikchr` shape wrappers.
