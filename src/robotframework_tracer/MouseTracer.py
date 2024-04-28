import ctypes
import tkinter as tk
from collections import deque
from ctypes import POINTER, byref, wintypes
from threading import Thread
from typing import Literal, Tuple, Union

from robotframework_tracer.style.CycleColors import CycleColors
from robotframework_tracer.win_api.mouse import Mouse


class MouseTracer:
    def __init__(
        self,
        canvas: tk.Canvas,
        fill: str,
        location: Tuple[float, float] = (0.0, 0.0),
        width: Union[float, Literal["fill"]] = "fill",
        height: Union[float, Literal["fill"]] = "fill",
    ) -> None:
        self.canvas = canvas
        self.mouse = Mouse()

        self.arrow_ids: deque = deque(maxlen=3)
        self.prev_mouse_click: Tuple[float, float] = (0.0, 0.0)
        self.canvas.pack()
        self.cycle_colors = CycleColors()

        # Calculate rectangle coordinates
        x0, y0 = location
        x1 = self.canvas.winfo_reqwidth() if width == "fill" else x0 + width
        y1 = self.canvas.winfo_reqheight() if height == "fill" else y0 + height

        self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill)

        self.mouse.subscribe_on_mouse_left_button_down(
            self._on_mouse_left_button_down
        )

    def _on_mouse_left_button_down(self, x: float, y: float):
        if len(self.arrow_ids) == self.arrow_ids.maxlen:
            self.canvas.delete(self.arrow_ids.popleft())
        line_id = self.canvas.create_line(
            self.prev_mouse_click[0],
            self.prev_mouse_click[1],
            x,
            y,
            arrow=tk.LAST,
            width=8,
            arrowshape=(32, 40, 12),
            fill=self.cycle_colors.get_color(),
        )
        self.cycle_colors.cycle()
        self.arrow_ids.append(line_id)
        self.prev_mouse_click = (x, y)
