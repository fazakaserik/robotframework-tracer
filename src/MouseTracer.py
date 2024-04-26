import threading
import tkinter as tk
from collections import deque
from typing import Literal, Tuple, Union


class MouseTracer:
    def __init__(
        self,
        canvas: tk.Canvas,
        fill: str,
        location: Tuple[float, float] = (0.0, 0.0),
        width: Union[float, Literal["fill"]] = "fill",
        height: Union[float, Literal["fill"]] = "fill",
    ) -> None:
        # Circular buffer for mouse locations, this will be used to draw the mouse path, while also guarantee that the path will disappear
        self._mouse_locations: deque = deque(maxlen=3)  # TODO make maxlen a parameter
        # Ensure the canvas is managed by a geometry manager
        canvas.pack()
        # Calculate rectangle coordinates
        x0, y0 = location
        x1: float = canvas.winfo_reqwidth() if width == "fill" else x0 + width
        y1: float = canvas.winfo_reqheight() if height == "fill" else y0 + height
        # Draw the rectangle where the mous trace will be
        canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
