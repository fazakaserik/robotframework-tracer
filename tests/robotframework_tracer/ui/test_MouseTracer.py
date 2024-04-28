import tkinter as tk
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from robotframework_tracer.style import CycleColors
from robotframework_tracer.style.tkinter import TkinterStyle
from robotframework_tracer.ui.MouseTracer import MouseTracer
from robotframework_tracer.win_api.mouse import Mouse


class TestMouseTracer(unittest.TestCase):

    def setUp(self):
        self.REQ_WIDTH = 100
        self.REQ_HEIGHT = 100
        self.ARG_LOCATION = (0, 0)
        self.ARG_WIDTH = 50
        self.ARG_HEIGHT = 50
        self.ARG_FILL = "red"

        self.mock_canvas = MagicMock(spec=tk.Canvas)
        self.mock_canvas.winfo_reqwidth.return_value = self.REQ_WIDTH
        self.mock_canvas.winfo_reqheight.return_value = self.REQ_HEIGHT

        self.mock_mouse = MagicMock(spec=Mouse)
        self.mock_cycle_colors = MagicMock(spec=CycleColors)
        self.mock_cycle_colors.get_color.return_value = self.ARG_FILL

        self.mouse_tracer = MouseTracer(
            canvas=self.mock_canvas,
            fill=self.ARG_FILL,
            mouse=self.mock_mouse,
            location=self.ARG_LOCATION,
            width=self.ARG_WIDTH,
            height=self.ARG_HEIGHT,
        )
        self.mouse_tracer.cycle_colors = self.mock_cycle_colors

    def test_initialization(self):
        self.mock_canvas.create_rectangle.assert_called_once()
        self.mock_mouse.subscribe_on_mouse_left_button_down.assert_called_once()

    def test_calculate_x1_with_fill(self):
        x1 = self.mouse_tracer._calculate_x1(
            self.ARG_LOCATION[0], width=MouseTracer.FILL
        )

        self.assertEqual(x1, self.REQ_WIDTH)

    def test_calculate_x1_with_numerical_width(self):
        x1 = self.mouse_tracer._calculate_x1(
            self.ARG_LOCATION[0], width=self.ARG_WIDTH
        )

        self.assertEqual(x1, self.ARG_LOCATION[0] + self.ARG_WIDTH)

    def test_calculate_y1_with_fill(self):
        y1 = self.mouse_tracer._calculate_y1(
            self.ARG_LOCATION[1], height=MouseTracer.FILL
        )

        self.assertEqual(y1, self.REQ_WIDTH)

    def test_calculate_y1_with_numerical_width(self):
        y1 = self.mouse_tracer._calculate_y1(
            self.ARG_LOCATION[1], height=self.ARG_WIDTH
        )

        self.assertEqual(y1, self.ARG_LOCATION[1] + self.ARG_HEIGHT)

    def test_draw_arrow_to_draws_on_canvas(self):
        self.mouse_tracer.prev_mouse_click = (0, 0)

        self.mouse_tracer._draw_arrow_to(self.ARG_LOCATION)

        self.mock_canvas.create_line.assert_called_once_with(
            self.mouse_tracer.prev_mouse_click[0],
            self.mouse_tracer.prev_mouse_click[1],
            self.ARG_LOCATION[0],
            self.ARG_LOCATION[1],
            arrow=tk.LAST,
            width=TkinterStyle.Arrow.WIDTH,
            arrowshape=TkinterStyle.Arrow.ARROWSHAPE,
            fill=self.ARG_FILL,
        )
        self.mock_cycle_colors.cycle.assert_called_once()
        self.assertEqual(self.mouse_tracer.prev_mouse_click, self.ARG_LOCATION)

    def test_draw_arrow_to_when_queue_is_full(self):
        for _ in range(self.mouse_tracer.arrow_ids.maxlen):
            self.mouse_tracer.arrow_ids.append(1)

        self.mouse_tracer._draw_arrow_to(self.ARG_LOCATION)

        self.assertTrue(self.mock_canvas.delete.called)
        self.assertEqual(self.mock_canvas.delete.call_count, 1)

    @patch.object(MouseTracer, "_draw_arrow_to")
    def test_on_mouse_left_button_down(self, mock_draw_arrow_to):
        self.mouse_tracer._on_mouse_left_button_down(
            self.ARG_LOCATION[0], self.ARG_LOCATION[1]
        )

        mock_draw_arrow_to.assert_called_once_with(self.ARG_LOCATION)


if __name__ == "__main__":
    unittest.main()
