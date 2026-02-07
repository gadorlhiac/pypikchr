import unittest

from pypikchr.diagram import Box, Line, Diagram


class TestFormatting(unittest.TestCase):
    def test_dimensions(self):
        """Verify that width, height, radius, diameter are correctly formatted."""
        b = Box("Test").width(2.0).height(1.5)
        md = b.md
        self.assertIn("width 2.0", md)
        self.assertIn("height 1.5", md)

        from pypikchr.diagram import Circle

        c = Circle().radius(0.5)
        self.assertIn("radius 0.5", md := c.md)

        c2 = Circle().diameter(1.0)
        self.assertIn("diameter 1.0", c2.md)

    def test_thickness(self):
        """Verify thick and thin attributes."""
        b = Box("Thick").thick()
        self.assertIn("thick", b.md)

        b2 = Box("Thin").thin()
        self.assertIn("thin", b2.md)

    def test_colors(self):
        """Verify fill and color attributes."""
        b = Box("Colored").fill("red").color("blue")
        md = b.md
        self.assertIn("fill red", md)
        self.assertIn("color blue", md)

    def test_line_styles(self):
        """Verify dotted and dashed attributes."""
        l = Line().dotted()
        self.assertIn("dotted", l.md)

        l2 = Line().dashed()
        self.assertIn("dashed", l2.md)

    def test_text_attributes(self):
        """Verify that custom attributes can be passed if needed."""
        # Pikchr allows attributes on text
        from pypikchr.diagram import Text

        t = Text("Large").width(2.0)
        self.assertIn('text "Large" width 2.0', t.md)


if __name__ == "__main__":
    unittest.main()
