import unittest
import warnings

from pypikchr.diagram import Box, Arrow, Diagram


class TestShapes(unittest.TestCase):
    def test_box_md(self):
        b = Box("Test").fill("red")
        self.assertIn('box "Test"', b.md)
        self.assertIn("fill red", b.md)

    def test_label_warning(self):
        b = Box("Test")
        with self.assertWarns(RuntimeWarning) as cm:
            b.label("low")
        self.assertIn("Lower case letters", str(cm.warning))
        self.assertEqual(b.name, "LOW")

    def test_positioning_helpers(self):
        b1 = Box("B1").label("B1")
        b2 = Box("B2").label("B2").right_of(b1, 0.5)
        self.assertIn("at B1.e + (0.5, 0)", b2.md)

    def test_diagram_md(self):
        d = Diagram()
        b1 = Box("B1").label("B1")
        b2 = Box("B2").label("B2").below(b1)
        d.add(b1).add(b2)
        self.assertIn('B1: box "B1"', d.md)
        self.assertIn('B2: box "B2" at B1.s', d.md)

    def test_dimensions(self):
        """Verify that width, height, radius, diameter are correctly formatted."""
        b = Box("Test").width(2.0).height(1.5)
        md = b.md
        self.assertIn("width 2.0", md)
        self.assertIn("height 1.5", md)

    def test_styles(self):
        """Verify thick, thin, dotted, dashed, fill and color attributes."""
        b = Box("Style").thick().dotted().fill("red").color("blue")
        md = b.md
        self.assertIn("thick", md)
        self.assertIn("dotted", md)
        self.assertIn("fill red", md)
        self.assertIn("color blue", md)


if __name__ == "__main__":
    unittest.main()
