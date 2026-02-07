import re
import unittest

from pypikchr.diagram import Box, Arrow, Diagram, Stack, Group


class TestFeatures(unittest.TestCase):
    def test_url_svg(self):
        """Verify that URLs are correctly embedded in the SVG output."""
        d = Diagram()
        d.add(Box("Link").url("https://example.com"))
        svg = str(d)
        self.assertIn('href="https://example.com"', svg)
        self.assertIn("<a ", svg)
        self.assertIn("Link", svg)
        self.assertNotIn("[[pypikchr-id:", svg)

    def test_auto_size_boxes(self):
        """Verify that auto_size_boxes normalizes widths."""
        d = Diagram()
        b1 = Box("Short")
        b2 = Box("Veeeery Looong Labeel")
        d.add(b1).add(b2)
        d.auto_size_boxes()

        md = d.md
        # Find all width attributes
        widths = re.findall(r"width ([\d.]+)", md)
        self.assertEqual(len(widths), 2)
        # They should both be the same
        self.assertEqual(widths[0], widths[1])
        # And should be based on the long label (approx 21 chars * 0.1 + 0.2 = 2.3)
        self.assertAlmostEqual(float(widths[0]), 2.3, places=2)

    def test_stack_layout(self):
        """Verify Stack helper generates correct pikchr markdown subdiagram."""
        s = Stack(direction="right", spacing=0.5)
        s.add(Box("A")).add(Box("B"))
        md = s.md
        self.assertIn("[", md)
        self.assertIn("]", md)
        self.assertIn("right", md)
        self.assertIn("dist 0.5", md)
        self.assertIn('box "A', md)
        self.assertIn('box "B', md)

    def test_group_layout(self):
        """Verify Group helper generates correct pikchr markdown subdiagram."""
        g = Group()
        g.add(Box("Inner"))
        md = g.md
        self.assertIn("[", md)
        self.assertIn("]", md)
        self.assertIn('box "Inner', md)

    def test_align_to(self):
        """Verify align_to helper positions shapes correctly."""
        b1 = Box("B1").label("B1")
        b2 = Box("B2").align_to(b1, "ne")
        self.assertIn("at B1.ne", b2.md)

    def test_multiple_urls_svg(self):
        """Verify multiple shape URLs are handled correctly in SVG."""
        d = Diagram()
        d.add(Box("A").url("urlA"))
        d.add(Box("B").url("urlB"))
        svg = str(d)
        self.assertIn('href="urlA"', svg)
        self.assertIn('href="urlB"', svg)
        self.assertEqual(svg.count("<a "), 2)
        self.assertEqual(svg.count("</a>"), 2)


if __name__ == "__main__":
    unittest.main()
