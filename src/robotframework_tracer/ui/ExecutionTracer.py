import ctypes
import threading
import tkinter as tk
from collections import deque
from ctypes import POINTER, byref, wintypes
from threading import Thread
from turtle import back
from typing import Literal, Tuple, Union

from robotframework_tracer.config.ExecutionTraceConfigurations import (
    ExecutionTraceConfigurations,
)
from robotframework_tracer.config.types.Location import Location
from robotframework_tracer.style.CycleColors import CycleColors
from robotframework_tracer.style.tkinter import TkinterStyle
from robotframework_tracer.ui.DisplayServiceManager import DisplayServiceManager
from robotframework_tracer.win_api.mouse import Mouse


class ExecutionTracer:

    def __init__(
        self,
        canvas: tk.Canvas,
        config: ExecutionTraceConfigurations,
    ) -> None:
        self.canvas = canvas
        self.config = config

        self._screen_width = self.canvas.winfo_reqwidth()
        self._screen_height = self.canvas.winfo_reqheight()

        self._frame = tk.Frame(
            master=self.canvas,
        )
        # Pack based on location config
        if config.location == Location.TOP_LEFT:
            self._frame.pack(anchor=tk.W, side=tk.TOP)
        elif config.location == Location.TOP_RIGHT:
            self._frame.pack(anchor=tk.E, side=tk.TOP)
        elif config.location == Location.BOTTOM_LEFT:
            self._frame.pack(anchor=tk.W, side=tk.BOTTOM)
        elif config.location == Location.BOTTOM_RIGHT:
            self._frame.pack(anchor=tk.E, side=tk.BOTTOM)

        # Add label to display executed keyword
        self._display_value = tk.StringVar(
            value="Waiting for Robot Framework execution..."
        )
        self._label = tk.Label(
            master=self._frame,
            textvariable=self._display_value,
            font=("Helvetica", 24, "bold"),
            fg="black",
            background="red",
            justify=tk.RIGHT,
        )
        self._label.pack(fill=tk.BOTH)

        # Initialize gRPC service
        display_service_manager = DisplayServiceManager(self.update_display)
        self.display_service = threading.Thread(
            target=display_service_manager.start_display_service,
            daemon=True,
        )
        self.display_service.start()

    def update_display(self, text: str):
        self.canvas.after(0, self._display, text)

    def _display(self, text: str):
        self._display_value.set(text)
        self.canvas.update()
