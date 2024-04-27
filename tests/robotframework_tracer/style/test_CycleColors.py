import unittest

from robotframework_tracer.style.CycleColors import CycleColors


class TestCycleColors(unittest.TestCase):
    def setUp(self):
        self.colors = ["red", "yellow", "green"]
        self.cycle_colors = CycleColors(colors=self.colors)

    def test_get_color(self):
        initial_color = self.cycle_colors.get_color()
        next_color = self.cycle_colors.get_color()

        self.assertEqual(initial_color, next_color)

    def test_get_next_color(self):
        initial_color = self.cycle_colors.get_color()
        next_color = self.cycle_colors.get_next_color()

        self.assertNotEqual(initial_color, next_color)

    def test_color_cycling(self):
        # Make a whole cycle
        for color in self.colors:
            self.assertEqual(self.cycle_colors.get_next_color(), color)
        # It should return the first one again
        self.assertEqual(self.cycle_colors.get_next_color(), self.colors[0])


if __name__ == "__main__":
    unittest.main()
