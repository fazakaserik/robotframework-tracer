import ctypes
import tkinter as tk
from collections import deque
from ctypes import POINTER, byref, wintypes
from threading import Thread
from typing import Literal, Tuple, Union

from robotframework_tracer.config.MouseTraceConfigurations import (
    MouseTraceConfigurations,
)
from robotframework_tracer.style.CycleColors import CycleColors
from robotframework_tracer.style.tkinter import TkinterStyle
from robotframework_tracer.win_api.mouse import Mouse


class MouseTracer:
    FILL: str = "fill"
    _FILL_LITERAL_TYPE = Literal["fill"]
    _FLEX_DIM_TYPE = Union[float, _FILL_LITERAL_TYPE]

    def __init__(
        self,
        canvas: tk.Canvas,
        fill: str,
        config: MouseTraceConfigurations,
        *,
        mouse: Mouse = Mouse(),
        location: Tuple[float, float] = (0.0, 0.0),
        width: _FLEX_DIM_TYPE = "fill",
        height: _FLEX_DIM_TYPE = "fill",
    ) -> None:

        # Only continue if this feature is enabled
        if not config.enabled:
            return

        self.canvas = canvas
        self.config = config
        self.mouse = mouse
        self.arrow_ids: deque = deque(maxlen=config.max_mouse_clicks_recorded)
        self.prev_mouse_click: Tuple[float, float] = (0.0, 0.0)
        self.canvas.pack()
        self.cycle_colors = CycleColors()

        # Calculate rectangle coordinates
        x0, y0 = location
        x1 = self._calculate_x1(x0, width)
        y1 = self._calculate_y1(y0, height)

        self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill)

        self.mouse.subscribe_on_mouse_left_button_down(
            self._on_mouse_left_button_down
        )

    def _calculate_x1(self, x0: float, width: _FLEX_DIM_TYPE) -> float:
        return self.canvas.winfo_reqwidth() if width == "fill" else x0 + width

    def _calculate_y1(self, y0: float, height: _FLEX_DIM_TYPE) -> float:
        return (
            self.canvas.winfo_reqheight() if height == "fill" else y0 + height
        )

    def _draw_arrow_to(self, target: Tuple[float, float]) -> None:
        if len(self.arrow_ids) == self.arrow_ids.maxlen:
            self.canvas.delete(self.arrow_ids.popleft())
        line_id = self.canvas.create_line(
            self.prev_mouse_click[0],
            self.prev_mouse_click[1],
            target[0],
            target[1],
            arrow=tk.LAST,
            width=TkinterStyle.Arrow.WIDTH,
            arrowshape=TkinterStyle.Arrow.ARROWSHAPE,
            fill=self.cycle_colors.get_color(),
        )
        self.cycle_colors.cycle()
        self.arrow_ids.append(line_id)
        self.prev_mouse_click = target

    def _on_mouse_left_button_down(self, x: float, y: float) -> None:
        self._draw_arrow_to((x, y))
