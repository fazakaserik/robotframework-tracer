import threading
import tkinter as tk
from ctypes import windll

from robotframework_tracer.Configurations import Configurations
from robotframework_tracer.style.tkinter import TkinterStyle
from robotframework_tracer.ui.DisplayServiceManager import DisplayServiceManager
from robotframework_tracer.ui.ExecutionTracer import ExecutionTracer
from robotframework_tracer.ui.MouseTracer import MouseTracer


class Display:

    def __init__(self):
        # VS Code configurations
        self._configurations = Configurations()

        # Initialize Tkinter root
        self._root = tk.Tk()
        self._root.title("Robot Framework Listener")
        self._root.attributes("-alpha", 1)
        self._root.attributes("-topmost", True)
        self._root.wm_attributes(
            "-transparentcolor", TkinterStyle.Colors.TRANSPARENT_COLOR
        )
        self.make_fullscreen()

        # Get dimensions
        self._screen_width = self._root.winfo_screenwidth()
        self._screen_height = self._root.winfo_screenheight()

        # Create a canvas for drawing lines
        self._canvas = tk.Canvas(
            self._root, width=self._screen_width, height=self._screen_height
        )
        self._execution_tracer = ExecutionTracer(
            canvas=self._canvas, fill=TkinterStyle.Colors.TRANSPARENT_COLOR
        )
        self._mouse_tracer = MouseTracer(
            canvas=self._canvas, fill=TkinterStyle.Colors.TRANSPARENT_COLOR
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)

        # Wait to configure the window for click-through until it's fully loaded
        self._root.after(
            10, lambda: self.make_click_through(self._root.winfo_id())
        )

    def start(self):
        # self._execution_tracer.start()
        self._root.mainloop()

    def make_click_through(self, hwnd):
        hwnd = windll.user32.GetParent(self._root.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, -20)
        style |= 0x80000 | 0x20
        windll.user32.SetWindowLongPtrW(hwnd, -20, style)

    def make_fullscreen(self, is_visible_on_tray: bool = False) -> None:
        if is_visible_on_tray:
            self._root.attributes("-fullscreen", True)
        else:
            self._root.overrideredirect(True)


# Gets called by Listener.py
if __name__ == "__main__":
    display = Display()
    display.start()
