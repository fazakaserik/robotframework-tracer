import threading
import tkinter as tk
from ctypes import windll

from robotframework_tracer.Configurations import Configurations
from robotframework_tracer.style.tkinter import TkinterStyle
from robotframework_tracer.ui.DisplayServiceManager import DisplayServiceManager
from robotframework_tracer.ui.MouseTracer import MouseTracer


class Display:

    def __init__(self):
        # VS Code configurations
        self._configurations = Configurations()

        # Initialize Tkinter
        self._root = tk.Tk()
        self._root.title("Robot Framework Listener")
        self._root.attributes("-alpha", 1)
        self._root.attributes("-topmost", True)
        self._root.overrideredirect(True)  # Do not show application on tray
        # self._root.attributes("-fullscreen", True)
        self._root.wm_attributes(
            "-transparentcolor", TkinterStyle.Colors.TRANSPARENT_COLOR
        )

        self._screen_width = self._root.winfo_screenwidth()
        self._screen_height = self._root.winfo_screenheight()

        self._display_value = tk.StringVar(
            value="Waiting for Robot Framework execution..."
        )
        self._keyword_label = tk.Label(
            master=self._root,
            textvariable=self._display_value,
            font=("Helvetica", 24, "bold"),
            fg="black",
        )
        self._keyword_label.place(x=0, y=0)
        self._keyword_label.pack(anchor="w")

        # Create a canvas for drawing lines
        self._canvas = tk.Canvas(
            self._root, width=self._screen_width, height=self._screen_height
        )
        self._mouse_tracer = MouseTracer(
            canvas=self._canvas, fill=TkinterStyle.Colors.TRANSPARENT_COLOR
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)

        # Settings for line drawing
        self._line_color = "red"
        self._line_lifetime = 5000
        self._previous_x, self._previous_y = None, None

        # Initialize gRPC service
        display_service_manager = DisplayServiceManager(self.update_display)
        self.display_service = threading.Thread(
            target=display_service_manager.start_display_service,
            daemon=True,
        )

        # Wait to configure the window for click-through until it's fully loaded
        self._root.after(
            10, lambda: self.make_click_through(self._root.winfo_id())
        )

    def start(self):
        self.display_service.start()
        self._root.mainloop()

    def make_click_through(self, hwnd):
        hwnd = windll.user32.GetParent(self._root.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, -20)
        style |= 0x80000 | 0x20
        windll.user32.SetWindowLongPtrW(hwnd, -20, style)

    def update_display(self, text: str):
        self._root.after(0, self._display, text)

    def _display(self, text: str):
        self._display_value.set(text)
        self._root.update()


# Gets called by Listener.py
if __name__ == "__main__":
    display = Display()
    display.start()
