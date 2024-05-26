import ctypes
import threading
import tkinter as tk
from collections import deque
from ctypes import POINTER, byref, wintypes
from threading import Thread
from typing import Literal, Tuple, Union

from robotframework_tracer.style.CycleColors import CycleColors
from robotframework_tracer.style.tkinter import TkinterStyle
from robotframework_tracer.ui.DisplayServiceManager import DisplayServiceManager
from robotframework_tracer.win_api.mouse import Mouse


class ExecutionTracer:
    FILL: str = "fill"
    _FILL_LITERAL_TYPE = Literal["fill"]
    _FLEX_DIM_TYPE = Union[float, _FILL_LITERAL_TYPE]

    def __init__(
        self,
        canvas: tk.Canvas,
        fill: str,
    ) -> None:
        self.canvas = canvas
        
        self._screen_width = self.canvas.winfo_reqwidth()
        self._screen_height = self.canvas.winfo_reqheight()

        self._display_value = tk.StringVar(
            value="Waiting for Robot Framework execution..."
        )
        
        self._label = tk.Label(
            master=self.canvas,
            textvariable=self._display_value,
            font=("Helvetica", 24, "bold"),
            fg="black",
        )
        self._label.place(x=0, y=0)
        self._label.pack(anchor="w")
        
        # Initialize gRPC service
        display_service_manager = DisplayServiceManager(self.update_display)
        self.display_service = threading.Thread(
            target=display_service_manager.start_display_service,
            daemon=True,
        )
        
    # def start(self):
        self.display_service.start()
        
    def update_display(self, text: str):
        self.canvas.after(0, self._display, text)

    def _display(self, text: str):
        self._display_value.set(text)
        self.canvas.update()
    