import unittest

from pypikchr.diagram import Box, Arrow, Diagram, Direction


class TestDAG(unittest.TestCase):
    def test_dag_chaining(self):
        d = Diagram(direction=Direction.down)
        s1 = Box("Start").label("S1")
        s2 = Box("End").label("S2").below(s1)

        # Using chain
        d.add(s1 >> Arrow() >> s2)

        self.assertIn('S1: box "Start"', d.md)
        # s1 >> Arrow() >> s2 results in s2 having prefix "S1: box \"Start\"; arrow; "
        # and s2 itself being 'S2: box "End" at S1.s'
        self.assertIn("arrow", d.md)
        self.assertIn('S2: box "End" at S1.s', d.md)


if __name__ == "__main__":
    unittest.main()
