import ctypes
import tkinter as tk
from collections import deque
from ctypes import POINTER, byref, wintypes
from threading import Thread
from typing import Literal, Tuple, Union

from Colors import CycleColors


# Define necessary structures from the WinAPI
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("pt", POINT),
        ("mouseData", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


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
        self.arrow_ids: deque = deque(maxlen=3)  # Adjust maxlen as needed
        self.prev_mouse_click = (0, 0)
        self.canvas.pack()
        self.cycle_colors = CycleColors()

        # Calculate rectangle coordinates
        x0, y0 = location
        x1 = self.canvas.winfo_reqwidth() if width == "fill" else x0 + width
        y1 = self.canvas.winfo_reqheight() if height == "fill" else y0 + height

        self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill)

        # Load user32 and set up hook
        self.user32 = ctypes.WinDLL("user32", use_last_error=True)
        self.LowLevelMouseProc = ctypes.WINFUNCTYPE(
            wintypes.LPARAM,
            wintypes.INT,
            wintypes.WPARAM,
            POINTER(MSLLHOOKSTRUCT),
        )
        self.hook_proc_instance = self.LowLevelMouseProc(self.py_mouse_proc)
        self.hook_id = self.user32.SetWindowsHookExA(
            14, self.hook_proc_instance, None, 0
        )

        if not self.hook_id:
            raise ctypes.WinError(ctypes.get_last_error())

        Thread(target=self.run_message_loop, daemon=True).start()

    def run_message_loop(self):
        msg = wintypes.MSG()
        while self.user32.GetMessageA(byref(msg), None, 0, 0) != 0:
            self.user32.TranslateMessage(byref(msg))
            self.user32.DispatchMessageA(byref(msg))
        self.user32.UnhookWindowsHookEx(self.hook_id)

    def py_mouse_proc(self, nCode, wParam, lParam):
        if nCode >= 0:  # HC_ACTION
            if wParam == 513:  # WM_LBUTTONDOWN
                mouse_struct = ctypes.cast(
                    lParam, POINTER(MSLLHOOKSTRUCT)
                ).contents

                # TODO: correct this offset
                mouse_struct.pt.y = mouse_struct.pt.y - 40

                if len(self.arrow_ids) == self.arrow_ids.maxlen:
                    self.canvas.delete(self.arrow_ids.popleft())
                x, y = self.prev_mouse_click
                line_id = self.canvas.create_line(
                    x,
                    y,
                    mouse_struct.pt.x,
                    mouse_struct.pt.y,
                    arrow=tk.LAST,
                    width=8,
                    arrowshape=(32, 40, 12),
                    fill=self.cycle_colors.get_next_color(),
                )
                self.arrow_ids.append(line_id)
                self.prev_mouse_click = (mouse_struct.pt.x, mouse_struct.pt.y)
            elif wParam == 514:  # WM_LBUTTONUP
                mouse_struct = ctypes.cast(
                    lParam, POINTER(MSLLHOOKSTRUCT)
                ).contents
        return self.user32.CallNextHookEx(None, nCode, wParam, lParam)
